import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { stillMode } from '../core/env';
gsap.registerPlugin(ScrollTrigger);
export interface ScrollStore { heroProgress: number }
export function initMotion(store: ScrollStore) {
  const mm = gsap.matchMedia();
  mm.add('(prefers-reduced-motion: no-preference)', () => {
    if (stillMode()) return;
    gsap.from('.hero-copy > *', { opacity: 0, y: 18, duration: .8, stagger: .08, ease: 'expo.out', clearProps: 'all' });
    ScrollTrigger.create({ trigger: '.hero', start: 'top top', end: 'bottom top', onUpdate: self => { store.heroProgress = self.progress; } });
  });
  return () => mm.revert();
}
