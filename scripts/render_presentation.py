"""Render actual EEVEE studio views from the editable source; never substitutes an image asset."""
import bpy,os,sys,argparse,time
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[1];B=Path(os.environ.get('CAT_BUILD_DIR','/build/'+P.name))
p=argparse.ArgumentParser();p.add_argument('--revision',type=int,default=12);p.add_argument('--resolution',type=int,default=1000);p.add_argument('--samples',type=int,default=40);p.add_argument('--views',default='hero,front,right,rear,left');p.add_argument('--full-fur-shadows',action='store_true');a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
bpy.ops.wm.open_mainfile(filepath=str(B/(P.name+'.blend')));s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.eevee.use_soft_shadows=True;s.eevee.taa_render_samples=a.samples;s.eevee.shadow_cube_size='1024';s.render.resolution_x=a.resolution;s.render.resolution_y=a.resolution
# Default preview retains all geometry but omits the fine hairs' shadow pass for speed.
# The .blend on disk is not modified, and full-fur-shadows enables the complete render.
if not a.full_fur_shadows:
 for m in bpy.data.materials:
  if m.name.startswith('02 '):m.shadow_method='NONE'
views={'hero':((3.2,-5.7,2.3),(0,.19,1.13),3.45),'front':((0,-7,1.42),(0,.1,1.13),2.86),'left':((-7,-.01,1.42),(0,.19,1.15),3.50),'right':((7,-.01,1.42),(0,.19,1.15),3.50),'rear':((0,7,1.42),(0,.20,1.12),2.92),'detail':((.9,-6,2.0),(0,-.95,1.68),1.12)}
t0=time.time()
for v in a.views.split(','):
 pos,target,scale=views[v];pos=Vector(pos);target=Vector(target);s.camera.location=target+(pos-target)*4;s.camera.rotation_euler=(target-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=scale
 for i,name in enumerate(['Model attribution','Tool attribution']):
  ob=bpy.data.objects[name];ob.location=(-scale*.445,scale*(.461-i*.028),-8);ob.data.size=scale*(.021 if i==0 else .0105)
 s.render.filepath=str(P/f'preview/renders/r{a.revision:02}_{v}.png');bpy.ops.render.render(write_still=True);print('PRESENTATION_VIEW_DONE',v,round(time.time()-t0,1),flush=True)
print('PRESENTATION_SET_DONE',flush=True)
