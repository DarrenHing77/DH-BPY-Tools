import bpy

class DH_ToolkitPreferences(bpy.types.AddonPreferences):
    bl_idname = "DH_Toolkit"  # This must match your addon's package name

    # Key binding preferences
    key_type: bpy.props.EnumProperty(
        name="Key",
        description="Key for the pie menu",
        items=[
            ('X', "X", "Use X key"),
            ('Z', "Z", "Use Z key"),
            ('A', "A", "Use A key"),
            ('S', "S", "Use S key"),
            ('D', "D", "Use D key"),
            ('F', "F", "Use F key"),
            ('W', "W", "Use W key"),
            ('E', "E", "Use E key"),
            ('R', "R", "Use R key"),
            ('TAB', "Tab", "Use Tab key"),
            ('SPACE', "Space", "Use Space key"),
            ('Q', "Q", "Use Q key")
        ],
        default='X'
    )
    
    use_shift: bpy.props.BoolProperty(
        name="Shift",
        description="Use Shift modifier",
        default=True
    )
    
    use_alt: bpy.props.BoolProperty(
        name="Alt",
        description="Use Alt modifier",
        default=False
    )
    
    use_ctrl: bpy.props.BoolProperty(
        name="Ctrl",
        description="Use Ctrl modifier",
        default=False
    )

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.label(text="DH Toolkit Keymap Settings", icon='KEYINGSET')
        
        # Key modifiers
        row = box.row()
        row.prop(self, "use_shift")
        row.prop(self, "use_alt")
        row.prop(self, "use_ctrl")
        
        # Key selection
        box.prop(self, "key_type")
        
        # Add a note about restarting Blender
        box.separator()
        box.label(text="Note: Restart Blender after changing keymap settings", icon='INFO')

# Register preferences
def register_pref():
    bpy.utils.register_class(DH_ToolkitPreferences)

def unregister_pref():
    bpy.utils.unregister_class(DH_ToolkitPreferences)