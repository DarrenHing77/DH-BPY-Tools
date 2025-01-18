import bpy

class DH_ToolkitPreferences(bpy.types.AddonPreferences):
    bl_idname = "DH_Toolkit"

    # Custom Keymap preference (String Property for key binding)
    custom_keymap: bpy.props.StringProperty(
        name="Custom Keymap",
        description="Set a custom keymap for DH Toolkit",
        default="X"  # Default key is 'X'
    ) # type: ignore

    def draw(self, context):
        layout = self.layout

        # Add label for Keymap Preferences
        layout.label(text="Keymap Preferences:")

        # Input field for custom keymap (e.g., 'X', 'C', etc.)
        layout.prop(self, "custom_keymap", text="Custom Keymap (e.g., X)")

        # Add a button to trigger the keymap configuration (optional for manual input)
        row = layout.row()
        row.operator("wm.keymap_config", text="Assign Keymap")

# Register preferences
def register_pref():
    bpy.utils.register_class(DH_ToolkitPreferences)

def unregister_pref():
    bpy.utils.unregister_class(DH_ToolkitPreferences)
