import os

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Soup", "3.0")

from gi.repository import Gtk, Gdk, Soup

import constants


@Gtk.Template(filename=os.path.join(constants.UI_DIR, "AppListView.ui"))
class AppListView(Gtk.ListView):
    __gtype_name__ = "AppListView"

    def __init__(self):
        super().__init__()

    def set_store(self, model: Gtk.ListStore):
        self.set_model(Gtk.NoSelection.new(model))