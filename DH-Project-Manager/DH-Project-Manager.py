import bpy
import os
import tempfile

def create_project_directories(context, project_name, directory):
    # Use the provided project name and directory
    project_path = os.path.join(directory, project_name)

    # Create the main project directory
    os.makedirs(project_path, exist_ok=True)

    # Define the subdirectory structure
    subdirectories = [
        os.path.join("01_Ref", "PR"),
        os.path.join("02_Photoshop", "PSD"),
        os.path.join("02_Photoshop", "images"),
        os.path.join("03_Blender", "Scenes"),
        os.path.join("03_Blender", "FBX"),
        os.path.join("03_Blender", "Textures"),
        os.path.join("03_Blender", "Renders"),
        os.path.join("04_Substance", "Scenes"),
        os.path.join("04_Substance", "FBX"),
        os.path.join("04_Substance", "Textures"),
        os.path.join("04_Substance", "SBS"),
        os.path.join("04_Substance", "SBSAR"),
        os.path.join("05_Resolve", "Resources"),
        os.path.join("05_Resolve", "Stills"),
        os.path.join("05_Resolve", "Videos")
    ]

    # Create subdirectories
    for subdir in subdirectories:
        subdir_path = os.path.join(project_path, subdir)
        os.makedirs(subdir_path, exist_ok=True)


# Operator to get project name and directory from the user
class GetProjectDetailsOperator(bpy.types.Operator):
    bl_idname = "object.get_project_details"
    bl_label = "Get Project Details"

    project_name: bpy.props.StringProperty(name="Project Name", default="MyProject")
    directory: bpy.props.StringProperty(name="Directory", subtype='DIR_PATH')
    save_scene: bpy.props.BoolProperty(name="Save Current Scene", default=False)

    def execute(self, context):
        if not self.project_name or not self.directory:
            self.report({'ERROR'}, "Please enter a project name and directory")
            return {'CANCELLED'}

        create_project_directories(context, self.project_name, self.directory)

        if self.save_scene:
            project_path = os.path.join(self.directory, self.project_name)
            scene_dir = os.path.join(project_path, "03_Blender", "Scenes")
            os.makedirs(scene_dir, exist_ok=True)
            filepath = os.path.join(scene_dir, f"{self.project_name}_v001.blend")
            bpy.ops.wm.save_as_mainfile(filepath=filepath)

        bpy.ops.object.project_manager_popup(
            'INVOKE_DEFAULT',
            project_name=self.project_name,
            directory=self.directory
        )
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Popup operator to display the success message
class ProjectManagerPopupOperator(bpy.types.Operator):
    bl_idname = "object.project_manager_popup"
    bl_label = "Project Created"

    project_name: bpy.props.StringProperty()
    directory: bpy.props.StringProperty()

    def execute(self, context):
        return context.window_manager.invoke_popup(self, width=400)

    def draw(self, context):
        layout = self.layout
        layout.label(text=f"Project '{self.project_name}' created in: {self.directory}")

# Register the popup operator
class CreateProjectDirectoriesOperator(bpy.types.Operator):
    bl_idname = "object.create_project_directories"
    bl_label = "Create Project Directories"

    def execute(self, context):
        bpy.ops.object.get_project_details('INVOKE_DEFAULT')
        return {'FINISHED'}

# Registration and unregistration functions
def register():
    bpy.utils.register_class(GetProjectDetailsOperator)
    bpy.utils.register_class(ProjectManagerPopupOperator)
    bpy.utils.register_class(CreateProjectDirectoriesOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(GetProjectDetailsOperator)
    bpy.utils.unregister_class(ProjectManagerPopupOperator)
    bpy.utils.unregister_class(CreateProjectDirectoriesOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

# Add to the 3D Viewport menu
def menu_func(self, context):
    self.layout.operator(CreateProjectDirectoriesOperator.bl_idname)

if __name__ == "__main__":
    register()