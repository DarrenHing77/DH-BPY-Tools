import bpy

from .mesh_menu import draw_mesh, draw_mask
from .display_menu import draw_display
from .project_menu import draw_project
from ..icons.icons import load_icons
from ..icons import *
from .brush_panel import draw_sculpt_panels
from .modifers_multires_menu import draw_modifiers_multires_menu
from ..operators.open_proj_dir import DH_OP_Open_Proj_Dir
from DH_Project_Manager import DH_OT_CreateProjectDirectories
from ..operators.multires_tools import SetMultiresViewportLevelsZero, SetMultiresViewportLevelsMax



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
        row = col_right.row()  # Create a row to place items side by side
        row.scale_y = 1.5
        
        box_sculpt = row.box()
        draw_sculpt_panels(box_sculpt, context)

        box_display = row.box()
        draw_display(box_display, context)

        

        # Add buttons directly to the pie menu
        col_center = pie.column()
        col_center.alignment = 'CENTER' # Align items in this column to the center
        box = col_center.box()
        draw_project(box, context)

         # Add an empty space to push "Project Manager" to the bottom
        col_center.separator()
        col_center.separator()

        # Add "Project Manager" to the bottom center
        col_center.operator("dh.open_proj_dir", text="Open Project", icon='FILE_FOLDER')
        col_center.operator("dh.create_project_directories", text="Project Manager", icon='FILE_FOLDER')
        col_center.operator("screen.userpref_show", text="Open Preferences")
        
        

        # Top center menu
        col_top_center = pie.column()
        col_top_center.alignment = 'CENTER'
        box = col_top_center.box()
        draw_modifiers_multires_menu(box,context)
        
        

       

        # Add "Open Project" to the middle
        

       
       
        

        
        

        
