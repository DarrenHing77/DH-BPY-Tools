import bpy
from ..icons.icons import load_icons

class DH_MT_Sculpt_Menu(bpy.types.Menu):
    """Context-specific pie menu for Sculpt Mode"""
    bl_idname = "DH_MT_Sculpt_Menu"
    bl_label = "DH Sculpt Toolkit"

    def draw(self, context):
        pie = self.layout.menu_pie()
        
        # LEFT - Brush Settings
        col_left = pie.column()
        box = col_left.box()
        box.label(text='Brush Settings')
        
        # Use direct access to brush settings
        if context.tool_settings and context.tool_settings.sculpt:
            brush = context.tool_settings.sculpt.brush
            if brush:
                # Show brush strength and size directly
                box.prop(brush, "strength", text="Strength")
                box.prop(brush, "size", text="Size")
                
                # Add Front Faces Only option
                if hasattr(brush, "use_frontface"):
                    box.prop(brush, "use_frontface", text="Front Faces Only")
                
                # Add Automasking options
                if hasattr(brush, "use_automasking_topology"):
                    box.prop(brush, "use_automasking_topology", text="Topology Automasking")
                
                # Add Stabilize Stroke options
                box.separator()
                box.label(text="Stroke:")
                
                # Stabilize
                if hasattr(brush, "use_smooth_stroke"):
                    row = box.row()
                    row.prop(brush, "use_smooth_stroke", text="Stabilize Stroke")
                    
                    # Show radius and factor if stabilize is enabled
                    if brush.use_smooth_stroke:
                        col = box.column(align=True)
                        col.prop(brush, "smooth_stroke_radius", text="Radius", slider=True)
                        col.prop(brush, "smooth_stroke_factor", text="Factor", slider=True)
                    
                # Add falloff curve if available
                box.separator()
                if hasattr(brush, "curve"):
                    box.label(text="Falloff Curve")
                    box.template_curve_mapping(brush, "curve", brush=True)
        
        # RIGHT - Brush Selection and Symmetry in the same column
        col_right = pie.column()
        
        # Brush selection box
        brush_box = col_right.box()
        brush_box.label(text='Brushes')
        
        # Create a grid for essential brushes
        grid = brush_box.grid_flow(row_major=True, columns=3, even_columns=True)
        
        # Use context_set_enum operator to set the sculpt tool
        # This is a more reliable approach in Blender 4.4
        brushes = [
            ("Draw", "DRAW"),
            ("Clay", "CLAY"),
            ("Clay Strips", "CLAY_STRIPS"),
            ("Grab", "GRAB"),
            ("Smooth", "SMOOTH"),
            ("Flatten", "FLATTEN"),
            ("Pinch", "PINCH"),
            ("Crease", "CREASE"),
            ("Mask", "MASK")
        ]
        
        for name, tool in brushes:
            op = grid.operator("wm.context_set_enum", text=name)
            op.data_path = "tool_settings.sculpt.sculpt_tool"
            op.value = tool
        
        # Add a separator between brushes and symmetry
        col_right.separator()
        
        # Symmetry box
        sym_box = col_right.box()
        sym_box.label(text='Symmetry')
        
        # Symmetry toggles
        sculpt = context.tool_settings.sculpt
        row = sym_box.row(align=True)
        row.prop(sculpt, "use_symmetry_x", text="X", toggle=True)
        row.prop(sculpt, "use_symmetry_y", text="Y", toggle=True)
        row.prop(sculpt, "use_symmetry_z", text="Z", toggle=True)
        
        # Symmetrize operation
        row = sym_box.row(align=True)
        row.operator("sculpt.symmetrize", text="+X to -X")
        row.operator("sculpt.symmetrize", text="-X to +X")
        
        # BOTTOM - Mask Tools with Box, Lasso, and Polyline
        col_bottom = pie.column()
        box = col_bottom.box()
        box.label(text='Mask Tools')
        
        # Mask extraction tools
        row = box.row(align=True)
        row.operator('dh.mask_extract', text="Extract Mask")
        row.operator('mesh.paint_mask_slice', text="Mask Slice")
        
        # Masking brushes
        box.label(text="Mask Brushes:")
        row = box.row(align=True)
        row.operator("paint.mask_box_gesture", text="Box").mode = 'VALUE'
        row.operator("paint.mask_lasso_gesture", text="Lasso").mode = 'VALUE'
        
        # Try to use polyline if it exists
        if hasattr(bpy.ops.paint, "mask_line_gesture"):
            row.operator("paint.mask_line_gesture", text="Line").mode = 'VALUE'
        
        # Mask flood fill operations
        box.separator()
        box.label(text="Mask Operations:")
        row = box.row(align=True)
        op = row.operator("paint.mask_flood_fill", text="Fill")
        op.mode = 'VALUE'
        op.value = 1.0
        
        op = row.operator("paint.mask_flood_fill", text="Clear")
        op.mode = 'VALUE'
        op.value = 0.0
        
        op = row.operator("paint.mask_flood_fill", text="Invert")
        op.mode = 'INVERT'
        
        # TOP - Dyntopo and Multires in the same column
        col_top = pie.column()
        
        # Dyntopo box
        dyntopo_box = col_top.box()
        dyntopo_box.label(text='Dynamic Topology')
        
        # Dyntopo toggle
        if context.sculpt_object:
            dyntopo_enabled = context.sculpt_object.use_dynamic_topology_sculpting
            
            if dyntopo_enabled:
                dyntopo_box.operator("sculpt.dynamic_topology_toggle", text="Disable Dyntopo")
            else:
                dyntopo_box.operator("sculpt.dynamic_topology_toggle", text="Enable Dyntopo")
            
            # Add detail settings if dyntopo is enabled
            if dyntopo_enabled:
                # Check if the sculpt context has these properties
                sculpt = context.tool_settings.sculpt
                if hasattr(sculpt, "detail_type_method"):
                    dyntopo_box.prop(sculpt, "detail_type_method", text="")
                    
                    # Add detail size based on method
                    if hasattr(sculpt, "constant_detail_resolution") and sculpt.detail_type_method == 'CONSTANT':
                        dyntopo_box.prop(sculpt, "constant_detail_resolution", text="Resolution")
                    elif hasattr(sculpt, "detail_percent") and sculpt.detail_type_method == 'BRUSH':
                        dyntopo_box.prop(sculpt, "detail_percent", text="Detail Percent")
                    elif hasattr(sculpt, "detail_size") and sculpt.detail_type_method == 'RELATIVE':
                        dyntopo_box.prop(sculpt, "detail_size", text="Detail Size")
                
                # Add detail operations
                dyntopo_box.operator("sculpt.detail_flood_fill", text="Detail Flood Fill")
                dyntopo_box.operator("sculpt.sample_detail_size", text="Sample Detail Size")
        
        # Add a separator between dyntopo and multires
        col_top.separator()
        
        # Multires box
        multires_box = col_top.box()
        multires_box.label(text='Multires')
        multires_box.operator('dh.set_multires_viewport_max', text="Set Multires Max")
        multires_box.operator('dh.set_multires_viewport_zero', text="Set Multires Min")
        
        # Add basic multires operations if there's a multires modifier
        ob = context.active_object
        if ob and ob.modifiers:
            multires = next((m for m in ob.modifiers if m.type == 'MULTIRES'), None)
            if multires:
                multires_box.operator("object.multires_subdivide", text="Subdivide")
                multires_box.operator("object.multires_higher_levels_delete", text="Delete Higher")
        
        # Leave all corner sections empty
        # TOP-LEFT - empty
        col_tl = pie.column()
        # Empty
        
        # TOP-RIGHT - empty
        col_tr = pie.column()
        # Empty
        
        # BOTTOM-LEFT - empty
        col_bl = pie.column()
        # Empty
        
        # BOTTOM-RIGHT - empty
        col_br = pie.column()
        # Empty