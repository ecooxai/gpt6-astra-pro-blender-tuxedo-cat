"""Pass 9: original eye anatomy and finer short-fur shading."""
from pathlib import Path
p=Path(__file__).with_name('build_cat.py');s=p.read_text()
changes=[
("bu.inputs['Strength'].default_value=.16;bu.inputs['Distance'].default_value=.009","bu.inputs['Strength'].default_value=.07;bu.inputs['Distance'].default_value=.0016"),
("ell('Chin',(0,-1.118,1.412),(.192,.17,.079),join=True)","ell('Chin',(0,-1.112,1.433),(.181,.165,.066),join=True)"),
("theta=s*.43;","theta=s*.27;"),
("C=Vector((s*.157,-1.134,1.724))","C=Vector((s*.167,-1.150,1.724))"),
("C,(.073,.027,.078)","C,(.074,.019,.071)"),
("irisR=.0695;nr=22;nt=192;iv=[C+N*.052]","irisR=.071;nr=22;nt=192;iv=[C+N*.038]"),
("irisR*1.075","irisR*.96"),
("d=.028+.024*math.sqrt(max(0,1-r*r))","d=.020+.018*math.sqrt(max(0,1-r*r))"),
("col=(.35+.21*rays,.26+.17*rays,.025+.050*rays)","col=(.29+.20*rays,.215+.15*rays,.027+.036*rays)"),
("pv=[C+N*.055]","pv=[C+N*.040]"),
("xx=.030*math.cos(ang);zz=.048*math.sin(ang)","xx=.0285*math.cos(ang);zz=.043*math.sin(ang)"),
("N*(.031+.024*math.sqrt(max(0,1-rr)))","N*(.022+.018*math.sqrt(max(0,1-rr)))"),
("C+U*(-.017)+V*.027+N*.053,(.009,.003,.012)","C+U*(-.019)+V*.024+N*.043,(.006,.0018,.008)"),
("C+U*.021+V*(-.021)+N*.052,(.003,.002,.004)","C+U*.022+V*(-.020)+N*.041,(.0022,.0012,.0028)"),
("inner=C+U*(.0725*math.cos(ang))+V*(.0785*math.sin(ang))+N*.029","inner=C+U*(.0735*math.cos(ang))+V*(.070*math.sin(ang)+s*.003*math.cos(ang))+N*.021"),
("projected=C+U*(.083*math.cos(ang))+V*(.088*math.sin(ang))","projected=C+U*(.086*math.cos(ang))+V*(.083*math.sin(ang))"),
("if y<-1.20:length*=.65;","if y<-1.20:length*=.40;"),
("radius=rng.uniform(.00037,.00076)*length_scale","radius=rng.uniform(.00023,.00049)*length_scale")]
for old,new in changes:
 if old not in s:raise RuntimeError('Missing anchor: '+old)
 s=s.replace(old,new)
p.write_text(s)
print('Pass 9 anatomy patch applied')
