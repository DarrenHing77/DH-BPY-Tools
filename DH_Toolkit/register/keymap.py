import bpy
import addon_utils

# Store keymap items to remove when unregistering
addon_keymaps = []

def get_addon_preferences():
    """Helper function to get addon preferences"""
    addon_name = "DH_Toolkit"
    
    # Get addon preferences
    addon_prefs = None
    try:
        addon_prefs = bpy.context.preferences.addons[addon_name].preferences
    except KeyError:
        # Addon not enabled, try to find it and enable
        for addon in addon_utils.modules():
            if addon.bl_info['name'] == addon_name:
                addon_utils.enable(addon.__name__, default_set=True)
                addon_prefs = bpy.context.preferences.addons[addon.__name__].preferences
                break
    
    return addon_prefs

def register_keymap():
    """Register keymaps based on user preferences"""
    # Get preferences
    prefs = get_addon_preferences()
    if not prefs:
        # Fallback to default if preferences not accessible
        key = 'X'
        shift = True
        alt = False
        ctrl = False
    else:
        key = prefs.key_type
        shift = prefs.use_shift
        alt = prefs.use_alt
        ctrl = prefs.use_ctrl
    
    # Get window manager and keyconfig
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    
    if kc:
        # Create new keymap for 3D View
        km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
        
        # Create new keymap item with preferences
        kmi = km.keymap_items.new(
            "wm.call_menu_pie", 
            key, 
            "PRESS", 
            shift=shift,
            alt=alt,
            ctrl=ctrl
        )
        kmi.properties.name = "DH_MT_Main_Menu"
        
        # Store for removal on unregister
        addon_keymaps.append((km, kmi))

def unregister_keymap():
    """Unregister and remove keymaps"""
    # Remove keymaps when unregistering
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    
    addon_keymaps.clear()