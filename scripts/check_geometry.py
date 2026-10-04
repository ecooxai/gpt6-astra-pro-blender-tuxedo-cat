"""Structural checks of our own Blender mesh. No reference-image analysis."""
import bpy,math,json,os
from pathlib import Path
from collections import Counter
P=Path(__file__).resolve().parents[1];B=Path(os.environ.get('CAT_BUILD_DIR','/build/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat'))
bpy.ops.wm.open_mainfile(filepath=str(B/'GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat.blend'))
body=bpy.data.objects['CAT • unified anatomical sculpt'];vs=[body.matrix_world@v.co for v in body.data.vertices];edges=Counter()
for poly in body.data.polygons:
 for e in poly.edge_keys:edges[e]+=1
feet={}
for side in [-1,1]:
 for limb in ['front','rear']:
  pts=[v for v in vs if side*v.x>.09 and v.z<.19 and ((v.y<-.66) if limb=='front' else (.54<v.y<.95))]
  feet[f'{limb}_{"left" if side<0 else "right"}']={'min_z':min(v.z for v in pts),'vertices':len(pts)}
result={'revision':bpy.context.scene.get('revision'),'vertices_body':len(vs),'polygons_body':len(body.data.polygons),'body_closed_edges':all(n==2 for n in edges.values()),'nonfinite_body_vertices':sum(not all(math.isfinite(v) for v in p) for p in vs),'bounds':{'min':[min(v[i] for v in vs) for i in range(3)],'max':[max(v[i] for v in vs) for i in range(3)]},'feet':feet,'ground_plane_z':bpy.data.objects['Studio ground'].location.z,'paw_left_right_height_delta':max(abs(feet[f'{leg}_left']['min_z']-feet[f'{leg}_right']['min_z']) for leg in ['front','rear']),'actual_groom_strands':sum(o.get('actual_strands',0) for o in bpy.data.collections['GROOM • authored strands'].objects),'note':'Structural validation only. This does not establish visual likeness or an independent quality score.'}
(P/'logs/geometry-tests.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2),flush=True)
assert result['body_closed_edges'] and result['nonfinite_body_vertices']==0
