import bpy

# Import main menu class
from .main_menu import DH_MT_Main_Menu

# Import context-specific menu classes
from .edit_menu import DH_MT_Edit_Menu
from .sculpt_menu import DH_MT_Sculpt_Menu
from .texture_paint_menu import DH_MT_Texture_Paint_Menu
from .weight_paint_menu import DH_MT_Weight_Paint_Menu
from .uv_edit_menu import DH_MT_UV_Edit_Menu

# All menu classes tuple
classes = (
    DH_MT_Main_Menu,
    DH_MT_Edit_Menu,
    DH_MT_Sculpt_Menu,
    DH_MT_Texture_Paint_Menu,
    DH_MT_Weight_Paint_Menu,
    DH_MT_UV_Edit_Menu,
)

# Dictionary to store context keymaps
context_keymaps = {}

def register_menus():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    # Register the keymaps after the menu classes
    register_context_keymaps()

def unregister_menus():
    # Unregister the keymaps first
    unregister_context_keymaps()
    
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

def get_addon_preferences():
    """Helper function to get addon preferences"""
    addon_name = "DH_Toolkit"
    prefs = None
    try:
        prefs = bpy.context.preferences.addons[addon_name].preferences
    except:
        pass
    return prefs

def register_context_keymaps():
    """Register keymaps for all context modes"""
    global context_keymaps
    
    # Get preferences for keymap settings
    prefs = get_addon_preferences()
    if not prefs:
        # Default shortcut settings if preferences not found
        key = 'X'
        shift = True
        alt = False
        ctrl = False
    else:
        key = prefs.key_type
        shift = prefs.use_shift
        alt = prefs.use_alt
        ctrl = prefs.use_ctrl
    
    # Get keyconfig
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    
    if kc:
        # Create keymap for Edit Mode
        km_edit = kc.keymaps.new(name="Mesh", space_type="EMPTY")
        kmi_edit = km_edit.keymap_items.new(
            "wm.call_menu_pie", 
            key, 
            "PRESS", 
            shift=shift,
            alt=alt,
            ctrl=ctrl
        )
        kmi_edit.properties.name = "DH_MT_Edit_Menu"
        context_keymaps["edit"] = (km_edit, kmi_edit)
        
        # Create keymap for Sculpt Mode
        km_sculpt = kc.keymaps.new(name="Sculpt", space_type="EMPTY")
        kmi_sculpt = km_sculpt.keymap_items.new(
            "wm.call_menu_pie", 
            key, 
            "PRESS", 
            shift=shift,
            alt=alt,
            ctrl=ctrl
        )
        kmi_sculpt.properties.name = "DH_MT_Sculpt_Menu"
        context_keymaps["sculpt"] = (km_sculpt, kmi_sculpt)
        
        # Create keymap for Texture Paint Mode
        km_texture = kc.keymaps.new(name="Image Paint", space_type="EMPTY")
        kmi_texture = km_texture.keymap_items.new(
            "wm.call_menu_pie", 
            key, 
            "PRESS", 
            shift=shift,
            alt=alt,
            ctrl=ctrl
        )
        kmi_texture.properties.name = "DH_MT_Texture_Paint_Menu"
        context_keymaps["texture"] = (km_texture, kmi_texture)
        
        # Create keymap for Weight Paint Mode
        km_weight = kc.keymaps.new(name="Weight Paint", space_type="EMPTY")
        kmi_weight = km_weight.keymap_items.new(
            "wm.call_menu_pie", 
            key, 
            "PRESS", 
            shift=shift,
            alt=alt,
            ctrl=ctrl
        )
        kmi_weight.properties.name = "DH_MT_Weight_Paint_Menu"
        context_keymaps["weight"] = (km_weight, kmi_weight)
        
        # Create keymap for UV Editor Mode
        km_uv = kc.keymaps.new(name="UV Editor", space_type="EMPTY")
        kmi_uv = km_uv.keymap_items.new(
            "wm.call_menu_pie", 
            key, 
            "PRESS", 
            shift=shift,
            alt=alt,
            ctrl=ctrl
        )
        kmi_uv.properties.name = "DH_MT_UV_Edit_Menu"
        context_keymaps["uv"] = (km_uv, kmi_uv)

def unregister_context_keymaps():
    """Remove all context-specific keymaps"""
    global context_keymaps
    
    # Remove each stored keymap
    for mode, (km, kmi) in context_keymaps.items():
        km.keymap_items.remove(kmi)
    
    # Clear the dictionary
    context_keymaps.clear()