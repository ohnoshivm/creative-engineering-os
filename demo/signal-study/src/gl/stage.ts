import * as THREE from 'three';
import vertexShader from './wave.vert.glsl?raw';
import fragmentShader from './wave.frag.glsl?raw';
export interface StageInput { pointer: { x: number; y: number }; fold: number; tension: number }
export function createStage(host: HTMLElement) {
  const canvas=document.createElement('canvas'); canvas.setAttribute('aria-hidden','true');host.appendChild(canvas);
  const renderer=new THREE.WebGLRenderer({canvas,antialias:true,powerPreference:'low-power'});
  renderer.outputColorSpace=THREE.SRGBColorSpace; renderer.setClearColor(0xcddbef);
  const scene=new THREE.Scene();
  const camera=new THREE.PerspectiveCamera(32,2,.1,50);camera.position.set(0,0,10);
  const geometry=new THREE.PlaneGeometry(9,4.5,128,64);
  const uniforms={uLines:{value:64},uTime:{value:0},uTension:{value:.4},uPhase:{value:0},uPointer:{value:new THREE.Vector2()}};
  const material=new THREE.ShaderMaterial({vertexShader,fragmentShader,uniforms,side:THREE.DoubleSide});
  const wave=new THREE.Mesh(geometry,material);wave.rotation.x=-.65;wave.rotation.z=-.12;scene.add(wave);
  let lastTime=0;
  function draw(){renderer.render(scene,camera);host.dataset.draws=String(renderer.info.render.calls);host.dataset.triangles=String(renderer.info.render.triangles);}
  function resize(){const w=host.clientWidth,h=host.clientHeight;renderer.setPixelRatio(Math.min(devicePixelRatio||1,1.5));renderer.setSize(w,h,false);camera.aspect=w/h;camera.position.z=w/h<1.3?17:11.4;camera.updateProjectionMatrix();uniforms.uLines.value=w<760?40:64;draw();}
  const ro=new ResizeObserver(resize);ro.observe(host);resize();
  function frame(time:number,dt:number,input:StageInput){lastTime=time;const k=1-Math.exp(-dt*6);uniforms.uTime.value=time;uniforms.uTension.value+=(input.tension-uniforms.uTension.value)*k;uniforms.uPhase.value+=(input.fold-uniforms.uPhase.value)*k;uniforms.uPointer.value.x+=(input.pointer.x-uniforms.uPointer.value.x)*k;uniforms.uPointer.value.y+=(input.pointer.y-uniforms.uPointer.value.y)*k;wave.rotation.y=input.pointer.x*.08;draw();host.dataset.phase=uniforms.uPhase.value.toFixed(3);host.dataset.pointer=uniforms.uPointer.value.x.toFixed(3);}
  function still(input:StageInput){uniforms.uTension.value=input.tension;uniforms.uPhase.value=input.fold;uniforms.uPointer.value.set(input.pointer.x,input.pointer.y);frame(lastTime,1,input);}
  function destroy(){ro.disconnect();geometry.dispose();material.dispose();renderer.dispose();renderer.forceContextLoss();canvas.remove();}
  return{canvas,renderer,frame,still,destroy};
}
