import os

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

import AppStore, UrlImage

import constants


@Gtk.Template(filename=os.path.join(constants.UI_DIR, "FlowAppButton.ui"))
class FlowAppButton(Gtk.Button):
    __gtype_name__ = "FlowAppButton"

    name_label: Gtk.Label = Gtk.Template.Child()
    author_label: Gtk.Label = Gtk.Template.Child()
    icon: UrlImage.UrlImage = Gtk.Template.Child()
    builder: Gtk.Builder = None

    def __init__(self, stillCenter, app_id: str, name: str, author: str, icon: str):
        super().__init__()
        self.app_id = app_id
        self.stillCenter = stillCenter
        self.name_label.set_label(name)
        self.author_label.set_label(author)
        self.icon.set_image_url(app_id, icon)
        self.connect("clicked", self.on_click)

    def on_click(self, *args, **kwargs):
        self.stillCenter.app_page.show_app(self.app_id)


@Gtk.Template(filename=os.path.join(constants.UI_DIR, "FlowApps.ui"))
class FlowApps(Gtk.Box):
    __gtype_name__ = "FlowApps"

    label = Gtk.Template.Child()
    flowbox = Gtk.Template.Child()

    def set_apps(self, stillCenter, apps: str, title: str):
        self.label.set_label(title)

        for item in AppStore.STORE[apps][:8]:
            self.flowbox.append(
                FlowAppButton(stillCenter, item.app_id, item.name, item.author, item.icon)
            )
