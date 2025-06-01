import bpy
from ..icons.icons import load_icons
from .brush_panel import draw_sculpt_panels

class DH_MT_Sculpt_Menu(bpy.types.Menu):
    """Context-specific pie menu for Sculpt Mode"""
    bl_idname = "DH_MT_Sculpt_Menu"
    bl_label = "DH Sculpt Toolkit"

    def draw(self, context):
        pie = self.layout.menu_pie()

        # LEFT - Brush Selection
        col_left = pie.column()
        brush_box = col_left.box()
        brush_box.label(text='Brushes')

        grid = brush_box.grid_flow(row_major=True, columns=3, even_columns=True)

        brushes = [
            ("Draw", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Draw"),
            ("Draw Sharp", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Draw Sharp"),
            ("Clay", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Clay"),
            ("Clay Strips", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Clay Strips"),
            ("Grab", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Grab"),
            ("Smooth", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Smooth"),
            ("Scrape", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Scrape/Fill"),
            ("Pinch", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Pinch"),
            ("Crease Sharp", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Crease Sharp"),
            ("Mask", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Mask"),
        ]

        for name, identifier in brushes:
            op = grid.operator("brush.asset_activate", text=name)
            op.asset_library_type = 'ESSENTIALS'
            op.asset_library_identifier = ""
            op.relative_asset_identifier = identifier

        # RIGHT - Sculpt Panels and Symmetry
        col_right = pie.column()

        # Sculpt Panels
        sculpt_box = col_right.box()
        draw_sculpt_panels(sculpt_box, context)

        # Symmetry Options
        sym_box = col_right.box()
        sym_box.label(text='Symmetry')
        sculpt = context.tool_settings.sculpt

        row = sym_box.row(align=True)
        row.prop(sculpt, "use_symmetry_x", text="X", toggle=True)
        row.prop(sculpt, "use_symmetry_y", text="Y", toggle=True)
        row.prop(sculpt, "use_symmetry_z", text="Z", toggle=True)

        row = sym_box.row(align=True)
        row.operator("sculpt.symmetrize", text="+X to -X")
        row.operator("sculpt.symmetrize", text="-X to +X")

        # BOTTOM - Mask Tools
        col_bottom = pie.column()
        box = col_bottom.box()
        box.label(text='Mask Tools')

        row = box.row(align=True)
        row.operator('dh.mask_extract', text="Extract Mask")
        row.operator('mesh.paint_mask_slice', text="Mask Slice")

        box.label(text="Mask Brushes:")
        row = box.row(align=True)
        row.operator("wm.tool_set_by_id", text="Box").name = "builtin.box_mask"
        row.operator("wm.tool_set_by_id", text="Lasso").name = "builtin.lasso_mask"
        row.operator("wm.tool_set_by_id", text="Line").name = "builtin.line_mask"

        



        

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


        box.separator()
        box.label(text='Preferences')
        row = box.row(align=True)
        row.operator("screen.userpref_show", text="Open Preferences")

        # TOP - Dyntopo and Multires
        col_top = pie.column()

        # Dyntopo
        dyntopo_box = col_top.box()
        dyntopo_box.label(text='Dynamic Topology')

        if context.sculpt_object:
            dyntopo_enabled = context.sculpt_object.use_dynamic_topology_sculpting

            dyntopo_box.operator("sculpt.dynamic_topology_toggle",
                                 text="Disable Dyntopo" if dyntopo_enabled else "Enable Dyntopo")

            if dyntopo_enabled:
                if hasattr(sculpt, "detail_type_method"):
                    dyntopo_box.prop(sculpt, "detail_type_method", text="")

                    if sculpt.detail_type_method == 'CONSTANT':
                        dyntopo_box.prop(sculpt, "constant_detail_resolution", text="Resolution")
                    elif sculpt.detail_type_method == 'BRUSH':
                        dyntopo_box.prop(sculpt, "detail_percent", text="Detail Percent")
                    elif sculpt.detail_type_method == 'RELATIVE':
                        dyntopo_box.prop(sculpt, "detail_size", text="Detail Size")

                    dyntopo_box.operator("sculpt.detail_flood_fill", text="Detail Flood Fill")
                    dyntopo_box.operator("sculpt.sample_detail_size", text="Sample Detail Size")

        # Multires
        col_top.separator()
        multires_box = col_top.box()
        multires_box.label(text='Multires')
        multires_box.operator('dh.set_multires_viewport_max', text="Set Multires Max")
        multires_box.operator('dh.set_multires_viewport_zero', text="Set Multires Min")

        ob = context.active_object
        if ob and ob.modifiers:
            multires = next((m for m in ob.modifiers if m.type == 'MULTIRES'), None)
            if multires:
                multires_box.operator("object.multires_subdivide", text="Subdivide")
                multires_box.operator("object.multires_higher_levels_delete", text="Delete Higher")

        # Empty corners
        pie.column()  # Top-Left
        pie.column()  # Top-Right
        pie.column()  # Bottom-Left
        pie.column()  # Bottom-Right
