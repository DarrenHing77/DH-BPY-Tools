import bpy
import os
import re

class DH_OP_BuildShader(bpy.types.Operator):
    bl_idname = "dh.build_shader"
    bl_label = "Build Shader From Textures"
    bl_options = {'REGISTER', 'UNDO'}

    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if not self.directory:
            self.report({'ERROR'}, "No directory selected. Try clicking buttons that actually matter next time.")
            return {'CANCELLED'}
        
        self.build_shader(context)
        return {'FINISHED'}

    def extract_token(self, name):
        # We're slicing that damn mesh name into something useful
        token = name.split('_')[0]
        token = re.sub(r'\d+$', '', token)
        return token.lower()

    def build_shader(self, context):
        obj = context.active_object
        if not obj or not obj.data or not hasattr(obj.data, 'materials'):
            self.report({'ERROR'}, "Select a goddamn mesh object first.")
            return

        search_token = self.extract_token(obj.name)
        print(f"Matching token: {search_token}")

        # We wipe the old nodes like a totalitarian regime
        mat = bpy.data.materials.new(name="AutoShader")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = (400, 0)

        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        links.new(bsdf.outputs['BSDF'], output_node.inputs['Surface'])

        # Priority order matters, don't screw with it
        texture_map = [
            ("orm", "ORM", "Non-Color"),
            ("basecolor", "Base Color", "sRGB"),
            ("diffusecolor", "Base Color", "sRGB"),
            ("normal", "Normal", "Non-Color"),
        ]

        matched = False

        for file in os.listdir(self.directory):
            filepath = os.path.join(self.directory, file)
            file_lower = file.lower()

            if search_token not in file_lower:
                continue

            for key, input_name, colorspace in texture_map:
                # Use word boundaries so we don't accidentally match substrings inside others
                if re.search(rf"\b{key}\b", file_lower):
                    matched = True
                    print(f"Matched {key} to {file}")
                    image = bpy.data.images.load(filepath)

                    tex_node = nodes.new(type='ShaderNodeTexImage')
                    tex_node.image = image
                    tex_node.location = (-400, 0)
                    tex_node.image.colorspace_settings.name = colorspace

                    if input_name == "Base Color":
                        links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])

                    elif input_name == "Normal":
                        normal_map = nodes.new(type='ShaderNodeNormalMap')
                        normal_map.location = (-200, -300)
                        links.new(tex_node.outputs['Color'], normal_map.inputs['Color'])
                        links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])

                    elif input_name == "ORM":
                        separate = nodes.new(type="ShaderNodeSeparateRGB")
                        separate.location = (-200, -600)
                        links.new(tex_node.outputs['Color'], separate.inputs['Image'])
                        links.new(separate.outputs['G'], bsdf.inputs['Roughness'])
                        links.new(separate.outputs['B'], bsdf.inputs['Metallic'])
                    break

        if not matched:
            self.report({'WARNING'}, f"No matching textures found for token '{search_token}'. Maybe check your filenames... or your life choices.")

        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)


