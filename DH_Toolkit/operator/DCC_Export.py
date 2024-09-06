import bpy

class DH_OP_dcc_export(bpy.types.Operator):
    
    ## imports objects from temp folder from other DCC's
    
    bl_idname = "dh.dcc_exporter"
    bl_label = "DCC_Import"
    bl_options = {'REGISTER', 'UNDO'}
    
   
    
    
    
    def draw(self,context):
        
        layout =  self.layout
       # layout.operator_context = 'INVOKE DEFAULT'
        layout.label(text ="DCC Exporter")
        
        layout.operator(DH_OP_dcc_import.bl_idname, text="Dialog Operator")
       


    
    
    def execute(self, context):
        directory = 'C:\\temp\\exported.obj'
        bpy.ops.export_scene.fbx(filepath = directory, use_selection=True)
        return {'FINISHED'}