import bpy

from .mesh_menu import draw_mesh, draw_mask
from ..icons.icons import load_icons
from .brush_panel import draw_sculpt_panels
from ..operators.open_proj_dir import DH_OP_Open_Proj_Dir


class DH_MT_Main_Menu(bpy.types.Menu):
    bl_idname = "DH_MT_Main_Menu"
    bl_label = "DH Toolkit"

    def draw(self, context):
        pie = self.layout.menu_pie()
        row = pie.row()

        # Create the left column
        col_left = row.column()
        box = col_left.box()
        icons = load_icons()
        draw_mesh(box, context)
        col_left.separator()
        draw_mask(box, context)

        # Create the right column
        col_right = row.column()
        
        box = col_right.box()
        col_right.scale_y = 1.5  # Adjust the size of the column
        row = pie.row()

        # Create the left column
        col_left = row.column()
        box = col_left.box()
        
        draw_sculpt_panels(box, context)
        row = pie.row()
        
        pie.operator("dh.open_proj_dir", text="Open Project",icon='FILE_FOLDER')

        # Create the left column
        #col_left = row.column()
        #box = col_left.box()
        

        
        

        
