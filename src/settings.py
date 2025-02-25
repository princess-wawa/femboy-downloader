from gi.repository import GLib, Gtk, Adw
from pathlib import Path
import os
import json

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
            print(e)

    def reload_preferences(self):
        try:
            f = open(self.file, 'r')
            self.preferences = json.loads(f.read())
            f.close()
        except Exception as e:
            print(e)

    def get_preference(self, key):
        self.reload_preferences()
        if key in self.preferences:
            return self.preCatgirlDownloader/data/ui/preferences.uiferences[key]
        else:
            return None
    def set_preference(self, key, value):
        self.preferences[key] = value
        try:
            f = open(self.file, "w+")
            f.write(json.dumps(self.preferences))
            f.close()
        except Exception as e:
            print(e)

preferencepath = str(Path(__file__).parent.parent / "ui" / "preferences.ui")

class settingswindow(Adw.PreferencesWindow):
    __gtype_name__ = 'PreferencesWindow'

    def __init__(self, window, **kwargs):
        builder = Gtk.Builder()
        builder.add_from_file(preferencepath)
        super().__init__(**kwargs)
        self.win = window
        self.settings = UserPreferences()

        
        self.nsfw_switch = builder.get_object("nsfw") 

        print(self.settings.get_preference("nsfw"))
        self.nsfw_switch.set_state(self.settings.get_preference("nsfw"))
        self.nsfw_switch.connect('notify::active', self.toggle_nsfw)

    def toggle_nsfw(self, switch, _active):
        pref = self.nsfw_switch.get_active()
        self.settings.set_preference("nsfw", pref)
