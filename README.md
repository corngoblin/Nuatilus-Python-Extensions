
# Nautilus-Python-Extensions

To make these work you'll need to install the package "nautilus-python" in Fedora, that would be `sudo dnf install nautilus-python`. 

To use these extensions, place the files in the directory `~/local/share/nautilus-python/extensions` and ensure they are executable.
# new-text.py

This extension adds a context menu option for creating a "New Text File." It'll make a new text file in the current directory.

<img width="221" height="283" alt="Screenshot From 2025-07-27 17-40-45" src="https://github.com/user-attachments/assets/d9933085-3549-4d6f-a69b-d124d194e039" />
<img width="449" height="177" alt="Screenshot From 2025-07-27 17-40-56" src="https://github.com/user-attachments/assets/5759a8bd-c189-42af-a872-8496e2bf4224" />

To create a new text file, type the desired name and click "Create" or press the Enter key. If you want the file to have a specific extension (e.g., `.sh,` `.py`), be sure to include it in the name.
# image-converter.py

This extension allows you to convert image files directly from the context menu. When you right-click an image file, you'll see an option to "Convert." Clicking this will open a submenu where you can select the desired format for conversion.

<img width="263" height="333" alt="Screenshot From 2025-07-27 17-45-09" src="https://github.com/user-attachments/assets/381f5f56-f99d-493e-a6ee-82dccba66e2b" />
<img width="259" height="131" alt="Screenshot From 2025-07-27 17-45-17" src="https://github.com/user-attachments/assets/905d9085-4857-4c97-9d33-83f24ee2d07e" />

Currently, it supports JPG, PNG, and WEBP formats. Adding support for additional formats is straightforward, as it utilizes ffmpeg for image conversion.
