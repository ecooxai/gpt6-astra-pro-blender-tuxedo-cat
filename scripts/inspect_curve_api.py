import bpy
print('CURVE_DATABLOCKS',[x for x in dir(bpy.data) if 'curve' in x],flush=True)
print('CURVES_TYPES',[x for x in dir(bpy.types) if x in ['Curves','CurvesGeometry','CurveMapping','CurvesPoint','CurveSlice']],flush=True)
if hasattr(bpy.types,'Curves'):print('CURVES_PROPERTIES',list(bpy.types.Curves.bl_rna.properties.keys()),flush=True)
try:
 bpy.ops.object.curves_empty_hair_add();o=bpy.context.object;print('NATIVE_HAIR',o.type,type(o.data).__name__,list(o.data.bl_rna.properties.keys()),flush=True)
 print('GEOMETRY_API',[(x,str(getattr(o.data,x))[:200]) for x in ['curves','points','attributes'] if hasattr(o.data,x)],flush=True)
except Exception as e:print('CURVES_OPERATOR_ERROR',str(e),flush=True)
for key in ['GeometryNodeMeshToCurve','GeometryNodeSetCurveRadius','GeometryNodeCurveSplineType','GeometryNodeCurveSetHandles']:
 try:
  ng=bpy.data.node_groups.new('test '+key,'GeometryNodeTree');n=ng.nodes.new(key);print('NODE',key,'INPUTS',[(p.name,p.bl_idname) for p in n.inputs], 'PROPS',list(n.bl_rna.properties.keys()),flush=True)
 except Exception as e:print('NODE_ERROR',key,str(e),flush=True)
