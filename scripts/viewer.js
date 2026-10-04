import * as THREE from 'three';
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js';
import {GLTFLoader} from 'three/examples/jsm/loaders/GLTFLoader.js';
export async function initViewer(el,url){
 const scene=new THREE.Scene();scene.background=new THREE.Color('#e8e9e5');
 const renderer=new THREE.WebGLRenderer({antialias:true,powerPreference:'low-power'});renderer.setPixelRatio(Math.min(devicePixelRatio,1.65));renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.2;el.appendChild(renderer.domElement);
 const camera=new THREE.PerspectiveCamera(31,1,.025,100);camera.position.set(3.0,2.30,5.4);
 const controls=new OrbitControls(camera,renderer.domElement);controls.target.set(0,1.12,-.18);controls.enableDamping=true;controls.dampingFactor=.08;controls.minDistance=2;controls.maxDistance=11;controls.maxPolarAngle=Math.PI*.54;
 scene.add(new THREE.HemisphereLight(0xeef2ff,0xb0aaa0,2.2));
 const light=new THREE.DirectionalLight(0xfff0d8,3.8);light.position.set(-3,6,5);light.castShadow=true;light.shadow.mapSize.set(2048,2048);Object.assign(light.shadow.camera,{left:-3,right:3,top:3,bottom:-3,near:.1,far:16});light.shadow.bias=-.00035;light.shadow.normalBias=.012;scene.add(light);
 const fill=new THREE.DirectionalLight(0xe4ecff,1.7);fill.position.set(4,3,0);scene.add(fill);const rim=new THREE.DirectionalLight(0xfff5df,2.5);rim.position.set(0,4,-4);scene.add(rim);
 const floor=new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.MeshStandardMaterial({color:0xe8e9e5,roughness:1}));floor.rotation.x=-Math.PI/2;floor.position.y=-.008;floor.receiveShadow=true;scene.add(floor);
 const gltf=await new GLTFLoader().loadAsync(url);gltf.scene.traverse(o=>{if(o.isMesh){o.castShadow=!o.name.includes('groom');o.receiveShadow=true;}});scene.add(gltf.scene);
 let visible=true;new IntersectionObserver(v=>visible=v[0].isIntersecting).observe(el);
 function resize(){const w=el.clientWidth,h=el.clientHeight;if(w&&h){renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();controls.update();renderer.render(scene,camera);}}
 new ResizeObserver(resize).observe(el);resize();function frame(){requestAnimationFrame(frame);if(visible&&!el.hidden){controls.update();renderer.render(scene,camera)}}frame();
 window.catViewer={scene,renderer,camera,controls,model:gltf.scene};return {resize,scene};
}
