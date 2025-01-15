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
    ) # type: ignore

    overwrite: bpy.props.BoolProperty(
        name="Overwrite Existing",
        description="If unchecked, it will create a new versioned folder",
        default=False,
    ) # type: ignore

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

        # Determine the export file name
        if len(context.selected_objects) > 1:
            # Use the name entered in the popup dialog for multiple selection
            object_name = self.export_name
        else:
            # Use the name of the active object for a single selection
            active_object = context.view_layer.objects.active
            if not active_object:
                self.report({'ERROR'}, "No active object selected for export.")
                return {'CANCELLED'}
            
            # Append the mesh option suffix (_low or _high)
            object_name = active_object.name + f"_{self.mesh_option.lower()}"

        # Check if we should overwrite or create a new versioned folder
        version_folder = os.path.join(fbx_directory, "v002")
        if not self.overwrite:
            # Check for existing version folders and create a new one if needed
            version_num = 2
            while os.path.exists(version_folder):
                version_num += 1
                version_folder = os.path.join(fbx_directory, f"v{str(version_num).zfill(3)}")
            
            # Create the new version folder
            os.makedirs(version_folder, exist_ok=True)
        else:
            # Ensure the folder exists
            os.makedirs(fbx_directory, exist_ok=True)

        # Set the output FBX file path
        fbx_file = os.path.join(version_folder, f"{object_name}.fbx")
        
        # Export the selected objects to the FBX file
        bpy.ops.export_scene.fbx(filepath=fbx_file, use_selection=True)
        
        self.report({'INFO'}, f"FBX exported to: {fbx_file}")
        return {'FINISHED'}

