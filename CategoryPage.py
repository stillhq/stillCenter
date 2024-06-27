import os

import gi

import AppGridView
import AppStore
import AppListView

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

import constants

category_pages = []


@Gtk.Template(filename=os.path.join(constants.UI_DIR, "CategoryPage.ui"))
class CategoryPage(Adw.NavigationPage):
    __gtype_name__ = "CategoryPage"

    category_title: Gtk.Label = Gtk.Template.Child()
    subcategory_button_box: Gtk.Box = Gtk.Template.Child()
    app_grid: AppGridView.AppGridView = Gtk.Template.Child()

    main_category_page = True
    stillCenter = None

    def __init__(self, stillCenter):
        super().__init__()
        self.stillCenter = stillCenter
        category_pages.append(self)

    def push_category(self, category, title):
        self.category_title.set_label(title)
        self.app_grid.set_model(Gtk.NoSelection.new(AppStore.STORE[category]))

        # Clear the subcategory buttons
        if self.main_category_page:
            # Clearing Buttons
            child = self.subcategory_button_box.get_first_child()
            while child is not None:
                self.subcategory_button_box.remove(child)
                child = self.subcategory_button_box.get_first_child()

            if category in constants.SUBCATEGORIES.keys():
                for subcategory in AppStore.SUBCATEGORIES[category]:
                    button = Gtk.Button(label=subcategory[1])
                    button.connect("clicked", self.on_subcategory_clicked, subcategory[0], subcategory[1])
                    self.subcategory_button_box.append(button)

        main_view = self.stillCenter.builder.get_object("main_view")
        main_view.push(self)

    def on_subcategory_clicked(self, button, subcategory, title):
        CategoryPage.new_for_subcategory(self.stillCenter, subcategory, title)

    @classmethod
    def push_subcategory(cls, stillCenter, category, title):
        page = cls(stillCenter)
        page.main_category_page = False
        page.set_category(category, title)
        return page
