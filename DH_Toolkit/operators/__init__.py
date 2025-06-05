import bpy

# operator classes
from .DCC_Import import DH_OP_dcc_import
from .simple_decimate import DH_OP_Decimate
from .color_picker import SetDiffuseColorOperator
from .open_proj_dir import DH_OP_Open_Proj_Dir
from .DCC_Export import DH_OP_dcc_export
from .mask_tools import DH_OP_MaskExtract
from .export_fbx_multi import DH_OP_dcc_split_export
from .project_manager import DH_OP_CreateProjectDirectories, DH_OP_Proj_Manage, DH_OP_Project_Manager_Popup
from .multires_tools import SetMultiresViewportLevelsMax, SetMultiresViewportLevelsZero
from .modifier_tools import DH_OP_CopyModifiers, DH_OP_toggle_modifiers_visibility
from .transform_utils import DH_OP_ResetTransforms
from .display_utils import DH_OP_ToggleWireframe, DH_OT_ToggleVisibilityOutliner, DH_OP_toggle_lock_camera, DH_OP_SwitchToShaderEditor
from .utils import DH_OT_smart_hide



# classes tuple
classes = (
    DH_OP_dcc_import, 
    DH_OP_Decimate,
    SetDiffuseColorOperator,
    DH_OP_CopyModifiers,
    DH_OP_ResetTransforms,
    DH_OP_Open_Proj_Dir,
    DH_OP_dcc_export,
    DH_OP_MaskExtract,
    DH_OP_dcc_split_export, 
    SetMultiresViewportLevelsMax,
    SetMultiresViewportLevelsZero,
    DH_OP_CreateProjectDirectories,
    DH_OP_Proj_Manage, 
    DH_OP_Project_Manager_Popup,
    DH_OP_ToggleWireframe,
    DH_OT_ToggleVisibilityOutliner,
    DH_OP_toggle_lock_camera,
    DH_OP_SwitchToShaderEditor,
    DH_OT_smart_hide,
    DH_OP_toggle_modifiers_visibility,
    
    
    
)

# Registering the operators
def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

# Unregistering the operators
def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

