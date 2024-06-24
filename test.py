import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

@Gtk.Template(filename="AppGridButton.ui")
class AppGridButton(Gtk.Button):
    __gtype_name__ = "AppGridButton"

    button_box = Gtk.Template.Child()

class Application(Gtk.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = Gtk.ApplicationWindow(application=self)
        button = AppGridButton()
        win.set_child(button)
        win.present()

app = Application()
app.run()