"""
Tugas 1: Material Library
Membuat 5 material berbeda dengan karakteristik unik
- 1 material logam (Copper)
- 1 material fabric (Denim)
- 1 material organik (Bark/Kulit Pohon)
- 1 material transparent (Jade)
- 1 material emisif (Neon Glow)

Nama: Muhammad Ihsan Ramadhan
NIM: 241511083
"""

import bpy
import math

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    for material in bpy.data.materials:
        if not material.users:
            bpy.data.materials.remove(material)
    
    print("Scene cleared.")

def create_copper_material(name="Copper_Metal"):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, 200)
    noise.inputs['Scale'].default_value = 15.0
    noise.inputs['Detail'].default_value = 8.0
    noise.inputs['Roughness'].default_value = 0.6
    
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-400, 200)
    colorramp.color_ramp.elements[0].color = (0.722, 0.451, 0.200, 1.0)
    colorramp.color_ramp.elements[1].color = (0.955, 0.637, 0.538, 1.0)
    
    noise2 = nodes.new('ShaderNodeTexNoise')
    noise2.location = (-600, -200)
    noise2.inputs['Scale'].default_value = 25.0
    
    colorramp2 = nodes.new('ShaderNodeValToRGB')
    colorramp2.location = (-400, -200)
    colorramp2.color_ramp.elements[0].position = 0.4
    colorramp2.color_ramp.elements[1].position = 0.7
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    bsdf.inputs['Metallic'].default_value = 1.0
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (300, 0)
    
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(tex_coord.outputs['Object'], noise2.inputs['Vector'])
    links.new(noise2.outputs['Fac'], colorramp2.inputs['Fac'])
    links.new(colorramp2.outputs['Color'], bsdf.inputs['Roughness'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_denim_material(name="Denim_Fabric"):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-800, 0)
    mapping.inputs['Scale'].default_value = (20.0, 20.0, 20.0)
    
    wave = nodes.new('ShaderNodeTexWave')
    wave.location = (-600, 200)
    wave.inputs['Scale'].default_value = 30.0
    wave.inputs['Distortion'].default_value = 1.0
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, -100)
    noise.inputs['Scale'].default_value = 50.0
    
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (-400, 100)
    mix.blend_type = 'MULTIPLY'
    mix.inputs['Fac'].default_value = 1.0
    
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-200, 100)
    colorramp.color_ramp.elements[0].color = (0.05, 0.08, 0.15, 1.0)
    colorramp.color_ramp.elements[1].color = (0.15, 0.25, 0.45, 1.0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (100, 0)
    bsdf.inputs['Roughness'].default_value = 0.8
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], wave.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(wave.outputs['Color'], mix.inputs['Color1'])
    links.new(noise.outputs['Fac'], mix.inputs['Color2'])
    links.new(mix.outputs['Color'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_bark_material(name="Tree_Bark"):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-800, 0)
    mapping.inputs['Scale'].default_value = (3.0, 3.0, 3.0)
    
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-600, 300)
    voronoi.feature = 'DISTANCE_TO_EDGE'
    voronoi.inputs['Scale'].default_value = 8.0
    
    noise1 = nodes.new('ShaderNodeTexNoise')
    noise1.location = (-600, 0)
    noise1.inputs['Scale'].default_value = 5.0
    noise1.inputs['Detail'].default_value = 15.0
    
    noise2 = nodes.new('ShaderNodeTexNoise')
    noise2.location = (-600, -300)
    noise2.inputs['Scale'].default_value = 20.0
    
    mix1 = nodes.new('ShaderNodeMixRGB')
    mix1.location = (-400, 200)
    mix1.blend_type = 'MULTIPLY'
    mix1.inputs['Fac'].default_value = 0.7
    
    mix2 = nodes.new('ShaderNodeMixRGB')
    mix2.location = (-200, 100)
    mix2.blend_type = 'ADD'
    mix2.inputs['Fac'].default_value = 0.3
    
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (0, 100)
    colorramp.color_ramp.elements[0].color = (0.15, 0.10, 0.05, 1.0)
    colorramp.color_ramp.elements[1].color = (0.35, 0.25, 0.15, 1.0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (300, 0)
    bsdf.inputs['Roughness'].default_value = 0.9
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (100, -200)
    bump.inputs['Strength'].default_value = 0.5
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (600, 0)
    
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], voronoi.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise1.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise2.inputs['Vector'])
    links.new(voronoi.outputs['Distance'], mix1.inputs['Color1'])
    links.new(noise1.outputs['Fac'], mix1.inputs['Color2'])
    links.new(mix1.outputs['Color'], mix2.inputs['Color1'])
    links.new(noise2.outputs['Fac'], mix2.inputs['Color2'])
    links.new(mix2.outputs['Color'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(noise1.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_jade_material(name="Jade_Stone"):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, 200)
    noise.inputs['Scale'].default_value = 10.0
    
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-400, 200)
    colorramp.color_ramp.elements[0].color = (0.05, 0.3, 0.2, 1.0)
    colorramp.color_ramp.elements[1].color = (0.2, 0.7, 0.5, 1.0)
    
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-600, -100)
    
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (-200, 100)
    mix.inputs['Fac'].default_value = 0.3
    
    layer_weight = nodes.new('ShaderNodeLayerWeight')
    layer_weight.location = (-400, -300)
    layer_weight.inputs['Blend'].default_value = 0.5
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (100, 0)
    bsdf.inputs['Roughness'].default_value = 0.1
    bsdf.inputs['IOR'].default_value = 1.55
    
    # Handle transmission input name for Blender 3.x and 4.x
    transmission_input = 'Transmission Weight' if 'Transmission Weight' in bsdf.inputs else 'Transmission'
    bsdf.inputs[transmission_input].default_value = 0.6
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    mat.blend_method = 'BLEND'
    
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(tex_coord.outputs['Object'], voronoi.inputs['Vector'])
    links.new(colorramp.outputs['Color'], mix.inputs['Color1'])
    links.new(voronoi.outputs['Distance'], mix.inputs['Color2'])
    links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(layer_weight.outputs['Facing'], bsdf.inputs['Roughness'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_neon_material(name="Neon_Glow"):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-800, 0)
    
    wave = nodes.new('ShaderNodeTexWave')
    wave.location = (-600, 200)
    wave.wave_type = 'BANDS'
    wave.inputs['Scale'].default_value = 5.0
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, -100)
    noise.inputs['Scale'].default_value = 15.0
    
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (-400, 100)
    mix.blend_type = 'ADD'
    
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-200, 100)
    
    rgb_color = nodes.new('ShaderNodeRGB')
    rgb_color.location = (-200, 300)
    rgb_color.outputs[0].default_value = (0.0, 1.0, 0.8, 1.0)
    
    emission = nodes.new('ShaderNodeEmission')
    emission.location = (100, 0)
    emission.inputs['Strength'].default_value = 15.0
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], wave.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(wave.outputs['Color'], mix.inputs['Color1'])
    links.new(noise.outputs['Fac'], mix.inputs['Color2'])
    links.new(mix.outputs['Color'], colorramp.inputs['Fac'])
    links.new(rgb_color.outputs['Color'], emission.inputs['Color'])
    links.new(colorramp.outputs['Color'], emission.inputs['Strength'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    return mat

def create_objects_with_materials():
    objects_info = []
    
    # 1. Copper Sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.2, location=(-5, 0, 1.2), segments=64, ring_count=32)
    sphere = bpy.context.active_object
    sphere.name = "Copper_Sphere"
    copper_mat = create_copper_material()
    sphere.data.materials.append(copper_mat)
    objects_info.append(("Sphere", copper_mat.name))
    
    # 2. Denim Cube
    bpy.ops.mesh.primitive_cube_add(size=2, location=(-2.5, 0, 1))
    cube = bpy.context.active_object
    cube.name = "Denim_Cube"
    denim_mat = create_denim_material()
    cube.data.materials.append(denim_mat)
    objects_info.append(("Cube", denim_mat.name))
    
    # 3. Bark Cylinder
    bpy.ops.mesh.primitive_cylinder_add(radius=0.8, depth=2.5, location=(0, 0, 1.25))
    cylinder = bpy.context.active_object
    cylinder.name = "Bark_Cylinder"
    bark_mat = create_bark_material()
    cylinder.data.materials.append(bark_mat)
    objects_info.append(("Cylinder", bark_mat.name))
    
    # 4. Jade Torus
    bpy.ops.mesh.primitive_torus_add(major_radius=1, minor_radius=0.4, location=(2.5, 0, 1))
    torus = bpy.context.active_object
    torus.name = "Jade_Torus"
    jade_mat = create_jade_material()
    torus.data.materials.append(jade_mat)
    objects_info.append(("Torus", jade_mat.name))
    
    # 5. Neon Suzanne
    bpy.ops.mesh.primitive_monkey_add(size=1.2, location=(5, 0, 1.2))
    monkey = bpy.context.active_object
    monkey.name = "Neon_Suzanne"
    neon_mat = create_neon_material()
    monkey.data.materials.append(neon_mat)
    objects_info.append(("Suzanne", neon_mat.name))
    
    print("Objects created.")
    return objects_info

def setup_lighting():
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(45), 0, math.radians(45))
    
    bpy.ops.object.light_add(type='AREA', location=(-3, -5, 5))
    area = bpy.context.active_object
    area.data.energy = 100
    area.data.size = 3
    area.rotation_euler = (math.radians(60), 0, math.radians(-30))
    
    print("Lighting setup complete.")

def setup_camera():
    bpy.ops.object.camera_add(location=(0, -12, 5))
    camera = bpy.context.active_object
    camera.rotation_euler = (math.radians(75), 0, 0)
    bpy.context.scene.camera = camera
    print("Camera setup complete.")

def setup_render():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128
    scene.cycles.use_denoising = True
    scene.display.shading.light = 'STUDIO'

def main():
    print("--- STARTING TUGAS 1 ---")
    
    clear_scene()
    create_objects_with_materials()
    setup_lighting()
    setup_camera()
    setup_render()
    
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    break
    
    print("--- EXECUTION COMPLETE ---")

if __name__ == "__main__":
    main()