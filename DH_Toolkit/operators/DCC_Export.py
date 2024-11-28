import bpy
import os

class DH_OP_dcc_export(bpy.types.Operator):
    """Exports selected objects to an FBX file"""
    bl_idname = "dh.dcc_exporter"
    bl_label = "DCC Exporter"
    bl_options = {'REGISTER', 'UNDO'}

    export_name: bpy.props.StringProperty(
        name="Export Name",
        description="Name of the exported FBX file",
        default="exported"
    )

    def invoke(self, context, event):
        # Show a popup dialog for naming the export file if multiple objects are selected
        if len(context.selected_objects) > 1:
            return context.window_manager.invoke_props_dialog(self)
        return self.execute(context)

    def draw(self, context):
        layout = self.layout
        if len(context.selected_objects) > 1:
            layout.prop(self, "export_name", text="File Name")
    
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
            object_name = active_object.name
        
        # Set the output FBX file path
        fbx_file = os.path.join(fbx_directory, f"{object_name}.fbx")
        
        # Export the selected objects to the FBX file
        bpy.ops.export_scene.fbx(filepath=fbx_file, use_selection=True)
        
        self.report({'INFO'}, f"FBX exported to: {fbx_file}")
        return {'FINISHED'}

