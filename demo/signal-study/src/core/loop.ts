// The single render-loop owner. gsap.ticker already runs one requestAnimationFrame for all tweens;
// the GL frame is added to the same tick so motion and rendering never drift apart.
import { gsap } from 'gsap';

type Tick = (time: number, deltaSeconds: number) => void;

export function createLoop() {
  const subscribers = new Set<Tick>();
  let running = false;
  const tick = (time: number, deltaMs: number) => {
    const dt = Math.min(deltaMs / 1000, 1 / 20); // clamp long frames (tab switches) so springs stay stable
    for (const fn of subscribers) fn(time, dt);
  };
  return {
    add(fn: Tick) { subscribers.add(fn); return () => subscribers.delete(fn); },
    start() { if (!running) { gsap.ticker.add(tick); running = true; } },
    stop() { if (running) { gsap.ticker.remove(tick); running = false; } },
    destroy() { this.stop(); subscribers.clear(); },
  };
}
