"""Export an independent lower-density GLB from the original Blender scene.
Full native curve groom and analytic pigment remain untouched in the source .blend.
Web copy uses sampled original pigment, tapered strand tubes, and inexpensive eye glints.
"""
import bpy,os,math,json
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[1];B=Path(os.environ.get('CAT_BUILD_DIR','/build/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat'))
bpy.ops.wm.open_mainfile(filepath=str(B/'GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat.blend'))
bpy.ops.object.select_all(action='DESELECT');exports=[];portable={}
def web_groom(src):
 guide=bpy.data.objects[src['guide_object']];old=guide.data;n=len(old.vertices)//4;stride=24 if src.name.startswith('Body groom') else (18 if src.name.startswith('Face microgroom') else (10 if src.name.startswith('Lid groom') else 5));vv=[];ff=[];cc=[];ca=old.color_attributes['Coat'];ra=old.attributes['FiberRadius']
 for h in range(0,n,stride):
  pts=[old.vertices[h*4+j].co.copy() for j in range(4)];base=len(vv)
  for j,p in enumerate(pts):
   axis=(pts[min(j+1,3)]-pts[max(0,j-1)]).normalized();u=axis.cross(Vector((.1,.12,1)))
   if u.length<.001:u=axis.cross(Vector((1,0,0)))
   u.normalize();v=axis.cross(u).normalized();r=ra.data[h*4+j].value
   for k in range(3):
    t=k*math.pi*2/3;vv.append(p+(u*math.cos(t)+v*math.sin(t))*r);cc.extend(ca.data[h*4+j].color)
   if j:
    for k in range(3):ff.append((base+(j-1)*3+k,base+(j-1)*3+(k+1)%3,base+j*3+(k+1)%3,base+j*3+k))
 me=bpy.data.meshes.new(src.name+' web tubes');me.from_pydata(vv,[],ff);me.update();colors=me.color_attributes.new(name='Coat',type='FLOAT_COLOR',domain='POINT');colors.data.foreach_set('color',cc)
 for poly in me.polygons:poly.use_smooth=True
 for m in src.data.materials:me.materials.append(m)
 ob=bpy.data.objects.new(src.name+' • web density',me);bpy.context.scene.collection.objects.link(ob);ob.matrix_world=src.matrix_world.copy();ob['web_strands']=len(vv)//12;return ob
for colname in ['CAT • original geometry','GROOM • authored strands']:
 for src in list(bpy.data.collections[colname].objects):
  # Full corneal optics are preserved in Blender. The mobile GLB avoids costly
  # transmission passes and retains the authored small reflection meshes instead.
  if src.name.startswith('Cornea '):continue
  if src.hide_render and not src.get('web_reflection_fallback',False):continue
  if src.type=='CURVES' and src.get('guide_object'):
   ob=web_groom(src)
  else:
   ob=src.copy();ob.data=src.data.copy();bpy.context.scene.collection.objects.link(ob);ob.hide_render=False;ob.hide_set(False)
   if 'groom' in ob.name.lower() and ob.type=='MESH':
    old=ob.data;vv=[];ff=[];cc=[];att=old.color_attributes.get('Coat');n=len(old.vertices)//12
    for h in range(0,n,12):
     base=len(vv)
     for j in range(12):vv.append(old.vertices[h*12+j].co.copy());cc.extend(att.data[h*12+j].color)
     for j in range(1,4):
      for k in range(3):ff.append((base+(j-1)*3+k,base+(j-1)*3+(k+1)%3,base+j*3+(k+1)%3,base+j*3+k))
    me=bpy.data.meshes.new(ob.name+' web density');me.from_pydata(vv,[],ff)
    for m in old.materials:me.materials.append(m)
    ca=me.color_attributes.new(name='Coat',type='FLOAT_COLOR',domain='POINT');ca.data.foreach_set('color',cc)
    for poly in me.polygons:poly.use_smooth=True
    ob.data=me
   elif 'unified anatomical' in ob.name:
    bpy.context.view_layer.objects.active=ob;ob.select_set(True);mod=ob.modifiers.new('Web silhouette-preserving reduction','DECIMATE');mod.ratio=.24;bpy.ops.object.modifier_apply(modifier=mod.name);ob.select_set(False)
  ob['source_revision']=bpy.context.scene.get('revision');exports.append(ob)
for ob in exports:
 for slot in ob.material_slots:
  m=slot.material
  if m and (m.name.startswith('01 •') or m.name.startswith('02 •')):
   if m.name not in portable:
    pm=m.copy();pm.name=m.name+' • portable colors';nn=pm.node_tree.nodes;ll=pm.node_tree.links;attr=nn.new('ShaderNodeVertexColor');attr.layer_name='Coat';bs=nn.get('Principled BSDF');ll.new(attr.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Sheen Weight'].default_value=0;bs.inputs['Roughness'].default_value=.94;bs.inputs['Specular IOR Level'].default_value=.04;portable[m.name]=pm
   slot.material=portable[m.name]
 ob.select_set(True)
bpy.context.view_layer.objects.active=exports[0];bpy.ops.object.convert(target='MESH')
out=P/'preview/downloads/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat.glb'
pending=out.with_name('.'+out.stem+'.pending.glb')
bpy.ops.export_scene.gltf(filepath=str(pending),export_format='GLB',use_selection=True,export_apply=True,export_cameras=False,export_lights=False,export_yup=True,export_extras=True)
os.replace(pending,out)
report={'revision':bpy.context.scene.get('revision'),'bytes':out.stat().st_size,'objects':len(exports),'web_strands':sum(ob.get('web_strands',0) for ob in exports),'notes':'Portable approximation: sampled original pigment, reduced strand density, and small eye reflection meshes; full analytic shader, corneal optics and native groom are preserved in Blender.'}
(P/'logs/export-report.json').write_text(json.dumps(report,indent=2));print('GLB_EXPORTED',str(out),out.stat().st_size,flush=True)
