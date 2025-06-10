import bpy
from ..icons.icons import load_icons

class DH_MT_Weight_Paint_Menu(bpy.types.Menu):
    bl_idname = "wm.dh_open_weight_popup"
    bl_label = "DH Weight Paint Toolkit"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Weight Paint Toolkit")

        box = layout.box()
        self.draw_weight_brushes(box, context)

        box = layout.box()
        self.draw_brush_settings(box, context)

        box = layout.box()
        self.draw_weight_tools(box, context)

        box = layout.box()
        self.draw_display_options(box, context)

    # Optional: add the others back if needed
    # box = layout.box()
    # self.draw_vertex_groups(box, context)

    
    def draw_weight_brushes(self, layout, context):
        layout.label(text="Weight Brushes")
        
        # Common weight painting brushes
        box = layout.box()
        
        
        # Row 1 - Basic brushes
        column = box.column()
        wpaint = context.tool_settings.weight_paint
        column.operator("wm.tool_set_by_id", text="Brush").name = "builtin.brush"
        column.operator("wm.tool_set_by_id", text="Blur").name = "builtin_brush.blur"
        
        # Row 2 - More brushes
        #row = box.row()
        column.operator("wm.tool_set_by_id", text="Average").name = "builtin_brush.average"
        column.operator("wm.tool_set_by_id", text="Smear").name = "builtin_brush.smear"
        column.operator("wm.tool_set_by_id", text="Gradient").name = "builtin.gradient"
        
       


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
                row.prop(context.scene.tool_settings.unified_paint_settings, "size", text="Size")
                row.prop(context.scene.tool_settings.unified_paint_settings, "weight", text="Weight")
                
                # Row 2 - Weight value
              #  row = box.row()
               # row.prop(brush, "weight", text="Weight")
                
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
        
        # Weight Painting options
       # wpaint = context.tool_settings.weight_paint
        
        # Row 1 - Auto normalize and multi-paint
        column = box.column()
        column.operator("paint.weight_set", text="Set Weight")
        column.operator("object.vertex_group_smooth", text="Smooth Weight")
        column.operator("dh.cycle_vertex_groups", text="Cycle Vertex Groups")
        
    
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

    
   