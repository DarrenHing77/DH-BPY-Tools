import bpy

def register_addon():
    # Register preferences first so they're available for keymap setup
    from .preferences import register_pref
    register_pref()
    
    # Register other components: properties, operators, menus, and keymaps
    from ..property import register_properties
    from ..operators import register_operators
    from ..menus import register_menus
    from .keymap import register_keymap, unregister_keymap
    
    register_properties()
    register_operators()
    register_menus()
    
    # Register keymap last (after preferences are available)
    register_keymap()

def unregister_addon():
    # Unregister keymap first
    from .keymap import unregister_keymap
    unregister_keymap()
    
    # Unregister other components
    from ..operators import unregister_operators
    from ..menus import unregister_menus
    
    unregister_operators()
    unregister_menus()
    
    # Unregister preferences last
    from .preferences import unregister_pref
    unregister_pref()