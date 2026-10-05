"""Original source-scene refinement; physical microcoat replaces unstable screen-space eye refraction."""
import bpy,bmesh,os
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[1];B=Path(os.environ.get('CAT_BUILD_DIR','/build/'+P.name));path=B/(P.name+'.blend')
bpy.ops.wm.open_mainfile(filepath=str(path));s=bpy.context.scene
nose=bpy.data.objects['Soft lobed cat nose'];bm=bmesh.new();bm.from_mesh(nose.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(nose.data);bm.free()
for mat in bpy.data.materials:
 if mat.name.startswith('04 '):
  bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Specular IOR Level'].default_value=0;bs.inputs['Roughness'].default_value=.94;bs.inputs['Base Color'].default_value=(.0005,.0007,.0006,1)
 if mat.name.startswith('08 '):
  bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Coat Weight'].default_value=.08;bs.inputs['Coat Roughness'].default_value=.06
 if mat.name.startswith('10 '):
  bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Coat Weight'].default_value=.22;bs.inputs['Coat Roughness'].default_value=.08
for side in [-1,1]:
 ob=bpy.data.objects.get('Cornea '+str(side));ob.hide_render=True;ob['optional_physical_cornea']=True
 for tag in ['Softbox eye reflection ','Secondary eye glint ']:
  ob=bpy.data.objects[tag+str(side)];ob.hide_render=False;ob.hide_set(False)
s.eevee.use_ssr=False;s.eevee.use_ssr_refraction=False;s.eevee.use_soft_shadows=True;s.eevee.taa_render_samples=32
s['revision']=12;s['eye_rendering']='Shallow original iris/pupil geometry with dielectric microcoat; optional physical corneas preserved but hidden.'
bpy.ops.wm.save_as_mainfile(filepath=str(path),compress=True)
# Only review render uses shadowless fine hairs; full saved scene retains complete groom shadows.
for m in bpy.data.materials:
 if m.name.startswith('02 '):m.shadow_method='NONE'
pos=Vector((.9,-6,2.0));target=Vector((0,-.95,1.68));scale=1.12;s.camera.location=target+(pos-target)*4;s.camera.rotation_euler=(target-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=scale
for i,name in enumerate(['Model attribution','Tool attribution']):
 ob=bpy.data.objects[name];ob.location=(-scale*.445,scale*(.461-i*.028),-8);ob.data.size=scale*(.021 if i==0 else .0105)
s.render.resolution_x=800;s.render.resolution_y=800;s.render.filepath=str(P/'preview/renders/r12_detail.png');bpy.ops.render.render(write_still=True);print('PASS12_EYE_REVIEW_READY',flush=True)
