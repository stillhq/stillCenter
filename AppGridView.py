import os

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

import constants


@Gtk.Template(filename=os.path.join(constants.UI_DIR, "AppGridView.ui"))
class AppGridView(Gtk.GridView):
    __gtype_name__ = "AppGridView"