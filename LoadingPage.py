import os

import gi

import constants

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw


@Gtk.Template(filename=os.path.join(constants.UI_DIR, "LoadingPage.ui"))
class LoadingPage(Adw.NavigationPage):
    __gtype_name__ = "LoadingPage"
    stillCenter = None
    spinner: Gtk.Spinner = Gtk.Template.Child()

    def __init__(self, stillCenter):
        super().__init__()
        self.stillCenter = stillCenter

    def push(self):
        self.spinner.start()
        self.stillCenter.main_view.push(self)

    def pop(self):
        self.stillCenter.main_view.pop()
        self.spinner.stop()
