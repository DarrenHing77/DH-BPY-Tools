import bpy
import os
import re

class DH_OP_dcc_split_export(bpy.types.Operator):
    """Exports each selected object as its own FBX file with versioning and quality options"""
    bl_idname = "dh.dcc_split_exporter"
    bl_label = "DCC Split Exporter"
    bl_options = {'REGISTER', 'UNDO'}

    # Quality selection: "low" or "high"
    quality: bpy.props.EnumProperty(
        name="Quality",
        description="Choose the export quality",
        items=[
            ('LOW', "Low", "Export as low quality"),
            ('HIGH', "High", "Export as high quality")
        ],
        default='LOW'
    ) # type: ignore

    # Checkbox for replacing the latest version
    replace_latest: bpy.props.BoolProperty(
        name="Replace Latest Version",
        description="Replace the latest version instead of creating a new one",
        default=False
    )  # type: ignore # <-- Correctly closed the parentheses here


    def invoke(self, context, event):
        # Show the popup menu for quality selection and replace option
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "quality", text="Export Quality")
        layout.prop(self, "replace_latest", text="Replace Latest Version")

    def execute(self, context):
        # Get the path of the current .blend file
        filepath = bpy.data.filepath
        if not filepath:
            self.report({'ERROR'}, "Please save the .blend file before exporting.")
            return {'CANCELLED'}
        
        # Get the directory of the current .blend file
        directory = os.path.dirname(filepath)
        
        # Go up one directory and create the "FBX_split" folder
        parent_directory = os.path.abspath(os.path.join(directory, os.pardir))
        split_fbx_directory = os.path.join(parent_directory, "FBX_split")
        os.makedirs(split_fbx_directory, exist_ok=True)

        # Determine version folder
        if self.replace_latest:
            # Find the latest version folder
            version_folders = [d for d in os.listdir(split_fbx_directory) if re.match(r'v\d{3}', d)]
            latest_version = max(version_folders, default='v000', key=lambda v: int(v[1:]))
            version_folder = latest_version
        else:
            # Create a new version folder
            version_folders = [d for d in os.listdir(split_fbx_directory) if re.match(r'v\d{3}', d)]
            latest_version_number = max((int(d[1:]) for d in version_folders), default=0)
            new_version_number = latest_version_number + 1
            version_folder = f"v{new_version_number:03}"
        
        # Full path to the version folder
        version_path = os.path.join(split_fbx_directory, version_folder)
        os.makedirs(version_path, exist_ok=True)

        # Loop through selected objects
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'ERROR'}, "No objects selected for export.")
            return {'CANCELLED'}
        
        for obj in selected_objects:
            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')
            
            # Select the current object
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            # Determine file name with quality suffix
            suffix = "_low" if self.quality == 'LOW' else "_high"
            fbx_file = os.path.join(version_path, f"{obj.name}{suffix}.fbx")
            
            # Export the current object to the FBX file
            bpy.ops.export_scene.fbx(filepath=fbx_file, use_selection=True)
        
        self.report({'INFO'}, f"Exported {len(selected_objects)} objects to: {version_path}")
        return {'FINISHED'}

