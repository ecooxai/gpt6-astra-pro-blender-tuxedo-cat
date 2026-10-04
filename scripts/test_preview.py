import json,time,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
P=Path(__file__).resolve().parents[1];errors=[];results={};target='http://127.0.0.1:8794/'
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/home/dev/.local/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
 page=browser.new_page(viewport={'width':1440,'height':1080},device_scale_factor=1)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto(target,wait_until='networkidle',timeout=60000);page.wait_for_timeout(1500)
 results['title']=page.title();results['desktop_overflow']=page.evaluate('document.documentElement.scrollWidth > innerWidth');page.screenshot(path=str(P/'preview/renders/desktop-ui.png'),full_page=True,timeout=120000,animations='disabled')
 status=page.evaluate('fetch("status.json").then(r=>r.json())')
 if status.get('hero'):
  page.wait_for_function('document.querySelector("#hero").naturalWidth>0');results['hero_loaded']=True
  for view in status.get('views',[]):
   page.locator(f'[data-id="{view["id"]}"]').click();page.wait_for_timeout(250);assert view['file'] in page.locator('#hero').get_attribute('src')
  results['view_controls']=len(status.get('views',[]))
  page.locator('#renderMode').click()
 if status.get('model'):
  page.locator('#orbitMode').click();page.wait_for_function('window.catViewer !== undefined',timeout=120000);page.wait_for_timeout(2000)
  page.wait_for_function('catViewer.renderer.info.render.triangles > 0',timeout=120000)
  results['webgl_meshes']=page.evaluate('(()=>{let n=0;catViewer.scene.traverse(o=>{if(o.isMesh)n++});return n})()');results['webgl_triangles']=page.evaluate('catViewer.renderer.info.render.triangles')
  page.screenshot(path=str(P/'preview/renders/webgl-ui.png'),full_page=False,timeout=120000,animations='disabled')
  b=page.locator('#webgl').bounding_box();page.mouse.move(b['x']+b['width']*.6,b['y']+b['height']*.5);page.mouse.down();page.mouse.move(b['x']+b['width']*.25,b['y']+b['height']*.5,steps=12);page.mouse.up();page.wait_for_timeout(500);results['orbit_drag']=True
  page.locator('#renderMode').click();results['render_switchback']=page.locator('#hero').is_visible()
 for width,height in [(390,844),(768,1024)]:
  page.set_viewport_size({'width':width,'height':height});page.goto(target,wait_until='networkidle');page.wait_for_timeout(800);results[f'overflow_{width}']=page.evaluate('document.documentElement.scrollWidth > innerWidth');page.screenshot(path=str(P/f'preview/renders/ui-{width}.png'),full_page=True,timeout=120000,animations='disabled')
 results['page_errors']=errors;browser.close()
(P/'logs/browser-tests.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
if errors or any(v for k,v in results.items() if 'overflow' in k):sys.exit(1)
