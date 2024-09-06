
bl_info = {
    "name": "DH_Toolkit",
    "description": "DH Tools",
    "author": "Darren Hing",
    "version": (1, 1),
    "blender": (4, 1, 0),
    "location": "View3D",
    "category": "3D View"}


def register():
    from .register import register_addon
    register_addon()


def unregister():
    from .register import unregister_addon
    unregister_addon()