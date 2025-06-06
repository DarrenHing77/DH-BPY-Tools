import bpy
import os
import sys
import subprocess
import webbrowser


class DH_OP_Open_Proj_Dir(bpy.types.Operator):
    """Open the project root directory in the system file manager."""
    bl_idname = "dh.open_proj_dir"
    bl_label = "Open Project"

    def execute(self, context):

        # get the path of the current blend file
        filepath = bpy.data.filepath

        # get the directory path
        directory = os.path.dirname(filepath)

        # go up two folders
        directory = os.path.abspath(os.path.join(directory, os.pardir, os.pardir))

        # open the directory in the system file manager
        try:
            if sys.platform.startswith("win"):
                subprocess.run(["start", directory], check=True, shell=True)
            elif sys.platform == "darwin":
                subprocess.run(["open", directory], check=True)
            else:
                subprocess.run(["xdg-open", directory], check=True)
        except Exception:
            webbrowser.open(directory)

        return {'FINISHED'}
