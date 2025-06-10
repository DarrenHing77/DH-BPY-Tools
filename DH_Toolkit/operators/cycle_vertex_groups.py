from ..utlity.text_overlay import TextOverlay
import bpy

class DH_OP_CycleVertexGroups(bpy.types.Operator):
    """Cycle Vertex Groups and display as overlay"""
    bl_idname = 'dh.cycle_vertex_groups'
    bl_label = 'DH Cycle Vertex Groups'
    bl_options = {'REGISTER', 'UNDO'}

    group_index: bpy.props.IntProperty(default=0)

    def invoke(self, context, event):
        obj = context.object
        if not obj or obj.type != 'MESH' or not obj.vertex_groups:
            self.report({'ERROR'}, "Select a mesh with vertex groups.")
            return {'CANCELLED'}

        self.groups = obj.vertex_groups
        self.group_index = obj.vertex_groups.active_index if obj.vertex_groups.active_index >= 0 else 0
        obj.vertex_groups.active_index = self.group_index

        # Overlay setup
        self.text_overlay = TextOverlay(
            text=f"Active Vertex Group: {self.groups[self.group_index].name}",
            size=72
        )
        self.text_overlay.setup_handler(context)
        context.area.tag_redraw()
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        obj = context.object
        groups = self.groups

        if not groups:
            self.text_overlay.remove_handler()
            return {'CANCELLED'}

        redraw = False

        if event.type == 'WHEELUPMOUSE':
            self.group_index = (self.group_index + 1) % len(groups)
            obj.vertex_groups.active_index = self.group_index
            redraw = True
        elif event.type == 'WHEELDOWNMOUSE':
            self.group_index = (self.group_index - 1) % len(groups)
            obj.vertex_groups.active_index = self.group_index
            redraw = True
        elif event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            self.text_overlay.remove_handler()
            return {'FINISHED'}
        elif event.type in {'ESC', 'RIGHTMOUSE'}:
            self.text_overlay.remove_handler()
            return {'CANCELLED'}

        if redraw:
            self.text_overlay.text = f"Active Vertex Group: {groups[self.group_index].name}"
            context.area.tag_redraw()

        return {'RUNNING_MODAL'}

    def cancel(self, context):
        self.text_overlay.remove_handler()
