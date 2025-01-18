bl_info = {
    "name": "DH Texture Tools",
    "blender": (4, 3, 0),
    "category": "UV",
    "version": (1, 0),
    "author": "Darren",
    "description": "Tools for creating and filling UDIM tiles",
}

import bpy

# Operator to add UDIM tiles
class DH_OT_AddTiles(bpy.types.Operator):
    """Add UDIM Tiles Based on UV Space"""
    bl_idname = "dh.add_tiles"
    bl_label = "Add UDIM Tiles"
    bl_options = {'REGISTER', 'UNDO'}

    max_udims: bpy.props.IntProperty(
        name="Max UDIMs",
        default=100,
        min=1,
        description="Maximum number of UDIM tiles to add",
    )
    image_name: bpy.props.StringProperty()

    def execute(self, context):
        # Find the image
        image = bpy.data.images.get(self.image_name)
        if not image or image.source != 'TILED':
            self.report({'ERROR'}, f"No UDIM-enabled image named '{self.image_name}' found.")
            return {'CANCELLED'}
        
        # Get selected objects
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if not selected_objects:
            self.report({'ERROR'}, "No mesh objects selected.")
            return {'CANCELLED'}
        
        occupied_udims = set()

        for obj in selected_objects:
            # Ensure the object has an active UV layer
            if not obj.data.uv_layers:
                self.report({'WARNING'}, f"Object '{obj.name}' has no UV layers. Skipping.")
                continue
            
            uv_layer = obj.data.uv_layers.active
            if not uv_layer:
                self.report({'WARNING'}, f"Object '{obj.name}' has no active UV map. Skipping.")
                continue
            
            # Find occupied UDIM tiles for this object
            for loop in obj.data.loops:
                try:
                    uv = uv_layer.data[loop.index].uv
                    udim_x = int(uv.x // 1)
                    udim_y = int(uv.y // 1)
                    udim_number = 1001 + udim_x + (udim_y * 10)
                    occupied_udims.add(udim_number)
                except IndexError:
                    self.report({'WARNING'}, f"UV data index out of range for object '{obj.name}'. Skipping.")
                    continue

        # Limit the number of tiles to avoid crashing
        if len(occupied_udims) > self.max_udims:
            self.report({'INFO'}, f"Too many UDIM tiles detected ({len(occupied_udims)}). Limiting to {self.max_udims} tiles.")
            occupied_udims = sorted(occupied_udims)[:self.max_udims]

        # Add UDIM tiles to the image
        for udim_number in sorted(occupied_udims):
            if udim_number not in [tile.number for tile in image.tiles]:
                image.tiles.new(tile_number=udim_number)
                self.report({'INFO'}, f"Created UDIM tile: {udim_number}")
            else:
                self.report({'INFO'}, f"UDIM tile already exists: {udim_number}")

        self.report({'INFO'}, f"UDIM tiles added successfully. Total tiles added: {len(occupied_udims)}")
        return {'FINISHED'}


# Operator to fill UDIM tiles
class DH_OT_FillTiles(bpy.types.Operator):
    """Fill All UDIM Tiles"""
    bl_idname = "dh.fill_tiles"
    bl_label = "Fill UDIM Tiles"
    bl_options = {'REGISTER', 'UNDO'}

    image_name: bpy.props.StringProperty()

    def execute(self, context):
        # Find the image
        image = bpy.data.images.get(self.image_name)
        if not image or image.source != 'TILED':
            self.report({'ERROR'}, f"No UDIM-enabled image named '{self.image_name}' found.")
            return {'CANCELLED'}
        
        # Find an Image Editor in the current workspace
        image_editor_area = None
        for area in context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                image_editor_area = area
                break

        if not image_editor_area:
            self.report({'ERROR'}, "No Image Editor area found in the current workspace.")
            return {'CANCELLED'}

        # Fill all tiles
        for tile in image.tiles:
            image.tiles.active = tile  # Set the tile as active
            with context.temp_override(area=image_editor_area, region=image_editor_area.regions[-1]):
                bpy.ops.image.tile_fill()  # Fill the tile
                self.report({'INFO'}, f"Filled UDIM tile: {tile.number}")

        self.report({'INFO'}, "All UDIM tiles filled successfully.")
        return {'FINISHED'}


# Panel in the N-Panel
class DH_PT_TextureToolsPanel(bpy.types.Panel):
    """Panel for DH Texture Tools"""
    bl_label = "DH Texture Tools"
    bl_idname = "DH_PT_texture_tools"
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "DH Tools"

    def draw(self, context):
        layout = self.layout

        # Filter UDIM-enabled images
        udim_images = [img.name for img in bpy.data.images if img.source == 'TILED']
        if not udim_images:
            layout.label(text="No UDIM-enabled images found.")
            return

        # Dropdown for selecting UDIM image
        layout.prop(context.scene, "dh_selected_udim_image", text="UDIM Image")

        # Buttons for operators
        layout.label(text="UDIM Operations:")
        layout.operator(DH_OT_AddTiles.bl_idname, text="Add UDIM Tiles").image_name = context.scene.dh_selected_udim_image
        layout.operator(DH_OT_FillTiles.bl_idname, text="Fill UDIM Tiles").image_name = context.scene.dh_selected_udim_image


# Property to store the selected UDIM image name
def update_selected_image(self, context):
    pass  # Placeholder for potential future use

def register_properties():
    bpy.types.Scene.dh_selected_udim_image = bpy.props.EnumProperty(
        name="Selected UDIM Image",
        items=lambda self, context: [(img.name, img.name, "") for img in bpy.data.images if img.source == 'TILED'],
        description="Select a UDIM-enabled image",
        update=update_selected_image
    )


def unregister_properties():
    del bpy.types.Scene.dh_selected_udim_image


# Register classes
classes = [DH_OT_AddTiles, DH_OT_FillTiles, DH_PT_TextureToolsPanel]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_properties()


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    unregister_properties()


if __name__ == "__main__":
    register()
