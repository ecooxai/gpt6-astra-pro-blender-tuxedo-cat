"""Actual transparent corneal geometry experiment; no reference image is read."""
import bpy,math,os
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[1];B=Path(os.environ.get('CAT_BUILD_DIR','/build/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat'))
bpy.ops.wm.open_mainfile(filepath=str(B/'GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat.blend'))
s=bpy.context.scene;s.eevee.use_ssr=True;s.eevee.use_ssr_refraction=True;s.eevee.taa_render_samples=20;s.render.resolution_x=800;s.render.resolution_y=800
mat=bpy.data.materials.new('11 • clear corneal film');mat.use_nodes=True;bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.98,.995,1,1);bs.inputs['Roughness'].default_value=.035;bs.inputs['IOR'].default_value=1.38;bs.inputs['Transmission Weight'].default_value=1;mat.blend_method='HASHED';mat.use_screen_refraction=True;mat.refraction_depth=.007;mat.shadow_method='NONE'
root=bpy.data.collections['CAT • original geometry'];offset=s.get('ground_offset',0)
for side in [-1,1]:
 theta=side*.43;N=Vector((math.sin(theta),-math.cos(theta),.015));U=Vector((math.cos(theta),math.sin(theta),0));V=Vector((0,0,1));C=Vector((side*.157,-1.134,1.724-offset));nr=18;nt=96;vv=[C+N*.062];ff=[];R=.0705
 for j in range(1,nr+1):
  r=j/nr
  for k in range(nt):
   t=2*math.pi*k/nt;vv.append(C+U*(R*r*math.cos(t))+V*(R*1.075*r*math.sin(t))+N*(.029+.033*math.sqrt(max(0,1-r*r))))
 for k in range(nt):ff.append((0,1+k,1+(k+1)%nt))
 for j in range(nr-1):
  for k in range(nt):
   i=1+j*nt+k;n=1+j*nt+(k+1)%nt;ff.append((i,n,n+nt,i+nt))
 me=bpy.data.meshes.new('Corneal dome '+str(side));me.from_pydata(vv,[],ff);ob=bpy.data.objects.new('Cornea '+str(side),me);root.objects.link(ob);me.materials.append(mat)
 for f in me.polygons:f.use_smooth=True
 solid=ob.modifiers.new('Corneal wall','SOLIDIFY');solid.thickness=.0008
 bpy.data.objects['Softbox eye reflection '+str(side)].hide_render=True;bpy.data.objects['Secondary eye glint '+str(side)].hide_render=True
pos=Vector((.5,-6,1.95));target=Vector((0,-.95,1.68));s.camera.location=target+(pos-target)*4;s.camera.rotation_euler=(target-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=1.08;s.render.filepath=str(P/'preview/renders/experiment_cornea_eevee.png');bpy.ops.render.render(write_still=True);print('CORNEA_TEST_COMPLETE',flush=True)
