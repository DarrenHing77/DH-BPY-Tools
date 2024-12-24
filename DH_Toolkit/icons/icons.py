import inspect
import os
import bpy
import bpy.utils.previews



dh_tools_icon_collections = {}
dh_tools_icons_loaded = False


#icons_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+"\\"+"icons"
#icons_dir = icons_path.replace("\\","/")

icons_path = os.path.join(os.path.dirname(__file__))
icons_dir = icons_path.replace("\\","/")

def load_icons():
    global dh_tools_icon_collections
    global dh_tools_icons_loaded

    if dh_tools_icons_loaded: return dh_tools_icon_collections["main"]

    custom_icons = bpy.utils.previews.new()

    

    # modals
    custom_icons.load("icon_separate", os.path.join(icons_dir, "separate.png"), 'IMAGE')
    custom_icons.load("icon_artstation", os.path.join(icons_dir, "artstation.png"), 'IMAGE')
    custom_icons.load("icon_gumroad", os.path.join(icons_dir, "gumroad.png"), 'IMAGE')
    custom_icons.load("icon_youtube", os.path.join(icons_dir, "youtube.png"), 'IMAGE')
    custom_icons.load("icon_tutocom", os.path.join(icons_dir, "tutocom.png"), 'IMAGE')
    custom_icons.load("icon_discord", os.path.join(icons_dir, "discord.png"), 'IMAGE')
    custom_icons.load("icon_twitter", os.path.join(icons_dir, "twitter.png"), 'IMAGE')
    custom_icons.load("icon_web", os.path.join(icons_dir, "web.png"), 'IMAGE')
    custom_icons.load("icon_patreon", os.path.join(icons_dir, "patreon.png"), 'IMAGE')
    custom_icons.load("icon_facebook", os.path.join(icons_dir, "facebook.png"), 'IMAGE')
    custom_icons.load("icon_tipeee", os.path.join(icons_dir, "tipeee.png"), 'IMAGE')

    custom_icons.load("icon_sym_plus_x", os.path.join(icons_dir, "sym_plus_x.png"), 'IMAGE')
    custom_icons.load("icon_sym_minus_x", os.path.join(icons_dir, "sym_minus_x.png"), 'IMAGE')
    custom_icons.load("icon_sym_plus_y", os.path.join(icons_dir, "sym_plus_y.png"), 'IMAGE')
    custom_icons.load("icon_sym_minus_y", os.path.join(icons_dir, "sym_minus_y.png"), 'IMAGE')
    custom_icons.load("icon_sym_plus_z", os.path.join(icons_dir, "sym_plus_z.png"), 'IMAGE')
    custom_icons.load("icon_sym_minus_z", os.path.join(icons_dir, "sym_minus_z.png"), 'IMAGE')

    custom_icons.load("icon_symmetrize", os.path.join(icons_dir, "symmetrize.png"), 'IMAGE')
    custom_icons.load("icon_dh_tools", os.path.join(icons_dir, "dh_tools.png"), 'IMAGE')
    custom_icons.load("icon_surface", os.path.join(icons_dir, "surface.png"), 'IMAGE')
    custom_icons.load("icon_enveloppe", os.path.join(icons_dir, "enveloppe.png"), 'IMAGE')
    custom_icons.load("icon_lathe", os.path.join(icons_dir, "lathe.png"), 'IMAGE')
    custom_icons.load("icon_curve", os.path.join(icons_dir, "curve.png"), 'IMAGE')
    custom_icons.load("icon_skin", os.path.join(icons_dir, "skin.png"), 'IMAGE')
    custom_icons.load("icon_cutter", os.path.join(icons_dir, "cutter.png"), 'IMAGE')
    custom_icons.load("icon_s", os.path.join(icons_dir, "s.png"), 'IMAGE')
    custom_icons.load("icon_u", os.path.join(icons_dir, "u.png"), 'IMAGE')
    custom_icons.load("icon_corrective_smooth", os.path.join(icons_dir, "corrective_smooth.png"), 'IMAGE')
    custom_icons.load("icon_options", os.path.join(icons_dir, "options.png"), 'IMAGE')
    custom_icons.load("icon_draw_mesh", os.path.join(icons_dir, "draw_mesh.png"), 'IMAGE')
    custom_icons.load("icon_draw_skin", os.path.join(icons_dir, "draw_skin.png"), 'IMAGE')
    custom_icons.load("icon_bevel", os.path.join(icons_dir, "bevel.png"), 'IMAGE')
    custom_icons.load("icon_subsurf", os.path.join(icons_dir, "subsurf.png"), 'IMAGE')
    custom_icons.load("icon_union", os.path.join(icons_dir, "union.png"), 'IMAGE')
    custom_icons.load("icon_difference", os.path.join(icons_dir, "difference.png"), 'IMAGE')
    custom_icons.load("icon_rebool", os.path.join(icons_dir, "rebool.png"), 'IMAGE')
    custom_icons.load("icon_lattice", os.path.join(icons_dir, "lattice.png"), 'IMAGE')
    custom_icons.load("icon_quick_pose", os.path.join(icons_dir, "quick_pose.png"), 'IMAGE')
    custom_icons.load("icon_bones", os.path.join(icons_dir, "bones.png"), 'IMAGE')
    custom_icons.load("icon_pose", os.path.join(icons_dir, "pose.png"), 'IMAGE')
    custom_icons.load("icon_primitives", os.path.join(icons_dir, "primitives.png"), 'IMAGE')
    custom_icons.load("icon_tools", os.path.join(icons_dir, "tools.png"), 'IMAGE')
    custom_icons.load("icon_library", os.path.join(icons_dir, "library.png"), 'IMAGE')
    custom_icons.load("icon_mask", os.path.join(icons_dir, "mask.png"), 'IMAGE')
    custom_icons.load("icon_hook", os.path.join(icons_dir, "hook.png"), 'IMAGE')
    custom_icons.load("icon_empty", os.path.join(icons_dir, "empty.png"), 'IMAGE')
    custom_icons.load("icon_remesh", os.path.join(icons_dir, "remesh.png"), 'IMAGE')
    custom_icons.load("icon_decimate", os.path.join(icons_dir, "decimate.png"), 'IMAGE')
    custom_icons.load("icon_delete", os.path.join(icons_dir, "delete.png"), 'IMAGE')
    custom_icons.load("icon_undo", os.path.join(icons_dir, "undo.png"), 'IMAGE')
   


    dh_tools_icon_collections["main"] = custom_icons
    dh_tools_icons_loaded = True

    return dh_tools_icon_collections["main"]


def dh_tools_clear_icons():
    global dh_tools_icons_loaded
    for icon in dh_tools_icon_collections.values():
        bpy.utils.previews.remove(icon)
    dh_tools_icon_collections.clear()
    dh_tools_icons_loaded = False