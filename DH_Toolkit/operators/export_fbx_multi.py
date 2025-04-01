import bpy
import os
import re
from bpy.props import EnumProperty, BoolProperty, FloatProperty, StringProperty

class DH_OP_dcc_split_export(bpy.types.Operator):
    """Exports each selected object as its own FBX file with versioning, quality options, and additional export settings"""
    bl_idname = "dh.dcc_split_exporter"
    bl_label = "DCC Split Exporter"
    bl_options = {'REGISTER', 'UNDO'}

    # Quality selection: "low" or "high"
    quality: EnumProperty(
        name="Quality",
        description="Choose the export quality",
        items=[
            ('LOW', "Low", "Export as low quality"),
            ('HIGH', "High", "Export as high quality")
        ],
        default='LOW'
    )

    # Checkbox for replacing the latest version
    replace_latest: BoolProperty(
        name="Replace Latest Version",
        description="Replace the latest version instead of creating a new one",
        default=False
    )
    
    # Additional export settings
    scale: FloatProperty(
        name="Scale",
        description="Scale factor for the export",
        default=1.0,
        min=0.01,
        max=1000.0
    )
    
    export_animations: BoolProperty(
        name="Export Animations",
        description="Include animations in the export",
        default=False
    )
    
    custom_suffix: StringProperty(
        name="Custom Suffix",
        description="Add a custom suffix to the filename (in addition to quality)",
        default=""
    )
    
    # Progress properties
    _total_objects = 0
    _current_object = 0

    def invoke(self, context, event):
        # Show the popup menu for export options
        return context.window_manager.invoke_props_dialog(self, width=350)

    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text="Version Control:")
        box.prop(self, "replace_latest")
        
        box = layout.box()
        box.label(text="Export Options:")
        box.prop(self, "quality")
        box.prop(self, "scale")
        box.prop(self, "export_animations")
        box.prop(self, "custom_suffix")

    def get_version_folder(self, split_fbx_directory):
        """Helper method to determine the version folder"""
        try:
            # Get all version folders
            if not os.path.exists(split_fbx_directory):
                os.makedirs(split_fbx_directory)
                return "v001"
                
            version_folders = [d for d in os.listdir(split_fbx_directory) 
                              if os.path.isdir(os.path.join(split_fbx_directory, d)) and 
                              re.match(r'v\d{3}', d)]
            
            if not version_folders:
                return "v001"
                
            if self.replace_latest:
                latest_version = max(version_folders, key=lambda v: int(v[1:]))
                return latest_version
            else:
                latest_version_number = max((int(d[1:]) for d in version_folders), default=0)
                new_version_number = latest_version_number + 1
                return f"v{new_version_number:03}"
        except Exception as e:
            self.report({'ERROR'}, f"Error determining version folder: {str(e)}")
            return "v001"  # Fallback to v001 in case of any issue

    def get_export_directory(self):
        """Helper method to get the export directory path"""
        try:
            # Get the path of the current .blend file
            filepath = bpy.data.filepath
            if not filepath:
                self.report({'ERROR'}, "Please save the .blend file before exporting.")
                return None
            
            # Get the directory of the current .blend file
            directory = os.path.dirname(filepath)
            
            # Go up one directory and create the "FBX_split" folder
            parent_directory = os.path.abspath(os.path.join(directory, os.pardir))
            split_fbx_directory = os.path.join(parent_directory, "FBX_split")
            
            # Check if we have write permissions
            if not os.access(parent_directory, os.W_OK):
                self.report({'ERROR'}, f"No write permission for directory: {parent_directory}")
                return None
                
            os.makedirs(split_fbx_directory, exist_ok=True)
            
            # Get the version folder
            version_folder = self.get_version_folder(split_fbx_directory)
            version_path = os.path.join(split_fbx_directory, version_folder)
            os.makedirs(version_path, exist_ok=True)
            
            return version_path
        except Exception as e:
            self.report({'ERROR'}, f"Failed to create export directory: {str(e)}")
            return None

    def export_object(self, obj, export_path):
        """Export a single object to FBX"""
        try:
            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')
            
            # Select the current object
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            
            # Determine file name with quality suffix
            quality_suffix = "_low" if self.quality == 'LOW' else "_high"
            custom_suffix = f"_{self.custom_suffix}" if self.custom_suffix else ""
            fbx_file = os.path.join(export_path, f"{obj.name}{quality_suffix}{custom_suffix}.fbx")
            
            # Export the current object to the FBX file with the specified settings
            bpy.ops.export_scene.fbx(
                filepath=fbx_file,
                use_selection=True,
                global_scale=self.scale,
                bake_anim=self.export_animations
            )
            
            return True
        except Exception as e:
            self.report({'ERROR'}, f"Failed to export {obj.name}: {str(e)}")
            return False

    def execute(self, context):
        # Get export directory
        export_path = self.get_export_directory()
        if not export_path:
            return {'CANCELLED'}
        
        # Get selected objects
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'ERROR'}, "No objects selected for export.")
            return {'CANCELLED'}
        
        # Initialize progress tracking
        self._total_objects = len(selected_objects)
        self._current_object = 0
        
        # Export each object
        successful_exports = 0
        failed_exports = 0
        
        for obj in selected_objects:
            self._current_object += 1
            
            # Update progress in status bar
            context.window_manager.progress_update(self._current_object / self._total_objects)
            context.window_manager.status_text_set(f"Exporting: {obj.name} ({self._current_object}/{self._total_objects})")
            
            # Export the object
            if self.export_object(obj, export_path):
                successful_exports += 1
            else:
                failed_exports += 1
        
        # Clear progress
        context.window_manager.progress_end()
        context.window_manager.status_text_set("")
        
        # Report results
        if failed_exports > 0:
            self.report({'WARNING'}, 
                       f"Exported {successful_exports} objects, {failed_exports} failed. Location: {export_path}")
        else:
            self.report({'INFO'}, 
                       f"Successfully exported {successful_exports} objects to: {export_path}")
        
        return {'FINISHED'}