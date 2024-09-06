import bpy

class DH_OP_Decimate(bpy.types.Operator):
    bl_idname = 'dh.decimate'
    bl_label = 'Simple Decimate'
    bl_description = 'Simple uniform decimation'
    bl_options = {'REGISTER', 'UNDO'}

    ratio: bpy.props.FloatProperty(
        name='Ratio',
        description='Percentage to decimate',
        min=0,
        max=1,
        default=0.5
    )

    @classmethod
    def poll(cls, context):
        return is_mesh_pool(context)

    def invoke(self, context, event):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.ed.undo_push()
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        bpy.ops.ed.undo_push()
        ob = context.active_object
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.decimate(ratio=self.ratio)
        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}
