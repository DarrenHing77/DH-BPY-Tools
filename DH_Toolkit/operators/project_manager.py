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
        "01_Ref",
        os.path.join("01_Ref", "PR"),
        "02_Photoshop",
        os.path.join("02_Photoshop", "PSD"),
        os.path.join("02_Photoshop", "images"),
        "03_Blender",
        os.path.join("03_Blender", "Scenes"),
        os.path.join("03_Blender", "FBX"),
        os.path.join("03_Blender", "Textures"),
        os.path.join("03_Blender", "Renders"),
        "04_Substance",
        os.path.join("04_Substance", "Scenes"),
        os.path.join("04_Substance", "FBX"),
        os.path.join("04_Substance", "Textures"),
        os.path.join("04_Substance", "Textures", "01_Painter"),
        os.path.join("04_Substance", "Textures", "02_Designer"),
        os.path.join("04_Substance", "SBS"),
        os.path.join("04_Substance", "SBSAR"),
        "05_Resolve",
        os.path.join("05_Resolve", "Resources"),
        os.path.join("05_Resolve", "Stills"),
        os.path.join("05_Resolve", "Videos"),
        "06_Daz"
    ]

    # Create subdirectories
    for subdir in subdirectories:
        subdir_path = os.path.join(project_path, subdir)
        os.makedirs(subdir_path, exist_ok=True)


# Operator to get project name and directory from the user
class DH_OP_Proj_Manage(bpy.types.Operator):
    bl_idname = "dh.project_manage"
    bl_label = "Project Manager"

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

        bpy.ops.dh.project_manager_popup(
            'INVOKE_DEFAULT',
            project_name=self.project_name,
            directory=self.directory
        )
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Popup operator to display the success message
class DH_OP_Project_Manager_Popup(bpy.types.Operator):
    bl_idname = "dh.project_manager_popup"
    bl_label = "Project Created"

    project_name: bpy.props.StringProperty()
    directory: bpy.props.StringProperty()

    def execute(self, context):
        return context.window_manager.invoke_popup(self, width=400)

    def draw(self, context):
        layout = self.layout
        layout.label(text=f"Project '{self.project_name}' created in: {self.directory}")

# Register the popup operator
class DH_OP_CreateProjectDirectories(bpy.types.Operator):
    bl_idname = "dh.create_project_directories"
    bl_label = "Create Project Directories"

    def execute(self, context):
        bpy.ops.dh.project_manage('INVOKE_DEFAULT')
        return {'FINISHED'}



