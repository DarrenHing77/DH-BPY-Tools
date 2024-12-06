import bpy

## MULTIRES SET MAX

class SetMultiresViewportLevelsMax(bpy.types.Operator):
    """Set Multires Viewport Levels to Maximum"""
    bl_idname = "dh.set_multires_viewport_max"
    bl_label = "Set Multires Viewport Levels to Maximum"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selected_objects = context.selected_objects
        for obj in selected_objects:
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
        selected_objects = context.selected_objects
        for obj in selected_objects:
            if obj.type == 'MESH':  # Only proceed for mesh objects
                for modifier in obj.modifiers:
                    if modifier.type == 'MULTIRES':
                        modifier.levels = 0  # Set viewport levels to zero
        self.report({'INFO'}, "Viewport levels set to zero for Multires modifiers.")
        return {'FINISHED'}

