"""Optional physical-lighting validation. Cycles + official OIDN, not image generation.
Reads only the authored Blender scene; never changes the main editable EEVEE file.
"""
import bpy,os,sys,argparse,subprocess,numpy as np,time
from pathlib import Path
P=Path(__file__).resolve().parents[1];B=Path(os.environ.get('CAT_BUILD_DIR','/build/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat'))
p=argparse.ArgumentParser();p.add_argument('--revision',type=int,required=True);p.add_argument('--resolution',type=int,default=1000);p.add_argument('--seconds',type=int,default=210);p.add_argument('--view',choices=['hero','detail'],default='hero');a=p.parse_args(sys.argv[sys.argv.index('--')+1:])
bpy.ops.wm.open_mainfile(filepath=str(B/'GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat.blend'));s=bpy.context.scene
assert s.get('revision')==a.revision,(s.get('revision'),a.revision)
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=256;s.cycles.time_limit=a.seconds;s.cycles.use_denoising=False;s.cycles.adaptive_threshold=.012;s.cycles.max_bounces=8;s.cycles.transmission_bounces=6;s.cycles.glossy_bounces=4;s.cycles.diffuse_bounces=3;s.render.resolution_x=a.resolution;s.render.resolution_y=a.resolution;s.render.resolution_percentage=100
for mat in bpy.data.materials:
 if mat.name.startswith('02 •'):
  n=mat.node_tree.nodes;l=mat.node_tree.links;attr=n.new('ShaderNodeAttribute');attr.attribute_name='Coat';hair=n.new('ShaderNodeBsdfHairPrincipled');hair.parametrization='COLOR';hair.inputs['Roughness'].default_value=.48;hair.inputs['Radial Roughness'].default_value=.55;mul=n.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=(.62,.62,.62,1);l.new(attr.outputs['Color'],mul.inputs[1]);l.new(mul.outputs[0],hair.inputs['Color']);l.new(hair.outputs[0],n.get('Material Output').inputs['Surface'])
bpy.data.materials['Studio • warm gray'].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=0
s.world.node_tree.nodes.get('Background').inputs[1].default_value=.30
bpy.data.lights['Fill • camera right'].energy=160
bpy.data.lights['Soft frontal bounce'].energy=95
s.view_settings.exposure=-.12
if 'Tool attribution' in bpy.data.objects:bpy.data.objects['Tool attribution'].data.body='mcp-colabdev  /  Blender Cycles + OIDN'
if a.view=='detail':
 from mathutils import Vector
 target=Vector((0,-.95,1.67));pos=Vector((.3,-6,1.97));s.camera.location=target+(pos-target)*4;s.camera.rotation_euler=(target-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=1.15
work=P/f'logs/denoise_r{a.revision:02}_{a.view}';work.mkdir(parents=True,exist_ok=True)
s.view_layers[0].cycles.denoising_store_passes=True;s.use_nodes=True;nodes=s.node_tree.nodes;nodes.clear();layers=nodes.new('CompositorNodeRLayers');composite=nodes.new('CompositorNodeComposite');s.node_tree.links.new(layers.outputs['Image'],composite.inputs[0]);aux=[]
for label,stem in [('Denoising Albedo','albedo'),('Denoising Normal','normal')]:
 if label in layers.outputs:
  out=nodes.new('CompositorNodeOutputFile');out.base_path=str(work);out.format.file_format='OPEN_EXR';out.format.color_depth='32';out.format.color_mode='RGB';out.file_slots[0].path=stem+'_';s.node_tree.links.new(layers.outputs[label],out.inputs[0]);aux.append(stem)
print('DENOISING_AUXILIARIES',aux,flush=True)
s.render.image_settings.file_format='OPEN_EXR';s.render.image_settings.color_depth='32';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(work/'raw.exr');bpy.ops.render.render(write_still=True)
def exr_to_pfm(source,dest):
 im=bpy.data.images.load(str(source),check_existing=False);w,h=im.size;pix=np.empty(w*h*4,dtype=np.float32);im.pixels.foreach_get(pix);rgb=pix.reshape(h,w,4)[:,:,:3].copy();bpy.data.images.remove(im)
 with open(dest,'wb') as f:f.write(f'PF\n{w} {h}\n-1.0\n'.encode());f.write(rgb.astype('<f4').tobytes())
 return w,h
w,h=exr_to_pfm(work/'raw.exr',work/'color.pfm');oidn=Path(os.environ.get('OIDN_DENOISE','/home/dev/.local/opt/oidn-2.5.1.x86_64.linux/bin/oidnDenoise'));assert oidn.exists(),str(oidn)
cmd=[str(oidn),'--hdr',str(work/'color.pfm'),'--output',str(work/'clean.pfm'),'--quality','high','--threads','4']
for stem,flag in [('albedo','--alb'),('normal','--nrm')]:
 source=work/(stem+'_0001.exr')
 if source.exists():exr_to_pfm(source,work/(stem+'.pfm'));cmd += [flag,str(work/(stem+'.pfm'))]
subprocess.run(cmd,check=True,timeout=150)
with open(work/'clean.pfm','rb') as f:
 magic=f.readline().strip();assert magic==b'PF';rw,rh=map(int,f.readline().split());scale=float(f.readline());dtype='<f4' if scale<0 else '>f4';data=np.frombuffer(f.read(),dtype=dtype).reshape(rh,rw,3);assert (rw,rh)==(w,h)
im=bpy.data.images.new('Original scene • denoised physical lighting',width=w,height=h,float_buffer=True);rgba=np.ones((h,w,4),dtype=np.float32);rgba[:,:,:3]=data;im.pixels.foreach_set(rgba.ravel());im.update();s.render.image_settings.file_format='PNG';s.render.image_settings.color_depth='8';s.render.image_settings.color_mode='RGBA';out=P/f'preview/renders/beauty_r{a.revision:02}_{a.view}_cycles_oidn.png';im.save_render(str(out),scene=s);print('BEAUTY_COMPLETE',out,flush=True)
