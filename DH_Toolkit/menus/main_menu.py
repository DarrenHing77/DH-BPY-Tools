import bpy

from .mesh_menu import draw_mesh, draw_mask
from ..icons.icons import load_icons
from .brush_panel import draw_sculpt_panels
from ..operators.open_proj_dir import DH_OP_Open_Proj_Dir
from ..operators.project_manager import DH_OP_Proj_Manage, DH_OP_Project_Manager_Popup, DH_OP_CreateProjectDirectories


class DH_MT_Main_Menu(bpy.types.Menu):
    bl_idname = "DH_MT_Main_Menu"
    bl_label = "DH Toolkit"

    def draw(self, context):
        pie = self.layout.menu_pie()
        
        # Left column
        col_left = pie.column()
        box = col_left.box()
        icons = load_icons()
        draw_mesh(box, context)
        col_left.separator()
        draw_mask(box, context)

        # Right column
        col_right = pie.column()
        box = col_right.box()
        col_right.scale_y = 1.5  
        draw_sculpt_panels(box, context)
        
        
        pie.operator("dh.open_proj_dir", text="Open Project", icon='FILE_FOLDER')

        # Add buttons directly to the pie menu
        col_center = pie.column()
        col_center.alignment = 'CENTER' # Align items in this column to the center

        # Add "Open Project" to the middle
        

        # Add an empty space to push "Project Manager" to the bottom
        col_center.separator()
        col_center.separator()

        # Add "Project Manager" to the bottom center
        col_center.operator("dh.create_project_directories", text="Project Manager", icon='FILE_FOLDER')
       
        

        
        

        
