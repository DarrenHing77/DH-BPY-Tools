import bpy

def register_addon():
    
    from .preferences import register_pref
    # Register other components: properties, operators, menus, and keymaps
    from ..property import register_properties
    from ..operators import register_operators
    from ..menus import register_menus
    from .keymap import register_keymap
    
    

    register_properties()
    register_operators()
    register_menus()
    register_keymap()
    register_pref()

def unregister_addon():
    # Unregister preferences
    from .preferences import unregister_pref

    # Unregister other components
    from ..operators import unregister_operators
    from ..menus import unregister_menus
    from .keymap import unregister_keymap
    

    unregister_operators()
    unregister_menus()
    unregister_keymap()
    unregister_pref()
