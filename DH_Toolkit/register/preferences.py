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

    # Shader Builder custom naming patterns - simplified inputs
    naming_separator: bpy.props.EnumProperty(
        name="Separator",
        description="Character used to separate parts of texture names",
        items=[
            ('_', "Underscore (_)", "wood_basecolor_4k"),
            ('-', "Dash (-)", "wood-basecolor-4k"),
            ('.', "Dot (.)", "wood.basecolor.4k"),
            ('', "None", "woodbasecolor4k"),
        ],
        default='_'
    )
    
    # Custom suffix patterns (user-friendly)
    suffix_basecolor: bpy.props.StringProperty(
        name="Base Color Suffix",
        description="What comes after your material name for base color (e.g., 'd', 'diff', 'albedo')",
        default="d"
    )
    suffix_normal: bpy.props.StringProperty(
        name="Normal Suffix",
        description="What comes after your material name for normals",
        default="n"
    )
    suffix_roughness: bpy.props.StringProperty(
        name="Roughness Suffix", 
        description="What comes after your material name for roughness",
        default="r"
    )
    suffix_metallic: bpy.props.StringProperty(
        name="Metallic Suffix",
        description="What comes after your material name for metallic",
        default="m"
    )
    suffix_orm: bpy.props.StringProperty(
        name="ORM Suffix",
        description="What comes after your material name for ORM packed textures",
        default="orm"
    )
    suffix_height: bpy.props.StringProperty(
        name="Height Suffix",
        description="What comes after your material name for height/displacement",
        default="h"
    )
    suffix_ao: bpy.props.StringProperty(
        name="AO Suffix",
        description="What comes after your material name for ambient occlusion", 
        default="ao"
    )
    suffix_emission: bpy.props.StringProperty(
        name="Emission Suffix",
        description="What comes after your material name for emission",
        default="e"
    )
    
    # Advanced regex toggle
    use_advanced_patterns: bpy.props.BoolProperty(
        name="Use Advanced Regex Patterns",
        description="Enable direct regex input for advanced users",
        default=False
    )
    
    # Advanced regex patterns (for power users)
    regex_basecolor: bpy.props.StringProperty(
        name="Base Color Regex",
        description="Custom regex pattern for base color textures",
        default=""
    )
    regex_normal: bpy.props.StringProperty(
        name="Normal Regex", 
        description="Custom regex pattern for normal textures",
        default=""
    )
    regex_roughness: bpy.props.StringProperty(
        name="Roughness Regex",
        description="Custom regex pattern for roughness textures", 
        default=""
    )
    regex_metallic: bpy.props.StringProperty(
        name="Metallic Regex",
        description="Custom regex pattern for metallic textures",
        default=""
    )
    regex_orm: bpy.props.StringProperty(
        name="ORM Regex",
        description="Custom regex pattern for ORM packed textures",
        default=""
    )
    regex_height: bpy.props.StringProperty(
        name="Height Regex",
        description="Custom regex pattern for height/displacement textures",
        default=""
    )
    regex_ao: bpy.props.StringProperty(
        name="AO Regex", 
        description="Custom regex pattern for ambient occlusion textures",
        default=""
    )
    regex_emission: bpy.props.StringProperty(
        name="Emission Regex",
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
        shader_box.label(text="Shader Builder Texture Naming", icon='TEXTURE')
        
        # Simple naming setup
        simple_box = shader_box.box()
        simple_box.label(text="Simple Setup:", icon='PREFERENCES')
        
        row = simple_box.row()
        row.prop(self, "naming_separator")
        
        simple_box.label(text="Set the suffix for each texture type:")
        col = simple_box.column()
        
        # Create two columns for better layout
        split = col.split(factor=0.5)
        left_col = split.column()
        right_col = split.column()
        
        left_col.prop(self, "suffix_basecolor")
        left_col.prop(self, "suffix_normal")
        left_col.prop(self, "suffix_roughness")
        left_col.prop(self, "suffix_metallic")
        
        right_col.prop(self, "suffix_orm")
        right_col.prop(self, "suffix_height")
        right_col.prop(self, "suffix_ao")
        right_col.prop(self, "suffix_emission")
        
        # Show example
        sep = self.naming_separator if self.naming_separator else ""
        example_text = f"Example: wood{sep}{self.suffix_basecolor}.jpg, wood{sep}{self.suffix_normal}.jpg"
        simple_box.label(text=example_text, icon='INFO')
        
        # Advanced toggle
        shader_box.separator()
        shader_box.prop(self, "use_advanced_patterns", icon='SETTINGS')
        
        # Advanced regex patterns (only show if enabled)
        if self.use_advanced_patterns:
            advanced_box = shader_box.box()
            advanced_box.label(text="Advanced Regex Patterns:", icon='SCRIPT')
            advanced_box.label(text="For power users who want full regex control")
            
            col = advanced_box.column()
            col.prop(self, "regex_basecolor")
            col.prop(self, "regex_normal") 
            col.prop(self, "regex_roughness")
            col.prop(self, "regex_metallic")
            col.prop(self, "regex_orm")
            col.prop(self, "regex_height")
            col.prop(self, "regex_ao")
            col.prop(self, "regex_emission")
            
            advanced_box.separator()
            advanced_box.label(text="Note: Advanced patterns override simple setup", icon='ERROR')


# Register preferences and the operator
def register_preferences():
    bpy.utils.register_class(DH_OP_SetShortcutKey)
    bpy.utils.register_class(DH_ToolkitPreferences)

def unregister_preferences():
    bpy.utils.unregister_class(DH_ToolkitPreferences)
    bpy.utils.unregister_class(DH_OP_SetShortcutKey)