// Realtime stage: a ribbon of polished metal that bends toward the pointer and folds with scroll.
// Lighting comes from an environment built in code (emissive panels → PMREM), so no HDR file is downloaded.
import * as THREE from 'three';

export interface StageInput { pointer: { x: number; y: number }; fold: number }

const RIBBON_SEGMENTS_X = 220;
const RIBBON_SEGMENTS_Y = 18;

function buildEnvironment(renderer: THREE.WebGLRenderer): THREE.Texture {
  const pmrem = new THREE.PMREMGenerator(renderer);
  const room = new THREE.Scene();
  const box = new THREE.Mesh(new THREE.BoxGeometry(30, 30, 30), new THREE.MeshBasicMaterial({ color: 0x0b0a08, side: THREE.BackSide }));
  room.add(box);
  const panel = (color: number, intensity: number, w: number, h: number, pos: [number, number, number], rot: [number, number, number] = [0, 0, 0]) => {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color, side: THREE.DoubleSide }));
    (m.material as THREE.MeshBasicMaterial).color.multiplyScalar(intensity);
    m.position.set(...pos); m.rotation.set(...rot); room.add(m);
  };
  panel(0xfff4e6, 3, 40, 10, [0, 7, 12], [0, 0, 0.12]); // warm softbox behind camera, tilted horizon
  panel(0x2f4bff, 4, 4, 16, [-12, 0, 2], [0, Math.PI / 2, 0]); // ultramarine strip (brand accent)
  panel(0xffffff, 6, 20, 3, [0, 12, 0], [Math.PI / 2, 0, 0]); // overhead
  const texture = pmrem.fromScene(room, 0.02).texture;
  pmrem.dispose();
  room.traverse((o) => { if (o instanceof THREE.Mesh) { o.geometry.dispose(); (o.material as THREE.Material).dispose(); } });
  return texture;
}

export function createStage(host: HTMLElement) {
  const canvas = document.createElement('canvas');
  canvas.setAttribute('aria-hidden', 'true');
  host.appendChild(canvas);

  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: 'high-performance' });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.0;
  renderer.setClearColor(0x16140f, 1);

  const scene = new THREE.Scene();
  scene.environment = buildEnvironment(renderer);
  const camera = new THREE.PerspectiveCamera(32, 2, 0.1, 50);
  camera.position.set(0, 0, 9);

  const geometry = new THREE.PlaneGeometry(9, 1.3, RIBBON_SEGMENTS_X, RIBBON_SEGMENTS_Y);
  const rest = Float32Array.from(geometry.attributes.position.array as Float32Array);
  const material = new THREE.MeshPhysicalMaterial({ color: 0xd9d2c4, metalness: 1, roughness: 0.18, clearcoat: 1, clearcoatRoughness: 0.08, iridescence: 0.35, side: THREE.DoubleSide });
  const ribbon = new THREE.Mesh(geometry, material);
  scene.add(ribbon);

  const smooth = { x: 0, y: 0, fold: 0 };
  const pos = geometry.attributes.position as THREE.BufferAttribute;

  function deform(time: number) {
    // A twisted S-ribbon: the centre line waves through depth, the cross-section rotates along the length,
    // so both faces turn into the light. Scroll adds fold (more twist, deeper wave); pointer bends it.
    const a = pos.array as Float32Array;
    const fold = smooth.fold;
    for (let i = 0; i < pos.count; i++) {
      const x0 = rest[i * 3], y0 = rest[i * 3 + 1];
      const u = x0 / 4.5; // -1..1 along the ribbon
      const wave = Math.sin(u * Math.PI * (0.9 + fold * 0.6) + time * 0.25);
      const cx = u * (4.2 - fold * 1.2);
      const cy = wave * (0.35 + fold * 0.5) + smooth.y * 0.35 * u;
      const cz = Math.cos(u * Math.PI * (0.8 + fold)) * (0.9 + fold * 0.8) - 0.9 + smooth.x * 0.8 * u;
      const theta = u * Math.PI * (0.75 + fold * 1.1) + smooth.x * 0.5 + Math.sin(time * 0.3) * 0.05;
      a[i * 3] = cx;
      a[i * 3 + 1] = cy + y0 * Math.cos(theta);
      a[i * 3 + 2] = cz + y0 * Math.sin(theta);
    }
    pos.needsUpdate = true;
    geometry.computeVertexNormals();
  }

  let hasRendered = false;
  function resize() {
    const w = host.clientWidth, h = host.clientHeight;
    const dpr = Math.min(window.devicePixelRatio || 1, w < 760 ? 1.5 : 2);
    renderer.setPixelRatio(dpr);
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.position.z = w / h < 1 ? 12.5 : 7.6;
    camera.updateProjectionMatrix();
    // Resizing clears the drawing buffer. Repaint the current geometry even when the loop is paused.
    if (hasRendered) renderer.render(scene, camera);
  }
  const ro = new ResizeObserver(resize);
  ro.observe(host);
  resize();

  function frame(time: number, dt: number, input: StageInput) {
    const k = 1 - Math.exp(-dt * 4); // frame-rate-independent smoothing toward the input
    smooth.x += (input.pointer.x - smooth.x) * k;
    smooth.y += (input.pointer.y - smooth.y) * k;
    smooth.fold += (input.fold - smooth.fold) * k;
    ribbon.rotation.y = -0.25 + smooth.x * 0.25;
    ribbon.rotation.x = -smooth.y * 0.15;
    deform(time);
    renderer.render(scene, camera);
    hasRendered = true;
  }

  function destroy() {
    ro.disconnect();
    geometry.dispose(); material.dispose(); scene.environment?.dispose();
    renderer.dispose(); renderer.forceContextLoss(); canvas.remove();
  }

  return { canvas, renderer, frame, destroy };
}
