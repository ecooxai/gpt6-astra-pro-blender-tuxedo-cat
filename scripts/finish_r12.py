"""Unify eyelid pigmentation and retain original authored eyelid/fiber geometry."""
import bpy,os
from pathlib import Path
P=Path(__file__).resolve().parents[1];B=Path(os.environ.get('CAT_BUILD_DIR','/build/'+P.name));fn=B/(P.name+'.blend');bpy.ops.wm.open_mainfile(filepath=str(fn))
m=bpy.data.materials.new('12 • matte black eyelid skin');m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.0012,.0014,.0016,1);bs.inputs['Roughness'].default_value=.96;bs.inputs['Specular IOR Level'].default_value=0
for ob in bpy.data.objects:
 if ob.name.startswith('Sculpted eyelids '):
  ob.data.materials.clear();ob.data.materials.append(m)
  for f in ob.data.polygons:f.material_index=0
 if ob.name.startswith('Softbox eye reflection '):ob.scale*=.72
bpy.ops.wm.save_as_mainfile(filepath=str(fn),compress=True);print('EYELID_PIGMENT_UNIFIED',flush=True)
