import * as THREE from 'three';
import frag from '../shaders/raymarch.frag?raw';
import { fullscreenMaterial, quad, type Experiment } from './lib';

/** SDF raymarching: smooth-min blobs; rendered at reduced resolution (fragment cost scales with pixels). */
export function raymarch(renderer: THREE.WebGLRenderer): Experiment {
  const scene = new THREE.Scene();
  const camera = new THREE.Camera();
  const uniforms = { uResolution: { value: new THREE.Vector2(1, 1) }, uPointer: { value: new THREE.Vector2() }, uTime: { value: 0 }, uBlend: { value: 0.55 } };
  const material = fullscreenMaterial(frag, uniforms);
  const geometry = quad();
  scene.add(new THREE.Mesh(geometry, material));
  return {
    name: 'raymarch',
    description: 'Signed distance fields merged with a smooth minimum; one blob follows the pointer.',
    frame(time, pointer) {
      uniforms.uTime.value = time;
      uniforms.uPointer.value.lerp(new THREE.Vector2(pointer.x, pointer.y), 0.12);
      renderer.render(scene, camera);
    },
    resize(w, h) { uniforms.uResolution.value.set(w, h); },
    destroy() { geometry.dispose(); material.dispose(); },
  };
}
