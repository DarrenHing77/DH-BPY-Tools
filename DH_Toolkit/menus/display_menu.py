import bpy
import os
from ..icons.icons import load_icons
import inspect


def draw_display(layout, context):
    ob = context.active_object
    layout.label(text='Display')
    
    
    layout.operator_context = 'INVOKE_DEFAULT'
    #icons = load_icons()
    
    
    #icon = icons.get("icon_primitives")
    layout.operator('dh.toggle_wireframe', text='Wireframe Override')
    layout.operator('dh.toggle_visibility_outliner', text='Unhide Outliner Selection')
    layout.operator('dh.switch_to_shader_editor', text='Shader Editor')
    
   
    
    layout.separator()
    

    
    
    
  