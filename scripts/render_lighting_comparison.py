"""Optional physical-lighting comparison of the authored scene. Does not overwrite the EEVEE scene."""
import bpy,os,sys,argparse,time
from pathlib import Path
P=Path(__file__).resolve().parents[1];B=Path(os.environ.get('CAT_BUILD_DIR','/build/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat'))
p=argparse.ArgumentParser();p.add_argument('--revision',type=int,default=4);p.add_argument('--resolution',type=int,default=800);p.add_argument('--samples',type=int,default=32);a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(B/'GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat.blend'));s=bpy.context.scene
assert s.get('revision')==a.revision,(s.get('revision'),a.revision)
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=a.samples;s.cycles.use_denoising=False;s.cycles.time_limit=150;s.cycles.adaptive_threshold=.022;s.cycles.max_bounces=6;s.cycles.diffuse_bounces=3;s.cycles.glossy_bounces=3;s.cycles.transmission_bounces=3;s.render.resolution_x=a.resolution;s.render.resolution_y=a.resolution
floor=bpy.data.materials['Studio • warm gray'].node_tree.nodes.get('Principled BSDF');floor.inputs['Emission Strength'].default_value=0
s.world.node_tree.nodes.get('Background').inputs[1].default_value=.38
s.render.filepath=str(P/f'preview/renders/lighting_r{a.revision:02}_cycles.png');bpy.ops.render.render(write_still=True);print('CYCLES_COMPARISON_COMPLETE',flush=True)
