import os

import gi

import constants
import sadb.database, sadb.Installe

gi.require_version("Gtk", "4.0")
from gi.repository import Gio, Gtk, GObject, GLib



class AppPage:
    installed = False
    app = None
    db = sadb.database.get_readable_db()

    def __init__(self, builder):
        self.window_builder = builder
        self.page_builder = Gtk.Builder()
        self.page_builder.add_from_file(os.path.join(constants.UI_DIR, "AppPage.ui"))

    def id_in_database(self, database, app_id):
        self.db.c.execute("SELECT id FROM ? WHERE id = ?", (database, app_id,))
        result = self.db.c.fetchone()
        return result is not None

    def show_app(self, app_id):
        if self.id_in_database("installed", app_id):
            self.db.c.execute("SELECT * FROM apps WHERE id=?", (app_id,))
            fetch_app = self.db.c.fetchone()
            if fetch_app is not None:
                self.app = self.db.column_to_installed_app(fetch_app)
                self.installed = True
            else:
                self.app = None
        else:
            self.installed = False
            self.app = self.db.get_app(app_id)

        if self.app is None:
            return

