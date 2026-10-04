from pathlib import Path
p=Path(__file__).with_name('build_cat.py');s=p.read_text()
def rep(a,b):
 global s
 assert a in s,a[:110];s=s.replace(a,b)
rep("P=Path(__file__).resolve().parents[1]", "P=Path(__file__).resolve().parents[1]\nsys.path.insert(0,str(P/'scripts'))\nfrom coat_field import coat_color, install_coat_shader\n(P/'preview/renders').mkdir(parents=True,exist_ok=True)\n(P/'preview/downloads').mkdir(parents=True,exist_ok=True)")
start=s.index('def coatcolor(p):');end=s.index('def paint(o,fn):',start);s=s[:start]+'coatcolor=coat_color\n'+s[end:]
rep("for i,v in enumerate(o.data.vertices):co.data[i].color=(*fn(o.matrix_world@v.co),1)","pos=o.data.attributes.new(name='CoatPosition',type='FLOAT_VECTOR',domain='POINT')\n for i,v in enumerate(o.data.vertices):\n  pp=o.matrix_world@v.co;co.data[i].color=(*fn(pp),1);pos.data[i].vector=pp")
rep("paint(body,coatcolor)","paint(body,coatcolor)\ninstall_coat_shader(coat)")
rep("span=.222*max(.045,1-.99*v**1.3)","span=.220*max(.035,1-.98*v)")
rep("xx=.274+.065*v+(u-.5)*span", "xx=.288+.012*math.sin(math.pi*v)+(u-.5)*span")
rep("yy=-.815-.215*v+.022*math.cos((u-.5)*math.pi)","yy=-.806-.225*v+.012*math.cos((u-.5)*math.pi)")
rep("zz=1.900+.080*math.sin(math.pi*v)-.035*v-.020*v**3-.030*(2*u-1)**2", "zz=1.884+.128*math.sin(math.pi*v*.87)-.037*v-.030*(2*u-1)**2")
rep("inn=ell('Subtle inner ear '+str(s),(s*.292,-.991,1.883),(.055,.012,.033),pink,seg=40,rings=24);inn.rotation_euler.y=s*.45;inner_ears.append(inn)","""ev=[(s*.289,-.961,1.898)];ef=[];en=64;er=8
 for j in range(1,er+1):
  r=j/er
  for k in range(en):
   t=k*2*math.pi/en;ev.append((s*.289+.054*r*math.cos(t),-.986+.025*(1-r*r),1.898+.052*r*math.sin(t)))
 for k in range(en):ef.append((0,1+k,1+(k+1)%en))
 for j in range(er-1):
  for k in range(en):
   q=1+j*en+k;nq=1+j*en+(k+1)%en;ef.append((q,nq,nq+en,q+en))
 em=bpy.data.meshes.new('Concave ear bowl '+str(s));em.from_pydata(ev,[],ef);em.update();inn=bpy.data.objects.new('Subtle inner ear '+str(s),em);root.objects.link(inn);em.materials.append(pink);em.materials.append(black)
 for poly in em.polygons:poly.use_smooth=True
 wall=inn.modifiers.new('Soft cartilage wall','SOLIDIFY');wall.thickness=.003;wall.material_offset=1;wall.material_offset_rim=1;inner_ears.append(inn)""")
rep("for s in [-1,1]:\n theta=s*.43", "from mathutils.bvhtree import BVHTree\n_body_bvh=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());eye_lids=[]\nfor s in [-1,1]:\n theta=s*.43")
rep("(.076,.041,.081)", "(.075,.032,.079)")
rep("# Shaped nose, philtrum, lips and whisker follicles.","""# Annular eyelid tissue joins the corneal margin to the actual sculpt surface.
 lv=[];lf=[];ln=96;lr=5
 for j in range(lr+1):
  w=j/lr;ease=w*w*(3-2*w)
  for k in range(ln):
   ang=k*2*math.pi/ln;inner=C+U*(.0725*math.cos(ang))+V*(.0785*math.sin(ang))+N*.029
   projected=C+U*(.106*math.cos(ang))+V*(.112*math.sin(ang));hit=_body_bvh.ray_cast(projected+N*.4,-N,1.0)[0]
   if hit is None:hit=projected-N*.025
   lv.append(inner.lerp(hit,ease)+N*(.0035*math.sin(math.pi*w)))
 for j in range(lr):
  for k in range(ln):
   q=j*ln+k;nq=j*ln+(k+1)%ln;lf.append((q,nq,nq+ln,q+ln))
 lm=bpy.data.meshes.new('Anatomical eyelid transition '+str(s));lm.from_pydata(lv,[],lf);lm.update();lid=bpy.data.objects.new('Sculpted eyelids '+str(s),lm);root.objects.link(lid);lm.materials.append(rim);lm.materials.append(coat)
 for i,poly in enumerate(lm.polygons):poly.use_smooth=True;poly.material_index=0 if i<ln else 1
 paint(lid,coatcolor);sub=lid.modifiers.new('Soft eyelid tissue','SUBSURF');sub.levels=1;eye_lids.append(lid)
# Shaped nose, philtrum, lips and whisker follicles.""")
rep("strand_curve('Philtrum',[(0,-1.324,1.519),(0,-1.329,1.495),(0,-1.323,1.475)],.005,rim)", "strand_curve('Philtrum',[(0,-1.324,1.519),(0,-1.329,1.495),(0,-1.323,1.475)],.003,rim)")
rep("],6),.003,rim)","],6),.0016,rim)")
rep("# Deterministic surface-area strand sampling", "nostrilmat=mat('Nose creases • soft charcoal',(.0012,.001,.001),.83)\nfor side in [-1,1]:\n nostril=ell('Nostril '+str(side),(side*.035,-1.339,1.538),(.011,.004,.0055),nostrilmat,seg=24,rings=16);nostril.rotation_euler.y=side*.24\nnb=nosemat.node_tree.nodes;nt=nb.new('ShaderNodeTexNoise');nt.inputs['Scale'].default_value=95;nt.inputs['Detail'].default_value=2;np=nb.new('ShaderNodeBump');np.inputs['Strength'].default_value=.10;np.inputs['Distance'].default_value=.0015;nosemat.node_tree.links.new(nt.outputs['Fac'],np.inputs['Height']);nosemat.node_tree.links.new(np.outputs['Normal'],nb.get('Principled BSDF').inputs['Normal'])\n# Deterministic surface-area strand sampling")
rep("if y<-1.287 and abs(x)<.067", "if name.startswith('Lid groom') and ((abs(x)-.179)/.079)**2+((z-1.724)/.085)**2<1.0:continue\n  if y<-1.287 and abs(x)<.067")
rep("if name.startswith('Inner ear'):direction", "if name.startswith('Lid groom'):direction=Vector((x-math.copysign(.179,x),-.01,z-1.724));length=.006+rng.random()*.006\n  elif name.startswith('Inner ear'):direction")
rep("for o in inner_ears:groom_surface(o,210,lambda p:(.36,.29,.235),'Inner ear groom '+o.name,.66)", "for o in inner_ears:groom_surface(o,360,lambda p:(.26,.225,.20),'Inner ear groom '+o.name,.66)\nfor o in eye_lids:groom_surface(o,1600,coatcolor,'Lid groom '+o.name,.72)")
p.write_text(s);print('REVISION_05_APPLIED')
