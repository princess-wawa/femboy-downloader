from gi.repository import GLib, Gtk, Adw
from pathlib import Path
import os
import json

from tools import *

class UserPreferences:
    def __init__(self):
        self.preferences = {
            "nsfw": False,
        }
        self.directory = GLib.get_user_config_dir()
        self.file = str(Path(__file__).parent.parent / "settings" / "settings.json")
        if not os.path.exists(self.file):
            f = open(self.file, "w+")
            f.write(json.dumps(self.preferences))
            f.close()
        try:
            f = open(self.file, 'r')
            self.preferences = json.loads(f.read())
            f.close()
        except Exception as e:
            log_error(e)

    def reload_preferences(self):
        try:
            f = open(self.file, 'r')
            self.preferences = json.loads(f.read())
            f.close()
        except Exception as e:
            log_error(e)

    def get_preference(self, key):
        self.reload_preferences()
        if key in self.preferences:
            return self.preferences[key]
        else:
            return None

    def set_preference(self, key, value):
        self.preferences[key] = value
        try:
            f = open(self.file, "w+")
            f.write(json.dumps(self.preferences))
            f.close()
            log(f"set preference {key} to {value}")
        except Exception as e:
            log_error(e)

preferencepath = str(Path(__file__).parent.parent / "ui" / "preferences.ui")

class settingswindow:
    def __init__(self, parent_window):
        builder = Gtk.Builder()
        builder.add_from_file(preferencepath)

        self.window = builder.get_object("PreferencesWindow")
        self.settings = UserPreferences()
        self.parent = parent_window

        # Setup switch
        self.nsfw_switch = builder.get_object("nsfw")
        print(self.settings.get_preference("nsfw"))
        self.nsfw_switch.set_state(bool(self.settings.get_preference("nsfw")))
        self.nsfw_switch.connect('notify::active', self.toggle_nsfw)

        self.window.set_transient_for(parent_window)
        self.window.set_modal(True)

    def toggle_nsfw(self, switch, _):
        self.settings.set_preference("nsfw", switch.get_active())

    def present(self):
        self.window.present()

