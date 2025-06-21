import bpy
import os
from ..icons.icons import load_icons

def draw_modifiers_multires_menu(layout, context):
    ob = context.active_object
    layout.label(text='Modifiers')
   
    layout.operator_context = 'INVOKE_DEFAULT'
    icons = load_icons()
    layout.operator('object.apply_all_modifiers', text="Apply Modifiers")
    icon = icons.get("icon_delete")
    layout.operator('object.delete_all_modifiers', text="Delete Modifiers", icon_value=icon.icon_id)
    layout.operator('dh_op.copy_modifiers', text="Copy Modifiers")
    layout.operator('dh_op.toggle_modifiers_visibility', text="Modifiers Vis")
    layout.separator()
    layout.label(text="Multires")
    icon = icons.get("icon_subdcube")
    layout.operator('dh.set_multires_viewport_max', text="Set Multires Max",icon_value=icon.icon_id)
    icon = icons.get("icon_cube")
    layout.operator('dh.set_multires_viewport_zero', text="Set Multires Min",icon_value=icon.icon_id)

