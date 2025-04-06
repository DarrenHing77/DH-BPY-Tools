import bpy
from ..icons.icons import load_icons
from .brush_panel import draw_sculpt_panels

class DH_MT_Sculpt_Menu(bpy.types.Menu):
    bl_idname = "DH_MT_Sculpt_Menu"
    bl_label = "DH Sculpt Toolkit"

    def draw(self, context):
        pie = self.layout.menu_pie()
        
        # Left column - Brushes
        col_left = pie.column()
        box_left = col_left.box()
        self.draw_brush_tools(box_left, context)
        
        # Right column - Sculpt Panels (reused from main menu)
        col_right = pie.column()
        box_right = col_right.box()
        draw_sculpt_panels(box_right, context)
        
        # Bottom column - Dyntopo and Remesh
        col_bottom = pie.column()
        box_bottom = col_bottom.box()
        self.draw_topology_tools(box_bottom, context)
        
        # Top column - Symmetry and Mirror
        col_top = pie.column()
        box_top = col_top.box()
        self.draw_symmetry_tools(box_top, context)
        
        # Bottom left - Mask Tools (reused from main menu)
        col_bottom_left = pie.column()
        box_bottom_left = col_bottom_left.box()
        self.draw_mask_tools(box_bottom_left, context)
        
        # Bottom right - Face Sets
        col_bottom_right = pie.column()
        box_bottom_right = col_bottom_right.box()
        self.draw_face_sets_tools(box_bottom_right, context)
        
        # Top left - Multires Tools (reused from main menu)
        col_top_left = pie.column()
        box_top_left = col_top_left.box()
        self.draw_multires_tools(box_top_left, context)
        
        # Top right - Display Options
        col_top_right = pie.column()
        box_top_right = col_top_right.box()
        self.draw_display_options(box_top_right, context)
    
    def draw_brush_tools(self, layout, context):
        layout.label(text="Brush Selection")
        
        # Common Brushes
        box = layout.box()
        box.label(text="Common Brushes")
        
        # Row 1 - Basic sculpting
        row = box.row()
        row.operator("sculpt.brush_select", text="Draw").sculpt_tool = 'DRAW'
        row.operator("sculpt.brush_select", text="Clay").sculpt_tool = 'CLAY'
        
        # Row 2 - Building shapes
        row = box.row()
        row.operator("sculpt.brush_select", text="Crease").sculpt_tool = 'CREASE'
        row.operator("sculpt.brush_select", text="Inflate").sculpt_tool = 'INFLATE'
        
        # Row 3 - Smoothing and refining
        row = box.row()
        row.operator("sculpt.brush_select", text="Smooth").sculpt_tool = 'SMOOTH'
        row.operator("sculpt.brush_select", text="Flatten").sculpt_tool = 'FLATTEN'
        
        # Row 4 - Detail work
        row = box.row()
        row.operator("sculpt.brush_select", text="Grab").sculpt_tool = 'GRAB'
        row.operator("sculpt.brush_select", text="Pinch").sculpt_tool = 'PINCH'
        
        # Stroke methods
        layout.separator()
        box = layout.box()
        box.label(text="Stroke Method")
        row = box.row(align=True)
        row.operator("sculpt.set_stroke_method", text="Dots").mode = 'DOTS'
        row.operator("sculpt.set_stroke_method", text="Drag").mode = 'DRAG'
        row.operator("sculpt.set_stroke_method", text="Space").mode = 'SPACE'
    
    def draw_topology_tools(self, layout, context):
        layout.label(text="Topology Tools")
        
        # Dyntopo section
        box = layout.box()
        box.label(text="Dynamic Topology")
        
        row = box.row(align=True)
        dyntopo_enabled = context.sculpt_object.use_dynamic_topology_sculpting if context.sculpt_object else False
        if dyntopo_enabled:
            row.operator("sculpt.dynamic_topology_toggle", text="Disable Dyntopo")
        else:
            row.operator("sculpt.dynamic_topology_toggle", text="Enable Dyntopo")
        
        row = box.row(align=True)
        row.operator("sculpt.detail_flood_fill", text="Detail Flood Fill")
        
        row = box.row(align=True)
        row.operator("sculpt.sample_detail_size", text="Sample Detail Size")
        
        # Remesh section
        box = layout.box()
        box.label(text="Remesh")
        
        row = box.row(align=True)
        row.operator("object.voxel_remesh", text="Voxel Remesh")
        row.operator("object.quadriflow_remesh", text="Quad Remesh")
        
        # Decimate (from your existing menu)
        layout.separator()
        layout.operator('dh.decimate', text="Decimate")
    
    def draw_symmetry_tools(self, layout, context):
        layout.label(text="Symmetry")
        
        # Access sculpt tool settings
        sculpt = context.tool_settings.sculpt
        
        # Symmetry toggles
        box = layout.box()
        box.label(text="Mirror")
        
        row = box.row(align=True)
        row.prop(sculpt, "use_symmetry_x", text="X", toggle=True)
        row.prop(sculpt, "use_symmetry_y", text="Y", toggle=True)
        row.prop(sculpt, "use_symmetry_z", text="Z", toggle=True)
        
        # Symmetrize
        box = layout.box()
        box.label(text="Symmetrize")
        
        row = box.row(align=True)
        row.operator("sculpt.symmetrize", text="+X to -X").direction = 'POSITIVE_X'
        row.operator("sculpt.symmetrize", text="-X to +X").direction = 'NEGATIVE_X'
        
        row = box.row(align=True)
        row.operator("sculpt.symmetrize", text="+Y to -Y").direction = 'POSITIVE_Y'
        row.operator("sculpt.symmetrize", text="-Y to +Y").direction = 'NEGATIVE_Y'
        
        row = box.row(align=True)
        row.operator("sculpt.symmetrize", text="+Z to -Z").direction = 'POSITIVE_Z'
        row.operator("sculpt.symmetrize", text="-Z to +Z").direction = 'NEGATIVE_Z'
    
    def draw_mask_tools(self, layout, context):
        layout.label(text="Mask Tools")
        
        # Basic mask operations
        box = layout.box()
        box.label(text="Create & Edit")
        
        row = box.row(align=True)
        row.operator("sculpt.mask_flood_fill", text="Fill").mode = 'VALUE'
        row.operator("sculpt.mask_flood_fill", text="Clear").mode = 'VALUE'
        row.operator("sculpt.mask_flood_fill", text="Invert").mode = 'INVERT'
        
        box.operator("sculpt.mask_box_gesture", text="Box Mask").mode = 'ADD'
        box.operator("sculpt.mask_lasso_gesture", text="Lasso Mask").mode = 'ADD'
        
        # Advanced mask tools (from your existing menu)
        layout.separator()
        layout.operator('dh.mask_extract', text="Extract Mask")
        layout.operator('mesh.paint_mask_slice', text="Mask Slice")
    
    def draw_face_sets_tools(self, layout, context):
        layout.label(text="Face Sets")
        
        # Basic face sets operations
        box = layout.box()
        box.label(text="Create & Edit")
        
        row = box.row(align=True)
        row.operator("sculpt.face_sets_create", text="From Visible").mode = 'VISIBLE'
        row.operator("sculpt.face_sets_create", text="From Masked").mode = 'MASKED'
        
        row = box.row(align=True)
        row.operator("sculpt.face_set_box_gesture", text="Box Face Set").mode = 'VALUE'
        row.operator("sculpt.face_set_lasso_gesture", text="Lasso Face Set").mode = 'VALUE'
        
        # Face set visibility
        box = layout.box()
        box.label(text="Visibility")
        
        row = box.row(align=True)
        row.operator("sculpt.face_sets_toggle_visibility", text="Toggle Visibility")
        row.operator("sculpt.face_sets_visibility_all", text="Show All").mode = 'SHOW'
    
    def draw_multires_tools(self, layout, context):
        layout.label(text="Multires Tools")
        
        # Basic multires operations
        box = layout.box()
        box.label(text="Subdivide")
        
        row = box.row(align=True)
        row.operator("object.multires_subdivide", text="Subdivide")
        row.operator("object.multires_higher_levels_delete", text="Delete Higher")
        
        # Level control (from your existing menu)
        layout.separator()
        layout.operator('dh.set_multires_viewport_max', text="Set Multires Max")
        layout.operator('dh.set_multires_viewport_zero', text="Set Multires Min")
        
        # Apply and bake
        box = layout.box()
        box.label(text="Apply & Bake")
        
        row = box.row(align=True)
        row.operator("object.multires_reshape", text="Reshape")
        row.operator("object.multires_base_apply", text="Apply Base")
    
    def draw_display_options(self, layout, context):
        layout.label(text="Display Options")
        
        # Viewport display options
        box = layout.box()
        box.label(text="Viewport")
        
        # Matcap and lighting
        row = box.row(align=True)
        row.operator("sculpt.toggle_matcap", text="Toggle Matcap")
        row.operator("sculpt.toggle_cavity", text="Toggle Cavity")
        
        # Face orientation and wireframe
        row = box.row(align=True)
        row.operator("sculpt.toggle_face_orientation", text="Face Orientation")
        
        # Wireframe toggle from main menu
        layout.separator()
        layout.operator('dh.toggle_wireframe', text='Wireframe Override')
        
        # Additional display utilities from main menu
        layout.separator()
        layout.operator('dh.toggle_visibility_outliner', text='Unhide Outliner Selection')
        layout.operator('dh.switch_to_shader_editor', text='Shader Editor')