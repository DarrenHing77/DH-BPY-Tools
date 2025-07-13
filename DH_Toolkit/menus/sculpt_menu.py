import bpy
from ..icons.icons import load_icons
from .brush_panel import draw_sculpt_panels

class DH_MT_Sculpt_Menu(bpy.types.Menu):
    """Context-specific pie menu for Sculpt Mode"""
    bl_idname = "DH_MT_Sculpt_Menu"
    bl_label = "DH Sculpt Toolkit"

    def draw(self, context):
        icons = load_icons()
        pie = self.layout.menu_pie()

        # LEFT - Brush Tools
        col_left = pie.column()

        # Face Sets Tools
        face_box = col_left.box()
        face_box.label(text='Face Sets')

        row = face_box.row(align=True)
        row.operator('sculpt.face_sets_create', text='From Masked').mode = 'MASKED'
        row.operator('sculpt.face_sets_create', text='From Visible').mode = 'VISIBLE'

        row = face_box.row(align=True)
        row.operator('sculpt.face_sets_create', text='From Edit Selection').mode = 'SELECTION'
        row.operator('sculpt.face_sets_init', text='Init Loose Parts').mode = 'LOOSE_PARTS'

        # Brushes
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
            ("Crease", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Crease"),
            ("Mask", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Mask"),
        ]
        
        for name, identifier in brushes:
            op = grid.operator("brush.asset_activate", text=name)
            op.asset_library_type = 'ESSENTIALS'
            op.asset_library_identifier = ""
            op.relative_asset_identifier = identifier

        # RIGHT - Brush Panel and Symmetry
        col_right = pie.column()

        draw_sculpt_panels(col_right, context)

        sym_box = col_right.box()
        sym_box.label(text='Symmetry')
        sculpt = context.tool_settings.sculpt

        row = sym_box.row(align=True)
        row.prop(context.object, "use_mesh_mirror_x", text="X", toggle=True)
        row.prop(context.object, "use_mesh_mirror_y", text="Y", toggle=True)
        row.prop(context.object, "use_mesh_mirror_z", text="Z", toggle=True)

        row = sym_box.row(align=True)
        row.operator("sculpt.symmetrize", text="+X to -X")
        row.operator("sculpt.symmetrize", text="-X to +X")

        # BOTTOM - Masking Tools
        col_bottom = pie.column()
        box = col_bottom.box()

        box.label(text="Mask Brushes:")
        row = box.row(align=True)
        row.scale_y = 1.3
        row.operator("wm.tool_set_by_id", text="Box").name = "builtin.box_mask"
        row.operator("wm.tool_set_by_id", text="Lasso").name = "builtin.lasso_mask"
        row.operator("wm.tool_set_by_id", text="Line").name = "builtin.line_mask"

        box.label(text="Transform:")
        row = box.row(align=True)
        row.scale_y = 1.3
        row.operator("wm.tool_set_by_id", text="Move").name = "builtin.move"
        row.operator("wm.tool_set_by_id", text="Rotate").name = "builtin.rotate"
        row.operator("wm.tool_set_by_id", text="Scale").name = "builtin.scale"

        box.label(text='Mask Tools')
        row = box.row(align=True)
        row.scale_y = 1.3
        row.operator('dh.mask_extract', text="Extract Mask")
        row.operator('mesh.paint_mask_slice', text="Mask Slice")

        
        pivot_box = col_bottom.box() 
        pivot_box.label(text='Transform Pivot')

        row = pivot_box.row(align=True)
        row.prop(context.scene.tool_settings, "transform_pivot_point", text="")


        row = pivot_box.row(align=True)
        row.prop(context.scene.transform_orientation_slots[1], "type", text="Orientation")
        
        

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

        # TOP - Multires, Dyntopo, and Modifiers
        col_top = pie.column()

        # Dyntopo
        dyntopo_box = col_top.box()
        dyntopo_box.label(text='Dynamic Topology')

        if context.sculpt_object:
            dyntopo_enabled = context.sculpt_object.use_dynamic_topology_sculpting

            dyntopo_box.operator("sculpt.dynamic_topology_toggle",
                                 text="Disable Dyntopo" if dyntopo_enabled else "Enable Dyntopo")

            if dyntopo_enabled:
                if hasattr(context.tool_settings.sculpt, "detail_type_method"):
                    dyntopo_box.prop(context.tool_settings.sculpt, "detail_type_method", text="")

                    if context.tool_settings.sculpt.detail_type_method == 'CONSTANT':
                        dyntopo_box.prop(context.tool_settings.sculpt, "constant_detail_resolution", text="Resolution")
                    elif context.tool_settings.sculpt.detail_type_method == 'BRUSH':
                        dyntopo_box.prop(context.tool_settings.sculpt, "detail_percent", text="Detail Percent")
                    elif context.tool_settings.sculpt.detail_type_method == 'RELATIVE':
                        dyntopo_box.prop(context.tool_settings.sculpt, "detail_size", text="Detail Size")

                    dyntopo_box.operator("sculpt.detail_flood_fill", text="Detail Flood Fill")
                    dyntopo_box.operator("sculpt.sample_detail_size", text="Sample Detail Size")

        # Multires
        col_top.separator()
        multires_box = col_top.box()
        multires_box.label(text='Multires')
        multires_box.operator('dh.set_multires_viewport_max', text="Set Multires Max")
        multires_box.operator('dh.set_multires_viewport_zero', text="Set Multires Min")
        multires_box.operator('dh.apply_multires_base', text="Apply Base")
        multires_box.operator('dh.multires_level_modal', text="Adjust Level (Modal)", icon='DRIVER')

        ob = context.active_object
        if ob and ob.modifiers:
            multires = next((m for m in ob.modifiers if m.type == 'MULTIRES'), None)
            if multires:
                multires_box.operator("object.multires_subdivide", text="Subdivide")
                multires_box.operator("object.multires_higher_levels_delete", text="Delete Higher")

        # Modifiers Box
        mod_box = col_top.box()
        mod_box.label(text='Modifiers')

        mod_box.operator('object.apply_all_modifiers', text="Apply Modifiers")
        icon = icons.get("icon_delete")
        mod_box.operator('object.delete_all_modifiers', text="Delete Modifiers", icon_value=icon.icon_id)
        mod_box.operator('dh_op.copy_modifiers', text="Copy Modifiers")

