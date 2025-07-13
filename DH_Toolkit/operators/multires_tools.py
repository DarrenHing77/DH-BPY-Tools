import bpy
from ..utlity.draw_2d import VerticalSlider
from mathutils import Vector
import bpy
from ..utlity.draw_2d import VerticalSlider
from mathutils import Vector

class DH_OP_multires_level_modal(bpy.types.Operator):
    """Modal operator to adjust multires subdivision levels"""
    bl_idname = "dh.multires_level_modal"
    bl_label = "Adjust Multires Level"
    bl_options = {'REGISTER', 'UNDO'}
        
    def invoke(self, context, event):
        # Initialize all state here
        self.multires_mod = None
        self.initial_level = 0
        self.current_level = 0
        self.is_sculpt_mode = False
        self.slider = None
        
        # Find multires modifier on active object
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Select a mesh object with multires modifier")
            return {'CANCELLED'}
            
        self.multires_mod = None
        for mod in obj.modifiers:
            if mod.type == 'MULTIRES':
                self.multires_mod = mod
                break
                
        if not self.multires_mod:
            self.report({'ERROR'}, "No multires modifier found")
            return {'CANCELLED'}
            
        # Check if we're in sculpt mode
        self.is_sculpt_mode = (context.mode == 'SCULPT')
        
        # Get current level based on mode
        if self.is_sculpt_mode:
            self.initial_level = self.multires_mod.sculpt_levels
            self.current_level = self.multires_mod.sculpt_levels
        else:
            self.initial_level = self.multires_mod.levels
            self.current_level = self.multires_mod.levels
            
        # Debug print
        print(f"🔥 Modal started: Initial level = {self.initial_level}, Total levels = {self.multires_mod.total_levels}")
        print(f"🔥 Mode: {'Sculpt' if self.is_sculpt_mode else 'Viewport'}")
            
        # Setup slider
        self.slider = VerticalSlider(
            center=Vector((context.region.width / 2, context.region.height / 2))
        )
        self.slider.setup_handler()
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            # Use slider for visual feedback and mouse tracking
            mouse_co = Vector((event.mouse_region_x, event.mouse_region_y))
            
            # Calculate level change
            level_change = self.slider.eval(
                mouse_co, 
                "Change",
                color=(0.204, 0.455, 0.922, 0.8),  # #3474eb
                unit_scale=40,
                digits=0
            )
            
            # Calculate target level
            target_level = max(0, min(self.multires_mod.total_levels, 
                                    self.initial_level + int(level_change)))
            
            if target_level != self.current_level:
                self.current_level = target_level
                self.apply_level(context)
                print(f"🔥 Level: {self.current_level}")
            
            # Add separate prominent text for current level
            self.slider.add_text(
                f"LEVEL: {self.current_level}/{self.multires_mod.total_levels} ({'SCULPT' if self.is_sculpt_mode else 'VIEWPORT'})",
                Vector((mouse_co.x + 50, mouse_co.y + 50)),
                32,  # Bigger text
                (1, 1, 1, 1)  # White
            )
            
            context.area.tag_redraw()

        elif event.type == 'WHEELUPMOUSE' and event.value == 'PRESS':
            # Mouse wheel up - increase level
            if self.current_level < self.multires_mod.total_levels:
                self.current_level += 1
                self.apply_level(context)
                print(f"🔥 Wheel UP: Level = {self.current_level}")
            
        elif event.type == 'WHEELDOWNMOUSE' and event.value == 'PRESS':
            # Mouse wheel down - decrease level
            if self.current_level > 0:
                self.current_level -= 1
                self.apply_level(context)
                print(f"🔥 Wheel DOWN: Level = {self.current_level}")
                
        elif event.type == 'UP_ARROW' and event.value == 'PRESS':
            # Arrow up - gradual increase
            if self.current_level < self.multires_mod.total_levels:
                self.current_level += 1
                self.apply_level(context)
                print(f"🔥 Arrow UP: Level = {self.current_level}")
                
        elif event.type == 'DOWN_ARROW' and event.value == 'PRESS':
            # Arrow down - gradual decrease
            if self.current_level > 0:
                self.current_level -= 1
                self.apply_level(context)
                print(f"🔥 Arrow DOWN: Level = {self.current_level}")

        elif event.type in {'LEFTMOUSE', 'SPACE', 'RET'}:
            # Confirm
            print(f"🔥 Modal finished at level: {self.current_level}")
            self.cleanup()
            return {'FINISHED'}

        elif event.type in {'ESC', 'RIGHTMOUSE'}:
            # Cancel - restore original level
            if self.is_sculpt_mode:
                self.multires_mod.sculpt_levels = self.initial_level
            else:
                self.multires_mod.levels = self.initial_level
            print(f"🔥 Modal cancelled, restored to: {self.initial_level}")
            self.cleanup()
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}
    
    def apply_level(self, context):
        """Apply current level to the appropriate multires property"""
        try:
            if self.is_sculpt_mode:
                self.multires_mod.sculpt_levels = self.current_level
                print(f"🔥 Applied sculpt_levels = {self.current_level}")
            else:
                self.multires_mod.levels = self.current_level
                print(f"🔥 Applied viewport levels = {self.current_level}")
            
            # Force viewport update
            context.area.tag_redraw()
            
            # Try additional update methods
            if context.object:
                context.object.update_tag()
            
        except Exception as e:
            print(f"🔥 ERROR in apply_level: {e}")
        
    def cleanup(self):
        """Clean up the slider"""
        if self.slider:
            self.slider.remove_handler()

    def cancel(self, context):
        self.cleanup()


## MULTIRES SET MAX - Updated to set both viewport and sculpt levels
class SetMultiresViewportLevelsMax(bpy.types.Operator):
    """Set Both Multires Viewport and Sculpt Levels to Maximum"""
    bl_idname = "dh.set_multires_viewport_max"
    bl_label = "Set Multires Levels to Maximum"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        target_objects = context.selected_objects or context.visible_objects
        for obj in target_objects:
            if obj.type == 'MESH':
                for modifier in obj.modifiers:
                    if modifier.type == 'MULTIRES':
                        # Set both viewport and sculpt levels to max
                        modifier.levels = modifier.total_levels
                        modifier.sculpt_levels = modifier.total_levels
        self.report({'INFO'}, "Both viewport and sculpt levels set to maximum.")
        return {'FINISHED'}


## MULTIRES SET ZERO - Updated to set both viewport and sculpt levels
class SetMultiresViewportLevelsZero(bpy.types.Operator):
    """Set Both Multires Viewport and Sculpt Levels to Zero"""
    bl_idname = "dh.set_multires_viewport_zero"
    bl_label = "Set Multires Levels to Zero"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        target_objects = context.selected_objects or context.visible_objects
        for obj in target_objects:
            if obj.type == 'MESH':
                for modifier in obj.modifiers:
                    if modifier.type == 'MULTIRES':
                        # Set both viewport and sculpt levels to zero
                        modifier.levels = 0
                        modifier.sculpt_levels = 0
        self.report({'INFO'}, "Both viewport and sculpt levels set to zero.")
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