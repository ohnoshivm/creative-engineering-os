// Section motion: one orchestrated hero entrance, staggered reveals per section, and a scroll-mapped
// progress value the 3D stage reads. Everything is registered inside one gsap.matchMedia so reduced
// motion gets complete content and no travel.
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export interface ScrollStore { heroProgress: number }

export function initMotion(store: ScrollStore) {
  const mm = gsap.matchMedia();

  mm.add('(prefers-reduced-motion: no-preference)', () => {
    document.documentElement.classList.add('js-motion');
    const headings = gsap.utils.toArray<HTMLElement>('main h2, .hero-copy > *');
    headings.forEach((el) => el.setAttribute('data-reveal', ''));

    gsap.to('.hero-copy > *', { opacity: 1, y: 0, duration: 0.9, ease: 'expo.out', stagger: 0.08, delay: 0.15 });

    ScrollTrigger.batch('main section:not(.hero) [data-reveal], main section:not(.hero) p, main section:not(.hero) li', {
      start: 'top 85%',
      once: true,
      onEnter: (els) => gsap.to(els, { opacity: 1, y: 0, duration: 0.8, ease: 'expo.out', stagger: 0.07, overwrite: true }),
    });
    gsap.set('main section:not(.hero) p, main section:not(.hero) li', { opacity: 0, y: 24 });

    ScrollTrigger.create({
      trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true,
      onUpdate: (self) => { store.heroProgress = self.progress; },
    });

    return () => document.documentElement.classList.remove('js-motion');
  });

  return () => mm.revert();
}
