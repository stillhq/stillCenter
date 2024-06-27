import os

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GObject

import AppStore, UrlImage

import constants

flow_apps = []

def set_stillcenter(stillCenter):
    for flow_app in flow_apps:
        flow_app.stillCenter = stillCenter

@Gtk.Template(filename=os.path.join(constants.UI_DIR, "FlowAppButton.ui"))
class FlowAppButton(Gtk.Button):
    __gtype_name__ = "FlowAppButton"

    name_label: Gtk.Label = Gtk.Template.Child()
    author_label: Gtk.Label = Gtk.Template.Child()
    icon: UrlImage.UrlImage = Gtk.Template.Child()

    def __init__(self, flow_apps, app_id: str, name: str, author: str, icon: str):
        super().__init__()
        self.flow_apps = flow_apps
        self.app_id = app_id
        self.name_label.set_label(name)
        self.author_label.set_label(author)
        self.icon.set_image_url(app_id, icon)
        self.connect("clicked", self.on_click)

    def on_click(self, *args, **kwargs):
        self.flow_apps.stillCenter.app_page.show_app(self.app_id)


@Gtk.Template(filename=os.path.join(constants.UI_DIR, "FlowApps.ui"))
class FlowApps(Gtk.Box):
    __gtype_name__ = "FlowApps"

    label = Gtk.Template.Child()
    flowbox = Gtk.Template.Child()
    stillCenter = None
    _tag = None
    _title = None

    def __init__(self):
        super().__init__()
        flow_apps.append(self)

    @GObject.property(type=str)
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value
        for item in AppStore.STORE[self._tag][:8]:
            self.flowbox.append(
                FlowAppButton(self, item.app_id, item.name, item.author, item.icon)
            )

    @GObject.property(type=str)
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        self.label.set_label(self._title)