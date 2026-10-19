# Esteban de la Peña, carnet 24171
# crear una nave espacial simple desde un unico cubo
# solo se añaden detalles extruidos en modo edicion; no se agregan objetos

import bpy
import math
from mathutils import Vector

# reiniciar la escena y dejar solo el cubo inicial
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
nave = bpy.context.object
nave.name = "Nave espacial"
bpy.context.view_layer.objects.active = nave
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.delete(type='VERT')
bpy.ops.object.mode_set(mode='OBJECT')

# crear una malla unica con volumenes extruidos desde las caras de un cubo
vertices = []
caras = []


def extruir_prisma(poligono, z_bajo, z_alto):
    """añade un prisma extruido como parte de la malla del cubo original."""
    inicio = len(vertices)
    cantidad = len(poligono)
    vertices.extend([(x, y, z_bajo) for x, y in poligono])
    vertices.extend([(x, y, z_alto) for x, y in poligono])
    caras.append(tuple(inicio + i for i in range(cantidad - 1, -1, -1)))
    caras.append(tuple(inicio + cantidad + i for i in range(cantidad)))
    for i in range(cantidad):
        siguiente = (i + 1) % cantidad
        caras.append((inicio + i, inicio + siguiente,
                      inicio + cantidad + siguiente, inicio + cantidad + i))


# fuselaje largo: proa hacia +y, creado al escalar la cara superior del cubo
extruir_prisma([(-0.45, -2.5), (0.45, -2.5), (0.45, 1.2), (0, 2.35), (-0.45, 1.2)], -0.25, 0.25)

# alas barridas laterales, agregadas como extrusiones a la misma malla
extruir_prisma([(0.38, 0.35), (2.15, -0.8), (1.8, -1.55), (0.42, -0.75)], -0.24, -0.02)
extruir_prisma([(-0.38, 0.35), (-2.15, -0.8), (-1.8, -1.55), (-0.42, -0.75)], -0.24, -0.02)

# estabilizadores traseros pequeños extruidos en el mismo objeto
extruir_prisma([(0.32, -1.75), (0.92, -2.3), (0.78, -2.5), (0.3, -2.1)], -0.22, -0.04)
extruir_prisma([(-0.32, -1.75), (-0.92, -2.3), (-0.78, -2.5), (-0.3, -2.1)], -0.22, -0.04)

# cabina poligonal elevada sobre el fuselaje, unida en una sola malla
extruir_prisma([(-0.3, -0.05), (0.3, -0.05), (0.28, 0.72), (0, 1.25), (-0.28, 0.72)], 0.24, 0.58)

# sustituir los vertices del cubo inicial por la malla final, sin crear objetos extra
malla = bpy.data.meshes.new("Malla extruida desde cubo")
malla.from_pydata(vertices, [], caras)
malla.update()
nave.data = malla

# un solo material con color base sencillo
material = bpy.data.materials.new(name="Gris azulado simple")
material.diffuse_color = (0.20, 0.34, 0.46, 1.0)
nave.data.materials.append(material)

# aplicar bevel para suavizar bordes sin añadir objetos
bpy.context.view_layer.objects.active = nave
bpy.ops.object.modifier_add(type='BEVEL')
nave.modifiers[-1].width = 0.04
nave.modifiers[-1].segments = 1
nave.modifiers[-1].name = "Bisel sencillo"

# triangulacion y exportacion OBJ con UV y normales
bpy.ops.object.modifier_apply(modifier="Bisel sencillo")
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
bpy.ops.object.mode_set(mode='OBJECT')

# asignar coordenadas UV automaticas
bpy.context.view_layer.objects.active = nave
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project(island_margin=0.02)
bpy.ops.object.mode_set(mode='OBJECT')

carpeta = bpy.path.abspath("//")
bpy.ops.wm.save_as_mainfile(filepath=carpeta + "nave_espacial.blend")
bpy.ops.wm.obj_export(filepath=carpeta + "nave_espacial.obj",
                      export_selected_objects=True,
                      export_triangulated_mesh=True,
                      export_uv=True,
                      export_normals=True,
                      export_materials=True)
