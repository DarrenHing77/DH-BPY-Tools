


def draw_sculpt_panels(layout, context):
    brush = context.tool_settings.sculpt.brush
    #layout.popover('SCULPT_TOOL_KIT_PT_brushes_list',
    #               text=brush.name,
    #               icon=brush_icon_get(brush))
    col = layout.column(align=True)
    col.popover('DH_TOOLKIT_PT_brush_panel')
    col.popover('VIEW3D_PT_tools_brush_settings_advanced')
    col.popover('VIEW3D_PT_tools_brush_options', text='Brush Options')
    col.popover('VIEW3D_PT_tools_brush_texture')
    col.popover('VIEW3D_PT_tools_brush_stroke')
    col.popover('VIEW3D_PT_tools_brush_falloff')
    col.popover('VIEW3D_PT_sculpt_options')
    col.popover('VIEW3D_PT_sculpt_dyntopo')
    col.popover('VIEW3D_PT_sculpt_voxel_remesh')
    col.popover('VIEW3D_PT_sculpt_symmetry')