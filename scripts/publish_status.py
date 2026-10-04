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
if views:d['views']=views
if args.score is not None:
 d['score']=args.score;d['iterations']=args.revision
 entry=dict(step=f'PASS {args.revision:02}',time=datetime.datetime.now().strftime('%H:%M'),title=args.title,notes=args.notes,score=args.score,image=hero)
 d['journal']=[e for e in d.get('journal',[]) if e['step']!=entry['step']]+[entry]
files=[]
for typ,fn,desc in [('BLEND',name+'.blend','Editable full-resolution sculpt, groom, materials, lights and camera.'),('GLB',name+'.glb','Optimized original geometry and vertex colors for interactive web viewing.'),('ZIP',name+'.zip','Source scripts, viewer, review journal, and complete Blender project.')]:
 f=Q/'downloads'/fn
 if f.exists():files.append(dict(type=typ,name={'BLEND':'Full Blender scene','GLB':'Interactive 3D model','ZIP':'Complete project archive'}[typ],url='downloads/'+fn,description=desc+f' {f.stat().st_size/1048576:.1f} MB.',path=str(f)))
for typ,fn,title,desc in [('PY','build_cat.py','Procedural build script','Reconstructs the cat from original mathematical geometry.'),('MD','Agents.md','Agent handoff','Exact paths, commands, limitations and completed review history.')]:
 src=P/('scripts/'+fn if typ=='PY' else fn)
 if src.exists():shutil.copy2(src,Q/'downloads'/fn);files.append(dict(type=typ,name=title,url='downloads/'+fn,description=desc,path=str(src)))
d['files']=files
if (Q/'downloads'/(name+'.glb')).exists():d['model']='downloads/'+name+'.glb'
tmp=Q/'status.tmp';tmp.write_text(json.dumps(d,indent=2));os.replace(tmp,Q/'status.json');print(json.dumps({'status':d['status'],'score':d.get('score'),'views':len(d.get('views',[])),'files':len(files)}))
