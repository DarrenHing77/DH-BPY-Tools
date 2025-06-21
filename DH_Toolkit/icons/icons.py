import inspect
import os
import bpy
import bpy.utils.previews



dh_tools_icon_collections = {}
dh_tools_icons_loaded = False


icons_path = os.path.join(os.path.dirname(__file__))
icons_dir = icons_path.replace("\\","/")

def load_icons():
    global dh_tools_icon_collections
    global dh_tools_icons_loaded

    if dh_tools_icons_loaded: return dh_tools_icon_collections["main"]

    custom_icons = bpy.utils.previews.new()

    

    # modals
    custom_icons.load("icon_separate", os.path.join(icons_dir, "separate.png"), 'IMAGE')
    custom_icons.load("icon_cube", os.path.join(icons_dir, "cube.png"), 'IMAGE')
    custom_icons.load("icon_shaderball", os.path.join(icons_dir, "shaderBall.png"), 'IMAGE')
    custom_icons.load("icon_knife", os.path.join(icons_dir, "knife.png"), 'IMAGE')
    custom_icons.load("icon_subdcube", os.path.join(icons_dir, "subdCube.png"), 'IMAGE')
    custom_icons.load("icon_brush", os.path.join(icons_dir, "brush.png"), 'IMAGE')
    custom_icons.load("icon_mask", os.path.join(icons_dir, "mask.png"), 'IMAGE')
    custom_icons.load("icon_grid", os.path.join(icons_dir, "grid.png"), 'IMAGE')
    custom_icons.load("icon_extract", os.path.join(icons_dir, "extract.png"), 'IMAGE')
    custom_icons.load("icon_delete", os.path.join(icons_dir, "delete.png"), 'IMAGE')
    custom_icons.load("icon_undo", os.path.join(icons_dir, "undo.png"), 'IMAGE')
    custom_icons.load("icon_switcharrow", os.path.join(icons_dir, "switchArrow.png"), 'IMAGE')
   


    dh_tools_icon_collections["main"] = custom_icons
    dh_tools_icons_loaded = True

    return dh_tools_icon_collections["main"]


def dh_tools_clear_icons():
    global dh_tools_icons_loaded
    for icon in dh_tools_icon_collections.values():
        bpy.utils.previews.remove(icon)
    dh_tools_icon_collections.clear()
    dh_tools_icons_loaded = False