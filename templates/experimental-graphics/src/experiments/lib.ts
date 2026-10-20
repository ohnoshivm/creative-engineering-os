import * as THREE from 'three';
import vert from '../shaders/fullscreen.vert?raw';
import common from '../shaders/common.glsl?raw';

/** A lab experiment: owns its GPU resources, reads pointer state, renders one frame per call. */
export interface Experiment {
  name: string;
  description: string;
  frame(time: number, pointer: { x: number; y: number; active: boolean }): void;
  resize(width: number, height: number): void;
  destroy(): void;
}

/** Fullscreen GLSL3 material; `// @common` in a fragment shader is replaced by the shared helpers. */
export function fullscreenMaterial(frag: string, uniforms: Record<string, THREE.IUniform>) {
  return new THREE.RawShaderMaterial({
    glslVersion: THREE.GLSL3,
    vertexShader: vert,
    fragmentShader: frag.replace('// @common', common),
    uniforms,
    depthTest: false,
    depthWrite: false,
  });
}

export const quad = () => new THREE.PlaneGeometry(2, 2);
