"""Publish completed local artifacts without inventing progress or review scores."""
import json,time,os
from pathlib import Path
P=Path(__file__).resolve().parents[1];D=P/'preview/renders'
def kind(n):
 if n.startswith('r') and n[1:3].isdigit():return 'Blender EEVEE'
 if n.startswith('beauty_'):return 'Blender Cycles + OIDN physical lighting'
 if n.startswith('lighting_'):return 'Blender Cycles lighting comparison'
 if n.startswith('experiment_'):return 'Blender experiment / '+n.rsplit('_',1)[-1].split('.')[0].upper()
 return 'Headless Chromium quality check'
while True:
 try:
  files=[f for f in D.glob('*.png') if time.time()-f.stat().st_mtime>2]
  files.sort(key=lambda f:(not(f.name.startswith('r') and f.name[1:3].isdigit()),-f.stat().st_mtime))
  data=[dict(file=f.name,modified=f.stat().st_mtime_ns,kind=kind(f.name),kb=round(f.stat().st_size/1024),path=str(f)) for f in files]
  text=json.dumps(data,indent=2);dest=D/'manifest.json'
  if not dest.exists() or dest.read_text()!=text:
   tmp=D/'manifest.watch.tmp';tmp.write_text(text);os.replace(tmp,dest)
 except (OSError,ValueError) as e:print(str(e),flush=True)
 time.sleep(4)
