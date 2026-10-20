import * as THREE from 'three';
import feedbackFrag from '../shaders/feedback.frag?raw';
import displayFrag from '../shaders/display.frag?raw';
import { fullscreenMaterial, quad, type Experiment } from './lib';

/** Multi-pass ping-pong: two half-float render targets swap each frame; a display pass draws the result. */
export function feedback(renderer: THREE.WebGLRenderer): Experiment {
  const camera = new THREE.Camera();
  const geometry = quad();
  const type = renderer.extensions.has('EXT_color_buffer_float') ? THREE.HalfFloatType : THREE.UnsignedByteType;
  const opts = { type, depthBuffer: false, minFilter: THREE.LinearFilter, magFilter: THREE.LinearFilter };
  let read = new THREE.WebGLRenderTarget(2, 2, opts);
  let write = new THREE.WebGLRenderTarget(2, 2, opts);
  const sim = { uPrev: { value: read.texture as THREE.Texture }, uResolution: { value: new THREE.Vector2(1, 1) }, uPointer: { value: new THREE.Vector2(0.5, 0.5) }, uTime: { value: 0 }, uInject: { value: 0 } };
  const simMat = fullscreenMaterial(feedbackFrag, sim);
  const dispUniforms = { uTex: { value: write.texture as THREE.Texture } };
  const dispMat = fullscreenMaterial(displayFrag, dispUniforms);
  const simScene = new THREE.Scene(); simScene.add(new THREE.Mesh(geometry, simMat));
  const dispScene = new THREE.Scene(); dispScene.add(new THREE.Mesh(geometry, dispMat));
  const last = new THREE.Vector2(0.5, 0.5);
  return {
    name: 'feedback',
    description: 'Ping-pong render targets: ink injected at the pointer, advected by a moving field, slowly fading.',
    frame(time, pointer) {
      const p = new THREE.Vector2(pointer.x * 0.5 + 0.5, pointer.y * 0.5 + 0.5);
      if (!pointer.active) p.set(0.5 + Math.cos(time * 0.7) * 0.25, 0.5 + Math.sin(time * 1.1) * 0.18); // idle path so the lab never looks dead
      sim.uInject.value = Math.min(1, last.distanceTo(p) * 60 + 0.15);
      last.copy(p);
      sim.uPointer.value.copy(p); sim.uTime.value = time; sim.uPrev.value = read.texture;
      renderer.setRenderTarget(write); renderer.render(simScene, camera);
      renderer.setRenderTarget(null);
      dispUniforms.uTex.value = write.texture; renderer.render(dispScene, camera);
      [read, write] = [write, read];
    },
    resize(w, h) { const s = 0.5; read.setSize(w * s, h * s); write.setSize(w * s, h * s); sim.uResolution.value.set(w, h); },
    destroy() { read.dispose(); write.dispose(); simMat.dispose(); dispMat.dispose(); geometry.dispose(); },
  };
}
