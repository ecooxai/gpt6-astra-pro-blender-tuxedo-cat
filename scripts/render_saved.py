"""Fast EEVEE reviews from the preserved full scene, without rebuilding geometry."""
import bpy,os,sys,argparse,time
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[1];B=Path(os.environ.get('CAT_BUILD_DIR','/build/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat'))
p=argparse.ArgumentParser();p.add_argument('--revision',type=int,default=2);p.add_argument('--resolution',type=int,default=720);p.add_argument('--samples',type=int,default=12);p.add_argument('--views',default='hero,front,right,rear,left');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(B/'GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat.blend'));s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=a.resolution;s.render.resolution_y=a.resolution;s.eevee.taa_render_samples=a.samples;s.eevee.use_soft_shadows=False;s.eevee.shadow_cube_size='512';s.eevee.shadow_cascade_size='1024'
for m in bpy.data.materials:
 if 'fibers' in m.name and hasattr(m,'shadow_method'):m.shadow_method='NONE'
views={'hero':((3.2,-5.7,2.3),(0,.19,1.13),3.45),'front':((0,-7,1.42),(0,.1,1.13),2.86),'left':((-7,-.01,1.42),(0,.19,1.15),3.50),'right':((7,-.01,1.42),(0,.19,1.15),3.50),'rear':((0,7,1.42),(0,.20,1.12),2.92)}
t0=time.time()
for v in a.views.split(','):
 pos,target,scale=views[v];s.camera.location=pos;s.camera.rotation_euler=(Vector(target)-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=scale;s.render.filepath=str(P/f'preview/renders/r{a.revision:02}_{v}.png');print('START_VIEW',v,flush=True);bpy.ops.render.render(write_still=True);print('RENDER_DONE',v,round(time.time()-t0,2),flush=True)
print('REVIEW_SET_COMPLETE',flush=True)
