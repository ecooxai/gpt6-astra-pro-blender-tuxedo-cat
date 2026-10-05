import json,datetime,os,shutil,argparse
from pathlib import Path
P=Path(__file__).resolve().parents[1];Q=P/'preview';B=Path('/build/GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat');name='GPT-6-Astra-Pro_mcp-colabdev_Blender_TuxedoCat'
p=argparse.ArgumentParser();p.add_argument('--revision',type=int,required=True);p.add_argument('--score',type=int);p.add_argument('--title',default='Original sculpt and procedural groom');p.add_argument('--notes',default='');p.add_argument('--status',default='Reviewing rendered geometry');args=p.parse_args()
d=json.loads((Q/'status.json').read_text());d.update(updated=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC'),status=args.status,progress=50)
hero=f'renders/r{args.revision:02}_hero.png'
if (Q/hero).exists():d['hero']=hero
views=[]
for v,title in [('front','Front view'),('left','Left profile'),('right','Right profile'),('rear','Rear view')]:
 f=f'renders/r{args.revision:02}_{v}.png'
 if (Q/f).exists():views.append(dict(id=v,label=title,file=f))
if len(views)==4:d['views']=views;d['viewSetRevision']=args.revision
if args.score is not None:
 d['score']=args.score;d['latest_revision']=args.revision
 entry=dict(step=f'PASS {args.revision:02}',time=datetime.datetime.now().strftime('%H:%M'),title=args.title,notes=args.notes,score=args.score,image=hero)
 d['journal']=[e for e in d.get('journal',[]) if e['step']!=entry['step']]+[entry]
d['iterations']=sum(1 for e in d.get('journal',[]) if str(e.get('step','')).startswith('PASS ') and e.get('score') is not None)
files=[]
for typ,fn,desc in [('BLEND',name+'.blend','Editable full-resolution sculpt, groom, materials, lights and camera.'),('GLB',name+'.glb','Optimized original geometry and vertex colors for interactive web viewing.'),('ZIP',name+'.zip','Source scripts, viewer, review journal, and complete Blender project.')]:
 f=Q/'downloads'/fn
 if f.exists():files.append(dict(type=typ,name={'BLEND':'Full Blender scene','GLB':'Interactive 3D model','ZIP':'Complete project archive'}[typ],url='downloads/'+fn+'?v='+str(f.stat().st_mtime_ns),description=desc+f' {f.stat().st_size/1048576:.1f} MB.',path=str(f)))
for typ,fn,title,desc in [('PY','native_groom.py','Native groom module','Companion module: editable fiber centerlines and eye coating geometry.'),('PY','coat_field.py','Procedural coat field','Companion module: original continuous black-and-white coat mathematics.'),('PY','build_cat.py','Procedural build script','Reconstructs the cat from original mathematical geometry.'),('MD','Agents.md','Agent handoff','Exact paths, commands, limitations and completed review history.')]:
 src=P/('scripts/'+fn if typ=='PY' else fn)
 if src.exists():shutil.copy2(src,Q/'downloads'/fn);files.append(dict(type=typ,name=title,url='downloads/'+fn,description=desc,path=str(src)))
sheet=Q/'renders'/f'r{args.revision:02}_four_views_GPT-6-Astra-Pro_mcp-colabdev_Blender.png'
if sheet.exists():files.append(dict(type='PNG',name='Four-view EEVEE sheet',url='renders/'+sheet.name,description='Front, right, rear and left: assembled from the actual current Blender renders.',path=str(sheet)))
release=P/'reports/release.json'
if release.exists():
 released=json.loads(release.read_text())
 for f in files:
  if f['type']=='ZIP':
   asset=next((a for a in released.get('assets',[]) if a.get('name')==name+'.zip'),None)
   if asset and asset.get('browser_download_url'):f['url']=asset['browser_download_url']
d['files']=files
if (Q/'downloads'/(name+'.glb')).exists():model_file=(name+'_web.glb') if (Q/'downloads'/(name+'_web.glb')).exists() else (name+'.glb');d['model']='downloads/'+model_file;d['modelVersion']=str((Q/'downloads'/model_file).stat().st_mtime_ns)
tmp=Q/'status.tmp';tmp.write_text(json.dumps(d,indent=2));os.replace(tmp,Q/'status.json');print(json.dumps({'status':d['status'],'score':d.get('score'),'views':len(d.get('views',[])),'files':len(files)}))

# An explicit archive exposes every generated PNG with its actual absolute path.
imgs=list((Q/'renders').glob('*.png'))
imgs.sort(key=lambda f:(not f.name.startswith('r'),-f.stat().st_mtime))
manifest=[dict(file=f.name,modified=f.stat().st_mtime_ns,kind=('Blender native-fur experiment / '+f.stem.rsplit('_',1)[-1].upper()) if f.name.startswith('experiment_native_') else ('Blender Cycles lighting comparison' if f.name.startswith('lighting_') else ('Blender EEVEE' if f.name.startswith('r') else ('Blender EEVEE cornea experiment' if f.name.startswith('experiment_cornea_') else ('Blender Cycles + OIDN physical-lighting comparison' if f.name.startswith('beauty_') else 'Browser QA capture')))),kb=round(f.stat().st_size/1024),path=str(f)) for f in imgs]
(Q/'renders/manifest.json').write_text(json.dumps(manifest,indent=2))
