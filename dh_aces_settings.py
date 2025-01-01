bl_info = {
    "name": "DH ACES Settings",
    "blender": (2, 80, 0),
    "category": "Node",
}

import bpy

# Define the operator for setting color space
class SetColorSpaceOperator(bpy.types.Operator):
    bl_idname = "node.set_color_space"
    bl_label = "Set Color Space"

    color_space: bpy.props.StringProperty()

    def execute(self, context):
        selected_nodes = context.selected_nodes

        for node in selected_nodes:
            if node.type == 'TEX_IMAGE' or node.type == 'IMAGE':
                if hasattr(node, 'image'):
                    node.image.colorspace_settings.name = self.color_space
                    self.report({'INFO'}, f"Set color space to '{self.color_space}' for {node.name}")

        return {'FINISHED'}

# Define the operator for converting to UDIM
class ConvertToUDIMOperator(bpy.types.Operator):
    bl_idname = "node.convert_to_udim"
    bl_label = "Convert to UDIM Tiles"

    def execute(self, context):
        selected_nodes = context.selected_nodes

        for node in selected_nodes:
            if node.type == 'TEX_IMAGE':
                if hasattr(node, 'image') and node.image is not None:
                    node.image.source = 'TILED'
                    self.report({'INFO'}, f"Converted {node.name} to UDIM tiles")

        return {'FINISHED'}

# Define the custom panel for the Shader Editor
class NODE_PT_CustomPanel(bpy.types.Panel):
    bl_label = "ACES Color Space Tools"
    bl_idname = "NODE_PT_aces_color_space"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.label(text="Set Color Space for Selected Nodes:")

        col.operator("node.set_color_space", text="ACEScg (Color Maps)").color_space = 'ACEScg'
        col.operator("node.set_color_space", text="Raw (Non-Color Data)").color_space = 'Raw'

        col.separator()
        col.label(text="Other Tools:")
        col.operator("node.convert_to_udim", text="Convert to UDIM Tiles")

# Register the operators and panel
def register():
    bpy.utils.register_class(SetColorSpaceOperator)
    bpy.utils.register_class(ConvertToUDIMOperator)
    bpy.utils.register_class(NODE_PT_CustomPanel)

# Unregister the operators and panel
def unregister():
    bpy.utils.unregister_class(SetColorSpaceOperator)
    bpy.utils.unregister_class(ConvertToUDIMOperator)
    bpy.utils.unregister_class(NODE_PT_CustomPanel)

# Only run this script in Blender's Text Editor or Python Console
if __name__ == "__main__":
    register()
