from pathlib import Path
p=Path(__file__).with_name('build_cat.py');s=p.read_text()
def rep(a,b):
 global s
 assert a in s,a[:110];s=s.replace(a,b)
rep("pupilmat=mat('08 • deep pupil',(.001,.0015,.0011),.1)","pupilmat=mat('08 • deep pupil',(.00015,.0002,.00015),.95)\npupilmat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=0")
rep("irisMat=attrmat('10 • radial golden iris fibers',.28)", "irisMat=attrmat('10 • radial golden iris fibers',.65)\nirisMat.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.06")
rep("rim=mat('04 • wet dark eyelid',(.013,.009,.006),.3)","rim=mat('04 • wet dark eyelid',(.008,.007,.006),.58)\nrim.node_tree.nodes.get('Principled BSDF').inputs['Specular IOR Level'].default_value=.18")
rep("-.037*v-.030*(2*u-1)**2", "-.037*v-.125*(2*u-1)**2*(1-v)")
rep("x=s*.214\n limb", "x=s*.230\n limb")
rep("(x,-.64,.38,.088,.105)", "(x,-.64,.38,.097,.108)")
rep("(x,-.659,.19,.086,.109)", "(x,-.659,.19,.093,.113)")
rep("if z<.031:continue", "if z<.010 or (z<.033 and normal.z<-.35):continue")
rep("if rng.random()<.12:length*=1.35", "if z<.22:length*=.16+.84*max(0,min(1,(z-.09)/.13))\n  if rng.random()<.12 and z>.2:length*=1.35")
rep(".0011+rr.random()*.0004", ".00065+rr.random()*.0003")
rep("for j in range(3):\n  start=Vector((s*(.135+j*.041),-1.12,1.83+j*.014));end=start+Vector((s*(.047+j*.033),-.045-j*.008,.106+j*.017));strand_curve", "for j in range(5):\n  start=Vector((s*(.131+j*.025),-1.12,1.832+j*.010));end=start+Vector((s*(.03+j*.024),-.04-j*.008,.113+j*.008));strand_curve")
rep("],7),.0009,white)", "],7),.00055,white)")
needle="views={'hero':"
insert="""# Camera-space Blender text supplies attribution in the actual rendered files.
creditmat=mat('Studio • attribution ink',(.035,.045,.039),1);credit_bs=creditmat.node_tree.nodes.get('Principled BSDF');credit_bs.inputs['Emission Color'].default_value=(.035,.045,.039,1);credit_bs.inputs['Emission Strength'].default_value=1
creditmat.shadow_method='NONE';credits=[]
for bodytext,tag in [('GPT-6 Astra Pro','Model attribution'),('mcp-colabdev  /  Blender EEVEE','Tool attribution')]:
 font=bpy.data.curves.new(tag,'FONT');font.body=bodytext;font.align_x='LEFT';font.align_y='TOP_BASELINE';font.extrude=0;ob=bpy.data.objects.new(tag,font);studiocol.objects.link(ob);ob.parent=cam;font.materials.append(creditmat);credits.append(ob)
 for attr in ['visible_shadow','visible_diffuse','visible_glossy','visible_transmission','visible_volume_scatter']:
  if hasattr(ob,attr):setattr(ob,attr,False)
views={'hero':"""
rep(needle,insert)
rep("cam.data.ortho_scale=scale\nsetcam('hero')", "cam.data.ortho_scale=scale\n for i,label in enumerate(credits):label.location=(-scale*.445,scale*(.461-i*.028),-8);label.data.size=scale*(.021 if i==0 else .0105)\nsetcam('hero')")
p.write_text(s);print('REVISION_07_APPLIED')
p=Path(__file__).with_name('render_beauty.py');s=p.read_text();s=s.replace("l.new(attr.outputs['Color'],hair.inputs['Color'])", "mul=n.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=(.62,.62,.62,1);l.new(attr.outputs['Color'],mul.inputs[1]);l.new(mul.outputs[0],hair.inputs['Color'])")
s=s.replace("s.world.node_tree.nodes.get('Background').inputs[1].default_value=.42", "s.world.node_tree.nodes.get('Background').inputs[1].default_value=.30\nbpy.data.lights['Fill • camera right'].energy=160\nbpy.data.lights['Soft frontal bounce'].energy=95\ns.view_settings.exposure=-.12\nif 'Tool attribution' in bpy.data.objects:bpy.data.objects['Tool attribution'].data.body='mcp-colabdev  /  Blender Cycles + OIDN'")
p.write_text(s)
