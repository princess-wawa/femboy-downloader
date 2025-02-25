import sys
import gi
import threading
import json
from pathlib import Path
import time
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, Adw, GdkPixbuf, GLib, Gdk
import buttons as buttons
import reddit as jp
from settings import *

apppath = str(Path(__file__).parent.parent / "ui" / "main.ui") 

class femboydownloaderApplication(Adw.Application):
    """The main application singleton class."""
    
    __gtype_name__ = 'WallpaperDownloaderWindow'
    settings = Gtk.Template.Child("settings")
    download = Gtk.Template.Child("download")
    wallpaper = Gtk.Template.Child("wallpaper")
    
    def __init__(self):
        super().__init__(application_id='wawa.femboydownloader',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.quit, ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('show-art-about', self.on_art_about_action)
             
    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        # Create a Builder
        builder = Gtk.Builder()
        builder.add_from_file(apppath)

        # Obtain and show the main window
        self.win = builder.get_object("main")
        self.win.set_application(self)  # Application will close once it no longer has active windows attached to it
        self.win.set_title("femboy Downloader")
        
        
        # set button up references
        self.settings = builder.get_object("settings")
        self.download = builder.get_object("download")
        self.wallpaper = builder.get_object("wallpaper")
        self.refresh = builder.get_object("refresh")
        self.settings.connect("clicked", self.on_settings_action)
        self.download.connect("clicked", self.on_download_action)
        self.wallpaper.connect("clicked", self.on_wallpaper_action)
        self.refresh.connect("clicked", self.async_on_refresh_action)
        
        #get things on the window
        self.image = builder.get_object("image")
        self.spinner = builder.get_object("spinner")
        self.spinner.stop()
        self.spinner.set_visible(False)
        
        self.win.present()
        path = str(Path(__file__).parent.parent / "response" / "response.jpg")
        self.image.set_from_file(path)

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = Adw.AboutWindow(transient_for=self.props.active_window,
                                application_name='femboy Downloader',
                                application_icon='/usr/share/icons/Adwaita/symbolic/emblems/emblem-photos-symbolic.svg',
                                developer_name='wawa',
                                version='0.0.1',
                                developers=['Princess_wawa'],
                                copyright='© 2024 princess_wawa')
        about.present()

    def on_art_about_action(self, widget, _):
        """Callback for the app.about action."""
        response = jp.getresponce()
        if response.get("Source", {}) != {}:
            about = Adw.AboutWindow(transient_for=self.props.active_window,
                                    artists=[f"u/{response['Author']}"],
                                    website=response['Source'])
        else:
            about = Adw.AboutWindow(transient_for=self.props.active_window,
                                    artists=[f"u/{response['Author']}"])
        about.present()

    def on_settings_action(self,widget):
        """Callback for the app.preferences action."""
        print("aaaaa")
        window = settingswindow(self.window)
        window.set_transient_for(self.window)
        window.set_modal(True)
        window.present()

        

    def on_download_action(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Save File",
            action=Gtk.FileChooserAction.SAVE,
        )

        # get the Downloads folder to create the dialog on it
        downloads_folder = str(Path(os.path.expanduser("~")) / "Downloads")
        gio_file = Gio.File.new_for_path(downloads_folder)
        dialog.set_current_folder(gio_file)

        # Set the default filename
        dialog.set_current_name("downloaded_wallpaper.jpg")
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("Save", Gtk.ResponseType.ACCEPT)

        # Handle the response
        def on_response(dialog, response):
            if response == Gtk.ResponseType.ACCEPT:
                save_path = dialog.get_file().get_path()
                print(f"File will be saved to: {save_path}")
                buttons.download(save_path)  

            dialog.destroy()

        dialog.connect("response", on_response)
        dialog.show()


        
    def on_wallpaper_action(self,widget):
        buttons.wallpaper()
    
    def show_error_dialog(self, aaa, title, message):
        dialog = Adw.AlertDialog.new(title, None)
        dialog.set_body(message)
        dialog.add_response("ok", "_OK")
        dialog.set_default_response("ok")
        dialog.set_close_response("ok")
        dialog.connect("response", self.on_response)
        dialog.present(self.refresh)

    def on_response(self, dialog, response):
        return
    
    def async_on_refresh_action(self, widget=""):
        t = threading.Thread(target=self.on_refresh_action, args=(self,))
        t.start()
        self.image.set_visible(False)
        self.spinner.set_visible(True)
        self.spinner.start()
        t.join

        
    def on_refresh_action(self, widget=""):
        a = jp.reloadimage()
        path = str(Path(__file__).parent.parent / "response" / "response.jpg")
        self.image.set_from_file(path)
        self.spinner.stop()
        self.spinner.set_visible(False)
        self.image.set_visible(True)
        if a != True:
            error = json.loads(a[1].decode('utf-8')).get("errors")[0]
            # ^ this is unreadable but it gets the error out of strings like b'{"errors":["Not found"]}'
            print(f"HTTP status code: {a[0]}, {a[1]}")
            self.show_error_dialog(self, f"HTTP status code:{a[0]}", f"{error}")
        
        
    
    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main():
    """The application's entry point."""
    app = femboydownloaderApplication()
    app.run(sys.argv)
    
main()
