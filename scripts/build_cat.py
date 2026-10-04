"""Original cat sculpt and groom. GPT-6 Astra Pro / mcp-colabdev / Blender EEVEE.
No external meshes, textures, images or downloaded character assets are read.
Coordinates: Z up, face toward -Y. Deterministic procedural geometry.
"""
import bpy, math, random, bisect, json, os, sys, time, argparse
from pathlib import Path
from mathutils import Vector
from mathutils.noise import noise_vector, noise
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P/'scripts'))
from coat_field import coat_color, install_coat_shader
from native_groom import create_native_groom, add_cornea
(P/'preview/renders').mkdir(parents=True,exist_ok=True)
(P/'preview/downloads').mkdir(parents=True,exist_ok=True)
B=Path(os.environ.get('CAT_BUILD_DIR','/build/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat'));B.mkdir(parents=True,exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--revision',type=int,default=1);parser.add_argument('--fur',type=int,default=65000);parser.add_argument('--resolution',type=int,default=900);parser.add_argument('--views',default='hero,front,left,right,rear');parser.add_argument('--samples',type=int,default=40)
a=parser.parse_args(sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [])
random.seed(71);t0=time.time();bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for d in bpy.data.materials:bpy.data.materials.remove(d)
scene=bpy.context.scene;scene.render.engine='BLENDER_EEVEE';scene.eevee.taa_render_samples=a.samples;scene.eevee.use_gtao=True;scene.eevee.gtao_distance=.14;scene.eevee.gtao_factor=.88;scene.eevee.use_soft_shadows=True
scene.render.resolution_x=a.resolution;scene.render.resolution_y=a.resolution;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.12
scene.world.color=(.45,.45,.45);scene.world.use_nodes=True;scene.world.node_tree.nodes.get('Background').inputs[0].default_value=(.65,.69,.75,1);scene.world.node_tree.nodes.get('Background').inputs[1].default_value=.27
root=bpy.data.collections.new('CAT • original geometry');scene.collection.children.link(root)
groomcol=bpy.data.collections.new('GROOM • authored strands');scene.collection.children.link(groomcol)
guidecol=bpy.data.collections.new('GUIDES • editable fiber centerlines');scene.collection.children.link(guidecol)
studiocol=bpy.data.collections.new('STUDIO • camera and lights');scene.collection.children.link(studiocol)
def move(o,col):
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);return o
def mat(name,c,rough=.5,metal=0):
 m=bpy.data.materials.new(name);m.use_nodes=True;b=m.node_tree.nodes.get('Principled BSDF');b.inputs['Base Color'].default_value=(*c,1);b.inputs['Roughness'].default_value=rough;b.inputs['Metallic'].default_value=metal;m.diffuse_color=(*c,1);return m
def attrmat(name,rough=.65):
 m=mat(name,(1,1,1),rough);n=m.node_tree.nodes;b=n.get('Principled BSDF');v=n.new('ShaderNodeVertexColor');v.layer_name='Coat';m.node_tree.links.new(v.outputs['Color'],b.inputs['Base Color']);return m
coat=attrmat('01 • procedural black and warm-white coat',.8)
n=coat.node_tree.nodes;b=n.get('Principled BSDF');b.inputs['Subsurface Weight'].default_value=.04;b.inputs['Subsurface Radius'].default_value=(.8,.5,.3);b.inputs['Sheen Weight'].default_value=.08; b.inputs['Specular IOR Level'].default_value=.13
tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=240;tex.inputs['Detail'].default_value=2.3;bu=n.new('ShaderNodeBump');bu.inputs['Strength'].default_value=.16;bu.inputs['Distance'].default_value=.009;coat.node_tree.links.new(tex.outputs['Fac'],bu.inputs['Height']);coat.node_tree.links.new(bu.outputs['Normal'],b.inputs['Normal'])
furmat=attrmat('02 • individually colored fibers',.76);furmat.node_tree.nodes.get('Principled BSDF').inputs['Sheen Weight'].default_value=.13; furmat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.18
black=mat('03 • soft black cartilage',(.0032,.0038,.0047),.93)
black.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.12
rim=mat('04 • wet dark eyelid',(.013,.009,.006),.3)
nosemat=mat('05 • charcoal rose nose',(.010,.009,.011),.40)
pink=mat('06 • muted warm ear interior',(.067,.039,.035),.92)
white=mat('07 • warm ivory whiskers',(.83,.81,.73),.47)
pupilmat=mat('08 • deep pupil',(.001,.0015,.0011),.1)
catchmat=mat('09 • corneal studio reflection',(.95,.98,1),.08);cb=catchmat.node_tree.nodes.get('Principled BSDF');cb.inputs['Emission Color'].default_value=(.7,.77,.8,1);cb.inputs['Emission Strength'].default_value=.4
irisMat=attrmat('10 • radial golden iris fibers',.28)
fa=furmat.node_tree.nodes.new('ShaderNodeAttribute');fa.attribute_name='Coat';furmat.node_tree.links.new(fa.outputs['Color'],furmat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
parts=[]
def ell(name,loc,scale,material=None,join=False,seg=48,rings=32):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for p in o.data.polygons:p.use_smooth=True
 if material:o.data.materials.append(material)
 move(o,root)
 if join:parts.append(o)
 return o
# Muscular forms merge into one skin surface, including the feet.
ell('Torso • ribcage',(0,.02,1.13),(.36,.86,.405),join=True)
ell('Abdomen',(0,.38,1.055),(.32,.51,.34),join=True)
ell('Pelvis',(0,.65,1.15),(.355,.36,.395),join=True)
ell('Shoulders',(0,-.49,1.25),(.33,.37,.40),join=True)
ell('Neck • chest ruff',(0,-.69,1.41),(.305,.31,.37),join=True)
ell('Full white chest',(0,-.705,1.18),(.255,.244,.365),join=True)
ell('Cranium',(0,-.88,1.70),(.35,.303,.292),join=True)
ell('Brow',(0,-.978,1.79),(.31,.218,.18),join=True)
for s in [-1,1]:
 ell('Cheek '+str(s),(s*.195,-.990,1.60),(.173,.207,.187),join=True)
 ell('Muzzle pillow '+str(s),(s*.101,-1.173,1.502),(.138,.139,.095),join=True)
ell('Chin',(0,-1.118,1.412),(.192,.17,.079),join=True)
def limb(name,rings):
 vv=[];ff=[];ns=24
 for j,(x,y,z,rx,ry) in enumerate(rings):
  for k in range(ns):
   t=k*2*math.pi/ns;vv.append((x+rx*math.cos(t),y+ry*math.sin(t),z))
  if j:
   for k in range(ns):ff.append(((j-1)*ns+k,(j-1)*ns+(k+1)%ns,j*ns+(k+1)%ns,j*ns+k))
 ff.extend([tuple(reversed(range(ns))),tuple((len(rings)-1)*ns+k for k in range(ns))])
 me=bpy.data.meshes.new(name);me.from_pydata(vv,[],ff);o=bpy.data.objects.new(name,me);root.objects.link(o);parts.append(o)
for s in [-1,1]:
 x=s*.214
 limb('Continuous front leg '+str(s),[(x,-.58,1.12,.14,.16),(x,-.59,.94,.133,.153),(x,-.605,.76,.12,.137),(x,-.622,.57,.104,.12),(x,-.64,.38,.088,.105),(x,-.659,.19,.086,.109),(x,-.682,.105,.096,.122)])
 ell('Front paw '+str(s),(x,-.736,.081),(.123,.163,.071),join=True)
 for k in range(4):ell('Front toe '+str(s)+'.'+str(k),(x+(k-1.5)*.051,-.861+abs(k-1.5)*.014,.066),(.037,.068,.049),join=True,seg=28,rings=20)
 ell('Hind haunch '+str(s),(s*.249,.646,.969),(.16,.231,.28),join=True)
 limb('Continuous angular hind leg '+str(s),[(s*.254,.66,.96,.148,.178),(s*.261,.617,.77,.13,.162),(s*.265,.665,.60,.11,.128),(s*.262,.757,.42,.082,.089),(s*.258,.80,.25,.073,.079),(s*.258,.788,.11,.082,.098)])
 ell('Hind paw '+str(s),(s*.257,.715,.077),(.113,.16,.066),join=True)
 for k in range(4):ell('Rear toe '+str(s)+'.'+str(k),(s*.257+(k-1.5)*.047,.604+abs(k-1.5)*.011,.057),(.033,.065,.045),join=True,seg=24,rings=16)
# Curved, full-bodied tail with smoothly varying circular sections.
def catmull(ps,steps=9):
 ps=[Vector(p) for p in ps];out=[]
 for i in range(len(ps)-1):
  p0=ps[max(0,i-1)];p1=ps[i];p2=ps[i+1];p3=ps[min(len(ps)-1,i+2)]
  for j in range(steps):
   t=j/steps;out.append(.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
 out.append(ps[-1]);return out
tailpath=catmull([(0,.83,1.27),(-.07,1.07,1.46),(-.21,1.31,1.69),(-.36,1.43,1.94),(-.42,1.41,2.14),(-.43,1.33,2.24)],10)
verts=[];faces=[];ns=20
for i,p in enumerate(tailpath):
 tang=(tailpath[min(i+1,len(tailpath)-1)]-tailpath[max(0,i-1)]).normalized();u=Vector((1,0,0));v=tang.cross(u).normalized();t=i/(len(tailpath)-1);r=.106+.023*math.sin(math.pi*t)-.026*t**7
 for j in range(ns):verts.append(p+r*(u*math.cos(j*2*math.pi/ns)+v*math.sin(j*2*math.pi/ns)))
 if i:
  for j in range(ns):faces.append(((i-1)*ns+j,(i-1)*ns+(j+1)%ns,i*ns+(j+1)%ns,i*ns+j))
faces += [tuple(reversed(range(ns))),tuple((len(tailpath)-1)*ns+j for j in range(ns))]
mesh=bpy.data.meshes.new('Tail swept topology');mesh.from_pydata(verts,[],faces);o=bpy.data.objects.new('Upright curved tail',mesh);root.objects.link(o);parts.append(o)
ell('Tail rounded tip',tailpath[-1],(.082,.080,.084),join=True)
bpy.ops.object.select_all(action='DESELECT')
for o in parts:o.select_set(True)
bpy.context.view_layer.objects.active=parts[0];bpy.ops.object.join();body=bpy.context.object;body.name='CAT • unified anatomical sculpt'
bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
rem=body.modifiers.new('Continuous skin • voxel union','REMESH');rem.mode='VOXEL';rem.voxel_size=.012;rem.use_smooth_shade=True;bpy.ops.object.modifier_apply(modifier=rem.name)
vg=body.vertex_groups.new(name='Preserve small toe contours')
for v in body.data.vertices:vg.add([v.index],.18 if v.co.z<.19 else 1.0,'REPLACE')
sm=body.modifiers.new('Organic relaxation','SMOOTH');sm.factor=1.2;sm.iterations=5;sm.vertex_group=vg.name;bpy.ops.object.modifier_apply(modifier=sm.name)
sub=body.modifiers.new('Skin surface subdivision','SUBSURF');sub.levels=1;bpy.ops.object.modifier_apply(modifier=sub.name)
# Anatomical eye sockets blend the eyelid into the cheek, rather than placing eyes on top.
for v in body.data.vertices:
 x,y,z=v.co
 if y< -1.02 and z>1.57:
  rr=((abs(x)-.174)/.083)**2+((z-1.724)/.088)**2
  if rr<2.25:
   v.co.y += .062*(1-rr/2.25)**2*max(0,min(1,(-y-1.02)/.08))
 if v.co.z<.062:v.co.z=max(.007,.010+(v.co.z-.013)*.7)
body.data.update()
body.data.materials.clear();body.data.materials.append(coat)
for p in body.data.polygons:p.use_smooth=True
# The reference markings are recreated analytically, never projected from an image.
coatcolor=coat_color
def paint(o,fn):
 co=o.data.color_attributes.new(name='Coat',type='FLOAT_COLOR',domain='POINT')
 pos=o.data.attributes.new(name='CoatPosition',type='FLOAT_VECTOR',domain='POINT')
 for i,v in enumerate(o.data.vertices):
  pp=o.matrix_world@v.co;co.data[i].color=(*fn(pp),1);pos.data[i].vector=pp
paint(body,coatcolor)
install_coat_shader(coat)
# Folded ears: the cartilage travels up, rolls forward and turns down into a rounded tip.
ears=[];inner_ears=[]
for s in [-1,1]:
 vv=[];ff=[];nu=14;nv=18
 for j in range(nv+1):
  v=j/nv;span=.205*max(.035,1-.98*v)
  for i in range(nu+1):
   u=i/nu;xx=.277+.008*math.sin(math.pi*v)+(u-.5)*span
   yy=-.806-.225*v+.012*math.cos((u-.5)*math.pi)
   zz=1.884+.103*math.sin(math.pi*v*.87)-.037*v-.030*(2*u-1)**2
   vv.append((s*xx,yy,zz))
 for j in range(nv):
  for i in range(nu):
   k=j*(nu+1)+i;face=(k,k+1,k+nu+2,k+nu+1);ff.append(face if s==1 else face[::-1])
 me=bpy.data.meshes.new('Folded cartilage topology');me.from_pydata(vv,[],ff);o=bpy.data.objects.new('Folded ear '+str(s),me);root.objects.link(o);o.data.materials.append(black)
 sol=o.modifiers.new('Soft cartilage thickness','SOLIDIFY');sol.thickness=.022;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=sol.name)
 su=o.modifiers.new('Rounded ear fold','SUBSURF');su.levels=2;bpy.ops.object.modifier_apply(modifier=su.name)
 for p in o.data.polygons:p.use_smooth=True
 ears.append(o)
 ev=[(s*.280,-.931,1.905)];ef=[];en=64;er=8
 for j in range(1,er+1):
  r=j/er
  for k in range(en):
   t=k*2*math.pi/en;ev.append((s*.280+.046*r*math.cos(t),-.953+.022*(1-r*r),1.905+.041*r*math.sin(t)))
 for k in range(en):ef.append((0,1+k,1+(k+1)%en))
 for j in range(er-1):
  for k in range(en):
   q=1+j*en+k;nq=1+j*en+(k+1)%en;ef.append((q,nq,nq+en,q+en))
 em=bpy.data.meshes.new('Concave ear bowl '+str(s));em.from_pydata(ev,[],ef);em.update();inn=bpy.data.objects.new('Subtle inner ear '+str(s),em);root.objects.link(inn);em.materials.append(pink);em.materials.append(black)
 for poly in em.polygons:poly.use_smooth=True
 wall=inn.modifiers.new('Soft cartilage wall','SOLIDIFY');wall.thickness=.003;wall.material_offset=0;wall.material_offset_rim=0;inner_ears.append(inn)
# Eye construction uses an embedded dark limbus, curved radial iris, vertical pupil and explicit small reflections.
from mathutils.bvhtree import BVHTree
_body_bvh=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get());eye_lids=[]
for s in [-1,1]:
 theta=s*.43;N=Vector((math.sin(theta),-math.cos(theta),.015));U=Vector((math.cos(theta),math.sin(theta),0));V=Vector((0,0,1));C=Vector((s*.157,-1.134,1.724))
 eye=ell('Eye socket '+str(s),C,(.073,.027,.078),rim,seg=64,rings=48);eye.rotation_euler.z=theta
 irisR=.0695;nr=22;nt=192;iv=[C+N*.052];ic=[(.36,.25,.04,1)];iff=[]
 for j in range(1,nr+1):
  r=j/nr
  for k in range(nt):
   ang=2*math.pi*k/nt;xx=irisR*r*math.cos(ang);zz=irisR*1.075*r*math.sin(ang);d=.028+.024*math.sqrt(max(0,1-r*r));iv.append(C+U*xx+V*zz+N*d)
   rays=.5+.20*math.sin(ang*97+2.3*math.sin(ang*23)+r*7)+.15*math.sin(ang*173-r*12)+.12*math.sin(ang*51+r*20)
   border=max(0,min(1,(1-r)/.055));inner=.7+.3*min(1,r/.35);col=(.35+.21*rays,.26+.17*rays,.025+.050*rays)
   ic.append(tuple(v*border*inner+.004*(1-border) for v in col)+(1,))
 for k in range(nt):iff.append((0,1+k,1+(k+1)%nt))
 for j in range(nr-1):
  for k in range(nt):
   idx=1+j*nt+k;nxt=1+j*nt+(k+1)%nt;iff.append((idx,nxt,nxt+nt,idx+nt))
 me=bpy.data.meshes.new('Radial iris '+str(s));me.from_pydata(iv,[],iff);eo=bpy.data.objects.new('Gold iris '+str(s),me);root.objects.link(eo);me.materials.append(irisMat);co=me.color_attributes.new(name='Coat',type='FLOAT_COLOR',domain='POINT')
 for i,c in enumerate(ic):co.data[i].color=c
 for po in me.polygons:po.use_smooth=True
 # Convex slit follows the front of the iris.
 pv=[C+N*.055];pf=[]
 for k in range(96):
  ang=k*math.pi*2/96;xx=.030*math.cos(ang);zz=.048*math.sin(ang);rr=(xx/irisR)**2+(zz/(irisR*1.075))**2;pv.append(C+U*xx+V*zz+N*(.031+.024*math.sqrt(max(0,1-rr))))
 for k in range(96):pf.append((0,k+1,(k+1)%96+1))
 me=bpy.data.meshes.new('Pupil slit');me.from_pydata(pv,[],pf);po=bpy.data.objects.new('Vertical pupil '+str(s),me);root.objects.link(po);me.materials.append(pupilmat)
 for poly in me.polygons:poly.use_smooth=True
 hi=ell('Softbox eye reflection '+str(s),C+U*(-.017)+V*.027+N*.053,(.009,.003,.012),catchmat,seg=32,rings=20);hi.rotation_euler.z=theta;hi.rotation_euler.y=-.25
 hi=ell('Secondary eye glint '+str(s),C+U*.021+V*(-.021)+N*.052,(.003,.002,.004),catchmat,seg=20,rings=12);hi.rotation_euler.z=theta
# Annular eyelid tissue joins the corneal margin to the actual sculpt surface.
 lv=[];lf=[];ln=96;lr=5
 for j in range(lr+1):
  w=j/lr;ease=w*w*(3-2*w)
  for k in range(ln):
   ang=k*2*math.pi/ln;inner=C+U*(.0725*math.cos(ang))+V*(.0785*math.sin(ang))+N*.029
   projected=C+U*(.083*math.cos(ang))+V*(.088*math.sin(ang));hit=_body_bvh.ray_cast(projected+N*.4,-N,1.0)[0]
   if hit is None:hit=projected-N*.025
   lv.append(inner.lerp(hit,ease)+N*(.0015*math.sin(math.pi*w)))
 for j in range(lr):
  for k in range(ln):
   q=j*ln+k;nq=j*ln+(k+1)%ln;lf.append((q,nq,nq+ln,q+ln))
 lm=bpy.data.meshes.new('Anatomical eyelid transition '+str(s));lm.from_pydata(lv,[],lf);lm.update();lid=bpy.data.objects.new('Sculpted eyelids '+str(s),lm);root.objects.link(lid);lm.materials.append(rim);lm.materials.append(coat)
 for i,poly in enumerate(lm.polygons):poly.use_smooth=True;poly.material_index=1
 paint(lid,coatcolor);sub=lid.modifiers.new('Soft eyelid tissue','SUBSURF');sub.levels=1;eye_lids.append(lid)
# Shaped nose, philtrum, lips and whisker follicles.
vs=[(-.062,-1.299,1.555),(.062,-1.299,1.555),(.049,-1.34,1.548),(0,-1.352,1.508),(-.049,-1.34,1.548),(0,-1.282,1.513)]
fs=[(0,1,2,4),(4,2,3),(0,4,3,5),(1,5,3,2),(0,5,1)]
me=bpy.data.meshes.new('Nose heart topology');me.from_pydata(vs,[],fs);nose=bpy.data.objects.new('Soft triangular nose',me);root.objects.link(nose);me.materials.append(nosemat);be=nose.modifiers.new('Rounded nose edges','BEVEL');be.width=.012;be.segments=3;su=nose.modifiers.new('Nose softness','SUBSURF');su.levels=2
for p in me.polygons:p.use_smooth=True
def strand_curve(name,points,radius,material,col=root):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=2;cu.bevel_depth=radius;cu.bevel_resolution=2;sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for i,p in enumerate(points):sp.points[i].co=(*p,1);sp.points[i].radius=max(.12,(1-i/(len(points)-1))**.6)
 ob=bpy.data.objects.new(name,cu);col.objects.link(ob);cu.materials.append(material);return ob
strand_curve('Philtrum',[(0,-1.324,1.519),(0,-1.329,1.495),(0,-1.323,1.475)],.003,rim)
for s in [-1,1]:
 strand_curve('Muzzle lip '+str(s),catmull([(0,-1.323,1.475),(s*.035,-1.307,1.462),(s*.091,-1.285,1.464),(s*.135,-1.248,1.487)],6),.0016,rim)
 for j in range(10):
  rr=random.Random(800+j);z=1.492+(j%4-1.5)*.022;xx=.091+(j//4)*.031;yy=-1.284+(j//4)*.017
  start=Vector((s*xx,yy,z));end=Vector((s*(.46+rr.random()*.14),-1.19+rr.uniform(-.19,.12),z+rr.uniform(-.15,.14)))
  mid=start.lerp(end,.48)+Vector((0,-.045,.026));pts=catmull([start,start.lerp(mid,.4),mid,end],5)
  strand_curve('Mystacial whisker '+str(s)+'.'+str(j),pts,.0011+rr.random()*.0004,white)
  ell('Whisker root '+str(s)+'.'+str(j),start,(.003,.002,.003),nosemat,seg=8,rings=6)
 for j in range(3):
  start=Vector((s*(.135+j*.041),-1.12,1.83+j*.014));end=start+Vector((s*(.047+j*.033),-.045-j*.008,.106+j*.017));strand_curve('Brow whisker '+str(s)+'.'+str(j),catmull([start,start.lerp(end,.5)+Vector((0,-.025,.01)),end],7),.0009,white)
print('SCULPT_READY',len(body.data.vertices),'vertices',flush=True)
nostrilmat=mat('Nose creases • soft charcoal',(.0012,.001,.001),.83)
for side in [-1,1]:
 nostril=ell('Nostril '+str(side),(side*.031,-1.333,1.539),(.004,.001,.002),nostrilmat,seg=24,rings=16);nostril.rotation_euler.y=side*.24
nb=nosemat.node_tree.nodes;nt=nb.new('ShaderNodeTexNoise');nt.inputs['Scale'].default_value=95;nt.inputs['Detail'].default_value=2;np=nb.new('ShaderNodeBump');np.inputs['Strength'].default_value=.10;np.inputs['Distance'].default_value=.0015;nosemat.node_tree.links.new(nt.outputs['Fac'],np.inputs['Height']);nosemat.node_tree.links.new(np.outputs['Normal'],nb.get('Principled BSDF').inputs['Normal'])
# Deterministic surface-area strand sampling of ORIGINAL geometry, not image analysis.
def groom_surface(obj,count,colorfn,name,length_scale=1):
 me=obj.data;me.calc_loop_triangles();tris=list(me.loop_triangles);cum=[];tot=0
 for tri in tris:tot+=tri.area;cum.append(tot)
 vs=[];radii=[];cols=[];rng=random.Random(171+count);M=obj.matrix_world;R=M.to_3x3()
 for h in range(count):
  tr=tris[bisect.bisect_left(cum,rng.random()*tot)];a0,b0,c0=[me.vertices[k] for k in tr.vertices];r1=math.sqrt(rng.random());r2=rng.random();weights=(1-r1,r1*(1-r2),r1*r2);p=M@(a0.co*weights[0]+b0.co*weights[1]+c0.co*weights[2]);normal=(R@(a0.normal*weights[0]+b0.normal*weights[1]+c0.normal*weights[2])).normalized();x,y,z=p
  # Keep the corneas and nose unobstructed.
  if name=='Body groom' and y<-1.09 and z>1.60 and ((abs(x)-.179)/.074)**2+((z-1.724)/.080)**2<1.03:continue
  if name.startswith('Lid groom') and ((abs(x)-.179)/.073)**2+((z-1.724)/.079)**2<1.0:continue
  if y<-1.287 and abs(x)<.067 and 1.502<z<1.574:continue
  if z<.031:continue
  if name.startswith('Lid groom'):direction=Vector((x-math.copysign(.179,x),-.01,z-1.724));length=.004+rng.random()*.004
  elif name.startswith('Inner ear'):direction=Vector((x*.7,-.4,1));length=.018+rng.random()*.029
  elif name.startswith('Ear groom'):direction=Vector((x*.8,-.2,.45));length=.012+rng.random()*.013
  elif y>1.0 and z>1.35:direction=Vector((0,.5,1));length=.028+rng.random()*.021
  elif z>1.40 and y<-.75:
   direction=Vector((x*2,.15,-.65));length=(.029+rng.random()*.022) if z<1.59 else (.009+rng.random()*.008)
   if y<-1.20:length*=.65;direction=Vector((x*3,0,-.2))
  elif z<.70:direction=Vector((0,-.07,-1));length=.019+rng.random()*.012
  else:direction=Vector((x*.8,.45,-.55));length=.027+rng.random()*.022
  if rng.random()<.12:length*=1.35
  length*=length_scale
  if name=='Body groom' and y<-.97 and z>1.57 and ((abs(x)-.179)/.16)**2+((z-1.724)/.16)**2<1.0:direction=Vector((x-math.copysign(.179,x),-.02,z-1.724))
  tangent=direction-normal*direction.dot(normal)
  if tangent.length<.01:tangent=normal.cross(Vector((.3,.9,.4)))
  tangent.normalize();jitter=Vector((rng.uniform(-1,1),rng.uniform(-1,1),rng.uniform(-1,1)))*.16
  axis=(normal*.53+tangent*.79+jitter).normalized();u=axis.cross(Vector((.12,.13,1)))
  if u.length<.01:u=axis.cross(Vector((1,0,0)))
  u.normalize();v=axis.cross(u).normalized();col=colorfn(p);variation=rng.uniform(.73,1.17);col=tuple(min(.95,c*variation) for c in col);radius=rng.uniform(.00037,.00076)*length_scale
  for t in [0,.36,.72,1]:
   cp=p+normal*(length*(.49*t-.12*t*t))+tangent*(length*.86*t)+jitter*(length*t*t)
   vs.append(tuple(cp));radii.append(radius*(1-.94*t));cols.append((*col,1))
 ob=create_native_groom(name,vs,radii,cols,furmat,groomcol,guidecol,count)
 print('GROOM_READY',name,ob['actual_strands'],'native curves',flush=True);return ob
hair=groom_surface(body,a.fur,coatcolor,'Body groom')
for o in ears:groom_surface(o,3000,lambda p:(.0032,.0038,.0047),'Ear groom '+o.name,.86)
for o in inner_ears:groom_surface(o,360,lambda p:(.26,.225,.20),'Inner ear groom '+o.name,.66)
for o in eye_lids:groom_surface(o,1600,coatcolor,'Lid groom '+o.name,.72)
# Put the lowest original skin point on the studio plane without altering coat coordinates.
ground_offset=min((body.matrix_world@v.co).z for v in body.data.vertices)
for col in [root,groomcol,guidecol]:
 for ob in col.objects:ob.location.z-=ground_offset
scene['ground_offset']=ground_offset
add_cornea(root,ground_offset)
furmat.shadow_method='NONE'
# Studio is purpose-built; no HDRI or backdrop image.
floor=mat('Studio • warm gray',(.64,.66,.635),.88)
fb=floor.node_tree.nodes.get('Principled BSDF');fb.inputs['Emission Color'].default_value=(.64,.66,.635,1);fb.inputs['Emission Strength'].default_value=1.04
bpy.ops.mesh.primitive_plane_add(size=1000,location=(0,0,0));o=bpy.context.object;o.name='Studio ground';o.data.materials.append(floor);move(o,studiocol)
def area(name,loc,power,size,target=(0,0,1),color=(1,1,1)):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=color;o=bpy.data.objects.new(name,d);studiocol.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
area('Large softbox • camera left',(-3,-4.5,6),550,4.0,color=(1,.94,.86))
area('Fill • camera right',(3,-2.0,3.8),340,3.0,color=(.88,.93,1))
area('Coat edge • rear strip',(0,3.5,4.8),540,3.0,color=(1,1,.97))
area('Soft frontal bounce',(0,-4.5,2.05),165,5.0,color=(1,.97,.92))
bpy.data.lights['Soft frontal bounce'].use_shadow=False
bpy.ops.object.camera_add();cam=bpy.context.object;cam.name='Studio camera';move(cam,studiocol);scene.camera=cam;cam.data.type='ORTHO';cam.data.lens=60;cam.data.clip_end=1500
views={'hero':((3.2,-5.7,2.3),(0,.19,1.13),3.45),'front':((0,-7,1.42),(0,.1,1.13),2.86),'left':((-7,-.01,1.42),(0,.19,1.15),3.50),'right':((7,-.01,1.42),(0,.19,1.15),3.50),'rear':((0,7,1.42),(0,.20,1.12),2.92),'detail':((.9,-6,2.0),(0,-.95,1.68),1.12)}
def setcam(v):
 pos,target,scale=views[v];target=Vector(target);pos=Vector(pos);cam.location=target+(pos-target)*4;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
setcam('hero');scene['author']='GPT-6 Astra Pro';scene['tools']='mcp-colabdev / Blender headless EEVEE';scene['revision']=a.revision;scene['assets']='All cat geometry, fibers and materials authored from scratch; reference inspection only.'
blend=B/'GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True);print('SAVED_BLEND',str(blend),flush=True)
for view in a.views.split(','):
 setcam(view);out=P/'preview'/'renders'/('r%02d_%s.png'%(a.revision,view));scene.render.filepath=str(out);bpy.ops.render.render(write_still=True);print('RENDER_DONE',view,str(out),round(time.time()-t0,1),flush=True)
setcam('hero');bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True);print('BUILD_COMPLETE',round(time.time()-t0,1),flush=True)
