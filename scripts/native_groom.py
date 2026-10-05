"""Editable native Blender curve fibers from original procedural centerlines."""
def create_native_groom(name,points,radii,colors,material,groom_collection,guide_collection,requested):
 import bpy
 n=len(points)//4;edges=[(h*4+j,h*4+j+1) for h in range(n) for j in range(3)]
 me=bpy.data.meshes.new(name+' centerlines');me.from_pydata(points,edges,[]);me.update()
 color=me.color_attributes.new(name='Coat',type='FLOAT_COLOR',domain='POINT');color.data.foreach_set('color',[v for c in colors for v in c])
 rad=me.attributes.new(name='FiberRadius',type='FLOAT',domain='POINT');rad.data.foreach_set('value',radii)
 source=bpy.data.objects.new(name+' editable guides',me);guide_collection.objects.link(source);source.hide_render=True;source.hide_set(True)
 hair=bpy.data.hair_curves.new(name+' native curves');ob=bpy.data.objects.new(name,hair);groom_collection.objects.link(ob);hair.materials.append(material)
 ng=bpy.data.node_groups.new('Centerlines to fine fibers • '+name,'GeometryNodeTree');ng.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');nn=ng.nodes;ll=ng.links
 info=nn.new('GeometryNodeObjectInfo');info.transform_space='RELATIVE';info.inputs['Object'].default_value=source;info.location=(-650,100)
 cv=nn.new('GeometryNodeMeshToCurve');cv.location=(-450,100);ll.new(info.outputs['Geometry'],cv.inputs['Mesh'])
 size=nn.new('GeometryNodeSetCurveRadius');size.location=(-240,100);ll.new(cv.outputs['Curve'],size.inputs['Curve'])
 at=nn.new('GeometryNodeInputNamedAttribute');at.data_type='FLOAT';at.inputs['Name'].default_value='FiberRadius';at.location=(-450,-150);ll.new(at.outputs['Attribute'],size.inputs['Radius'])
 spline=nn.new('GeometryNodeCurveSplineType');spline.spline_type='BEZIER';spline.location=(-40,100);ll.new(size.outputs['Curve'],spline.inputs['Curve'])
 handles=nn.new('GeometryNodeCurveSetHandles');handles.handle_type='AUTO';handles.mode={'LEFT','RIGHT'};handles.location=(160,100);ll.new(spline.outputs['Curve'],handles.inputs['Curve'])
 assign=nn.new('GeometryNodeSetMaterial');assign.inputs['Material'].default_value=material;assign.location=(360,100);ll.new(handles.outputs['Curve'],assign.inputs['Geometry']);out=nn.new('NodeGroupOutput');out.location=(570,100);ll.new(assign.outputs['Geometry'],out.inputs['Geometry'])
 mod=ob.modifiers.new('Editable fine native groom','NODES');mod.node_group=ng;ob['requested_strands']=requested;ob['actual_strands']=n;ob['guide_object']=source.name
 return ob

def add_cornea(root,ground_offset=0):
 """Shallow physical film over the newly embedded, rounder eyes."""
 import bpy,math
 from mathutils import Vector
 scene=bpy.context.scene;scene.eevee.use_ssr=True;scene.eevee.use_ssr_refraction=True
 m=bpy.data.materials.new('11 • shallow clear corneal film');m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.997,.998,1,1);bs.inputs['Roughness'].default_value=.07;bs.inputs['IOR'].default_value=1.34;bs.inputs['Transmission Weight'].default_value=1
 m.blend_method='OPAQUE';m.use_screen_refraction=True;m.refraction_depth=.001;m.shadow_method='NONE'
 for side in [-1,1]:
  theta=side*.27;N=Vector((math.sin(theta),-math.cos(theta),.015));U=Vector((math.cos(theta),math.sin(theta),0));V=Vector((0,0,1));C=Vector((side*.167,-1.150,1.724-ground_offset));nr=18;nt=96;vv=[C+N*.042];ff=[];R=.072
  for j in range(1,nr+1):
   r=j/nr
   for k in range(nt):
    t=2*math.pi*k/nt;vv.append(C+U*(R*r*math.cos(t))+V*(R*.96*r*math.sin(t))+N*(.021+.021*math.sqrt(max(0,1-r*r))))
  for k in range(nt):ff.append((0,1+k,1+(k+1)%nt))
  for j in range(nr-1):
   for k in range(nt):
    i=1+j*nt+k;n=1+j*nt+(k+1)%nt;ff.append((i,n,n+nt,i+nt))
  me=bpy.data.meshes.new('Corneal dome '+str(side));me.from_pydata(vv,[],ff);ob=bpy.data.objects.new('Cornea '+str(side),me);root.objects.link(ob);me.materials.append(m)
  for f in me.polygons:f.use_smooth=True
  wall=ob.modifiers.new('Very thin optical wall','SOLIDIFY');wall.thickness=.00035
  for label in ['Softbox eye reflection ','Secondary eye glint ']:
   glint=bpy.data.objects.get(label+str(side))
   if glint:glint.hide_render=True;glint.hide_set(True);glint['web_reflection_fallback']=True
 return m
