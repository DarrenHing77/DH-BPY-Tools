import bpy
import os

class DH_OP_dcc_export(bpy.types.Operator):
    """Exports selected objects to an FBX file with version control"""
    bl_idname = "dh.dcc_exporter"
    bl_label = "DCC Exporter"
    bl_options = {'REGISTER', 'UNDO'}

    export_name: bpy.props.StringProperty(
        name="Export Name",
        description="Name of the exported FBX file",
        default="exported"
    )  # type: ignore

    mesh_option: bpy.props.EnumProperty(
        name="Mesh Option",
        items=[("LOW", "Low", "Save as low-poly"), ("HIGH", "High", "Save as high-poly")],
        default="LOW",
    )

    overwrite: bpy.props.BoolProperty(
        name="Overwrite Existing",
        description="If unchecked, it will create a new versioned folder",
        default=False,
    )

    def invoke(self, context, event):
        # If there is a single selected object, set the default export name to the object's name
        if len(context.selected_objects) == 1:
            active_object = context.view_layer.objects.active
            if active_object:
                self.export_name = active_object.name
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "export_name", text="File Name")
        layout.prop(self, "mesh_option", text="Mesh Option")
        layout.prop(self, "overwrite", text="Overwrite Existing")

    def execute(self, context):
        # Get the path of the current .blend file
        filepath = bpy.data.filepath
        if not filepath:
            self.report({'ERROR'}, "Please save the .blend file before exporting.")
            return {'CANCELLED'}
        
        # Get the directory of the current .blend file
        directory = os.path.dirname(filepath)
        
        # Go up one directory and create an "FBX" folder
        parent_directory = os.path.abspath(os.path.join(directory, os.pardir))
        fbx_directory = os.path.join(parent_directory, "FBX")
        
        # Ensure the FBX folder exists
        os.makedirs(fbx_directory, exist_ok=True)

        # Determine the export file name with the mesh_option suffix
        object_name = f"{self.export_name}_{self.mesh_option.lower()}"

        # Initialize version folder to `v001`
        version_folder = os.path.join(fbx_directory, "v001")
        version_num = 1

        # Check if the file exists in the folder
        file_exists = False
        fbx_file = os.path.join(version_folder, f"{object_name}.fbx")

        if os.path.exists(fbx_file):
            file_exists = True

        # Logic for when to create a new version folder
        if file_exists and not self.overwrite:
            version_num += 1
            version_folder = os.path.join(fbx_directory, f"v{str(version_num).zfill(3)}")
            os.makedirs(version_folder, exist_ok=True)
        else:
            os.makedirs(version_folder, exist_ok=True)

        # Export the selected objects to the FBX file
        bpy.ops.export_scene.fbx(filepath=fbx_file, use_selection=True)
        
        self.report({'INFO'}, f"FBX exported to: {fbx_file}")
        return {'FINISHED'}
