import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
export async function initViewer(el,url){
 const scene=new THREE.Scene();scene.background=new THREE.Color('#e8e9e5');
 const renderer=new THREE.WebGLRenderer({antialias:true,powerPreference:'low-power'});renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFShadowMap;renderer.shadowMap.autoUpdate=false;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.08;el.appendChild(renderer.domElement);
 const camera=new THREE.PerspectiveCamera(31,1,.025,100);camera.position.set(2.8,2.25,5.0);
 const controls=new OrbitControls(camera,renderer.domElement);controls.target.set(0,1.12,-.18);controls.enableDamping=true;controls.dampingFactor=.18;controls.minDistance=2;controls.maxDistance=11;controls.maxPolarAngle=Math.PI*.54;
 scene.add(new THREE.HemisphereLight(0xeef2ff,0xb0aaa0,1.65));
 const light=new THREE.DirectionalLight(0xfff0d8,3.0);light.position.set(-3,9,4);light.castShadow=true;light.shadow.mapSize.set(1024,1024);Object.assign(light.shadow.camera,{left:-3,right:3,top:3,bottom:-3,near:.1,far:16});light.shadow.radius=3;light.shadow.bias=-.00035;light.shadow.normalBias=.008;scene.add(light);
 const fill=new THREE.DirectionalLight(0xe4ecff,1.25);fill.position.set(4,3,0);scene.add(fill);const rim=new THREE.DirectionalLight(0xfff5df,1.8);rim.position.set(0,4,-4);scene.add(rim);
 const floor=new THREE.Mesh(new THREE.PlaneGeometry(12,12),new THREE.ShadowMaterial({opacity:.10}));floor.rotation.x=-Math.PI/2;floor.position.y=-.006;floor.receiveShadow=true;scene.add(floor);
 let model=null,dirty=true,visible=true,last=0,loadGeneration=0;
 function disposeModel(node){const geometries=new Set(),materials=new Set();node.traverse(o=>{if(o.isMesh){geometries.add(o.geometry);for(const m of [o.material].flat())materials.add(m)}});for(const g of geometries)g.dispose();for(const m of materials)m.dispose();}

 async function loadModel(source){const generation=++loadGeneration;const gltf=await new GLTFLoader().loadAsync(source);if(generation!==loadGeneration){disposeModel(gltf.scene);return;}gltf.scene.traverse(o=>{if(o.isMesh){const groom=o.name.toLowerCase().includes('groom');o.castShadow=!groom;o.receiveShadow=!groom;for(const m of [o.material].flat()){if(m.name.includes('coat')||m.name.includes('fibers')){m.roughness=.94;if('specularIntensity' in m)m.specularIntensity=.10}}}});if(model){scene.remove(model);disposeModel(model)}model=gltf.scene;scene.add(model);renderer.shadowMap.needsUpdate=true;dirty=true;if(window.catViewer)window.catViewer.model=model;}
 try{await loadModel(url)}catch(error){renderer.dispose();renderer.domElement.remove();controls.dispose();throw error}controls.addEventListener('change',()=>dirty=true);new IntersectionObserver(v=>{visible=v[0].isIntersecting;if(visible)dirty=true}).observe(el);
 function resize(){const w=el.clientWidth,h=el.clientHeight;if(w&&h){renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();dirty=true;}}
 new ResizeObserver(resize).observe(el);resize();
 function frame(now){requestAnimationFrame(frame);if(visible&&!el.hidden&&now-last>33){controls.update();if(dirty){renderer.render(scene,camera);dirty=false;last=now;}}}requestAnimationFrame(frame);
 renderer.domElement.setAttribute('aria-label','Interactive black and white cat. Drag to orbit; scroll or pinch to zoom.');renderer.domElement.setAttribute('role','img');window.catViewer={scene,renderer,camera,controls,model};return {resize,scene,loadModel};
}
