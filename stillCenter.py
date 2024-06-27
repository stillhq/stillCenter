import CategoryPage
import constants
import os
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw
from CategoryButtonBig import CategoryButtonBig
import AppStore, AppPage, FlowApps, AppGridView, AppListView, CategoryPage

class StillCenter(Adw.Application):
    def __init__(self):
        super().__init__(application_id="io.stillhq.stillCenter")

        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.path.join(constants.UI_DIR, "stillCenter.ui"))

        # Get objects from the builder
        self.window = self.builder.get_object("window")
        self.sidebar = self.builder.get_object("main_sidebar")
        self.sidebar_split = self.builder.get_object("sidebar_split_view")
        self.main_stack = self.builder.get_object("main_stack")
        self.categories_flowbox = self.builder.get_object("categories_flowbox")

        # Setting up the sidebar
        self.sidebar_index = []
        main_stack_pages = self.main_stack.get_pages()
        for i in range(main_stack_pages.get_n_items()):
            stack_page = main_stack_pages.get_item(i)
            sidebar_row = Gtk.ListBoxRow()
            label = Gtk.Label(label=stack_page.get_title(), xalign=0)
            sidebar_row.set_child(label)
            self.sidebar_index.append(stack_page.get_name())
            self.sidebar.append(sidebar_row)
        self.sidebar.connect("row-selected", self.sidebar_selected)

        # Set IDs of Flowboxes for Featured Apps
        FlowApps.set_stillcenter(self)

        # Populating Categories
        self.categories_flowbox.append(
            CategoryButtonBig(self, "Audio", "Audio", "audio-x-generic-symbolic")
        )
        self.categories_flowbox.append(
            CategoryButtonBig(self, "Development", "Development", "applications-engineering-symbolic")
        )
        self.categories_flowbox.append(
            CategoryButtonBig(self, "Education", "Education", "accessories-dictionary-symbolic")
        )
        self.categories_flowbox.append(
            CategoryButtonBig(self, "Game", "Games", "applications-games-symbolic")
        )
        self.categories_flowbox.append(
            CategoryButtonBig(self, "Graphics", "Graphics", "applications-graphics-symbolic")
        )
        self.categories_flowbox.append(
            CategoryButtonBig(self, "Network", "Network", "preferences-system-network-symbolic")
        )
        self.categories_flowbox.append(
            CategoryButtonBig(self, "Office", "Office", "applications-office-symbolic")
        )
        self.categories_flowbox.append(
            CategoryButtonBig(self, "Utility", "Utilities", "applications-utilities-symbolic")
        )
        self.categories_flowbox.append(
            CategoryButtonBig(self, "Video", "Video", "applications-multimedia-symbolic")
        )
        self.categories_flowbox.append(
            CategoryButtonBig(self, "System", "System", "preferences-other-symbolic")
        )

        # Set models of ListViews
        self.builder.get_object("available_updates").set_store(AppStore.INSTALLED_STORE["update"])
        self.builder.get_object("installed").set_store(AppStore.INSTALLED_STORE["no_update"])

        # Loading base pages
        self.app_page = AppPage.AppPage(self)
        self.category_page = CategoryPage.CategoryPage(self)

    def sidebar_selected(self, _listbox, row):
        self.main_stack.set_visible_child_name(self.sidebar_index[row.get_index()])
        if self.sidebar_split.get_collapsed() and not self.sidebar_split.get_show_content():
            self.sidebar_split.set_show_content(True)
        # if self.stack.get_visible_child_name() == "search":
        #     self.stack.get_visible_child().reset()

    def do_activate(self):
        self.window.set_application(self)
        self.window.present()
