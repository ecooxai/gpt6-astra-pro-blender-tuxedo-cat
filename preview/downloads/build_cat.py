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
parser.add_argument('--fast-preview',action='store_true')
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
tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=240;tex.inputs['Detail'].default_value=2.3;bu=n.new('ShaderNodeBump');bu.inputs['Strength'].default_value=.07;bu.inputs['Distance'].default_value=.0016;coat.node_tree.links.new(tex.outputs['Fac'],bu.inputs['Height']);coat.node_tree.links.new(bu.outputs['Normal'],b.inputs['Normal'])
furmat=attrmat('02 • individually colored fibers',.76);furmat.node_tree.nodes.get('Principled BSDF').inputs['Sheen Weight'].default_value=.06; furmat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.08
black=mat('03 • soft black cartilage',(.0032,.0038,.0047),.93)
black.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.12
rim=mat('04 • wet dark eyelid',(.0005,.0007,.0006),.94)
rim.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=0
nosemat=mat('05 • charcoal rose nose',(.010,.009,.011),.40)
lidskin=mat('12 • matte black eyelid skin',(.0012,.0014,.0016),.96);lidskin.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=0
pink=mat('06 • muted warm ear interior',(.067,.039,.035),.92)
white=mat('07 • warm ivory whiskers',(.83,.81,.73),.47)
pupilmat=mat('08 • deep pupil',(.00015,.0002,.00015),.95)
pupilmat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=0
pupilmat.node_tree.nodes.get('Principled BSDF').inputs['Coat Weight'].default_value=.08;pupilmat.node_tree.nodes.get('Principled BSDF').inputs['Coat Roughness'].default_value=.06
catchmat=mat('09 • corneal studio reflection',(.95,.98,1),.08);cb=catchmat.node_tree.nodes.get('Principled BSDF');cb.inputs['Emission Color'].default_value=(.7,.77,.8,1);cb.inputs['Emission Strength'].default_value=.4
irisMat=attrmat('10 • radial golden iris fibers',.65)
irisMat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.06
irisMat.node_tree.nodes.get('Principled BSDF').inputs['Coat Weight'].default_value=.22;irisMat.node_tree.nodes.get('Principled BSDF').inputs['Coat Roughness'].default_value=.08
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
ell('Chin',(0,-1.112,1.433),(.181,.165,.066),join=True)
def limb(name,rings):
 vv=[];ff=[];ns=24
 for j,(x,y,z,rx,ry) in enumerate(rings):
  for k in range(ns):
   t=k*2*math.pi/ns;dy=(.10*(1-min(1,z/1.15)) if 'front' in name else -.14*(1-min(1,z/.96))) if x<0 else 0;vv.append((x+rx*math.cos(t),y+dy+ry*math.sin(t),z))
  if j:
   for k in range(ns):ff.append(((j-1)*ns+k,(j-1)*ns+(k+1)%ns,j*ns+(k+1)%ns,j*ns+k))
 ff.extend([tuple(reversed(range(ns))),tuple((len(rings)-1)*ns+k for k in range(ns))])
 me=bpy.data.meshes.new(name);me.from_pydata(vv,[],ff);o=bpy.data.objects.new(name,me);root.objects.link(o);parts.append(o)
for s in [-1,1]:
 x=s*.230
 limb('Continuous front leg '+str(s),[(x,-.58,1.12,.14,.16),(x,-.59,.94,.133,.153),(x,-.605,.76,.12,.137),(x,-.622,.57,.104,.12),(x,-.64,.38,.097,.108),(x,-.659,.19,.093,.113),(x,-.682,.105,.096,.122)])
 ell('Front paw '+str(s),(x,-.736+(.10 if s<0 else 0),.081),(.123,.163,.071),join=True)
 for k in range(4):ell('Front toe '+str(s)+'.'+str(k),(x+(k-1.5)*.051,-.861+abs(k-1.5)*.014+(.10 if s<0 else 0),.066),(.037,.068,.049),join=True,seg=28,rings=20)
 ell('Hind haunch '+str(s),(s*.249,.646,.969),(.16,.231,.28),join=True)
 limb('Continuous angular hind leg '+str(s),[(s*.254,.66,.96,.148,.178),(s*.261,.617,.77,.13,.162),(s*.265,.665,.60,.11,.128),(s*.262,.757,.42,.082,.089),(s*.258,.80,.25,.073,.079),(s*.258,.788,.11,.082,.098)])
 ell('Hind paw '+str(s),(s*.257,.715-(.14 if s<0 else 0),.077),(.113,.16,.066),join=True)
 for k in range(4):ell('Rear toe '+str(s)+'.'+str(k),(s*.257+(k-1.5)*.047,.604+abs(k-1.5)*.011-(.14 if s<0 else 0),.057),(.033,.065,.045),join=True,seg=24,rings=16)
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
# Soft anatomical toe channels, sculpted into our own continuous mesh.
for v in body.data.vertices:
 x,y,z=v.co;side=-1 if x<0 else 1;cy=-.736+(.10 if side<0 else 0)
 if z<.115 and y<cy-.095 and abs(x-side*.230)<.112:
  gap=min(abs(x-(side*.230+t)) for t in [-.051,0,.051]);v.co.y+=.006*math.exp(-(gap/.008)**2)*math.exp(-((z-.061)/.045)**2)
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
from mathutils.bvhtree import BVHTree
_ear_bvh=BVHTree.FromObject(body,bpy.context.evaluated_depsgraph_get())
ears=[];inner_ears=[]
for s in [-1,1]:
 vv=[];ff=[];nu=18;nv=24
 for j in range(nv+1):
  v=j/nv
  for i in range(nu+1):
   u=i/nu;q=2*u-1;seed=Vector((s*(.252+.090*q),-.790,1.895));nearest,norm,_,_=_ear_bvh.find_nearest(seed)
   p0=(nearest-norm*.009) if nearest is not None else seed
   p1=Vector((s*(.275+.081*q),-.866,1.974-.018*q*q))
   p2=Vector((s*(.287+.040*q),-.970,1.939-.009*q*q))
   tip,tn,_,_=_ear_bvh.find_nearest(Vector((s*(.305+.002*q),-.987,1.845)));p3=tip+tn*.009
   if v<.37:t=v/.37;aa,bb=p0,p1
   elif v<.72:t=(v-.37)/.35;aa,bb=p1,p2
   else:t=(v-.72)/.28;aa,bb=p2,p3
   t=t*t*(3-2*t);vv.append(tuple(aa.lerp(bb,t)))
 for j in range(nv):
  for i in range(nu):
   k=j*(nu+1)+i;face=(k,k+1,k+nu+2,k+nu+1);ff.append(face if s==1 else face[::-1])
 me=bpy.data.meshes.new('Folded cartilage topology');me.from_pydata(vv,[],ff);o=bpy.data.objects.new('Folded ear '+str(s),me);root.objects.link(o);o.data.materials.append(black)
 sol=o.modifiers.new('Soft cartilage thickness','SOLIDIFY');sol.thickness=.012;bpy.context.view_layer.objects.active=o;bpy.ops.object.modifier_apply(modifier=sol.name)
 su=o.modifiers.new('Rounded ear fold','SUBSURF');su.levels=2;bpy.ops.object.modifier_apply(modifier=su.name)
 for p in o.data.polygons:p.use_smooth=True
 ears.append(o)
 ev=[(s*.277,-.923,1.911)];ef=[];en=64;er=8
 for j in range(1,er+1):
  r=j/er
  for k in range(en):
   t=k*2*math.pi/en;ev.append((s*.277+.037*r*math.cos(t),-.943+.020*(1-r*r),1.911+.025*r*math.sin(t)))
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
 theta=s*.27;N=Vector((math.sin(theta),-math.cos(theta),.015));U=Vector((math.cos(theta),math.sin(theta),0));V=Vector((0,0,1));C=Vector((s*.167,-1.150,1.724))
 eye=ell('Eye socket '+str(s),C,(.074,.019,.071),rim,seg=64,rings=48);eye.rotation_euler.z=theta
 irisR=.071;nr=22;nt=192;iv=[C+N*.038];ic=[(.36,.25,.04,1)];iff=[]
 for j in range(1,nr+1):
  r=j/nr
  for k in range(nt):
   ang=2*math.pi*k/nt;xx=irisR*r*math.cos(ang);zz=irisR*.96*r*math.sin(ang);d=.020+.018*math.sqrt(max(0,1-r*r));iv.append(C+U*xx+V*zz+N*d)
   rays=.5+.20*math.sin(ang*97+2.3*math.sin(ang*23)+r*7)+.15*math.sin(ang*173-r*12)+.12*math.sin(ang*51+r*20)
   border=max(0,min(1,(1-r)/.055));inner=.7+.3*min(1,r/.35);col=(.29+.20*rays,.215+.15*rays,.027+.036*rays)
   ic.append(tuple(v*border*inner+.004*(1-border) for v in col)+(1,))
 for k in range(nt):iff.append((0,1+k,1+(k+1)%nt))
 for j in range(nr-1):
  for k in range(nt):
   idx=1+j*nt+k;nxt=1+j*nt+(k+1)%nt;iff.append((idx,nxt,nxt+nt,idx+nt))
 me=bpy.data.meshes.new('Radial iris '+str(s));me.from_pydata(iv,[],iff);eo=bpy.data.objects.new('Gold iris '+str(s),me);root.objects.link(eo);me.materials.append(irisMat);co=me.color_attributes.new(name='Coat',type='FLOAT_COLOR',domain='POINT')
 for i,c in enumerate(ic):co.data[i].color=c
 for po in me.polygons:po.use_smooth=True
 # Convex slit follows the front of the iris.
 pv=[C+N*.040];pf=[]
 for k in range(96):
  ang=k*math.pi*2/96;xx=.0285*math.cos(ang);zz=.043*math.sin(ang);rr=(xx/irisR)**2+(zz/(irisR*.96))**2;pv.append(C+U*xx+V*zz+N*(.022+.018*math.sqrt(max(0,1-rr))))
 for k in range(96):pf.append((0,k+1,(k+1)%96+1))
 me=bpy.data.meshes.new('Pupil slit');me.from_pydata(pv,[],pf);po=bpy.data.objects.new('Vertical pupil '+str(s),me);root.objects.link(po);me.materials.append(pupilmat)
 for poly in me.polygons:poly.use_smooth=True
 hi=ell('Softbox eye reflection '+str(s),C+U*(-.019)+V*.024+N*.043,(.00432,.001296,.00576),catchmat,seg=32,rings=20);hi.rotation_euler.z=theta;hi.rotation_euler.y=-.25
 hi=ell('Secondary eye glint '+str(s),C+U*.022+V*(-.020)+N*.041,(.0022,.0012,.0028),catchmat,seg=20,rings=12);hi.rotation_euler.z=theta
# Annular eyelid tissue joins the corneal margin to the actual sculpt surface.
 lv=[];lf=[];ln=96;lr=5
 for j in range(lr+1):
  w=j/lr;ease=w*w*(3-2*w)
  for k in range(ln):
   ang=k*2*math.pi/ln;inner=C+U*(.0735*math.cos(ang))+V*(.070*math.sin(ang)+s*.003*math.cos(ang))+N*.021
   projected=C+U*(.086*math.cos(ang))+V*(.083*math.sin(ang));hit=_body_bvh.ray_cast(projected+N*.4,-N,1.0)[0]
   if hit is None:hit=projected-N*.025
   lv.append(inner.lerp(hit,ease)+N*(.0015*math.sin(math.pi*w)))
 for j in range(lr):
  for k in range(ln):
   q=j*ln+k;nq=j*ln+(k+1)%ln;lf.append((q,nq,nq+ln,q+ln))
 lm=bpy.data.meshes.new('Anatomical eyelid transition '+str(s));lm.from_pydata(lv,[],lf);lm.update();lid=bpy.data.objects.new('Sculpted eyelids '+str(s),lm);root.objects.link(lid);lm.materials.append(rim);lm.materials.append(lidskin)
 for i,poly in enumerate(lm.polygons):poly.use_smooth=True;poly.material_index=1
 paint(lid,coatcolor);sub=lid.modifiers.new('Soft eyelid tissue','SUBSURF');sub.levels=1;eye_lids.append(lid)
# Shaped nose, philtrum, lips and whisker follicles.
# Rounded nasal planum: upper lobes, shallow notch and soft lower point.
outline=[(0,1.550),(.024,1.554),(.043,1.545),(.032,1.529),(0,1.512),(-.032,1.529),(-.043,1.545),(-.024,1.554)]
vs=[(0,-1.357,1.536)]+[(x,-1.337-.010*(1-abs(x)/.05),z) for x,z in outline]+[(x,-1.311,z) for x,z in outline]+[(0,-1.308,1.536)];fs=[]
for k in range(8):
 n=(k+1)%8;fs.extend([(0,1+n,1+k),(1+k,1+n,9+n,9+k),(17,9+k,9+n)])
me=bpy.data.meshes.new('Original rounded nasal topology');me.from_pydata(vs,[],fs);nose=bpy.data.objects.new('Soft lobed cat nose',me);root.objects.link(nose);me.materials.append(nosemat);su=nose.modifiers.new('Rounded nasal planum','SUBSURF');su.levels=2
for p in me.polygons:p.use_smooth=True
def strand_curve(name,points,radius,material,col=root):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=2;cu.bevel_depth=radius;cu.bevel_resolution=2;sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for i,p in enumerate(points):sp.points[i].co=(*p,1);sp.points[i].radius=max(.12,(1-i/(len(points)-1))**.6)
 ob=bpy.data.objects.new(name,cu);col.objects.link(ob);cu.materials.append(material);return ob
strand_curve('Philtrum',[(0,-1.324,1.519),(0,-1.329,1.495),(0,-1.323,1.475)],.0019,rim)
for s in [-1,1]:
 strand_curve('Muzzle lip '+str(s),catmull([(0,-1.323,1.475),(s*.035,-1.307,1.462),(s*.091,-1.285,1.464),(s*.135,-1.248,1.487)],6),.0016,rim)
 for j in range(10):
  rr=random.Random(800+j);z=1.492+(j%4-1.5)*.022;xx=.091+(j//4)*.031;yy=-1.284+(j//4)*.017
  start=Vector((s*xx,yy,z));end=Vector((s*(.46+rr.random()*.14),-1.19+rr.uniform(-.19,.12),z+rr.uniform(-.15,.14)))
  mid=start.lerp(end,.48)+Vector((0,-.045,.026));pts=catmull([start,start.lerp(mid,.4),mid,end],5)
  strand_curve('Mystacial whisker '+str(s)+'.'+str(j),pts,.00065+rr.random()*.0003,white)
  ell('Whisker root '+str(s)+'.'+str(j),start,(.003,.002,.003),nosemat,seg=8,rings=6)
 for j in range(4):
  rr=random.Random(912+j+int(s));probe=Vector((s*(.135+j*.027),-2,1.833+j*.005));hit=_body_bvh.ray_cast(probe,Vector((0,1,0)),1.2)[0]
  start=hit+Vector((0,-.002,0)) if hit is not None else Vector((probe.x,-1.12,probe.z));end=start+Vector((s*(.034+j*.027),-.018+rr.uniform(-.03,.02),.096+rr.uniform(-.018,.035)));mid=start.lerp(end,.55)+Vector((-s*.015,-.023,.018));strand_curve('Brow whisker '+str(s)+'.'+str(j),catmull([start,mid,end],10),.00035+rr.random()*.00010,white)
print('SCULPT_READY',len(body.data.vertices),'vertices',flush=True)
nostrilmat=mat('Nose creases • soft charcoal',(.0012,.001,.001),.83)
for side in [-1,1]:
 nostril=ell('Nostril '+str(side),(side*.025,-1.349,1.540),(.0055,.0018,.003),nostrilmat,seg=24,rings=16);nostril.rotation_euler.y=side*.24
nb=nosemat.node_tree.nodes;nt=nb.new('ShaderNodeTexNoise');nt.inputs['Scale'].default_value=95;nt.inputs['Detail'].default_value=2;np=nb.new('ShaderNodeBump');np.inputs['Strength'].default_value=.10;np.inputs['Distance'].default_value=.0015;nosemat.node_tree.links.new(nt.outputs['Fac'],np.inputs['Height']);nosemat.node_tree.links.new(np.outputs['Normal'],nb.get('Principled BSDF').inputs['Normal'])
# Deterministic surface-area strand sampling of ORIGINAL geometry, not image analysis.
def groom_surface(obj,count,colorfn,name,length_scale=1,region=None):
 me=obj.data;me.calc_loop_triangles();tris=list(me.loop_triangles);cum=[];tot=0
 if region=='face':tris=[tr for tr in tris if sum(me.vertices[k].co.z for k in tr.vertices)>4.45 and sum(me.vertices[k].co.y for k in tr.vertices)<-2.52]
 for tri in tris:tot+=tri.area;cum.append(tot)
 vs=[];radii=[];cols=[];rng=random.Random(171+count);M=obj.matrix_world;R=M.to_3x3()
 for h in range(count):
  tr=tris[bisect.bisect_left(cum,rng.random()*tot)];a0,b0,c0=[me.vertices[k] for k in tr.vertices];r1=math.sqrt(rng.random());r2=rng.random();weights=(1-r1,r1*(1-r2),r1*r2);p=M@(a0.co*weights[0]+b0.co*weights[1]+c0.co*weights[2]);normal=(R@(a0.normal*weights[0]+b0.normal*weights[1]+c0.normal*weights[2])).normalized();x,y,z=p
  # Keep the corneas and nose unobstructed.
  if name in ('Body groom','Face microgroom') and y<-1.09 and z>1.60 and ((abs(x)-.177)/.073)**2+((z-1.724)/.071)**2<1.02:continue
  if name.startswith('Lid groom') and ((abs(x)-.177)/.072)**2+((z-1.724)/.069)**2<1.0:continue
  if y<-1.287 and abs(x)<.067 and 1.502<z<1.574:continue
  if z<.010 or (z<.033 and normal.z<-.35):continue
  if name.startswith('Lid groom'):direction=Vector((x-math.copysign(.179,x),-.01,z-1.724));length=.004+rng.random()*.004
  elif name.startswith('Inner ear'):direction=Vector((x*.7,-.4,1));length=.018+rng.random()*.029
  elif name.startswith('Ear groom'):direction=Vector((x*.8,-.2,.45));length=.012+rng.random()*.013
  elif y>1.0 and z>1.35:direction=Vector((0,.5,1));length=.028+rng.random()*.021
  elif z>1.40 and y<-.75:
   direction=Vector((x*2,.15,-.65));length=(.029+rng.random()*.022) if z<1.59 else (.009+rng.random()*.008)
   if y<-1.20:length*=.40;direction=Vector((x*3,0,-.2))
  elif z<.70:direction=Vector((0,-.07,-1));length=.019+rng.random()*.012
  else:direction=Vector((x*.8,.45,-.55));length=.027+rng.random()*.022
  if z<.22:length*=.16+.84*max(0,min(1,(z-.09)/.13))
  if rng.random()<.12 and z>.2:length*=1.35
  length*=length_scale
  if name in ('Body groom','Face microgroom') and y<-.97 and z>1.57 and ((abs(x)-.179)/.16)**2+((z-1.724)/.16)**2<1.0:direction=Vector((x-math.copysign(.179,x),-.02,z-1.724))
  tangent=direction-normal*direction.dot(normal)
  if tangent.length<.01:tangent=normal.cross(Vector((.3,.9,.4)))
  tangent.normalize();jitter=Vector((rng.uniform(-1,1),rng.uniform(-1,1),rng.uniform(-1,1)))*.16
  axis=(normal*.53+tangent*.79+jitter).normalized();u=axis.cross(Vector((.12,.13,1)))
  if u.length<.01:u=axis.cross(Vector((1,0,0)))
  u.normalize();v=axis.cross(u).normalized();col=colorfn(p);variation=rng.uniform(.73,1.17);col=tuple(min(.95,c*variation) for c in col);radius=rng.uniform(.00023,.00049)*length_scale
  for t in [0,.36,.72,1]:
   cp=p+normal*(length*(.49*t-.12*t*t))+tangent*(length*.86*t)+jitter*(length*t*t)
   vs.append(tuple(cp));radii.append(radius*(1-.94*t));cols.append((*col,1))
 ob=create_native_groom(name,vs,radii,cols,furmat,groomcol,guidecol,count)
 print('GROOM_READY',name,ob['actual_strands'],'native curves',flush=True);return ob
hair=groom_surface(body,a.fur,coatcolor,'Body groom')
groom_surface(body,95000,coatcolor,'Face microgroom',.67,region='face')
for o in ears:groom_surface(o,3000,lambda p:(.0032,.0038,.0047),'Ear groom '+o.name,.86)
for o in inner_ears:groom_surface(o,700,lambda p:(.43,.39,.34),'Inner ear groom '+o.name,.66)
for o in eye_lids:groom_surface(o,6000,coatcolor,'Lid groom '+o.name,.88)
# Put the lowest original skin point on the studio plane without altering coat coordinates.
ground_offset=min((body.matrix_world@v.co).z for v in body.data.vertices)
for col in [root,groomcol,guidecol]:
 for ob in col.objects:ob.location.z-=ground_offset
scene['ground_offset']=ground_offset
add_cornea(root,ground_offset)
furmat.shadow_method='OPAQUE'
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
# Camera-space Blender text supplies attribution in the actual rendered files.
creditmat=mat('Studio • attribution ink',(.035,.045,.039),1);credit_bs=creditmat.node_tree.nodes.get('Principled BSDF');credit_bs.inputs['Emission Color'].default_value=(.035,.045,.039,1);credit_bs.inputs['Emission Strength'].default_value=1
creditmat.shadow_method='NONE';credits=[]
for bodytext,tag in [('GPT-6 Astra Pro','Model attribution'),('mcp-colabdev  /  Blender EEVEE','Tool attribution')]:
 font=bpy.data.curves.new(tag,'FONT');font.body=bodytext;font.align_x='LEFT';font.align_y='TOP_BASELINE';font.extrude=0;ob=bpy.data.objects.new(tag,font);studiocol.objects.link(ob);ob.parent=cam;font.materials.append(creditmat);credits.append(ob)
 for attr in ['visible_shadow','visible_diffuse','visible_glossy','visible_transmission','visible_volume_scatter']:
  if hasattr(ob,attr):setattr(ob,attr,False)
views={'hero':((3.2,-5.7,2.3),(0,.19,1.13),3.45),'front':((0,-7,1.42),(0,.1,1.13),2.86),'left':((-7,-.01,1.42),(0,.19,1.15),3.50),'right':((7,-.01,1.42),(0,.19,1.15),3.50),'rear':((0,7,1.42),(0,.20,1.12),2.92),'detail':((.9,-6,2.0),(0,-.95,1.68),1.12)}
def setcam(v):
 pos,target,scale=views[v];target=Vector(target);pos=Vector(pos);cam.location=target+(pos-target)*4;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
 for i,label in enumerate(credits):label.location=(-scale*.445,scale*(.461-i*.028),-8);label.data.size=scale*(.021 if i==0 else .0105)
setcam('hero');scene['author']='GPT-6 Astra Pro';scene['tools']='mcp-colabdev / Blender headless EEVEE';scene['revision']=a.revision;scene['assets']='All cat geometry, fibers and materials authored from scratch; reference inspection only.'
blend=B/'GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True);print('SAVED_BLEND',str(blend),flush=True)
saved_shadow=furmat.shadow_method;saved_soft=scene.eevee.use_soft_shadows;saved_cube=scene.eevee.shadow_cube_size
if a.fast_preview:
 furmat.shadow_method='NONE';scene.eevee.use_soft_shadows=False;scene.eevee.shadow_cube_size='512'
for view in a.views.split(','):
 setcam(view);out=P/'preview'/'renders'/('r%02d_%s.png'%(a.revision,view));scene.render.filepath=str(out);bpy.ops.render.render(write_still=True);print('RENDER_DONE',view,str(out),round(time.time()-t0,1),flush=True)
furmat.shadow_method=saved_shadow;scene.eevee.use_soft_shadows=saved_soft;scene.eevee.shadow_cube_size=saved_cube
setcam('hero');bpy.ops.wm.save_as_mainfile(filepath=str(blend),compress=True);print('BUILD_COMPLETE',round(time.time()-t0,1),flush=True)
