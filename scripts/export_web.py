"""Export an independent, lower-density, vertex-colored GLB. Never overwrite the full groom .blend."""
import bpy,sys,math,time,os
from pathlib import Path
P=Path(__file__).resolve().parents[1];B=Path(os.environ.get('CAT_BUILD_DIR','/build/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat'))
bpy.ops.wm.open_mainfile(filepath=str(B/'GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat.blend'))
bpy.ops.object.select_all(action='DESELECT');exports=[]
for colname in ['CAT • original geometry','GROOM • authored strands']:
 for src in list(bpy.data.collections[colname].objects):
  ob=src.copy();ob.data=src.data.copy();bpy.context.scene.collection.objects.link(ob);exports.append(ob)
  if 'groom' in ob.name.lower() and ob.type=='MESH':
   # Every twelfth actual strand retained as complete tapered triangles.
   old=ob.data;vv=[];ff=[];colors=[];att=old.color_attributes.get('Coat');n=len(old.vertices)//12
   for h in range(0,n,12):
    base=len(vv)
    for j in range(12):vv.append(old.vertices[h*12+j].co.copy());colors.extend(att.data[h*12+j].color)
    for j in range(1,4):
     for k in range(3):ff.append((base+(j-1)*3+k,base+(j-1)*3+(k+1)%3,base+j*3+(k+1)%3,base+j*3+k))
   me=bpy.data.meshes.new(ob.name+' web density');me.from_pydata(vv,[],ff);me.materials.clear()
   for m in old.materials:me.materials.append(m)
   ca=me.color_attributes.new(name='Coat',type='FLOAT_COLOR',domain='POINT');ca.data.foreach_set('color',colors)
   for p in me.polygons:p.use_smooth=True
   ob.data=me
  elif 'unified anatomical' in ob.name:
   bpy.context.view_layer.objects.active=ob;ob.select_set(True);mod=ob.modifiers.new('Web silhouette-preserving reduction','DECIMATE');mod.ratio=.24;bpy.ops.object.modifier_apply(modifier=mod.name);ob.select_set(False)
# glTF cannot represent Blender's analytic node group. Preserve its sampled original
# Coat field as vertex colors in this portable lower-detail copy, never changing the .blend.
portable={}
for ob in exports:
 for slot in ob.material_slots:
  m=slot.material
  if not m or not m.name.startswith('01 •'):continue
  if m.name not in portable:
   pm=m.copy();pm.name='01 • portable procedural coat colors';nn=pm.node_tree.nodes;ll=pm.node_tree.links;vertex=nn.new('ShaderNodeVertexColor');vertex.layer_name='Coat';ll.new(vertex.outputs['Color'],nn.get('Principled BSDF').inputs['Base Color']);portable[m.name]=pm
  slot.material=portable[m.name]
for ob in exports:ob.select_set(True)
bpy.context.view_layer.objects.active=exports[0];bpy.ops.object.convert(target='MESH')
out=P/'preview/downloads/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat.glb'
bpy.ops.export_scene.gltf(filepath=str(out),export_format='GLB',use_selection=True,export_apply=True,export_cameras=False,export_lights=False,export_yup=True)
print('GLB_EXPORTED',out,out.stat().st_size,flush=True)
