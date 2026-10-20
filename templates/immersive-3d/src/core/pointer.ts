// Pointer store: normalised -1..1 relative to an element, smoothed by the consumer.
export interface PointerState { x: number; y: number; inside: boolean }

export function createPointer(target: HTMLElement) {
  const state: PointerState = { x: 0, y: 0, inside: false };
  const onMove = (e: PointerEvent) => {
    const r = target.getBoundingClientRect();
    state.x = ((e.clientX - r.left) / r.width) * 2 - 1;
    state.y = -(((e.clientY - r.top) / r.height) * 2 - 1);
    state.inside = true;
  };
  const onLeave = () => { state.inside = false; state.x = 0; state.y = 0; };
  target.addEventListener('pointermove', onMove, { passive: true });
  target.addEventListener('pointerleave', onLeave);
  return { state, destroy: () => { target.removeEventListener('pointermove', onMove); target.removeEventListener('pointerleave', onLeave); } };
}
