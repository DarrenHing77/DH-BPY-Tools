import bpy
import os
from ..icons.icons import load_icons
import inspect





def draw_mesh(layout, context):
    ob = context.active_object
    layout.label(text='Mesh')
    
    
    layout.operator_context = 'INVOKE_DEFAULT'
    icons = load_icons()
    
    #layout.operator("dh.decimate", text = "decimate")
    icon = icons.get("icon_primitives")
    layout.operator('object.join', text='Join',icon_value=icon.icon_id)
    
    icon = icons.get("icon_separate")
   
    layout.operator('mesh.separate',icon_value=icon.icon_id ).type="LOOSE"
    
    
    
    layout.operator("dh.dcc_importer", text="DCC Import")
    layout.operator("dh.dcc_exporter", text="DCC Export")
    layout.operator("dh.export_obj_multi", text="Multi OBJ Export") # new operator 


def draw_mask(layout, context):
    ob = context.active_object
    layout.label(text='Mask Tools')
    layout.operator('dh.mask_extract')
    layout.operator('sculpt_tool_kit.mask_split')
    layout.operator('sculpt_tool_kit.mask_decimate')
    if ob:
        if not ob.get('MASK_RIG'):
            layout.operator('sculpt_tool_kit.mask_deform_add')
        else:
            layout.operator('sculpt_tool_kit.mask_deform_remove')
    

