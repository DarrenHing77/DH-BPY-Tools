import bpy

## MULTIRES SET MAX

class SetMultiresViewportLevelsMax(bpy.types.Operator):
    """Set Multires Viewport Levels to Maximum"""
    bl_idname = "dh.set_multires_viewport_max"
    bl_label = "Set Multires Viewport Levels to Maximum"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        target_objects = context.selected_objects or context.visible_objects
        for obj in target_objects:
            if obj.type == 'MESH':  # Only proceed for mesh objects
                for modifier in obj.modifiers:
                    if modifier.type == 'MULTIRES':
                        modifier.levels = modifier.total_levels  # Set to max (total levels)
        self.report({'INFO'}, "Viewport levels set to maximum for Multires modifiers.")
        return {'FINISHED'}



## MULTIRES SET ZERO

class SetMultiresViewportLevelsZero(bpy.types.Operator):
    """Set Multires Viewport Levels to Zero"""
    bl_idname = "dh.set_multires_viewport_zero"
    bl_label = "Set Multires Viewport Levels to Zero"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        target_objects = context.selected_objects or context.visible_objects
        for obj in target_objects:
            if obj.type == 'MESH':  # Only proceed for mesh objects
                for modifier in obj.modifiers:
                    if modifier.type == 'MULTIRES':
                        modifier.levels = 0  # Set viewport levels to zero
        self.report({'INFO'}, "Viewport levels set to zero for Multires modifiers.")
        return {'FINISHED'}


## MULTIRES APPLY BASE

class ApplyMultiresBase(bpy.types.Operator):
    """Apply Base for Multires Modifiers"""
    bl_idname = "dh.apply_multires_base"
    bl_label = "Apply Base for Multires"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        target_objects = context.selected_objects or context.visible_objects
        current_mode = context.mode
        if current_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        for obj in target_objects:
            if obj.type == 'MESH':
                context.view_layer.objects.active = obj
                for modifier in obj.modifiers:
                    if modifier.type == 'MULTIRES':
                        bpy.ops.object.multires_base_apply(modifier=modifier.name)
        if current_mode != 'OBJECT':
            bpy.ops.object.mode_set(mode=current_mode)
        self.report({'INFO'}, "Applied base for Multires modifiers.")
        return {'FINISHED'}

