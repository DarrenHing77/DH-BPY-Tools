def register_addon():
    
    # properties
    from ..property import register_properties
    
    #Operators
    from ..operators import register_operators
    register_operators()
    
    # Menus
    from ..menus import register_menus
    register_menus()
    
    #Keymaps
    from .keymap import register_keymap
    register_keymap()
    
    

def unregister_addon():
    
    # properties
    from ..property import register_properties
    
    #Operators
    from ..operators import unregister_operators
    unregister_operators()
    
    #Menus
    from ..menus import unregister_menus
    unregister_menus()
    
    # keymaps
    from .keymap import unregister_keymap
    unregister_keymap()

