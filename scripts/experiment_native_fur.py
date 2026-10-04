"""Convert our original strand tubes to native hair curves, preserving positions and colors.
This experiment never overwrites the approved full scene or web export.
"""
import bpy,os,sys,argparse,numpy as np
from pathlib import Path
P=Path(__file__).resolve().parents[1];B=Path(os.environ.get('CAT_BUILD_DIR','/build/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat'))
p=argparse.ArgumentParser();p.add_argument('--engine',choices=['EEVEE','CYCLES'],default='EEVEE');a=p.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
bpy.ops.wm.open_mainfile(filepath=str(B/'GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat.blend'))
native=bpy.data.collections.new('FUR • native curve experiment');bpy.context.scene.collection.children.link(native)
guides=bpy.data.collections.new('GUIDES • original strand centers');bpy.context.scene.collection.children.link(guides)
m=bpy.data.materials['02 • individually colored fibers'].copy();m.name='Native fiber shading • original coat attributes';nodes=m.node_tree.nodes;links=m.node_tree.links;attr=nodes.new('ShaderNodeAttribute');attr.attribute_name='Coat'
if a.engine=='CYCLES':
 sh=nodes.new('ShaderNodeBsdfHairPrincipled');sh.parametrization='COLOR';sh.inputs['Roughness'].default_value=.35
 if 'Radial Roughness' in sh.inputs:sh.inputs['Radial Roughness'].default_value=.4
 links.new(attr.outputs['Color'],sh.inputs['Color']);links.new(sh.outputs[0],nodes.get('Material Output').inputs['Surface'])
else:links.new(attr.outputs['Color'],nodes.get('Principled BSDF').inputs['Base Color'])
count=0
for old in list(bpy.data.collections['GROOM • authored strands'].objects):
 mesh=old.data;n=len(mesh.vertices)//12;coords=np.empty(len(mesh.vertices)*3,dtype=np.float32);mesh.vertices.foreach_get('co',coords);coords=coords.reshape(n,4,3,3);centers=coords.mean(axis=2);radii=np.linalg.norm(coords-centers[:,:,None,:],axis=-1).mean(axis=2)
 color=np.empty(len(mesh.vertices)*4,dtype=np.float32);mesh.color_attributes['Coat'].data.foreach_get('color',color);color=color.reshape(n,4,3,4)[:,:,0,:]
 points=centers.reshape(-1,3);idx=np.arange(n,dtype=np.int32)[:,None]*4+np.arange(3,dtype=np.int32)[None,:];edges=np.stack([idx,idx+1],axis=-1).reshape(-1,2)
 me=bpy.data.meshes.new(old.name+' guide chains');me.from_pydata(points.tolist(),edges.tolist(),[]);me.update();co=me.color_attributes.new(name='Coat',type='FLOAT_COLOR',domain='POINT');co.data.foreach_set('color',color.ravel());rad=me.attributes.new(name='FiberRadius',type='FLOAT',domain='POINT');rad.data.foreach_set('value',radii.ravel())
 source=bpy.data.objects.new(old.name+' editable guides',me);guides.objects.link(source);source.matrix_world=old.matrix_world.copy();source.hide_render=True;source.hide_set(True)
 hd=bpy.data.hair_curves.new(old.name+' native strands');ob=bpy.data.objects.new(old.name+' • native curves',hd);native.objects.link(ob);ob.matrix_world=old.matrix_world.copy();hd.materials.append(m)
 ng=bpy.data.node_groups.new('Original strand chains → native curves '+old.name,'GeometryNodeTree');ng.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');nn=ng.nodes;ll=ng.links
 info=nn.new('GeometryNodeObjectInfo');info.transform_space='ORIGINAL';info.inputs['Object'].default_value=source
 conv=nn.new('GeometryNodeMeshToCurve');ll.new(info.outputs['Geometry'],conv.inputs['Mesh'])
 radnode=nn.new('GeometryNodeSetCurveRadius');ll.new(conv.outputs['Curve'],radnode.inputs['Curve']);att=nn.new('GeometryNodeInputNamedAttribute');att.data_type='FLOAT';att.inputs['Name'].default_value='FiberRadius';ll.new(att.outputs['Attribute'],radnode.inputs['Radius'])
 smooth=nn.new('GeometryNodeCurveSplineType');smooth.spline_type='BEZIER';ll.new(radnode.outputs['Curve'],smooth.inputs['Curve']);handles=nn.new('GeometryNodeCurveSetHandles');handles.handle_type='AUTO';handles.mode={'LEFT','RIGHT'};ll.new(smooth.outputs['Curve'],handles.inputs['Curve'])
 assign=nn.new('GeometryNodeSetMaterial');assign.inputs['Material'].default_value=m;ll.new(handles.outputs['Curve'],assign.inputs['Geometry']);out=nn.new('NodeGroupOutput');ll.new(assign.outputs['Geometry'],out.inputs['Geometry'])
 mod=ob.modifiers.new('Procedural native groom','NODES');mod.node_group=ng;ob['actual_strands']=n;old.hide_render=True;old.hide_set(True);count+=n
 print('NATIVE_CONVERTED',old.name,n,flush=True)
bpy.context.view_layer.update();print('NATIVE_STRANDS_TOTAL',count,flush=True)
s=bpy.context.scene;s.render.resolution_x=800;s.render.resolution_y=800;s.render.resolution_percentage=100;s.eevee.taa_render_samples=16
if a.engine=='CYCLES':
 s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=128;s.cycles.time_limit=150;s.cycles.use_denoising=False;s.cycles.adaptive_threshold=.02;s.cycles.max_bounces=6
 bpy.data.materials['Studio • warm gray'].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=0
else:s.render.engine='BLENDER_EEVEE'
exp=B/'experiments';exp.mkdir(exist_ok=True);bpy.ops.wm.save_as_mainfile(filepath=str(exp/f'GPT-6-Astra-Pro_Blender_native_fur_{a.engine.lower()}.blend'),compress=True)
s.render.filepath=str(P/f'preview/renders/experiment_native_{a.engine.lower()}.png');bpy.ops.render.render(write_still=True);print('NATIVE_FUR_TEST_COMPLETE',a.engine,flush=True)
