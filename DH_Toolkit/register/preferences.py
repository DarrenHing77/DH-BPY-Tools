import bpy

class DH_OP_SetShortcutKey(bpy.types.Operator):
    bl_idname = "dh.set_shortcut_key"
    bl_label = "Click to press any key"
    bl_description = "Click then press any key to set it as the shortcut key"
    bl_options = {'REGISTER', 'INTERNAL'}

    # Static variable to store the button text
    button_text = "Click to set key"

    @classmethod
    def set_button_text(cls, text):
        cls.button_text = text
        # Force UI redraw
        for area in bpy.context.screen.areas:
            if area.type == 'PREFERENCES':
                area.tag_redraw()

    def invoke(self, context, event):
        # Start the modal operation
        DH_OP_SetShortcutKey.set_button_text("Press any key...")
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        # List of events to ignore
        ignored_keys = {
            'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE', 
            'LEFTMOUSE', 'RIGHTMOUSE', 'MIDDLEMOUSE',
            'LEFT_CTRL', 'RIGHT_CTRL', 
            'LEFT_ALT', 'RIGHT_ALT', 
            'LEFT_SHIFT', 'RIGHT_SHIFT'
        }

        # When a key is pressed
        if event.value == 'PRESS' and event.type not in ignored_keys:
            # Get addon preferences
            prefs = context.preferences.addons["DH_Toolkit"].preferences
            # Set the new key
            prefs.key_type = event.type
            # Update button text
            DH_OP_SetShortcutKey.set_button_text(f"Key: {event.type}")
            
            # Update keymap if necessary
            from .keymap import unregister_keymap, register_keymap
            unregister_keymap()
            register_keymap()
            
            return {'FINISHED'}
        
        # Cancel operation
        elif event.type == 'ESC':
            DH_OP_SetShortcutKey.set_button_text("Click to set key")
            return {'CANCELLED'}
        
        return {'RUNNING_MODAL'}


class DH_ToolkitPreferences(bpy.types.AddonPreferences):
    bl_idname = "DH_Toolkit"  # This must match your addon's package name

    # Key binding preferences
    key_type: bpy.props.StringProperty(
        name="Key",
        description="Key for the pie menu",
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

    # Shader Builder custom naming patterns
    custom_basecolor: bpy.props.StringProperty(
        name="Base Color Pattern",
        description="Custom regex pattern for base color textures (e.g., 'col|color_map')",
        default=""
    )
    custom_normal: bpy.props.StringProperty(
        name="Normal Pattern", 
        description="Custom regex pattern for normal textures",
        default=""
    )
    custom_roughness: bpy.props.StringProperty(
        name="Roughness Pattern",
        description="Custom regex pattern for roughness textures", 
        default=""
    )
    custom_metallic: bpy.props.StringProperty(
        name="Metallic Pattern",
        description="Custom regex pattern for metallic textures",
        default=""
    )
    custom_orm: bpy.props.StringProperty(
        name="ORM Pattern",
        description="Custom regex pattern for ORM packed textures",
        default=""
    )
    custom_height: bpy.props.StringProperty(
        name="Height Pattern",
        description="Custom regex pattern for height/displacement textures",
        default=""
    )
    custom_ao: bpy.props.StringProperty(
        name="AO Pattern", 
        description="Custom regex pattern for ambient occlusion textures",
        default=""
    )
    custom_emission: bpy.props.StringProperty(
        name="Emission Pattern",
        description="Custom regex pattern for emission textures", 
        default=""
    )

    def draw(self, context):
        layout = self.layout
        
        # Keymap settings section
        box = layout.box()
        box.label(text="DH Toolkit Keymap Settings", icon='KEYINGSET')
        
        # Key modifiers
        row = box.row()
        row.prop(self, "use_shift")
        row.prop(self, "use_alt")
        row.prop(self, "use_ctrl")
        
        # Key selection button
        row = box.row()
        row.label(text="Shortcut Key:")
        row.operator("dh.set_shortcut_key", text=DH_OP_SetShortcutKey.button_text)
        
        # Current key info
        if self.key_type:
            box.label(text=f"Current key: {self.key_type}")
        
        # Add a note about keymap changes
        box.separator()
        box.label(text="Note: Keymap changes apply immediately", icon='INFO')

        # Shader Builder settings section
        layout.separator()
        shader_box = layout.box()
        shader_box.label(text="Shader Builder Custom Patterns", icon='TEXTURE')
        shader_box.label(text="Use regex patterns to match your studio's texture naming conventions.")
        
        pattern_box = shader_box.box()
        col = pattern_box.column()
        
        col.prop(self, "custom_basecolor")
        col.prop(self, "custom_normal") 
        col.prop(self, "custom_roughness")
        col.prop(self, "custom_metallic")
        col.prop(self, "custom_orm")
        col.prop(self, "custom_height")
        col.prop(self, "custom_ao")
        col.prop(self, "custom_emission")
        
        shader_box.separator()
        shader_box.label(text="Examples:")
        shader_box.label(text="• 'mymat_d|my_diffuse' - matches either naming style")
        shader_box.label(text="• 'studio_.*_col' - matches studio_anything_col")
        shader_box.label(text="• '\\w+_basecolor_\\d+k' - matches word_basecolor_4k patterns")


# Register preferences and the operator
def register_preferences():
    bpy.utils.register_class(DH_OP_SetShortcutKey)
    bpy.utils.register_class(DH_ToolkitPreferences)

def unregister_preferences():
    bpy.utils.unregister_class(DH_ToolkitPreferences)
    bpy.utils.unregister_class(DH_OP_SetShortcutKey)