"""Create a clean reproducible archive; exclude dependencies, secrets and temporary data."""
import hashlib,json,zipfile,os,subprocess,datetime
from pathlib import Path
P=Path(__file__).resolve().parents[1];N=P.name;D=P/'preview/downloads';D.mkdir(exist_ok=True);out=D/(N+'.zip');tmp=D/('.'+N+'.pending.zip')
allowed_top={'README.md','Agents.md','package.json','package-lock.json','index.html','.gitignore','THIRD_PARTY_NOTICES.txt'}
files=[]
for f in P.rglob('*'):
 if not f.is_file():continue
 rel=f.relative_to(P);parts=rel.parts
 if parts[0] not in {'scripts','preview','reports'} and str(rel) not in allowed_top:continue
 if any(x in {'node_modules','__pycache__','.git','logs','reference'} for x in parts):continue
 if f.suffix in {'.zip','.pyc','.blend1','.exr','.pfm','.log','.tmp'} or '.pending.' in f.name or f.name.startswith('.'):continue
 if f.name.endswith('.sha256') or f.name in {'PROJECT_MANIFEST.json','archive-validation.json'}:continue
 if f.suffix.lower() in {'.ttf','.otf','.woff','.woff2','.pem','.key'}:raise RuntimeError('Forbidden distributable file: '+str(f))
 files.append(f)
files.sort();status=json.loads((P/'preview/status.json').read_text());manifest={'project':N,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip(),'reviewed_main_iterations':status.get('iterations',0),'latest_self_assessed_score':status.get('score'),'requested_iterations':20000,'requested_score_above':95,'files':[]}
for f in files:
 manifest['files'].append({'path':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':hashlib.file_digest(open(f,'rb'),'sha256').hexdigest()})
(D/'PROJECT_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
with zipfile.ZipFile(tmp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in files:z.write(f,arcname=N+'/'+str(f.relative_to(P)))
 z.write(D/'PROJECT_MANIFEST.json',arcname=N+'/PROJECT_MANIFEST.json')
with zipfile.ZipFile(tmp) as z:
 bad=z.testzip();assert bad is None,bad
os.replace(tmp,out);digest=hashlib.file_digest(open(out,'rb'),'sha256').hexdigest();(D/(N+'.zip.sha256')).write_text(digest+'  '+out.name+'\n')
report={'archive':str(out),'bytes':out.stat().st_size,'sha256':digest,'file_count':len(files)+1,'crc_verified':True};(P/'reports/archive-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
