import os

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

import constants


@Gtk.Template(filename=os.path.join(constants.UI_DIR, "CategoryButtonBig.ui"))
class CategoryButtonBig(Gtk.Button):
    __gtype_name__ = "CategoryButtonBig"

    category: str = None
    title: str = None
    label: Gtk.Label = Gtk.Template.Child()
    icon: Gtk.Image = Gtk.Template.Child()
    stillCenter = None

    def __init__(self, stillCenter, category: str, title: str, icon: str):
        super().__init__()
        self.category = category
        self.title = title
        self.stillCenter = stillCenter
        self.label.set_label(title)
        self.icon.set_from_icon_name(icon)

        self.connect("clicked", self.clicked)

    def clicked(self, button):
        self.stillCenter.category_page.push_category(self.category, self.title)