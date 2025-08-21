import bpy
import os

# 🧹 Clean the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ========== Materials ==========

# Floor with wood texture
bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
floor = bpy.context.active_object
mat_floor = bpy.data.materials.new("FloorMaterial")
mat_floor.use_nodes = True
nodes = mat_floor.node_tree.nodes
links = mat_floor.node_tree.links

# Clear default nodes
for node in nodes:
    nodes.remove(node)

output = nodes.new(type="ShaderNodeOutputMaterial")
bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
tex_image = nodes.new(type="ShaderNodeTexImage")

# NOTE: replace with path to your texture
tex_image.image = bpy.data.images.load("/app/textures/wood.jpg")

# link nodes
links.new(tex_image.outputs['Color'], bsdf.inputs['Base Color'])
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

floor.data.materials.append(mat_floor)

# Sphere with glass material
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1))
sphere = bpy.context.active_object
mat_sphere = bpy.data.materials.new("SphereMaterial")
mat_sphere.use_nodes = True
nodes = mat_sphere.node_tree.nodes
links = mat_sphere.node_tree.links
for node in nodes:
    nodes.remove(node)

# Output node
output = nodes.new(type="ShaderNodeOutputMaterial")

# Glass shader node
glass = nodes.new(type="ShaderNodeBsdfGlass")
glass.inputs['Roughness'].default_value = 0.05
glass.inputs['IOR'].default_value = 1.45
# Link glass to output
links.new(glass.outputs['BSDF'], output.inputs['Surface'])

sphere.data.materials.append(mat_sphere)

# ========== Lights ==========

# Area light
bpy.ops.object.light_add(type='AREA', location=(5, 5, 5))
light = bpy.context.active_object
light.data.energy = 1000

# Spot light for dramatic shadows
bpy.ops.object.light_add(type='SPOT', location=(0, -5, 5))
spot = bpy.context.active_object
spot.data.energy = 800

# HDRI Environment lighting
world = bpy.context.scene.world
world.use_nodes = True
nodes = world.node_tree.nodes
bg = nodes["Background"]
env_tex = nodes.new("ShaderNodeTexEnvironment")
# NOTE: replace with path to your HDRI
env_tex.image = bpy.data.images.load("/app/textures/studio_hdri.hdr")
world.node_tree.links.new(env_tex.outputs["Color"], bg.inputs["Color"])

# ========== Cameras ==========
cameras = []
bpy.ops.object.camera_add(location=(3, -4, 2), rotation=(1.1, 0, 0.9))
cameras.append(bpy.context.active_object)

bpy.ops.object.camera_add(location=(-4, -2, 3), rotation=(1.2, 0, -0.7))
cameras.append(bpy.context.active_object)

bpy.ops.object.camera_add(location=(0, 5, 3), rotation=(1.3, 0, 3.14))
cameras.append(bpy.context.active_object)

# ========== Render settings ==========
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 64
scene.cycles.device = 'CPU'   
scene.render.image_settings.file_format = 'PNG'

# ========== Render loop ==========
output_dir = "/app/output/"
os.makedirs(output_dir, exist_ok=True)

for i, cam in enumerate(cameras, start=1):
    scene.camera = cam
    scene.render.filepath = os.path.join(output_dir, f"render_cam_{i}.png")
    bpy.ops.render.render(write_still=True)
    print(f"✅ Render {i} saved at {scene.render.filepath}")
