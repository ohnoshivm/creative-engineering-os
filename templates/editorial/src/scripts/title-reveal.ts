// The page's single orchestrated moment: the title lines unmask once on load.
// Respects reduced motion (does nothing) and fails open (lines are visible until JS opts in).
import { gsap } from 'gsap';

const mm = gsap.matchMedia();
mm.add('(prefers-reduced-motion: no-preference)', () => {
  const lines = gsap.utils.toArray<HTMLElement>('.title .line');
  if (!lines.length) return;
  document.documentElement.classList.add('js-motion');
  gsap.to(lines, { clipPath: 'inset(0 0 0% 0)', y: 0, duration: 1.1, ease: 'expo.out', stagger: 0.09, delay: 0.1 });
});
