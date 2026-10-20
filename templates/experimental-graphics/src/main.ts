// Lab shell: one renderer, one loop, swappable experiments (`?exp=name`), a live frame-time readout,
// reduced-motion → single frame, no WebGL2 → readable message.
import './styles.css';
import * as THREE from 'three';
import type { Experiment } from './experiments/lib';
import { raymarch } from './experiments/raymarch';
import { feedback } from './experiments/feedback';

const REGISTRY = new Map<string, (r: THREE.WebGLRenderer) => Experiment>([['raymarch', raymarch], ['feedback', feedback]]);
const canvas = document.querySelector<HTMLCanvasElement>('#gl')!;
const stat = document.querySelector<HTMLElement>('#stat')!;
const desc = document.querySelector<HTMLElement>('#exp-desc')!;
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
const still = new URLSearchParams(location.search).has('still');

const gl = canvas.getContext('webgl2', { antialias: false, powerPreference: 'high-performance' });
if (!gl) {
  document.querySelector<HTMLElement>('#fallback')!.hidden = false;
  document.documentElement.dataset.lab = 'unavailable';
} else {
  const renderer = new THREE.WebGLRenderer({ canvas, context: gl });
  renderer.setPixelRatio(Math.min(devicePixelRatio, 1.25)); // labs run fragment-heavy shaders; cap DPR
  const pointer = { x: 0, y: 0, active: false };
  addEventListener('pointermove', (e) => { pointer.x = (e.clientX / innerWidth) * 2 - 1; pointer.y = -((e.clientY / innerHeight) * 2 - 1); pointer.active = true; }, { passive: true });

  let exp: Experiment | null = null;
  function drawStill() {
    if (!exp || (!reduced && !still)) return;
    if (still && exp.name === 'feedback') {
      // Reproducible accumulated ink, computed before the browser presents one static frame.
      for (let i = 0; i < 120; i++) exp.frame(i / 60, pointer);
    } else exp.frame(2, pointer);
  }
  const size = () => {
    renderer.setSize(innerWidth, innerHeight, false);
    const v = renderer.getDrawingBufferSize(new THREE.Vector2());
    exp?.resize(v.x, v.y);
    drawStill(); // resizing clears the buffer, including when no animation loop is running
  };
  function select(name: string) {
    exp?.destroy();
    exp = (REGISTRY.get(name) ?? raymarch)(renderer);
    desc.textContent = exp.description;
    document.querySelectorAll<HTMLButtonElement>('[data-exp]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.exp === exp!.name)));
    const query = new URLSearchParams(location.search);
    query.set('exp', exp.name);
    history.replaceState(null, '', `?${query}`);
    size();
    document.documentElement.dataset.lab = exp.name;
  }
  document.querySelectorAll<HTMLButtonElement>('[data-exp]').forEach((b) => {
    b.disabled = false;
    b.addEventListener('click', () => select(b.dataset.exp!));
  });
  addEventListener('resize', size);
  select(new URLSearchParams(location.search).get('exp') ?? 'raymarch');

  if (!reduced && !still) {
    const times: number[] = [];
    let last = performance.now();
    renderer.setAnimationLoop((t) => {
      exp?.frame(t / 1000, pointer);
      const now = performance.now(); times.push(now - last); last = now;
      if (times.length >= 60) { const s = [...times].sort((a, b) => a - b); stat.textContent = `frame p50 ${s[30].toFixed(1)} ms · p95 ${s[57].toFixed(1)} ms`; times.length = 0; }
    });
  } else {
    stat.textContent = reduced ? 'Reduced motion: showing a single frame.' : 'Still frame for visual inspection.';
  }
}
