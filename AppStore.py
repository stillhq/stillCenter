import os

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gio, Gtk, GObject, GLib

import sadb.database

STORE = {"all": Gio.ListStore()}
INSTALLED_STORE = {"installed": Gio.ListStore(), "update": Gio.ListStore(), "no_update": Gio.ListStore()}


class AppItem(GObject.Object):
    __gtype_name__ = "AppItem"

    def __init__(self, app_id, name, author, icon):
        super().__init__()
        self._app_id = app_id
        self._name = name
        self._author = author
        self._author_visible = self._author is not None
        self._icon = icon
        self._installed = False
        self._update = False

    @classmethod
    def new_installed(cls, app_id, name, author, icon, installed, update):
        app = cls(app_id, name, author, icon)
        app._installed = installed
        app._update = update
        return app

    @GObject.Property(type=str)
    def app_id(self):
        return self._app_id

    @app_id.setter
    def app_id(self, value):
        self._app_id = value

    @GObject.Property(type=str)
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @GObject.Property(type=str)
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value
        self.author_visible = self._author is not None

    @GObject.Property(type=bool, default=True)
    def author_visible(self):
        return self._author_visible

    @author_visible.setter
    def author_visible(self, value):
        self._author_visible = value

    @GObject.Property(type=str)
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value

    @GObject.Property(type=bool, default=False)
    def installed(self):
        return self._installed

    @installed.setter
    def installed(self, value):
        self._installed = value

    @GObject.Property(type=bool, default=False)
    def update(self):
        return self._update

    @update.setter
    def update(self, value):
        self._update = value


def refresh_app_store():
    db = sadb.database.get_readable_db()
    db.c.execute("SELECT id, name, author, icon_url, categories, keywords FROM apps")
    apps_columns = db.c.fetchall()

    for app in apps_columns:
        categories = app[4].split(",")
        keywords = app[5].split(",")

        app_item = AppItem(app[0], app[1], app[2], app[3])

        for category in categories:
            if category not in STORE.keys():
                STORE[category] = Gio.ListStore()
            STORE[category].append(app_item)
        for keyword in keywords:
            if keyword not in STORE.keys():
                STORE[keyword] = Gio.ListStore()
            STORE[keyword].append(app_item)
        STORE["all"].append(app_item)


def refresh_installed_store():
    db = sadb.database.get_readable_db()
    db.c.execute("SELECT id, name, author, icon_url, categories, keywords, update_available FROM installed")
    apps_columns = db.c.fetchall()

    for app in apps_columns:
        app_item = AppItem.new_installed(app[0], app[1], app[2], app[3], True, app[6])

        INSTALLED_STORE["installed"].append(app_item)
        if app[6]:
            INSTALLED_STORE["update"].append(app_item)
        else:
            INSTALLED_STORE["no_update"].append(app_item)
