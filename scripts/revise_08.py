from pathlib import Path
p=Path(__file__).with_name('build_cat.py');s=p.read_text()
def rep(a,b):
 global s
 assert a in s,a[:110];s=s.replace(a,b)
rep("ears=[];inner_ears=[]", "from mathutils.bvhtree import BVHTree\n_ear_bvh=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())\nears=[];inner_ears=[]")
start=s.index(' vv=[];ff=[];nu=14;nv=18');end=s.index(' for j in range(nv):',start)
s=s[:start]+''' vv=[];ff=[];nu=18;nv=24
 for j in range(nv+1):
  v=j/nv
  for i in range(nu+1):
   u=i/nu;q=2*u-1;seed=Vector((s*(.252+.090*q),-.790,1.895));nearest,norm,_,_=_ear_bvh.find_nearest(seed)
   p0=(nearest-norm*.009) if nearest is not None else seed
   p1=Vector((s*(.275+.075*q),-.866,1.984-.018*q*q))
   p2=Vector((s*(.287+.040*q),-.970,1.939-.009*q*q))
   p3=Vector((s*(.291+.002*q),-1.022,1.891))
   if v<.37:t=v/.37;aa,bb=p0,p1
   elif v<.72:t=(v-.37)/.35;aa,bb=p1,p2
   else:t=(v-.72)/.28;aa,bb=p2,p3
   t=t*t*(3-2*t);vv.append(tuple(aa.lerp(bb,t)))
'''+s[end:]
rep("sol.thickness=.022", "sol.thickness=.012")
rep("ev=[(s*.280,-.931,1.905)]", "ev=[(s*.277,-.923,1.911)]")
rep("(s*.280+.046*r*math.cos(t),-.953+.022*(1-r*r),1.905+.041*r*math.sin(t))", "(s*.277+.037*r*math.cos(t),-.943+.020*(1-r*r),1.911+.025*r*math.sin(t))")
rep("furmat.node_tree.nodes.get('Principled BSDF').inputs['Sheen Weight'].default_value=.13", "furmat.node_tree.nodes.get('Principled BSDF').inputs['Sheen Weight'].default_value=.06")
rep("furmat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.18", "furmat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.08")
rep("furmat.shadow_method='NONE'", "furmat.shadow_method='OPAQUE'")
p.write_text(s);print('REVISION_08_APPLIED')
