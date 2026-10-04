from pathlib import Path
p=Path(__file__).with_name('build_cat.py');s=p.read_text()
def rep(a,b):
 global s
 assert a in s,a[:90];s=s.replace(a,b)
rep("scene.eevee.use_soft_shadows=False","scene.eevee.use_soft_shadows=True")
rep("scene.eevee.gtao_factor=1.13","scene.eevee.gtao_factor=.88")
rep("(s*.207,-.992,1.60),(.191,.229,.202)","(s*.195,-.990,1.60),(.173,.207,.187)")
rep("ell('Full white chest',(0,-.715,1.16),(.285,.291,.34)","ell('Full white chest',(0,-.705,1.18),(.255,.244,.365)")
rep("x=s*.235\n limb", "x=s*.214\n limb")
rep("-.841+abs(k-1.5)*.01,.064),(.037,.064,.049)","-.861+abs(k-1.5)*.014,.066),(.037,.068,.049)")
rep("rem.voxel_size=.014", "rem.voxel_size=.012")
needle="for v in body.data.vertices:\n if v.co.z<.062:v.co.z=max(.007,.010+(v.co.z-.013)*.7)"
replacement='''# Anatomical eye sockets blend the eyelid into the cheek, rather than placing eyes on top.
for v in body.data.vertices:
 x,y,z=v.co
 if y< -1.02 and z>1.57:
  rr=((abs(x)-.174)/.089)**2+((z-1.724)/.094)**2
  if rr<2.25:
   v.co.y += .075*(1-rr/2.25)**2*max(0,min(1,(-y-1.02)/.08))
 if v.co.z<.062:v.co.z=max(.007,.010+(v.co.z-.013)*.7)
body.data.update()'''
rep(needle,replacement)
rep("span=.212*(1-.73*v**2)","span=.222*max(.045,1-.99*v**1.3)")
rep("xx=.287+(u-.5)*span+.018*math.sin(math.pi*v)","xx=.274+.065*v+(u-.5)*span")
rep("zz=1.903+.076*math.sin(math.pi*v*.91)-.046*v-.032*(2*u-1)**2","zz=1.900+.080*math.sin(math.pi*v)-.035*v-.020*v**3-.030*(2*u-1)**2")
rep("(s*.294,-.999,1.883),(.046,.012,.026)","(s*.292,-.991,1.883),(.055,.012,.033)")
rep("(.081,.043,.086)","(.076,.041,.081)")
rep("((abs(x)-.157)/.088)**2+((z-1.724)/.094)**2<1.04","((abs(x)-.174)/.087)**2+((z-1.724)/.091)**2<1.04")
rep("area('Coat edge • rear strip',(0,3.5,4.8),650,3.0,color=(1,1,.97))","area('Coat edge • rear strip',(0,3.5,4.8),540,3.0,color=(1,1,.97))\narea('Soft frontal bounce',(0,-4.5,2.05),165,5.0,color=(1,.97,.92))\nbpy.data.lights['Soft frontal bounce'].use_shadow=False")
p.write_text(s);print('REVISION_03_APPLIED')
