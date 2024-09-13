bl_info = {
    "name": "DH Aces Settings",
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
                    print(f"Set color space to '{self.color_space}' for {node.name}")

        return {'FINISHED'}

# Define the custom N-panel menu for the Shader Editor
class NODE_PT_CustomPanel(bpy.types.Panel):
    bl_label = "Color Space Tools"
    bl_idname = "NODE_PT_color_space"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.label(text="Set Color Space Comp:")

        col.operator("node.set_color_space", text="Utility - sRGB - Texture").color_space = 'Utility - sRGB - Texture'
        col.operator("node.set_color_space", text="Utility - Raw").color_space = 'Utility - Raw'

# Define the custom C-panel menu for the Compositor
class COMPOSITING_PT_CustomPanel(bpy.types.Panel):
    bl_label = "Color Space Tools"
    bl_idname = "COMPOSITING_PT_color_space"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.label(text="Set Color Space:")

        col.operator("node.set_color_space", text="Utility - sRGB - Texture").color_space = 'Utility - sRGB - Texture'
        col.operator("node.set_color_space", text="Utility - Raw").color_space = 'Utility - Raw'

# Register the operator and panels
def register():
    bpy.utils.register_class(SetColorSpaceOperator)
    bpy.utils.register_class(NODE_PT_CustomPanel)
    bpy.utils.register_class(COMPOSITING_PT_CustomPanel)

# Unregister the operator and panels
def unregister():
    bpy.utils.unregister_class(SetColorSpaceOperator)
    bpy.utils.unregister_class(NODE_PT_CustomPanel)
    bpy.utils.unregister_class(COMPOSITING_PT_CustomPanel)

# Only run this script in Blender's Text Editor or Python Console
if __name__ == "__main__":
    register()
