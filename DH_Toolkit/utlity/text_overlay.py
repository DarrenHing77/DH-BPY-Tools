import bpy
import blf
from mathutils import Vector

class TextOverlay:
    def __init__(self, text="", position=None, color=(1,1,1,1), size=64):
        self.text = text
        self.position = position if position else Vector((0, 0))
        self.color = color
        self.size = size
        self._handler = None

    def draw(self, context):
        region = context.region
        font_id = 0
        blf.size(font_id, self.size, 72)
        w, h = blf.dimensions(font_id, self.text)
        x = (region.width - w) / 2
        y = region.height * 0.10  # 10% up from bottom
        # Black outline
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            blf.position(font_id, x+dx, y+dy, 0)
            blf.color(font_id, 0, 0, 0, 1)
            blf.draw(font_id, self.text)
        # Main text
        blf.position(font_id, x, y, 0)
        blf.color(font_id, *self.color)
        blf.draw(font_id, self.text)

    def setup_handler(self, context):
        self._handler = bpy.types.SpaceView3D.draw_handler_add(
            self.draw, (context,), 'WINDOW', 'POST_PIXEL'
        )

    def remove_handler(self):
        if self._handler:
            bpy.types.SpaceView3D.draw_handler_remove(self._handler, 'WINDOW')
            self._handler = None
