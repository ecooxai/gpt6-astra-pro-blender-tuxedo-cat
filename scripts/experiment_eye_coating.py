"""Optical approximation test on our own scene: reflective thin film, no refraction."""
import bpy,os
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[1];B=Path(os.environ.get('CAT_BUILD_DIR','/build/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat'))
bpy.ops.wm.open_mainfile(filepath=str(B/'GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat.blend'));s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.eevee.use_ssr=False;s.eevee.use_ssr_refraction=False;s.eevee.taa_render_samples=12;s.render.resolution_x=640;s.render.resolution_y=640
m=bpy.data.materials['11 • clear corneal film'];n=m.node_tree.nodes;n.clear();l=m.node_tree.links;t=n.new('ShaderNodeBsdfTransparent');t.inputs[0].default_value=(1,1,1,1);g=n.new('ShaderNodeBsdfGlossy');g.inputs['Color'].default_value=(1,1,1,1);g.inputs['Roughness'].default_value=.055;fr=n.new('ShaderNodeFresnel');fr.inputs['IOR'].default_value=1.34;mix=n.new('ShaderNodeMixShader');l.new(fr.outputs[0],mix.inputs[0]);l.new(t.outputs[0],mix.inputs[1]);l.new(g.outputs[0],mix.inputs[2]);out=n.new('ShaderNodeOutputMaterial');l.new(mix.outputs[0],out.inputs['Surface']);m.blend_method='BLEND';m.show_transparent_back=False;m.use_screen_refraction=False;m.shadow_method='NONE'
for o in bpy.data.objects:
 if o.name.startswith('Cornea '):o.modifiers.clear()
 if o.name in ['Model attribution','Tool attribution']:o.hide_render=True
bpy.data.materials['02 • individually colored fibers'].shadow_method='NONE'
for name in ['Fill • camera right','Coat edge • rear strip']:bpy.data.lights[name].use_shadow=False
target=Vector((0,-.95,1.67));pos=Vector((.3,-6,1.97));s.camera.location=target+(pos-target)*4;s.camera.rotation_euler=(target-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=1.12;s.render.filepath=str(P/'preview/renders/experiment_eye_coating_eevee.png');bpy.ops.render.render(write_still=True);print('EYE_COATING_TEST_COMPLETE',flush=True)
