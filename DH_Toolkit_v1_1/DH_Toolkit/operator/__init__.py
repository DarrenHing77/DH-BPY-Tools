import bpy

from .DCC_Import import DH_OP_dcc_import
from .simple_decimate import DH_OP_Decimate
from .color_picker import SetDiffuseColorOperator
from .open_proj_dir import DH_OP_Open_Proj_Dir
from .DCC_Export import DH_OP_dcc_export
from .mask_tools import DH_OP_MaskExtract

classes = (DH_OP_dcc_import, DH_OP_Decimate,SetDiffuseColorOperator,DH_OP_Open_Proj_Dir,
           DH_OP_dcc_export, DH_OP_MaskExtract
           )

def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
        