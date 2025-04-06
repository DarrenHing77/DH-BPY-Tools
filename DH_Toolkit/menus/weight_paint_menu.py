import bpy
from ..icons.icons import load_icons

class DH_MT_Weight_Paint_Menu(bpy.types.Menu):
    bl_idname = "DH_MT_Weight_Paint_Menu"
    bl_label = "DH Weight Paint Toolkit"

    def draw(self, context):
        pie = self.layout.menu_pie()
        
        # Left column - Brushes
        col_left = pie.column()
        box_left = col_left.box()
        self.draw_weight_brushes(box_left, context)
        
        # Right column - Brush Settings
        col_right = pie.column()
        box_right = col_right.box()
        self.draw_brush_settings(box_right, context)
        
        # Bottom column - Weight Tools
        col_bottom = pie.column()
        box_bottom = col_bottom.box()
        self.draw_weight_tools(box_bottom, context)
        
        # Top column - Vertex Groups
        col_top = pie.column()
        box_top = col_top.box()
        self.draw_vertex_groups(box_top, context)
        
        # Bottom left - Weight Gradients
        col_bottom_left = pie.column()
        box_bottom_left = col_bottom_left.box()
        self.draw_weight_gradients(box_bottom_left, context)
        
        # Bottom right - Weight Transfer
        col_bottom_right = pie.column()
        box_bottom_right = col_bottom_right.box()
        self.draw_weight_transfer(box_bottom_right, context)
        
        # Top left - Armature/Bone Selection
        col_top_left = pie.column()
        box_top_left = col_top_left.box()
        self.draw_bone_selection(box_top_left, context)
        
        # Top right - Display Options (reused partly from main menu)
        col_top_right = pie.column()
        box_top_right = col_top_right.box()
        self.draw_display_options(box_top_right, context)
    
    def draw_weight_brushes(self, layout, context):
        layout.label(text="Weight Brushes")
        
        # Common weight painting brushes
        box = layout.box()
        box.label(text="Common Brushes")
        
        # Row 1 - Basic brushes
        row = box.row()
        row.operator("paint.brush_select", text="Draw").weight_paint_tool = 'DRAW'
        row.operator("paint.brush_select", text="Blur").weight_paint_tool = 'BLUR'
        
        # Row 2 - More brushes
        row = box.row()
        row.operator("paint.brush_select", text="Average").weight_paint_tool = 'AVERAGE'
        row.operator("paint.brush_select", text="Smear").weight_paint_tool = 'SMEAR'
        
        # Row 3 - Even more brushes
        row = box.row()
        row.operator("paint.brush_select", text="Draw Sharp").weight_paint_tool = 'DRAW_SHARP'
        row.operator("paint.brush_select", text="Multiply").weight_paint_tool = 'MULTIPLY'
        
        # Additional brush settings
        layout.separator()
        layout.operator("brush.reset", text="Reset Brush")
    
    def draw_brush_settings(self, layout, context):
        layout.label(text="Brush Settings")
        
        if context.tool_settings.weight_paint:
            brush = context.tool_settings.weight_paint.brush
            if brush:
                # Brush properties section
                box = layout.box()
                box.label(text="Brush Properties")
                
                # Row 1 - Size and Strength
                row = box.row()
                row.prop(brush, "size", text="Size")
                row.prop(brush, "strength", text="Strength")
                
                # Row 2 - Weight value
                row = box.row()
                row.prop(brush, "weight", text="Weight")
                
                # Additional properties
                box.prop(brush, "use_pressure_size", text="Size Pressure")
                box.prop(brush, "use_pressure_strength", text="Strength Pressure")
                
                # Falloff curve if available
                if hasattr(brush, "curve"):
                    box.label(text="Falloff Curve:")
                    box.template_curve_mapping(brush, "curve")
    
    def draw_weight_tools(self, layout, context):
        layout.label(text="Weight Tools")
        
        # Common weight operations
        box = layout.box()
        box.label(text="Common Operations")
        
        # Weight Painting options
        wpaint = context.tool_settings.weight_paint
        
        # Row 1 - Auto normalize and multi-paint
        row = box.row()
        row.prop(wpaint, "use_auto_normalize", text="Auto Normalize")
        row.prop(wpaint, "use_multipaint", text="Multi-Paint")
        
        # Row 2 - Lock and symmetry options
        if hasattr(wpaint, "use_lock_relative"):
            row = box.row()
            row.prop(wpaint, "use_lock_relative", text="Lock Relative")
        
        row = box.row()
        row.prop(context.object, "use_mesh_mirror_x", text="X-Mirror")
        
        # Special weight operations
        box = layout.box()
        box.label(text="Special Operations")
        
        # Row 1 - Smooth and clean
        row = box.row()
        row.operator("object.vertex_group_smooth", text="Smooth Weights")
        row.operator("object.vertex_group_clean", text="Clean Weights")
        
        # Row 2 - Quantize and levels
        row = box.row()
        row.operator("object.vertex_group_quantize", text="Quantize")
        row.operator("object.vertex_group_levels", text="Levels")
        
        # Row 3 - Normalize
        box.operator("object.vertex_group_normalize_all", text="Normalize All")
    
    def draw_vertex_groups(self, layout, context):
        layout.label(text="Vertex Groups")
        
        # Only show if there's an active object with vertex groups
        obj = context.active_object
        if not obj or not obj.vertex_groups:
            layout.label(text="No vertex groups")
            layout.operator("object.vertex_group_add", text="Add Vertex Group")
            return
        
        # Vertex group management
        box = layout.box()
        box.label(text="Group Management")
        
        # Row 1 - Add and remove
        row = box.row()
        row.operator("object.vertex_group_add", text="Add")
        row.operator("object.vertex_group_remove", text="Remove")
        
        # Row 2 - Assign and remove selection
        row = box.row()
        row.operator("object.vertex_group_assign", text="Assign")
        row.operator("object.vertex_group_remove_from", text="Remove")
        
        # Row 3 - Select and deselect
        row = box.row()
        row.operator("object.vertex_group_select", text="Select")
        row.operator("object.vertex_group_deselect", text="Deselect")
        
        # Active vertex group display
        box = layout.box()
        box.label(text="Active Group")
        
        if obj.vertex_groups.active:
            row = box.row()
            row.template_ID(obj, "vertex_groups", new="object.vertex_group_add")
    
    def draw_weight_gradients(self, layout, context):
        layout.label(text="Weight Gradients")
        
        # Gradient tools
        box = layout.box()
        box.label(text="Gradient Tools")
        
        # Row 1 - Linear and radial gradients
        row = box.row()
        row.operator("paint.weight_gradient", text="Linear").type = 'LINEAR'
        row.operator("paint.weight_gradient", text="Radial").type = 'RADIAL'
        
        # Row 2 - Gradient options
        box = layout.box()
        box.label(text="Options")
        
        row = box.row()
        row.operator("paint.weight_set", text="Set Weight")
        
        # Row 3 - Fill
        row = box.row()
        op = row.operator("paint.weight_fill", text="Fill with Active")
        op = row.operator("paint.weight_fill", text="Fill with Value")
        op.use_active = False
    
    def draw_weight_transfer(self, layout, context):
        layout.label(text="Weight Transfer")
        
        # Transfer options
        box = layout.box()
        box.label(text="Transfer Options")
        
        # Row 1 - Data transfer operator
        row = box.row()
        row.operator("object.data_transfer", text="Transfer Weights")
        
        # Additional transfer options
        box = layout.box()
        box.label(text="Copy Between Objects")
        
        # Row 2 - Copy and paste
        row = box.row()
        row.operator("object.vertex_group_copy", text="Copy Groups")
        row.operator("object.vertex_group_copy_to_linked", text="Copy to Linked")
        
        # Mirror weights
        box = layout.box()
        box.label(text="Mirror")
        box.operator("object.vertex_group_mirror", text="Mirror Vertex Groups")
    
    def draw_bone_selection(self, layout, context):
        layout.label(text="Bone Selection")
        
        # Check if the active object has an armature modifier
        obj = context.active_object
        has_armature = False
        
        if obj and obj.modifiers:
            for mod in obj.modifiers:
                if mod.type == 'ARMATURE' and mod.object:
                    has_armature = True
                    armature = mod.object
                    break
        
        if not has_armature:
            layout.label(text="No armature found")
            return
        
        # Armature bone selection
        box = layout.box()
        box.label(text="Bone Selection")
        
        # List a few bones if available
        if armature and armature.data:
            for i, bone in enumerate(armature.data.bones):
                if i < 5:  # Show max 5 bones
                    row = box.row()
                    op = row.operator("paint.weight_sample_group", text=bone.name)
                    op.group = bone.name
                elif i == 5:
                    box.label(text="... more bones")
                    break
        
        # Weight lock options
        box = layout.box()
        box.label(text="Weight Lock")
        
        row = box.row()
        row.operator("paint.weight_from_bones", text="Assign From Bones")
    
    def draw_display_options(self, layout, context):
        layout.label(text="Display Options")
        
        # Display settings
        box = layout.box()
        box.label(text="Display")
        
        # Row 1 - Zero weights display
        row = box.row()
        row.prop(context.tool_settings, "vertex_group_user", expand=True)
        
        # Row 2 - Weight display options
        if hasattr(context.space_data, "overlay"):
            row = box.row()
            row.prop(context.space_data.overlay, "show_weight", text="Show Weights")
        
        # Row 3 - Weight colors
        row = box.row()
        if hasattr(context.preferences.themes[0], "weight_paint"):
            wp = context.preferences.themes[0].weight_paint
            row.label(text="Weight Colors:")
            row.prop(wp, "low_color", text="Zero")
            row.prop(wp, "high_color", text="One")
        
        # Additional display utilities from main menu
        layout.separator()
        layout.operator('dh.toggle_wireframe', text='Wireframe Override')