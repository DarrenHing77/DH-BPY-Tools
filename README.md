# DH-BPY-Tools

A collection of Blender add-ons written in Python.  These scripts provide
custom modelling and project management utilities, sculpting pie menus and
helpers for handling UDIM textures or ACES colour settings.  They are intended
for Blender power users who want a set of convenience tools.

## Repository contents

- **DH_Toolkit/** – main add-on providing a pie menu and numerous operators for
  exporting, project setup and mesh utilities.
- **DH_Custom_Sculpt_Pie.py** – simple pie menu that exposes common sculpt
  brushes.
- **DH-Project-Manager/** – utility script to generate a folder layout for a new
  project.
- **dh_texture_tools.py** – operators for adding and filling UDIM tiles from the
  Image Editor.
- **dh_aces_settings.py** – panel for setting image colour spaces and converting
  image nodes to UDIMs.

All modules rely on the `bpy` module and therefore must be run from inside
Blender.

## Installing an add‑on

Each script or directory can be installed individually:

1. In Blender open **Edit → Preferences → Add-ons**.
2. Click **Install…** and select the Python file or the `DH_Toolkit` folder
   (zipped).
3. Enable the add-on from the list.

Alternatively the repository can be cloned into the Blender add-ons directory
(usually `~/Library/Application Support/Blender/[version]/scripts/addons/` on
macOS or `%APPDATA%\Blender Foundation\Blender\[version]\scripts\addons` on
Windows).

## Usage highlights

### DH_Toolkit

After enabling, a main pie menu becomes available (default shortcut `Shift+X`).
It provides quick access to modelling and sculpt utilities, project management
operators and export functions such as multi–FBX export.  Preferences for the
shortcut key are found under **Edit → Preferences → Add-ons → DH Toolkit**.

### Custom Sculpt Pie

In sculpt mode press `W` to open a menu of commonly used sculpting brushes.

### Project Manager

Invoke **Create Project Directories** from the *Object* menu to generate a
standardised folder tree.  Folders in the popup can be expanded or collapsed to
manage long hierarchies. Optionally the current scene can be saved to the new
project directory.

### Texture Tools and ACES Settings

`dh_texture_tools.py` adds a panel in the Image Editor for managing UDIM tiles.
`dh_aces_settings.py` adds controls in the Shader Editor for setting colour
spaces and converting textures to UDIM.

## Development

Pull requests are welcome.  Changes should be tested in a recent version of
Blender.  There is no automated test suite; manual verification is required.

## License

No explicit license is provided with the repository.  Consult the repository
owner before distributing modified versions.
