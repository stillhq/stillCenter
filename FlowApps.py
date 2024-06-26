import os

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

import constants


@Gtk.Template(filename=os.path.join(constants.UI_DIR, "FlowApps.ui"))
class FlowApps(Gtk.Box):
    __gtype_name__ = "FlowApps"

    label = Gtk.Template.Child()
    flowbox = Gtk.Template.Child()