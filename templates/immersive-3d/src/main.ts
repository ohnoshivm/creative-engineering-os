// Boot order: HTML and poster are already painted → motion → (idle) 3D stage, only when WebGL2 exists.
import './styles.css';
import { canUseWebGL2, prefersReducedMotion, stillMode } from './core/env';
import { createLoop } from './core/loop';
import { createPointer } from './core/pointer';
import { initMotion, type ScrollStore } from './motion/sections';

const scroll: ScrollStore = { heroProgress: 0 };
const destroyMotion = initMotion(scroll);
const host = document.querySelector<HTMLElement>('[data-stage]');

async function mountStage(el: HTMLElement) {
  const { createStage } = await import('./gl/stage');
  const stage = createStage(el);
  const pointer = createPointer(el);
  const loop = createLoop();
  const input = { pointer: pointer.state, fold: 0 };
  el.classList.add('is-live');
  document.documentElement.dataset.stage = 'live';

  if (prefersReducedMotion() || stillMode()) {
    stage.frame(1.2, 1, { pointer: { x: 0.2, y: 0.1 }, fold: 0.2 }); // one deterministic still frame
    return () => { pointer.destroy(); stage.destroy(); };
  }

  loop.add((time, dt) => { input.fold = scroll.heroProgress; stage.frame(time, dt, input); });

  // Render only while the stage is on screen and the tab is visible.
  const io = new IntersectionObserver(([entry]) => (entry.isIntersecting ? loop.start() : loop.stop()));
  io.observe(el);
  stage.canvas.addEventListener('webglcontextlost', (e) => { e.preventDefault(); loop.stop(); el.classList.remove('is-live'); });

  return () => { io.disconnect(); loop.destroy(); pointer.destroy(); stage.destroy(); };
}

let destroyStage: (() => void) | undefined;
if (host && canUseWebGL2()) {
  const start = () => mountStage(host).then((d) => { destroyStage = d; }).catch((err) => {
    console.warn('3D stage unavailable, keeping poster:', err);
    document.documentElement.dataset.stage = 'poster';
  });
  if ('requestIdleCallback' in window) requestIdleCallback(start, { timeout: 1200 }); else setTimeout(start, 300);
} else {
  document.documentElement.dataset.stage = 'poster';
}

// Vite HMR / SPA teardown hook.
if (import.meta.hot) import.meta.hot.dispose(() => { destroyStage?.(); destroyMotion(); });
