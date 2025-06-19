import bpy
import addon_utils

# Store keymap items to remove when unregistering
addon_keymaps = []

def get_addon_preferences():
    """Helper function to get addon preferences"""
    addon_name = "DH_Toolkit"
    addon_prefs = None
    try:
        addon_prefs = bpy.context.preferences.addons[addon_name].preferences
    except KeyError:
        for addon in addon_utils.modules():
            if addon.bl_info['name'] == addon_name:
                addon_utils.enable(addon.__name__, default_set=True)
                addon_prefs = bpy.context.preferences.addons[addon.__name__].preferences
                break
    return addon_prefs

def register_keymap():
    """Register keymaps based on user preferences"""
    prefs = get_addon_preferences()
    if not prefs:
        key = 'X'
        shift = True
        alt = False
        ctrl = False
    else:
        key = prefs.key_type
        shift = prefs.use_shift
        alt = prefs.use_alt
        ctrl = prefs.use_ctrl

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if not kc:
        return

    # Pie menu keymap
    km_pie = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi_pie = km_pie.keymap_items.new(
        "wm.call_menu_pie",
        key,
        "PRESS",
        shift=shift,
        alt=alt,
        ctrl=ctrl
    )
    kmi_pie.properties.name = "DH_MT_Main_Menu"
    addon_keymaps.append((km_pie, kmi_pie))

    # Loop select keymap
    km_loop = kc.keymaps.new(name="Mesh", space_type="EMPTY")

    kmi1 = km_loop.keymap_items.new('mesh.loop_select', 'LEFTMOUSE', 'DOUBLE_CLICK')
    kmi1.properties.extend = False
    kmi1.properties.deselect = False
    kmi1.properties.toggle = False

    kmi2 = km_loop.keymap_items.new('mesh.loop_select', 'LEFTMOUSE', 'DOUBLE_CLICK', shift=True)
    kmi2.properties.extend = True
    kmi2.properties.toggle = True

    kmi3 = km_loop.keymap_items.new('mesh.loop_select', 'LEFTMOUSE', 'DOUBLE_CLICK', ctrl=True)
    kmi3.properties.extend = False
    kmi3.properties.deselect = True
    kmi3.properties.toggle = False

    # Smart Hide keymap (hardcoded example)
    km_hide = kc.keymaps.new(name="3D View", space_type="VIEW_3D")

    kmi_hide = km_hide.keymap_items.new(
        idname="object.dh_smart_hide",
        type='H',  # Pick your key here
        value='PRESS',
        ctrl=True, shift=False, alt=False
    )

    addon_keymaps.extend([
        (km_loop, kmi1),
        (km_loop, kmi2),
        (km_loop, kmi3),
    ])
    addon_keymaps.append((km_hide, kmi_hide))

    
def unregister_keymap():
    """Unregister and remove keymaps"""
    for km, kmi in addon_keymaps:
        try:
            km.keymap_items.remove(kmi)
        except:
            pass
    addon_keymaps.clear()
