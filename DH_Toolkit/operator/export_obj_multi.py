import bpy
import os
from bpy.app.handlers import persistent


class DH_OP_export_obj_multi(bpy.types.Operator):

    bl_idname = "dh.export_obj_multi"
    bl_label = "Export_OBJ_Multi"
    bl_options = {'REGISTER', 'UNDO'}

    # Get the path of the current blend file
    filepath = bpy.data.filepath

    # Get the directory path
    directory = os.path.dirname(filepath)

    # Go up a folder
    export_directory = os.path.abspath(os.path.join(directory, os.pardir))

    # Create the export directory if it doesn't exist
    export_directory = os.path.join(export_directory, "obj")
    os.makedirs(export_directory, exist_ok=True)

    # Get the currently selected objects
    selected_objects = bpy.context.selected_objects

    # Iterate through selected objects and export them individually
    for obj in selected_objects:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        # Get the object name
        obj_name = obj.name

        # Check if "_v001" is already in the name
        if "_v001" not in obj_name:
            obj_name += "_v001"

        # Set shading to smooth
        bpy.ops.object.shade_smooth()

        # Set the export path and filename
        export_filename = os.path.join(export_directory, f"{obj_name}.obj")

        # Export the object as an OBJ file
        bpy.ops.export_scene.obj(
            filepath=export_filename,
            use_selection=True,
            use_materials=True,
            use_normals=True,
        )

        obj.select_set(False)

    # Deselect all objects after exporting
    bpy.ops.object.select_all(action='DESELECT')
