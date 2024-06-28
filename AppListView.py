import os

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

import constants


@Gtk.Template(filename=os.path.join(constants.UI_DIR, "AppListView.ui"))
class AppListView(Gtk.ListView):
    __gtype_name__ = "AppListView"
    stillCenter = None

    def __init__(self):
        super().__init__()
        self.connect("activate", self.activate)

    def set_store(self, stillCenter, model: Gtk.ListStore):
        self.stillCenter = stillCenter
        self.set_model(Gtk.NoSelection.new(model))

    def activate(self, _app_list_view, index):
        self.stillCenter.app_page.show_app(self.get_model().get_item(index).app_id)
