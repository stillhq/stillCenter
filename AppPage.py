import os
import threading
from typing import Optional

import gi

import constants
import sadb, sadb.database
from SamInterface import sam_interface

import UrlImage
import sam.quick

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
    update_available = False
    app = None
    db = sadb.database.get_readable_db()

    def __init__(self, stillCenter):
        self.stillCenter = stillCenter
        self.page_builder = Gtk.Builder()
        self.page_builder.add_from_file(os.path.join(constants.UI_DIR, "AppPage.ui"))
        self.nav_page = self.page_builder.get_object("nav_page")
        self.icon = self.page_builder.get_object("icon")
        self.name = self.page_builder.get_object("name_label")
        self.author = self.page_builder.get_object("author_label")
        self.rating_button = self.page_builder.get_object("rating_button")
        self.rating_label = self.page_builder.get_object("rating_label")
        self.remove_button = self.page_builder.get_object("remove_button")
        self.install_button = self.page_builder.get_object("install_button")
        self.update_button = self.page_builder.get_object("update_button")
        self.screenshot_scroll = self.page_builder.get_object("screenshot_scroll")
        self.screenshot_box = self.page_builder.get_object("screenshot_box")
        self.summary = self.page_builder.get_object("summary_label")
        self.description = self.page_builder.get_object("description")
        self.homepage_row = self.page_builder.get_object("homepage_row")
        self.donate_row = self.page_builder.get_object("donate_row")
        self.source_row = self.page_builder.get_object("source_row")
        self.category_row = self.page_builder.get_object("category_row")
        self.keyword_row = self.page_builder.get_object("keyword_row")

        sam_interface.connect_to_signal("queue_changed", self.check_buttons)
        self.install_button.connect("clicked", lambda button: self.run_action("install"))
        self.update_button.connect("clicked", lambda button: self.run_action("update"))
        self.remove_button.connect("clicked", lambda button: self.run_action("remove"))
        #sam_interface.connect_to_signal("percent_changed", self.update_percentage)

    def id_in_installed_database(self, app_id):
        self.db.c.execute("SELECT id FROM installed WHERE id = ?", (app_id,))
        result = self.db.c.fetchone()
        return result is not None

    def show_app(self, app_id):
        # Get an installed app if it exists, or try to get a remote app
        if self.id_in_installed_database(app_id):
            self.db.c.execute("SELECT * FROM installed WHERE id=?", (app_id,))
            fetch_app = self.db.c.fetchone()
            if fetch_app is not None:
                self.app = self.db.column_to_installed_app(fetch_app)
                self.installed = True
                self.update_available = self.app.update_available
            else:
                self.app = None
        else:
            self.installed = False
            self.app = self.db.get_app(app_id)

        if self.app is None:
            return

        # clear screenshot boxes
        child = self.screenshot_box.get_first_child()
        while child is not None:
            self.screenshot_box.remove(child)
            child = self.screenshot_box.get_first_child()

        # Set icon, name, author
        self.icon.set_image_url(self.app.app_id, self.app.icon_url)
        self.name.set_label(self.app.name)
        if self.app.author is not None:
            self.author.set_visible(True)
            self.author.set_label(self.app.author)
        else:
            self.author.set_visible(False)

        # Set rating text and rating css
        rating_text, rating_css = still_rating_to_display(self.app.still_rating)
        self.rating_label.set_label(rating_text)
        clear_css_classes(self.rating_button)
        if rating_css is not None:
            self.rating_button.add_css_class(rating_css)
            self.rating_button.add_css_class(f"{rating_css}-button")

        self.update_buttons()

        # summary and description
        self.summary.set_label(self.app.summary)
        self.description.set_label(self.app.description)

        # Set info rows
        set_row_if_not_none(self.homepage_row, self.app.homepage)
        set_row_if_not_none(self.donate_row, self.app.donate_url)
        self.source_row.set_title(f"Primary Source: {self.app.primary_src}")
        self.source_row.set_subtitle(self.app.src_pkg_name)
        set_row_if_not_none(self.category_row, ", ".join(self.app.categories))
        set_row_if_not_none(self.keyword_row, ", ".join(self.app.keywords))

        # Add screenshots
        for screenshot in self.app.screenshot_urls:
            if screenshot != "":
                image = UrlImage.UrlImage()
                image.set_image_url(self.app.app_id, screenshot)
                self.screenshot_box.append(image)
            else:
                self.app.screenshot_urls.remove(screenshot)
        self.screenshot_scroll.set_visible(len(self.app.screenshot_urls) > 0)

        # Show the page
        main_view = self.stillCenter.builder.get_object("main_view")
        main_view.push(self.nav_page)

    def update_buttons_async(self):
        database = sadb.database.get_readable_db()
        database.c.execute("SELECT id, update_available FROM installed WHERE src_pkg_name = ?", (self.app.src_pkg_name,))  # temp
        app = database.c.fetchone()

        if app is not None:
            self.installed = True
            self.update_available = app[1]
        else:
            self.installed = False
            self.update_available = False
        GLib.idle_add(self.update_buttons)
        GLib.idle_add(self.update_percentage)

    def update_buttons(self):
        in_queue = False
        queue = sam.quick.get_queue_dicts()
        if not queue:
            queue = {}   # so code doesn't break
        if len(queue) != 0:
            if self.app.src_pkg_name in [action["package_id"] for action in queue]:
                in_queue = True
                self.install_button.set_sensitive(False)
                self.update_button.set_sensitive(False)
                self.remove_button.set_sensitive(False)

                if self.app.src_pkg_name == queue[0]["package_id"]:
                    match queue[0]["task"].lower():
                        case "install":
                            self.install_button.set_label(f"Installing {queue[0]["progress"]}%")
                        case "remove":
                            self.remove_button.set_label(f"Removing {queue[0]["progress"]}%")
                        case "update":
                            self.update_button.set_label(f"Updating {queue[0]["progress"]}%")
                else:
                    self.install_button.set_label("Waiting")
        if not in_queue:
            self.update_button.set_sensitive(True)
            self.remove_button.set_sensitive(True)

            if self.installed:
                self.install_button.set_sensitive(False)
                self.install_button.remove_css_class("suggested-action")
                self.install_button.set_label("Installed")
                if self.update_available:
                    self.update_button.set_visible(True)
                self.remove_button.set_visible(True)
                # self.try_btn.set_visible(False)
            else:
                self.install_button.add_css_class("suggested-action")
                self.install_button.set_label("Install")
                self.install_button.set_sensitive(True)
                self.update_button.set_visible(False)
                self.remove_button.set_visible(False)
                # self.try_btn.set_visible(self.app.demo_url is not None and self.app.demo_url != "")

    def check_buttons(self):
        if self.app is None:
            return

        # Temporarily disable buttons while checking
        self.install_button.set_label("Loading...")
        self.install_button.set_sensitive(False)
        self.update_button.set_visible(False)
        self.remove_button.set_visible(False)
        thread = threading.Thread(target=self.update_buttons_async)
        thread.start()


    def update_percentage(self):
        queue = sam.quick.get_queue_dicts()
        if not queue:
            return
        if len(queue) != 0:
            if self.app.src_pkg_name in [action["package_id"] for action in queue]:
                self.install_button.set_sensitive(False)
                self.update_button.set_sensitive(False)
                self.remove_button.set_sensitive(False)
                print(queue)
                if self.app.src_pkg_name == queue[0]["package_id"]:
                    match queue[0]["task"].lower():
                        case "install":
                            self.install_button.set_label(f"Installing {queue[0]["progress"]}%")
                        case "remove":
                            self.remove_button.set_label(f"Removing {queue[0]["progress"]}%")
                        case "update":
                            self.update_button.set_label(f"Updating {queue[0]["progress"]}%")
                else:
                    self.install_button.set_label("Waiting")
            else:
                self.update_button.set_sensitive(True)
                self.remove_button.set_sensitive(True)
        else:
            if self.installed:
                self.install_button.set_label(f"Installed")
                self.install_button.set_sensitive(False)
            else:
                self.install_button.set_label(f"Install")
                self.install_button.set_sensitive(True)


    def run_action(self, action):
        sam_interface.add_dict_to_queue(
            {
                "package_id": self.app.src_pkg_name,
                "app_name": self.app.name,
                "task": action,
                "manager_id": self.app.primary_src,
                "background": "True"
            }
        )
