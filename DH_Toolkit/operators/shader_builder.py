import bpy
import os

class DH_OP_BuildShader(bpy.types.Operator):
    bl_idname = "dh.build_shader"
    bl_label = "Build Shader From Selected Textures"
    bl_options = {'REGISTER', 'UNDO'}

    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if not self.files:
            self.report({'ERROR'}, "No files selected.")
            return {'CANCELLED'}

        self.build_shader(context)
        return {'FINISHED'}

    def build_shader(self, context):
        obj = context.active_object
        if not obj or not obj.data or not hasattr(obj.data, 'materials'):
            self.report({'ERROR'}, "Select a goddamn mesh object first.")
            return

        # Create material named after object
        clean_name = self.clean_material_name(obj.name)
        mat = bpy.data.materials.new(name=clean_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)

        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        links.new(bsdf.outputs['BSDF'], output_node.inputs['Surface'])

        texture_keywords = {
            "basecolor": ["basecolor", "albedo", "diffuse"],
            "normal": ["normal", "nrm"],
            "orm": ["occlusionroughnessmetallic", "orm"],
        }

        matched = False

        for file_elem in self.files:
            file = file_elem.name
            filepath = os.path.join(self.directory, file)
            file_lower = file.lower()
            tokens = file_lower.split("_")

            tex_type = None

            for key, keywords in texture_keywords.items():
                if any(kw in tokens for kw in keywords):
                    tex_type = key
                    break

            if not tex_type:
                print(f"Skipping {file} — no matching texture type found.")
                continue

            matched = True
            image = bpy.data.images.load(filepath)
            tex_node = nodes.new(type='ShaderNodeTexImage')
            tex_node.image = image
            tex_node.location = (-400, 0)
            tex_node.image.colorspace_settings.name = "sRGB" if tex_type == "basecolor" else "Non-Color"

            if tex_type == "basecolor":
                links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])

            elif tex_type == "normal":
                normal_map = nodes.new(type='ShaderNodeNormalMap')
                normal_map.location = (-200, -300)
                links.new(tex_node.outputs['Color'], normal_map.inputs['Color'])
                links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])

            elif tex_type == "orm":
                separate = nodes.new(type="ShaderNodeSeparateRGB")
                separate.location = (-200, -600)
                links.new(tex_node.outputs['Color'], separate.inputs['Image'])
                links.new(separate.outputs['G'], bsdf.inputs['Roughness'])
                links.new(separate.outputs['B'], bsdf.inputs['Metallic'])

        if not matched:
            self.report({'WARNING'}, "No matching textures found.")

        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

    def clean_material_name(self, name):
        # Strip suffixes that Blender loves to add when duplicating
        return name.split(".")[0]

