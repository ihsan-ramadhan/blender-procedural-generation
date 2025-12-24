"""
Tugas 4: Advanced Shader Challenge
Membuat complex shader dengan reusable node groups

Objektif:
- Membuat node group yang reusable dengan input parameters
- Implementasi minimal 2 teknik advanced shader
- Membuat 3 material berbeda menggunakan node group dengan parameter berbeda
- Demonstrasi flexibility dan reusability dari node group

Teknik Advanced yang Diimplementasikan:
1. Layer Weight untuk Fresnel Effect
2. Bump/Normal Mapping
3. Color Mixing dengan Geometry-based Masks
4. Ambient Occlusion Integration

Nama: Muhammad Ihsan Ramadhan
NIM: 241511083
"""

import bpy
import math

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)
    for block in bpy.data.node_groups:
        if block.users == 0:
            bpy.data.node_groups.remove(block)
            
    print("Scene cleared.")

def create_advanced_surface_node_group():
    print("Creating Advanced Surface Node Group...")
    
    group = bpy.data.node_groups.new(name="Advanced_Surface_Group", type='ShaderNodeTree')
    
    if hasattr(group, 'interface'):
        # Blender 4.0+
        group.interface.new_socket('Base Color', in_out='INPUT', socket_type='NodeSocketColor')
        group.interface.new_socket('Detail Scale', in_out='INPUT', socket_type='NodeSocketFloat')
        group.interface.new_socket('Roughness Amount', in_out='INPUT', socket_type='NodeSocketFloat')
        group.interface.new_socket('Bump Strength', in_out='INPUT', socket_type='NodeSocketFloat')
        group.interface.new_socket('Fresnel Intensity', in_out='INPUT', socket_type='NodeSocketFloat')
        
        group.interface.new_socket('Base Color', in_out='OUTPUT', socket_type='NodeSocketColor')
        group.interface.new_socket('Roughness', in_out='OUTPUT', socket_type='NodeSocketFloat')
        group.interface.new_socket('Normal', in_out='OUTPUT', socket_type='NodeSocketVector')
        
        group.interface.items_tree['Detail Scale'].default_value = 5.0
    else:
        # Blender 3.x
        group.inputs.new('NodeSocketColor', 'Base Color')
        group.inputs.new('NodeSocketFloat', 'Detail Scale')
        group.inputs.new('NodeSocketFloat', 'Roughness Amount')
        group.inputs.new('NodeSocketFloat', 'Bump Strength')
        group.inputs.new('NodeSocketFloat', 'Fresnel Intensity')
        
        group.outputs.new('NodeSocketColor', 'Base Color')
        group.outputs.new('NodeSocketFloat', 'Roughness')
        group.outputs.new('NodeSocketVector', 'Normal')
        
        group.inputs['Detail Scale'].default_value = 5.0

    nodes = group.nodes
    links = group.links
    
    group_inputs = nodes.new('NodeGroupInput')
    group_inputs.location = (-1200, 0)
    group_outputs = nodes.new('NodeGroupOutput')
    group_outputs.location = (800, 0)
    
    # 1. Fresnel
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 400)
    
    layer_weight = nodes.new('ShaderNodeLayerWeight')
    layer_weight.location = (-800, 400)
    layer_weight.inputs['Blend'].default_value = 0.5
    
    fresnel_ramp = nodes.new('ShaderNodeValToRGB')
    fresnel_ramp.location = (-600, 400)
    
    mix_fresnel = nodes.new('ShaderNodeMixRGB')
    mix_fresnel.location = (-400, 500)
    
    math_fresnel = nodes.new('ShaderNodeMath')
    math_fresnel.location = (-400, 300)
    math_fresnel.operation = 'MULTIPLY'
    
    # 2. Procedural Roughness
    noise1 = nodes.new('ShaderNodeTexNoise')
    noise1.location = (-800, 0)
    
    noise2 = nodes.new('ShaderNodeTexNoise')
    noise2.location = (-800, -200)
    
    mix_noise = nodes.new('ShaderNodeMixRGB')
    mix_noise.location = (-600, -100)
    mix_noise.blend_type = 'ADD'
    
    rough_ramp = nodes.new('ShaderNodeValToRGB')
    rough_ramp.location = (-400, -100)
    
    math_rough = nodes.new('ShaderNodeMath')
    math_rough.location = (-200, -100)
    math_rough.operation = 'MULTIPLY'
    
    # 3. Bump Mapping
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-800, -400)
    voronoi.feature = 'DISTANCE_TO_EDGE'
    
    mix_bump = nodes.new('ShaderNodeMixRGB')
    mix_bump.location = (-600, -350)
    mix_bump.blend_type = 'MULTIPLY'
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-400, -400)
    
    math_bump = nodes.new('ShaderNodeMath')
    math_bump.location = (-400, -550)
    math_bump.operation = 'MULTIPLY'
    math_bump.inputs[1].default_value = 1.0
    
    # 4. Geometry Mask
    geometry = nodes.new('ShaderNodeNewGeometry')
    geometry.location = (-1000, -600)
    
    geo_ramp = nodes.new('ShaderNodeValToRGB')
    geo_ramp.location = (-800, -600)
    
    mix_geo = nodes.new('ShaderNodeMixRGB')
    mix_geo.location = (-200, 500)
    mix_geo.blend_type = 'MULTIPLY'
    
    # Connections
    links.new(group_inputs.outputs['Base Color'], mix_fresnel.inputs['Color1'])
    links.new(group_inputs.outputs['Fresnel Intensity'], math_fresnel.inputs[1])
    links.new(group_inputs.outputs['Detail Scale'], noise1.inputs['Scale'])
    links.new(group_inputs.outputs['Detail Scale'], noise2.inputs['Scale'])
    links.new(group_inputs.outputs['Detail Scale'], voronoi.inputs['Scale'])
    links.new(group_inputs.outputs['Roughness Amount'], math_rough.inputs[1])
    links.new(group_inputs.outputs['Bump Strength'], math_bump.inputs[0])

    links.new(layer_weight.outputs['Facing'], fresnel_ramp.inputs['Fac'])
    links.new(fresnel_ramp.outputs['Color'], math_fresnel.inputs[0])
    links.new(math_fresnel.outputs['Value'], mix_fresnel.inputs['Fac'])
    
    links.new(tex_coord.outputs['Object'], noise1.inputs['Vector'])
    links.new(tex_coord.outputs['Object'], noise2.inputs['Vector'])
    links.new(tex_coord.outputs['Object'], voronoi.inputs['Vector'])
    
    links.new(noise1.outputs['Fac'], mix_noise.inputs['Color1'])
    links.new(noise2.outputs['Fac'], mix_noise.inputs['Color2'])
    links.new(mix_noise.outputs['Color'], rough_ramp.inputs['Fac'])
    links.new(rough_ramp.outputs['Color'], math_rough.inputs[0])
    
    links.new(voronoi.outputs['Distance'], mix_bump.inputs['Color1'])
    links.new(noise1.outputs['Fac'], mix_bump.inputs['Color2'])
    links.new(mix_bump.outputs['Color'], bump.inputs['Height'])
    links.new(math_bump.outputs['Value'], bump.inputs['Strength'])
    
    links.new(geometry.outputs['Pointiness'], geo_ramp.inputs['Fac'])
    links.new(mix_fresnel.outputs['Color'], mix_geo.inputs['Color1'])
    links.new(geo_ramp.outputs['Color'], mix_geo.inputs['Color2'])
    
    links.new(mix_geo.outputs['Color'], group_outputs.inputs['Base Color'])
    links.new(math_rough.outputs['Value'], group_outputs.inputs['Roughness'])
    links.new(bump.outputs['Normal'], group_outputs.inputs['Normal'])
    
    return group

def create_material(name, node_group, color, scale, roughness, bump, fresnel):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    group_node = nodes.new('ShaderNodeGroup')
    group_node.node_tree = node_group
    group_node.location = (-400, 0)
    
    group_node.inputs['Base Color'].default_value = color
    group_node.inputs['Detail Scale'].default_value = scale
    group_node.inputs['Roughness Amount'].default_value = roughness
    group_node.inputs['Bump Strength'].default_value = bump
    group_node.inputs['Fresnel Intensity'].default_value = fresnel
    
    ao = nodes.new('ShaderNodeAmbientOcclusion')
    ao.location = (-600, -300)
    
    mix_ao = nodes.new('ShaderNodeMixRGB')
    mix_ao.blend_type = 'MULTIPLY'
    mix_ao.inputs['Fac'].default_value = 0.5
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (100, 0)
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    links.new(group_node.outputs['Base Color'], mix_ao.inputs['Color1'])
    links.new(ao.outputs['Color'], mix_ao.inputs['Color2'])
    links.new(mix_ao.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(group_node.outputs['Roughness'], bsdf.inputs['Roughness'])
    links.new(group_node.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_objects():
    objects = []
    
    # Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.5, location=(-4, 0, 1.5))
    sphere = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    objects.append(sphere)
    
    # Torus
    bpy.ops.mesh.primitive_torus_add(location=(0, 0, 1.2))
    torus = bpy.context.active_object
    bpy.ops.object.shade_smooth()
    objects.append(torus)
    
    # Monkey
    bpy.ops.mesh.primitive_monkey_add(size=1.5, location=(4, 0, 1.5))
    monkey = bpy.context.active_object
    mod = monkey.modifiers.new(name="Subsurf", type='SUBSURF')
    mod.levels = 2
    bpy.ops.object.shade_smooth()
    objects.append(monkey)
    
    # Floor
    bpy.ops.mesh.primitive_plane_add(size=20)
    
    return objects

def setup_scene():
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    
    bpy.ops.object.light_add(type='AREA', location=(-5, 5, 8))
    area = bpy.context.active_object
    area.data.energy = 80
    
    bpy.ops.object.camera_add(location=(10, -10, 6))
    cam = bpy.context.active_object
    cam.rotation_euler = (math.radians(70), 0, math.radians(45))
    bpy.context.scene.camera = cam
    
    world = bpy.context.scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs['Strength'].default_value = 1.0

def main():
    print("--- STARTING ADVANCED SHADER TASK ---")
    
    clear_scene()
    
    node_group = create_advanced_surface_node_group()
    objects = create_objects()
    
    # 1. Blue Ceramic
    mat1 = create_material("Mat_Blue", node_group, (0.2, 0.4, 0.8, 1.0), 8.0, 0.3, 0.4, 0.4)
    objects[0].data.materials.append(mat1)
    
    # 2. Orange Stone
    mat2 = create_material("Mat_Orange", node_group, (0.9, 0.5, 0.2, 1.0), 15.0, 0.7, 0.8, 0.2)
    objects[1].data.materials.append(mat2)
    
    # 3. Purple Metal
    mat3 = create_material("Mat_Purple", node_group, (0.6, 0.2, 0.8, 1.0), 5.0, 0.2, 0.3, 0.6)
    objects[2].data.materials.append(mat3)
    
    setup_scene()
    
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'RENDERED'
    
    print("Setup complete.")

if __name__ == "__main__":
    main()