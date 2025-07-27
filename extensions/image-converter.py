import gi
gi.require_version('Nautilus', '4.0')
from gi.repository import Nautilus, GObject
import subprocess
import os

class ImageConvertExtension(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        super().__init__()

    def get_file_items(self, files):
        if not files:
            return

        if not all(f.get_mime_type().startswith('image/') for f in files):
            return

        convert_menu_item = Nautilus.MenuItem(
            name="ImageConvertExtension::Convert",
            label="Convert",
            tip="Convert selected images to different formats"
        )

        submenu = Nautilus.Menu()

        formats = [
            ("jpg", "Convert to JPG"),
            ("png", "Convert to PNG"),
            ("webp", "Convert to WEBP"),
        ]

        for fmt, label in formats:
            item = Nautilus.MenuItem(
                name=f"ImageConvertExtension::ConvertTo{fmt.upper()}",
                label=label,
                tip=f"Convert selected images to {fmt.upper()}"
            )
            item.connect("activate", self.convert_to_format, files, fmt)
            submenu.append_item(item)

        convert_menu_item.set_submenu(submenu)

        return [convert_menu_item]

    def convert_to_format(self, menu, files, fmt):
        for f in files:
            path = f.get_location().get_path()
            dirname, basename = os.path.split(path)
            name, ext = os.path.splitext(basename)
            output_path = os.path.join(dirname, f"{name}_converted.{fmt}")

            subprocess.run(
                ['ffmpeg', '-y', '-i', path, output_path],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

