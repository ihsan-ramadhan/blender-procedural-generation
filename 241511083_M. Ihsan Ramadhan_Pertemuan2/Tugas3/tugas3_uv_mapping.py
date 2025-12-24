"""
Tugas 3: UV Mapping Project - Blender Python Script
Objek: Robot Arm (Mechanical Object)
Melakukan UV unwrapping dengan seams untuk optimal texture application

Author: Muhammad Ihsan Ramadhan
NIM: 241511083

Deskripsi:
Script ini membuat robot arm sederhana dengan multiple components,
melakukan UV unwrapping menggunakan seams, pack UV islands,
dan apply checker texture untuk verifikasi UV quality.
"""

import bpy
import bmesh
import math
from mathutils import Vector

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    print("Scene cleared")

def create_robot_arm():
    print("Creating mesh...")
    
    # Base
    bpy.ops.mesh.primitive_cylinder_add(radius=1.5, depth=0.3, location=(0, 0, 0.15))
    base = bpy.context.active_object
    base.name = "Robot_Base"
    
    # Lower Arm
    bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=3, location=(0, 0, 1.8))
    lower_arm = bpy.context.active_object
    
    # Joint
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 3.3))
    joint = bpy.context.active_object
    
    # Upper Arm
    bpy.ops.mesh.primitive_cylinder_add(radius=0.35, depth=2.5, location=(0, 1.25, 4.05))
    upper_arm = bpy.context.active_object
    upper_arm.rotation_euler = (math.radians(90), 0, 0)
    
    # Effector
    bpy.ops.mesh.primitive_cube_add(size=0.6, location=(0, 2.5, 4.05))
    effector = bpy.context.active_object
    effector.scale = (0.8, 0.5, 1.2)
    
    # Join
    bpy.ops.object.select_all(action='DESELECT')
    for obj in [base, lower_arm, joint, upper_arm, effector]:
        obj.select_set(True)
    
    bpy.context.view_layer.objects.active = base
    bpy.ops.object.join()
    robot = bpy.context.active_object
    robot.name = "Robot_Arm"
    
    return robot

def mark_seams_by_angle(obj, angle=30):
    print(f"Marking seams (Threshold: {angle} deg)...")
    
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_mode(type='EDGE')
    
    angle_rad = math.radians(angle)
    bm = bmesh.from_edit_mesh(obj.data)
    bm.edges.ensure_lookup_table()
    
    count = 0
    for edge in bm.edges:
        if len(edge.link_faces) == 2:
            face1 = edge.link_faces[0]
            face2 = edge.link_faces[1]
            if face1.normal.angle(face2.normal) > angle_rad:
                edge.seam = True
                count += 1
    
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')
    print(f"Marked {count} seams.")

def mark_additional_seams(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(obj.data)
    bm.edges.ensure_lookup_table()
    
    for edge in bm.edges:
        if len(edge.verts) == 2:
            v1, v2 = edge.verts
            if abs(v1.co.z - v2.co.z) > 0.5:
                if abs(v1.co.x) < 0.01 and abs(v2.co.x) < 0.01:
                    edge.seam = True
    
    bmesh.update_edit_mesh(obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')

def unwrap_with_seams(obj):
    print("Unwrapping UVs...")
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
    bpy.ops.object.mode_set(mode='OBJECT')

def pack_uv_islands(obj, margin=0.02):
    print("Packing UV islands...")
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.pack_islands(margin=margin, rotate=True)
    bpy.ops.object.mode_set(mode='OBJECT')

def create_checker_material():
    mat = bpy.data.materials.new(name="UV_Checker")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    
    tex_coord = nodes.new('ShaderNodeTexCoord')
    checker = nodes.new('ShaderNodeTexChecker')
    checker.inputs['Scale'].default_value = 16.0
    checker.inputs['Color1'].default_value = (0.8, 0.8, 0.8, 1.0)
    checker.inputs['Color2'].default_value = (0.2, 0.2, 0.2, 1.0)
    
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    output = nodes.new('ShaderNodeOutputMaterial')
    
    links.new(tex_coord.outputs['UV'], checker.inputs['Vector'])
    links.new(checker.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
    
    return mat

def export_uv_layout(obj, filepath="uv_layout.png"):
    print(f"Exporting UV layout to {filepath}")
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    try:
        bpy.ops.uv.export_layout(filepath=filepath, size=(2048, 2048), opacity=0.25)
    except:
        print("Export failed (usually due to running in background without UI)")
    bpy.ops.object.mode_set(mode='OBJECT')

def setup_viewport_check(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'

def setup_camera(obj):
    for o in bpy.data.objects:
        if o.type == 'CAMERA':
            bpy.data.objects.remove(o)
            
    bbox = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    center = sum((Vector(b) for b in bbox), Vector()) / 8
    
    bpy.ops.object.camera_add(location=(center.x + 8, center.y - 8, center.z + 5))
    camera = bpy.context.active_object
    camera.name = "Camera_UV_Check"
    
    direction = center - camera.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    camera.rotation_euler = rot_quat.to_euler()
    bpy.context.scene.camera = camera

def main():
    print("--- STARTING UV MAPPING TASK ---")
    
    clear_scene()
    robot = create_robot_arm()
    
    mark_seams_by_angle(robot)
    mark_additional_seams(robot)
    
    unwrap_with_seams(robot)
    pack_uv_islands(robot)
    
    mat = create_checker_material()
    robot.data.materials.append(mat)
    
    export_uv_layout(robot, filepath="//uv_layout.png")
    
    setup_viewport_check(robot)
    setup_camera(robot)
    
    print("Task completed. Check viewport for checker pattern.")

if __name__ == "__main__":
    main()