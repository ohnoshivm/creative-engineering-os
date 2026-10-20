// Capability and preference detection, evaluated once at boot.
export const prefersReducedMotion = (): boolean => matchMedia('(prefers-reduced-motion: reduce)').matches;

export function canUseWebGL2(): boolean {
  try {
    const c = document.createElement('canvas');
    const gl = c.getContext('webgl2');
    gl?.getExtension('WEBGL_lose_context')?.loseContext();
    return !!gl;
  } catch {
    return false;
  }
}

/** `?still` freezes the scene on one deterministic frame (visual regression, screenshots). */
export const stillMode = (): boolean => new URLSearchParams(location.search).has('still');
