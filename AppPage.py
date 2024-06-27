import os
from typing import Optional

import gi

import constants
import sadb, sadb.database

import UrlImage

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, Gtk, GObject, GLib


def clear_css_classes(widget):
    for css_class in widget.get_css_classes():
        widget.remove_css_class(css_class)


def set_row_if_not_none(row, value):
    if value is not None and value != "":
        row.set_visible(True)
        row.set_subtitle(value)
    else:
        row.set_visible(False)

def still_rating_to_display(rating: sadb.StillRating) -> tuple[str, Optional[str]]:
    match rating:
        case sadb.StillRating.CAUTION:
            return "Caution", "warning"
        case sadb.StillRating.BRONZE:
            return "Bronze", "bronze"
        case sadb.StillRating.SILVER:
            return "Silver", "silver"
        case sadb.StillRating.GOLD:
            return "Gold", "gold"
        case sadb.StillRating.GOLD_PLUS:
            return "Gold+", "gold-plus"
        case _:
            return "Unknown", None


class AppPage:
    installed = False
    app = None
    db = sadb.database.get_readable_db()

    def __init__(self, stillCenter):
        self.stillCenter = stillCenter
        self.page_builder = Gtk.Builder()
        self.page_builder.add_from_file(os.path.join(constants.UI_DIR, "AppPage.ui"))
        self.nav_page = self.page_builder.get_object("app_page")
        self.icon = self.page_builder.get_object("icon")
        self.author = self.page_builder.get_object("author")
        self.name = self.page_builder.get_object("name")
        self.rating_button = self.page_builder.get_object("rating_button")
        self.rating_label = self.page_builder.get_object("rating_label")
        self.remove_button = self.page_builder.get_object("remove_button")
        self.install_button = self.page_builder.get_object("install_button")
        self.update_button = self.page_builder.get_object("update_button")
        self.screenshot_box = self.page_builder.get_object("screenshotBox")
        self.summary = self.page_builder.get_object("app_summary")
        self.description = self.page_builder.get_object("description")
        self.homepage_row = self.page_builder.get_object("homepage_row")
        self.donate_row = self.page_builder.get_object("donate_row")
        self.source_row = self.page_builder.get_object("source_row")
        self.category_row = self.page_builder.get_object("category_row")
        self.keywords_row = self.page_builder.get_object("keywords_row")

    def id_in_database(self, app_id):
        self.db.c.execute("SELECT id FROM installed WHERE id = ?", (app_id,))
        result = self.db.c.fetchone()
        return result is not None

    def show_app(self, app_id):
        # Get an installed app if it exists, or try to get a remote app
        if self.id_in_database(app_id):
            self.db.c.execute("SELECT * FROM apps WHERE id=?", (app_id,))
            fetch_app = self.db.c.fetchone()
            if fetch_app is not None:
                self.app = self.db.column_to_installed_app(fetch_app)
                self.installed = True
            else:
                self.app = None
        else:
            self.installed = False
            self.app = self.db.get_app(app_id)

        if self.app is None:
            return

        # clear screenshot boxes
        for child in self.screenshot_box.get_children():
            self.screenshot_box.remove(child)

        # Set icon, name, author
        self.icon.set_from_url(self.app.icon_url)
        self.name.set_label(self.app.name)
        self.author.set_label(self.app.author)

        # Set rating text and rating css
        rating_text, rating_css = still_rating_to_display(self.app.still_rating)
        self.rating_label.set_label(rating_text)
        clear_css_classes(self.rating_button)
        if rating_css is not None:
            self.rating_button.add_css_class(rating_css)
            self.rating_button.add_css_class(f"{rating_css}-button")

        # Install, update, remove buttons
        if self.installed:
            self.remove_button.set_visible(True)
            self.install_button.set_label("Installed")
            self.install_button.set_sensitive(False)
            self.update_button.set_visible(self.app.update_available)
        else:
            self.remove_button.set_visible(False)
            self.install_button.set_label("Install")
            self.install_button.set_sensitive(True)
            self.update_button.set_visible(False)

        # summary and description
        self.summary.set_label(self.app.summary)
        self.description.set_label(self.app.description)

        # Set info rows
        set_row_if_not_none(self.homepage_row, self.app.homepage)
        set_row_if_not_none(self.donate_row, self.app.donate_url)
        self.source_row.set_title(f"Primary Source: {self.app.primary_src}")
        self.source_row.set_subtitle(self.app.src_pkg_name)
        set_row_if_not_none(self.category_row, ", ".join(self.app.categories))
        set_row_if_not_none(self.keywords_row, ", ".join(self.app.keywords))

        # Add screenshots
        for screenshot in self.app.screenshot_urls:
            image = UrlImage.UrlImage()
            image.set_from_url(screenshot)
            self.screenshot_box.add(image)

        # Show the page
        self.stillCenter.builder.get_object("main_view").add(self.nav_page)