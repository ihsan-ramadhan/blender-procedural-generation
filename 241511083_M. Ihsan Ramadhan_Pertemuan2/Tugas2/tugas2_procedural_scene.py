"""
Tugas 2: Procedural Texture Scene
Tema: Natural - Forest Floor (Lantai Hutan)
Scene menampilkan berbagai elemen alami dengan procedural textures:
- Ground (Tanah), Rocks (Batu), Wood Logs (Kayu), Moss (Lumut), dll

Konsep Scene:
Scene ini merepresentasikan lantai hutan yang natural dengan berbagai elemen organik.
Menggunakan procedural textures untuk menciptakan material tanah berlumut, batu-batu
dengan tekstur alami, kayu lapuk, dan vegetasi sederhana. Displacement digunakan pada
ground untuk detail geometri terrain yang realistis.

Nama: Muhammad Ihsan Ramadhan
NIM: 241511083
"""

import bpy
import math
import random

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    for material in bpy.data.materials:
        if not material.users:
            bpy.data.materials.remove(material)
    print("Scene cleared.")

def create_forest_ground_material(name="Forest_Ground"):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1200, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-1000, 0)
    mapping.inputs['Scale'].default_value = (5.0, 5.0, 5.0)
    
    noise1 = nodes.new('ShaderNodeTexNoise')
    noise1.location = (-800, 300)
    noise1.inputs['Scale'].default_value = 8.0
    noise1.inputs['Detail'].default_value = 15.0
    
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-800, 0)
    voronoi.inputs['Scale'].default_value = 12.0
    
    noise2 = nodes.new('ShaderNodeTexNoise')
    noise2.location = (-800, -300)
    noise2.inputs['Scale'].default_value = 25.0
    
    mix1 = nodes.new('ShaderNodeMixRGB')
    mix1.location = (-600, 200)
    mix1.blend_type = 'MULTIPLY'
    mix1.inputs['Fac'].default_value = 0.5
    
    mix2 = nodes.new('ShaderNodeMixRGB')
    mix2.location = (-400, 100)
    mix2.blend_type = 'ADD'
    
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-200, 100)
    colorramp.color_ramp.elements[0].color = (0.15, 0.10, 0.05, 1.0)
    colorramp.color_ramp.elements[1].color = (0.25, 0.18, 0.10, 1.0)
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (0, -200)
    bump.inputs['Strength'].default_value = 0.3
    
    displacement = nodes.new('ShaderNodeDisplacement')
    displacement.location = (200, -400)
    displacement.inputs['Scale'].default_value = 0.15
    displacement.inputs['Midlevel'].default_value = 0.5
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Roughness'].default_value = 0.9
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (500, 0)
    
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise1.inputs['Vector'])
    links.new(mapping.outputs['Vector'], voronoi.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise2.inputs['Vector'])
    links.new(noise1.outputs['Fac'], mix1.inputs['Color1'])
    links.new(voronoi.outputs['Distance'], mix1.inputs['Color2'])
    links.new(mix1.outputs['Color'], mix2.inputs['Color1'])
    links.new(noise2.outputs['Fac'], mix2.inputs['Color2'])
    links.new(mix2.outputs['Color'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(mix2.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(mix2.outputs['Color'], displacement.inputs['Height'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    links.new(displacement.outputs['Displacement'], output.inputs['Displacement'])
    
    return mat

def create_mossy_rock_material(name="Mossy_Rock"):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-800, 300)
    voronoi.feature = 'DISTANCE_TO_EDGE'
    voronoi.inputs['Scale'].default_value = 5.0
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-800, 0)
    noise.inputs['Detail'].default_value = 15.0
    
    magic = nodes.new('ShaderNodeTexMagic')
    magic.location = (-800, -300)
    magic.inputs['Scale'].default_value = 8.0
    magic.inputs['Distortion'].default_value = 2.0
    
    colorramp_moss = nodes.new('ShaderNodeValToRGB')
    colorramp_moss.location = (-600, -300)
    colorramp_moss.color_ramp.elements[0].position = 0.4
    colorramp_moss.color_ramp.elements[1].position = 0.6
    
    rock_color = nodes.new('ShaderNodeRGB')
    rock_color.location = (-400, 400)
    rock_color.outputs[0].default_value = (0.3, 0.3, 0.35, 1.0)
    
    moss_color = nodes.new('ShaderNodeRGB')
    moss_color.location = (-400, 200)
    moss_color.outputs[0].default_value = (0.1, 0.3, 0.15, 1.0)
    
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (-200, 300)
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (0, -100)
    bump.inputs['Strength'].default_value = 0.5
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Roughness'].default_value = 0.85
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (500, 0)
    
    links.new(tex_coord.outputs['Object'], voronoi.inputs['Vector'])
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(tex_coord.outputs['Object'], magic.inputs['Vector'])
    links.new(magic.outputs['Fac'], colorramp_moss.inputs['Fac'])
    links.new(rock_color.outputs['Color'], mix.inputs['Color1'])
    links.new(moss_color.outputs['Color'], mix.inputs['Color2'])
    links.new(colorramp_moss.outputs['Color'], mix.inputs['Fac'])
    links.new(mix.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_old_wood_material(name="Old_Wood_Log"):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    
    mapping = nodes.new('ShaderNodeMapping')
    mapping.location = (-800, 0)
    mapping.inputs['Scale'].default_value = (1.0, 1.0, 15.0)
    mapping.inputs['Rotation'].default_value = (0, 0, math.radians(90))
    
    wave = nodes.new('ShaderNodeTexWave')
    wave.location = (-600, 200)
    wave.wave_type = 'RINGS'
    wave.rings_direction = 'Z'
    wave.inputs['Scale'].default_value = 12.0
    wave.inputs['Distortion'].default_value = 2.5
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, -100)
    noise.inputs['Scale'].default_value = 25.0
    
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (-400, 100)
    mix.blend_type = 'MULTIPLY'
    mix.inputs['Fac'].default_value = 0.8
    
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-200, 100)
    colorramp.color_ramp.elements[0].color = (0.25, 0.18, 0.10, 1.0)
    colorramp.color_ramp.elements[1].color = (0.45, 0.35, 0.22, 1.0)
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (0, -150)
    bump.inputs['Strength'].default_value = 0.4
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    bsdf.inputs['Roughness'].default_value = 0.7
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (500, 0)
    
    links.new(tex_coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], wave.inputs['Vector'])
    links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
    links.new(wave.outputs['Color'], mix.inputs['Color1'])
    links.new(noise.outputs['Fac'], mix.inputs['Color2'])
    links.new(mix.outputs['Color'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(mix.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_moss_carpet_material(name="Moss_Carpet"):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-900, 0)
    
    noise1 = nodes.new('ShaderNodeTexNoise')
    noise1.location = (-700, 200)
    noise1.inputs['Scale'].default_value = 30.0
    
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-700, -100)
    voronoi.inputs['Scale'].default_value = 20.0
    
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (-500, 100)
    mix.blend_type = 'ADD'
    
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-300, 100)
    colorramp.color_ramp.elements[0].color = (0.05, 0.20, 0.08, 1.0)
    colorramp.color_ramp.elements[1].color = (0.15, 0.40, 0.18, 1.0)
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-100, -100)
    bump.inputs['Strength'].default_value = 0.2
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (100, 0)
    bsdf.inputs['Roughness'].default_value = 0.95
    
    output = nodes.new('ShaderNodeOutputMaterial')
    output.location = (400, 0)
    
    links.new(tex_coord.outputs['Object'], noise1.inputs['Vector'])
    links.new(tex_coord.outputs['Object'], voronoi.inputs['Vector'])
    links.new(noise1.outputs['Fac'], mix.inputs['Color1'])
    links.new(voronoi.outputs['Distance'], mix.inputs['Color2'])
    links.new(mix.outputs['Color'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(mix.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_pebbles_material(name="Small_Pebbles"):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-600, 200)
    voronoi.inputs['Scale'].default_value = 15.0
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, -100)
    noise.inputs['Scale'].default_value = 20.0
    
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-400, 200)
    colorramp.color_ramp.elements[0].color = (0.35, 0.35, 0.38, 1.0)
    colorramp.color_ramp.elements[1].color = (0.55, 0.55, 0.58, 1.0)
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (-200, -100)
    bump.inputs['Strength'].default_value = 0.6
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    
    output = nodes.new('ShaderNodeOutputMaterial')
    
    links.new(tex_coord.outputs['Object'], voronoi.inputs['Vector'])
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(voronoi.outputs['Distance'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_tree_bark_material(name="Rough_Bark"):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)
    
    wave = nodes.new('ShaderNodeTexWave')
    wave.location = (-800, 300)
    wave.wave_type = 'BANDS'
    wave.bands_direction = 'Y'
    wave.inputs['Scale'].default_value = 8.0
    wave.inputs['Distortion'].default_value = 3.0
    
    voronoi = nodes.new('ShaderNodeTexVoronoi')
    voronoi.location = (-800, 0)
    voronoi.feature = 'DISTANCE_TO_EDGE'
    voronoi.inputs['Scale'].default_value = 6.0
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-800, -300)
    
    mix1 = nodes.new('ShaderNodeMixRGB')
    mix1.location = (-600, 200)
    mix1.blend_type = 'MULTIPLY'
    
    mix2 = nodes.new('ShaderNodeMixRGB')
    mix2.location = (-400, 100)
    mix2.blend_type = 'ADD'
    
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-200, 100)
    colorramp.color_ramp.elements[0].color = (0.18, 0.12, 0.08, 1.0)
    colorramp.color_ramp.elements[1].color = (0.32, 0.22, 0.15, 1.0)
    
    bump = nodes.new('ShaderNodeBump')
    bump.location = (0, -150)
    bump.inputs['Strength'].default_value = 0.7
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    
    output = nodes.new('ShaderNodeOutputMaterial')
    
    links.new(tex_coord.outputs['Object'], wave.inputs['Vector'])
    links.new(tex_coord.outputs['Object'], voronoi.inputs['Vector'])
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(wave.outputs['Color'], mix1.inputs['Color1'])
    links.new(voronoi.outputs['Distance'], mix1.inputs['Color2'])
    links.new(mix1.outputs['Color'], mix2.inputs['Color1'])
    links.new(noise.outputs['Fac'], mix2.inputs['Color2'])
    links.new(mix2.outputs['Color'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(mix2.outputs['Color'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_wet_leaves_material(name="Wet_Leaves"):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    
    magic = nodes.new('ShaderNodeTexMagic')
    magic.location = (-700, 200)
    magic.inputs['Scale'].default_value = 12.0
    magic.inputs['Distortion'].default_value = 3.0
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-700, -100)
    
    colorramp = nodes.new('ShaderNodeValToRGB')
    colorramp.location = (-500, 200)
    colorramp.color_ramp.elements[0].color = (0.15, 0.08, 0.02, 1.0)
    colorramp.color_ramp.elements[1].color = (0.35, 0.25, 0.08, 1.0)
    
    colorramp2 = nodes.new('ShaderNodeValToRGB')
    colorramp2.location = (-500, -100)
    colorramp2.color_ramp.elements[0].color = (0.2, 0.2, 0.2, 1.0)
    colorramp2.color_ramp.elements[1].color = (0.6, 0.6, 0.6, 1.0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (-200, 0)
    
    output = nodes.new('ShaderNodeOutputMaterial')
    
    links.new(tex_coord.outputs['Object'], magic.inputs['Vector'])
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(magic.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(noise.outputs['Fac'], colorramp2.inputs['Fac'])
    links.new(colorramp.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(colorramp2.outputs['Color'], bsdf.inputs['Roughness'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_mushroom_material(name="Forest_Mushroom"):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    
    checker = nodes.new('ShaderNodeTexChecker')
    checker.location = (-600, 200)
    checker.inputs['Scale'].default_value = 8.0
    
    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-600, -100)
    
    mix = nodes.new('ShaderNodeMixRGB')
    mix.location = (-400, 100)
    
    color1 = nodes.new('ShaderNodeRGB')
    color1.outputs[0].default_value = (0.6, 0.1, 0.05, 1.0)
    
    color2 = nodes.new('ShaderNodeRGB')
    color2.outputs[0].default_value = (0.9, 0.85, 0.8, 1.0)
    
    mix_color = nodes.new('ShaderNodeMixRGB')
    mix_color.location = (-200, 300)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    output = nodes.new('ShaderNodeOutputMaterial')
    
    links.new(tex_coord.outputs['Object'], checker.inputs['Vector'])
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])
    links.new(checker.outputs['Color'], mix.inputs['Color1'])
    links.new(noise.outputs['Fac'], mix.inputs['Color2'])
    links.new(color1.outputs['Color'], mix_color.inputs['Color1'])
    links.new(color2.outputs['Color'], mix_color.inputs['Color2'])
    links.new(mix.outputs['Color'], mix_color.inputs['Fac'])
    links.new(mix_color.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def create_scene_objects():
    print("Creating scene objects...")
    
    # 1. Ground Plane
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
    ground = bpy.context.active_object
    ground.name = "Forest_Ground"
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide(number_cuts=6)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    subsurf = ground.modifiers.new(name="Subdivision", type='SUBSURF')
    subsurf.levels = 2
    subsurf.render_levels = 3
    
    ground_mat = create_forest_ground_material()
    ground.data.materials.append(ground_mat)
    
    # 2. Rocks
    rock_positions = [(-4, 3, 0.8), (5, -2, 0.6), (-2, -5, 0.5)]
    mossy_mat = create_mossy_rock_material()
    
    for i, pos in enumerate(rock_positions):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1.2, location=pos)
        rock = bpy.context.active_object
        rock.name = f"Mossy_Rock_{i+1}"
        rock.scale = (1.0 + random.uniform(-0.3, 0.3), 
                     1.0 + random.uniform(-0.3, 0.3), 
                     0.6 + random.uniform(-0.2, 0.2))
        rock.data.materials.append(mossy_mat)
    
    # 3. Wood Logs
    wood_mat = create_old_wood_material()
    log_data = [
        ((-3, -2, 0.3), (math.radians(90), 0, math.radians(30)), 3.0),
        ((4, 4, 0.25), (math.radians(90), 0, math.radians(-45)), 2.5)
    ]
    
    for i, (pos, rot, length) in enumerate(log_data):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=length, location=pos)
        log = bpy.context.active_object
        log.name = f"Old_Log_{i+1}"
        log.rotation_euler = rot
        log.data.materials.append(wood_mat)
    
    # 4. Moss Carpet
    moss_mat = create_moss_carpet_material()
    moss_positions = [(2, 1, 0.05), (-1, 4, 0.05), (3, -4, 0.05)]
    
    for i, pos in enumerate(moss_positions):
        bpy.ops.mesh.primitive_plane_add(size=2, location=pos)
        moss = bpy.context.active_object
        moss.name = f"Moss_Patch_{i+1}"
        moss.scale = (1.2 + random.uniform(-0.3, 0.3), 
                     1.0 + random.uniform(-0.3, 0.3), 
                     1.0)
        moss.rotation_euler[2] = random.uniform(0, math.radians(360))
        moss.data.materials.append(moss_mat)
    
    # 5. Pebbles
    pebbles_mat = create_pebbles_material()
    bpy.ops.mesh.primitive_plane_add(size=3, location=(-5, -4, 0.02))
    pebbles = bpy.context.active_object
    pebbles.name = "Pebbles_Area"
    pebbles.data.materials.append(pebbles_mat)
    
    # 6. Stump
    bark_mat = create_tree_bark_material()
    bpy.ops.mesh.primitive_cylinder_add(radius=1.0, depth=1.2, location=(6, 2, 0.6))
    stump = bpy.context.active_object
    stump.name = "Tree_Stump"
    stump.data.materials.append(bark_mat)
    
    # 7. Wet Leaves
    leaves_mat = create_wet_leaves_material()
    bpy.ops.mesh.primitive_plane_add(size=1.5, location=(1, -2, 0.03))
    leaves = bpy.context.active_object
    leaves.name = "Wet_Leaves"
    leaves.data.materials.append(leaves_mat)
    
    # 8. Mushrooms
    mushroom_mat = create_mushroom_material()
    mushroom_positions = [(-1, 2, 0.15), (0.5, 2.5, 0.15)]
    
    for i, pos in enumerate(mushroom_positions):
        # Cap
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.25, location=pos, segments=16, ring_count=8)
        cap = bpy.context.active_object
        cap.name = f"Mushroom_Cap_{i+1}"
        cap.scale[2] = 0.6
        cap.data.materials.append(mushroom_mat)
        
        # Stem
        stem_pos = (pos[0], pos[1], pos[2] - 0.15)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.3, location=stem_pos)
        stem = bpy.context.active_object
        stem.name = f"Mushroom_Stem_{i+1}"
        
        # Simple stem material
        stem_mat = bpy.data.materials.new(f"Stem_Mat_{i+1}")
        stem_mat.use_nodes = True
        stem_mat.node_tree.nodes["Principled BSDF"].inputs['Base Color'].default_value = (0.9, 0.85, 0.75, 1.0)
        stem.data.materials.append(stem_mat)

    print("All objects created.")

def setup_lighting():
    # Sun
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    sun = bpy.context.active_object
    sun.name = "Forest_Sun"
    sun.data.energy = 2.0
    sun.data.color = (1.0, 0.95, 0.8)
    sun.rotation_euler = (math.radians(60), 0, math.radians(30))
    
    # Fill
    bpy.ops.object.light_add(type='AREA', location=(-5, 5, 8))
    area = bpy.context.active_object
    area.name = "Ambient_Fill"
    area.data.energy = 50
    area.data.color = (0.7, 0.8, 1.0)
    
    # Spot
    bpy.ops.object.light_add(type='SPOT', location=(3, -3, 6))
    spot = bpy.context.active_object
    spot.name = "Accent_Spot"
    spot.data.energy = 100
    spot.rotation_euler = (math.radians(70), 0, math.radians(135))

    print("Lighting setup done.")

def setup_camera():
    # Camera Wide
    bpy.ops.object.camera_add(location=(12, -12, 8))
    cam1 = bpy.context.active_object
    cam1.name = "Camera_Wide"
    cam1.rotation_euler = (math.radians(65), 0, math.radians(45))
    cam1.data.lens = 35
    bpy.context.scene.camera = cam1
    
    # Camera Closeup
    bpy.ops.object.camera_add(location=(5, -8, 4))
    cam2 = bpy.context.active_object
    cam2.name = "Camera_Closeup"
    cam2.rotation_euler = (math.radians(75), 0, math.radians(30))
    cam2.data.lens = 50
    
    print("Cameras setup done.")

def setup_world():
    world = bpy.context.scene.world
    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links
    nodes.clear()
    
    sky = nodes.new('ShaderNodeTexSky')
    sky.sky_type = 'HOSEK_WILKIE'
    
    bg = nodes.new('ShaderNodeBackground')
    bg.inputs['Strength'].default_value = 0.8
    
    mix = nodes.new('ShaderNodeMixRGB')
    mix.blend_type = 'MULTIPLY'
    mix.inputs['Fac'].default_value = 0.5
    mix.inputs['Color2'].default_value = (0.3, 0.4, 0.3, 1.0)
    
    output = nodes.new('ShaderNodeOutputWorld')
    
    links.new(sky.outputs['Color'], mix.inputs['Color1'])
    links.new(mix.outputs['Color'], bg.inputs['Color'])
    links.new(bg.outputs['Background'], output.inputs['Surface'])
    
    print("World environment done.")

def main():
    print("--- STARTING TUGAS 2 ---")
    
    clear_scene()
    create_scene_objects()
    setup_lighting()
    setup_camera()
    setup_world()
    
    # Set shading to Material
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'
                    break
    
    print("Scene generated successfully.")

if __name__ == "__main__":
    main()