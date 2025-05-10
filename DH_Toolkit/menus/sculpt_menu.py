import bpy
from ..icons.icons import load_icons
from .brush_panel import draw_sculpt_panels

def draw_common_brushes(layout, context):
    layout.label(text='Common Brushes')
    
    # Create a grid for compact brush layout
    grid = layout.grid_flow(row_major=True, columns=2, even_columns=True)
    
    # Clay brushes
    grid.operator("sculpt.brush_select", text="Clay").sculpt_tool = 'CLAY'
    grid.operator("sculpt.brush_select", text="Clay Strips").sculpt_tool = 'CLAY_STRIPS'
    grid.operator("sculpt.brush_select", text="Clay Thumb").sculpt_tool = 'CLAY_THUMB'
    
    # Draw brushes
    grid.operator("sculpt.brush_select", text="Draw").sculpt_tool = 'DRAW'
    grid.operator("sculpt.brush_select", text="Draw Sharp").sculpt_tool = 'DRAW_SHARP'
    
    # Scrape and flatten
    grid.operator("sculpt.brush_select", text="Scrape").sculpt_tool = 'SCRAPE'
    grid.operator("sculpt.brush_select", text="Flatten").sculpt_tool = 'FLATTEN'
    
    # Mask brushes
    layout.separator()
    layout.label(text='Mask Brushes')
    grid = layout.grid_flow(row_major=True, columns=2, even_columns=True)
    grid.operator("sculpt.brush_select", text="Mask").sculpt_tool = 'MASK'
    grid.operator("sculpt.brush_select", text="Draw Face Sets").sculpt_tool = 'DRAW_FACE_SETS'
    
    # Trim brushes
    layout.separator()
    layout.label(text='Trim Brushes')
    grid = layout.grid_flow(row_major=True, columns=2, even_columns=True)
    grid.operator("sculpt.brush_select", text="Trim").sculpt_tool = 'TRIM'
    grid.operator("sculpt.brush_select", text="Fill").sculpt_tool = 'FILL'
    
    # Shape modification
    layout.separator()
    layout.label(text='Deformation')
    grid = layout.grid_flow(row_major=True, columns=2, even_columns=True)
    grid.operator("sculpt.brush_select", text="Grab").sculpt_tool = 'GRAB'
    grid.operator("sculpt.brush_select", text="Pinch").sculpt_tool = 'PINCH'
    grid.operator("sculpt.brush_select", text="Smooth").sculpt_tool = 'SMOOTH'

def draw_mask_tools(layout, context):
    layout.label(text='Mask Tools')
    layout.operator('dh.mask_extract', text="Extract Mask")
    layout.operator('mesh.paint_mask_slice', text="Mask Slice")
    
    # Add mask utilities
    row = layout.row(align=True)
    row.operator("sculpt.mask_flood_fill", text="Fill").mode = 'VALUE'
    row.operator("sculpt.mask_flood_fill", text="Clear").mode = 'VALUE'
    
    row = layout.row(align=True)
    row.operator("sculpt.mask_flood_fill", text="Invert").mode = 'INVERT'
    row.operator("paint.mask_lasso_gesture", text="Lasso").mode = 'VALUE'

def draw_dyntopo_tools(layout, context):
    layout.label(text='Dynamic Topology')
    
    # Check if dyntopo is enabled
    if context.sculpt_object:
        dyntopo_enabled = context.sculpt_object.use_dynamic_topology_sculpting
        
        # Enable/disable button
        if dyntopo_enabled:
            layout.operator("sculpt.dynamic_topology_toggle", text="Disable Dyntopo")
        else:
            layout.operator("sculpt.dynamic_topology_toggle", text="Enable Dyntopo")
        
        # Dyntopo settings if enabled
        if dyntopo_enabled:
            sculpt = context.tool_settings.sculpt
            layout.prop(sculpt, "detail_type_method", text="")
            
            if sculpt.detail_type_method == 'CONSTANT':
                layout.prop(sculpt, "constant_detail_resolution")
            elif sculpt.detail_type_method == 'BRUSH':
                layout.prop(sculpt, "detail_percent")
            elif sculpt.detail_type_method == 'RELATIVE':
                layout.prop(sculpt, "detail_size")
                
            # Detail tools
            layout.separator()
            row = layout.row(align=True)
            row.operator("sculpt.detail_flood_fill", text="Detail Flood Fill")
            row.operator("sculpt.sample_detail_size", text="Sample Detail")

def draw_multires_tools(layout, context):
    layout.label(text='Multires')
    
    # Add level controls
    row = layout.row(align=True)
    row.operator('dh.set_multires_viewport_max', text="Set Max")
    row.operator('dh.set_multires_viewport_zero', text="Set Min")
    
    # Add basic multires operations
    ob = context.active_object
    if ob and ob.modifiers:
        multires = next((m for m in ob.modifiers if m.type == 'MULTIRES'), None)
        if multires:
            # Show current level
            layout.separator()
            if hasattr(multires, "levels"):
                layout.label(text=f"Current Level: {multires.levels}/{multires.total_levels}")
                
            # Add level operations
            row = layout.row(align=True)
            row.operator("object.multires_subdivide", text="Subdivide")
            row.operator("object.multires_higher_levels_delete", text="Del Higher")
            
            # Apply button
            layout.operator("object.multires_apply_base", text="Apply Base")

def draw_symmetry_tools(layout, context):
    layout.label(text='Symmetry')
    
    # Access sculpt tool settings
    sculpt = context.tool_settings.sculpt
    
    # Symmetry toggles
    row = layout.row(align=True)
    row.prop(sculpt, "use_symmetry_x", text="X", toggle=True)
    row.prop(sculpt, "use_symmetry_y", text="Y", toggle=True)
    row.prop(sculpt, "use_symmetry_z", text="Z", toggle=True)
    
    # Symmetrize options
    layout.separator()
    row = layout.row(align=True)
    row.operator("sculpt.symmetrize", text="+X to -X").direction = 'POSITIVE_X'
    row.operator("sculpt.symmetrize", text="-X to +X").direction = 'NEGATIVE_X'
    
    # Lock options if available
    if hasattr(sculpt, "lock_x") or hasattr(sculpt, "lock_y") or hasattr(sculpt, "lock_z"):
        layout.separator()
        layout.label(text="Lock:")
        row = layout.row(align=True)
        if hasattr(sculpt, "lock_x"):
            row.prop(sculpt, "lock_x", text="X", toggle=True)
        if hasattr(sculpt, "lock_y"):
            row.prop(sculpt, "lock_y", text="Y", toggle=True)
        if hasattr(sculpt, "lock_z"):
            row.prop(sculpt, "lock_z", text="Z", toggle=True)

def draw_remesh_tools(layout, context):
    layout.label(text='Remesh')
    layout.operator('dh.decimate', text="Decimate")
    
    # Add remesh options
    ob = context.active_object
    if ob and ob.type == 'MESH':
        layout.operator("object.voxel_remesh", text="Voxel Remesh")
        layout.operator("object.quadriflow_remesh", text="Quad Remesh")
        
        # Voxel size if available
        if hasattr(context.scene, "remesh_voxel_size"):
            layout.prop(context.scene, "remesh_voxel_size", text="Voxel Size")
            
        # Smooth iterations
        layout.operator("sculpt.sample_detail_size", text="Sample Detail")


class DH_MT_Sculpt_Menu(bpy.types.Menu):
    bl_idname = "DH_MT_Sculpt_Menu"
    bl_label = "DH Sculpt Toolkit"

    def draw(self, context):
        pie = self.layout.menu_pie()
        
        # LEFT - Brush Panels (from your existing code)
        col_left = pie.column()
        box = col_left.box()
        box.label(text='Brush Panels')
        # Use your existing draw_sculpt_panels function
        draw_sculpt_panels(box, context)
        
        # RIGHT - Common Brushes
        col_right = pie.column()
        box = col_right.box()
        draw_common_brushes(box, context)
        
        # BOTTOM - Mask and Remesh Tools
        col_bottom = pie.column()
        
        # Mask Tools on top
        box1 = col_bottom.box()
        draw_mask_tools(box1, context)
        
        col_bottom.separator()
        
        # Remesh Tools below
        box2 = col_bottom.box()
        draw_remesh_tools(box2, context)
        
        # TOP - Dyntopo Tools
        col_top = pie.column()
        box = col_top.box()
        draw_dyntopo_tools(box, context)
        
        # BOTTOM-LEFT - Multires Tools
        col_bl = pie.column()
        box = col_bl.box()
        draw_multires_tools(box, context)
        
        # BOTTOM-RIGHT - Symmetry Tools
        col_br = pie.column()
        box = col_br.box()
        draw_symmetry_tools(box, context)
        
        # TOP-LEFT - empty to ensure good spacing
        col_tl = pie.column()
        # Intentionally empty
        
        # TOP-RIGHT - empty to ensure good spacing
        col_tr = pie.column()
        # Intentionally empty