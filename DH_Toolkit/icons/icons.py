import bpy
import os

_icon_collection = None

def load_icons():
    global _icon_collection
    if _icon_collection is None:
        _icon_collection = bpy.utils.previews.new()
        icons_dir = os.path.join(os.path.dirname(__file__))
        
        # Load all your icons
        _icon_collection.load("icon_separate", os.path.join(icons_dir, "separate.png"), 'IMAGE')
        _icon_collection.load("icon_cube", os.path.join(icons_dir, "cube.png"), 'IMAGE')
        _icon_collection.load("icon_shaderball", os.path.join(icons_dir, "shaderBall.png"), 'IMAGE')
        _icon_collection.load("icon_knife", os.path.join(icons_dir, "knife.png"), 'IMAGE')
        _icon_collection.load("icon_subdcube", os.path.join(icons_dir, "subdCube.png"), 'IMAGE')
        _icon_collection.load("icon_brush", os.path.join(icons_dir, "brush.png"), 'IMAGE')
        _icon_collection.load("icon_mask", os.path.join(icons_dir, "mask.png"), 'IMAGE')
        _icon_collection.load("icon_grid", os.path.join(icons_dir, "grid.png"), 'IMAGE')
        _icon_collection.load("icon_extract", os.path.join(icons_dir, "extract.png"), 'IMAGE')
        _icon_collection.load("icon_delete", os.path.join(icons_dir, "delete.png"), 'IMAGE')
        _icon_collection.load("icon_undo", os.path.join(icons_dir, "undo.png"), 'IMAGE')
        _icon_collection.load("icon_switcharrow", os.path.join(icons_dir, "switchArrow.png"), 'IMAGE')
        _icon_collection.load("icon_camera", os.path.join(icons_dir, "camera.png"), 'IMAGE')
        _icon_collection.load("icon_disk", os.path.join(icons_dir, "disk.png"), 'IMAGE')
    
    return _icon_collection

def dh_tools_clear_icons():
    global _icon_collection
    if _icon_collection:
        bpy.utils.previews.remove(_icon_collection)
        _icon_collection = None