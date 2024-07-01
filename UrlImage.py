import os
import shutil
from typing import Optional
from urllib.parse import urlparse, unquote

import gi
from gi.overrides.GdkPixbuf import GdkPixbuf

gi.require_version("Gtk", "4.0")
gi.require_version("Gdk", "4.0")
gi.require_version("Soup", "3.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Gdk, Soup, GLib, GObject, Adw

import constants

# Set cache location to ~/.cache/stillcenter
_CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache/stillcenter")
_ICON_DIR = os.path.join(_CACHE_DIR, "icons")
_SCREENSHOT_DIR = os.path.join(_CACHE_DIR, "screenshots")

for dir in [_CACHE_DIR, _ICON_DIR, _SCREENSHOT_DIR]:
    if not os.path.exists(dir):
        os.makedirs(dir)

# Clear out screenshot dir
shutil.rmtree(_SCREENSHOT_DIR)
os.makedirs(_SCREENSHOT_DIR)

@Gtk.Template(filename=os.path.join(constants.UI_DIR, "UrlImage.ui"))
class UrlImage(Adw.Bin):
    __gtype_name__ = "UrlImage"
    _screenshot: bool = False
    _image_url: str = ""
    _app_id: str = "app"
    image_dir = _ICON_DIR
    image_path = ""
    image: Gtk.Image = Gtk.Template.Child()

    def __init__(self):
        super().__init__()

    @GObject.Property(type=bool, default=False)
    def screenshot(self):
        return self._screenshot

    @screenshot.setter
    def screenshot(self, value):
        self._screenshot = value
        if value:
            self.image_dir = _SCREENSHOT_DIR
        else:
            self.image_dir = _ICON_DIR

    @GObject.Property(type=str)
    def app_id(self):
        return self._app_id

    @app_id.setter
    def app_id(self, value):
        self._app_id = value

        self.set_image_url(value, self._image_url)

    @GObject.Property(type=str)
    def image_url(self):
        return self._image_url

    @image_url.setter
    def image_url(self, value):
        self._image_url = value
        self.set_image_url(self._app_id, value)

    def clear_image(self):
        self.image.set_from_paintable(
            Gtk.IconTheme.get_for_display(
                Gdk.Display.get_default()
            ).lookup_icon(
                "image-missing-symbolic", [],
                64, 1, 1, Gtk.TextDirection.NONE
            )
        )

    def on_receive_bytes(self, session, result, message):
        bytes = session.send_and_read_finish(result)
        if message.get_status() != Soup.Status.OK:
            self.clear_image()

        with open(self.image_path, "wb") as f:
            f.write(bytes.get_data())

        try:
            texture = Gdk.Texture.new_from_bytes(bytes)
            self.image.set_from_paintable(texture)
        except GLib.Error:
            self.clear_image()

    def set_image_url(self, app_id, url):
        self.image_path = get_file_name_from_url(url, app_id, self.image_dir)

        if self.image_path is None:
            return

        if os.path.exists(self.image_path):
            self.image.set_from_file(self.image_path)
            return

        session = Soup.Session()
        try:
            message = Soup.Message(
                method="GET",
                uri=GLib.Uri.parse(url, GLib.UriFlags.NONE)
            )
        except GLib.GError:
            self.clear_image()
            return

        session.send_and_read_async(
            message, GLib.PRIORITY_DEFAULT, None, self.on_receive_bytes, message
        )


def get_file_name_from_url(url: Optional[str], app_id: str, base_dir: str) -> Optional[str]:
    if url == "" or url is None:
        return None
    if os.path.exists(url):
        return url

    # Parse the url to get the path
    path = urlparse(url).path

    # Get the file name from the path
    try:
        filename = unquote(path.split('/')[-1])
    except TypeError:
        return None

    return os.path.join(base_dir, f"{app_id}-{filename}")