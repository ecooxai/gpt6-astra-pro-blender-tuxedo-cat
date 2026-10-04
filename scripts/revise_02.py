from pathlib import Path
p=Path(__file__).with_name('build_cat.py');s=p.read_text()
def rep(a,b):
 global s
 assert a in s,a[:100]
 s=s.replace(a,b)
rep("scene.view_settings.exposure=.35","scene.view_settings.exposure=.12")
rep("default_value=.32","default_value=.27")
rep("b.inputs['Sheen Weight'].default_value=.2","b.inputs['Sheen Weight'].default_value=.12; b.inputs['Specular IOR Level'].default_value=.20")
rep("furmat.node_tree.nodes.get('Principled BSDF').inputs['Sheen Weight'].default_value=.35","furmat.node_tree.nodes.get('Principled BSDF').inputs['Sheen Weight'].default_value=.13; furmat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.18")
rep("bu.inputs['Strength'].default_value=.25","bu.inputs['Strength'].default_value=.16")
rep("ell('Cranium'","ell('Full white chest',(0,-.715,1.16),(.285,.291,.34),join=True)\nell('Cranium'")
start=s.index('for s in [-1,1]:\n x=s*.235');end=s.index('# Curved, full-bodied tail',start)
limbs='''def limb(name,rings):
 vv=[];ff=[];ns=24
 for j,(x,y,z,rx,ry) in enumerate(rings):
  for k in range(ns):
   t=k*2*math.pi/ns;vv.append((x+rx*math.cos(t),y+ry*math.sin(t),z))
  if j:
   for k in range(ns):ff.append(((j-1)*ns+k,(j-1)*ns+(k+1)%ns,j*ns+(k+1)%ns,j*ns+k))
 ff.extend([tuple(reversed(range(ns))),tuple((len(rings)-1)*ns+k for k in range(ns))])
 me=bpy.data.meshes.new(name);me.from_pydata(vv,[],ff);o=bpy.data.objects.new(name,me);root.objects.link(o);parts.append(o)
for s in [-1,1]:
 x=s*.235
 limb('Continuous front leg '+str(s),[(x,-.58,1.12,.14,.16),(x,-.59,.94,.133,.153),(x,-.605,.76,.12,.137),(x,-.622,.57,.104,.12),(x,-.64,.38,.088,.105),(x,-.659,.19,.086,.109),(x,-.682,.105,.096,.122)])
 ell('Front paw '+str(s),(x,-.736,.081),(.123,.163,.071),join=True)
 for k in range(4):ell('Front toe '+str(s)+'.'+str(k),(x+(k-1.5)*.051,-.841+abs(k-1.5)*.01,.064),(.037,.064,.049),join=True,seg=28,rings=20)
 ell('Hind haunch '+str(s),(s*.249,.646,.969),(.16,.231,.28),join=True)
 limb('Continuous angular hind leg '+str(s),[(s*.254,.66,.96,.148,.178),(s*.261,.617,.77,.13,.162),(s*.265,.665,.60,.11,.128),(s*.262,.757,.42,.082,.089),(s*.258,.80,.25,.073,.079),(s*.258,.788,.11,.082,.098)])
 ell('Hind paw '+str(s),(s*.257,.715,.077),(.113,.16,.066),join=True)
 for k in range(4):ell('Rear toe '+str(s)+'.'+str(k),(s*.257+(k-1.5)*.047,.604+abs(k-1.5)*.011,.057),(.033,.065,.045),join=True,seg=24,rings=16)
'''
s=s[:start]+limbs+s[end:]
rep("[(0,.83,1.27),(0,1.07,1.45),(.015,1.34,1.62),(.04,1.52,1.85),(.035,1.57,2.10),(.015,1.52,2.23)]","[(0,.83,1.27),(-.07,1.07,1.46),(-.21,1.31,1.69),(-.36,1.43,1.94),(-.42,1.41,2.14),(-.43,1.33,2.24)]")
rep("r=.102+.023*math.sin(math.pi*t)-.04*t**7","r=.106+.023*math.sin(math.pi*t)-.026*t**7")
rep("(.065,.064,.075)","(.082,.080,.084)")
rep("body.data.materials.clear();body.data.materials.append(coat)","for v in body.data.vertices:\n if v.co.z<.062:v.co.z=max(.007,.010+(v.co.z-.013)*.7)\nbody.data.materials.clear();body.data.materials.append(coat)")
rep("width=.022+.15*max(0,min(1,(1.87-z)/.43))**1.6","width=.005+.155*max(0,min(1,(1.945-z)/.43))**1.85")
rep("if ax<width+edge*.24:isblack=False","if ax<width+edge*.20 and z<1.935+edge*.25:isblack=False")
rep("if z<1.515 and y<-1.05:isblack=False","if z<1.565-.025*min(1,ax/.3) and y<-.74:isblack=False")
rep("if .2<y<.49 and z<.81 and ax>.15:isblack=True","if .2<y<.49 and .745<z<.81 and ax<.17:isblack=True")
rep("if y>1.00 and z>1.32:isblack=True","if y>.89 and z>1.37:isblack=True")
rep("return (.011,.013,.015)","return (.0032,.0038,.0047)")
rep("span=.235*(1-.59*v**2)","span=.212*(1-.73*v**2)")
rep("xx=.267+(u-.5)*span+.031*math.sin(math.pi*v)","xx=.287+(u-.5)*span+.018*math.sin(math.pi*v)")
rep("zz=1.877+.137*math.sin(math.pi*v*.91)-.049*v-.052*(2*u-1)**2","zz=1.903+.076*math.sin(math.pi*v*.91)-.046*v-.032*(2*u-1)**2")
rep("(s*.281,-.996,1.879),(.058,.014,.039)","(s*.294,-.999,1.883),(.046,.012,.026)")
rep("lambda p:(.01,.012,.014)","lambda p:(.0032,.0038,.0047)")
rep("C=Vector((s*.168,-1.157,1.712))","C=Vector((s*.157,-1.134,1.724))")
rep("(.105,.066,.113)","(.081,.043,.086)")
rep("irisR=.092","irisR=.0695")
rep("iv=[C+N*.076]","iv=[C+N*.052]")
rep("d=.046+.031*math.sqrt(max(0,1-r*r))","d=.028+.024*math.sqrt(max(0,1-r*r))")
rep("col=(.58+.16*rays,.41+.17*rays,.065+.045*rays)","col=(.35+.21*rays,.26+.17*rays,.025+.050*rays)")
rep("pv=[C+N*.080]","pv=[C+N*.055]")
rep("xx=.023*math.cos(ang);zz=.073*math.sin(ang)","xx=.027*math.cos(ang);zz=.047*math.sin(ang)")
rep("N*(.049+.032*math.sqrt(max(0,1-rr)))","N*(.031+.024*math.sqrt(max(0,1-rr)))")
rep("C+U*(-.028)+V*.041+N*.076,(.017,.004,.022)","C+U*(-.017)+V*.027+N*.053,(.009,.003,.012)")
rep("C+U*.029+V*(-.027)+N*.076,(.006,.003,.009)","C+U*.021+V*(-.021)+N*.052,(.003,.002,.004)")
rep("range(12):\n  rr=random.Random", "range(10):\n  rr=random.Random")
rep("for j in range(5):\n  start=Vector((s*(.139+j*.025),-1.127,1.821+j*.008));end=start+Vector((s*(.04+j*.024),-.02,.13+j*.013))", "for j in range(3):\n  start=Vector((s*(.135+j*.041),-1.12,1.83+j*.014));end=start+Vector((s*(.047+j*.033),-.045-j*.008,.106+j*.017))")
rep("((abs(x)-.168)/.118)**2+((z-1.712)/.126)**2<1.05","((abs(x)-.157)/.088)**2+((z-1.724)/.094)**2<1.04")
rep("length=.035+rng.random()*.030","length=.042+rng.random()*.031")
rep("radius=rng.uniform(.00065,.00125)","radius=rng.uniform(.00072,.00130)")
rep("normal*(length*(.31*t-.11*t*t))","normal*(length*(.44*t-.15*t*t))")
rep("name=='Body groom' and y<-1.09 and z>1.58","name=='Body groom' and y<-1.09 and z>1.60")
p.write_text(s);print('REVISION_02_APPLIED')
