#!/usr/bin/env python3
import gi
import os
import sys

# Require necessary versions
try:
    gi.require_version('Nautilus', '4.0')
    gi.require_version('Gtk', '4.0')
    gi.require_version('Adw', '1')
except ValueError as e:
    print(f"Error requiring GI versions: {e}", file=sys.stderr, flush=True)

from gi.repository import Nautilus, GObject, Gtk, Adw, Gdk

# Initialize libadwaita (Adw)
Adw.init()

class NewTextFileExtension(GObject.GObject, Nautilus.MenuProvider):
    def get_background_items(self, folder):
        """
        Provide right-click menu item to create a new text file.
        """
        item = Nautilus.MenuItem(
            name="NewTextFileExtension::NewTextFile",
            label="New Text File",
            tip="Create a new blank text file"
        )
        item.connect('activate', self.create_new_text_file, folder)
        return [item]

    def create_new_text_file(self, menu, folder):
        """
        Show dialog to enter filename and create the file.
        """
        dialog = Adw.Dialog()
        dialog.set_title("New Text File")
        dialog.set_content_width(450)

        # Setup dialog layout with header and content box
        root = Adw.ToolbarView()
        header_bar = Adw.HeaderBar()
        header_bar.set_decoration_layout(':close')
        root.add_top_bar(header_bar)

        content_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            hexpand=True,
            spacing=8,
            margin_top=16,
            margin_bottom=16,
            margin_start=16,
            margin_end=16
        )
        root.set_content(content_box)

        # Entry row for filename input
        list_box = Gtk.ListBox(css_classes=["boxed-list-separate"])
        content_box.append(list_box)
        entry_row = Adw.EntryRow(title="File Name")
        list_box.append(entry_row)

        # Create button to trigger file creation
        create_button = Gtk.Button(
            label="Create",
            css_classes=["pill", "suggested-action"],
            halign=Gtk.Align.CENTER,
            margin_top=8
        )
        content_box.append(create_button)

        dialog.set_child(root)

        def create_file(_=None):
            filename = entry_row.get_text().strip()
            if not filename:
                self.show_error("Please enter a file name.")
                return

            folder_path = folder.get_location().get_path()
            new_file_path = os.path.join(folder_path, filename)

            if os.path.exists(new_file_path):
                self.show_error(f"File '{filename}' already exists.")
                return

            try:
                with open(new_file_path, 'w'):
                    pass  # Create an empty file
            except Exception as e:
                self.show_error(f"Failed to create file:\n{e}")
            else:
                dialog.close()

        # Connect button click to create_file
        create_button.connect("clicked", create_file)

        # Handle Enter key to trigger create_file
        key_controller = Gtk.EventControllerKey.new()
        key_controller.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        dialog.add_controller(key_controller)

        def on_key_pressed(controller, keyval, *args):
            if keyval in (Gdk.KEY_Return, Gdk.KEY_KP_Enter):
                create_file()
                return Gdk.EVENT_STOP
            return Gdk.EVENT_PROPAGATE

        key_controller.connect("key-pressed", on_key_pressed)

        # Show dialog and focus input
        entry_row.set_can_focus(True)
        dialog.present()
        entry_row.grab_focus()

    def show_error(self, message):
        """
        Display an error dialog with the given message.
        """
        error_dialog = Adw.MessageDialog.new()
        error_dialog.props.heading = "Error"
        error_dialog.props.body = message
        error_dialog.add_response("close", "Close")
        error_dialog.connect("response", lambda d, r: d.destroy())
        error_dialog.present()

