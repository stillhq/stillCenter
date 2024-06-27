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
    label: Gtk.Label = Gtk.Template.Child()
    icon: Gtk.Image = Gtk.Template.Child()
    builder: Gtk.Builder = None

    def __init__(self, builder: Gtk.Builder, category: str, title: str, icon: str):
        super().__init__()
        self.category = category
        self.builder = builder
        self.label.set_label(title)
        self.icon.set_from_icon_name(icon)
