// Scroll choreography for Template B.
// - Native scroll by default. `?lenis` opts into Lenis smoothing, driven from gsap.ticker (one RAF owner).
// - Everything motion-related is registered in one gsap.matchMedia, so reduced motion gets the static page.
// - Content is visible without JS; classes added here opt into hidden start states.
import './styles.css';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

/** Wrap words in spans. Assistive tech reads one visually hidden copy of the sentence; the animated
 *  word spans are presentation only (aria-hidden), so screen readers never hear fragments. */
function splitWords(el: HTMLElement) {
  const text = (el.textContent ?? '').trim();
  const words = text.split(/\s+/).map((w) => `<span class="w">${w}</span>`).join(' ');
  el.innerHTML = `<span class="visually-hidden">${text}</span><span aria-hidden="true">${words}</span>`;
  return Array.from(el.querySelectorAll<HTMLElement>('.w'));
}

async function maybeLenis() {
  if (!new URLSearchParams(location.search).has('lenis')) return () => {};
  const { default: Lenis } = await import('lenis');
  const lenis = new Lenis({ lerp: 0.12, wheelMultiplier: 1 }); // τ≈100 ms feel; keyboard/anchors stay native
  lenis.on('scroll', ScrollTrigger.update);
  const raf = (t: number) => lenis.raf(t * 1000);
  gsap.ticker.add(raf);
  gsap.ticker.lagSmoothing(0);
  return () => { gsap.ticker.remove(raf); lenis.destroy(); };
}

const mm = gsap.matchMedia();
mm.add('(prefers-reduced-motion: no-preference)', () => {
  document.documentElement.classList.add('js-motion');
  let killLenis = () => {};
  maybeLenis().then((k) => { killLenis = k; });

  // 1. Hero: the one load moment — words rise on a short beat.
  const title = document.querySelector<HTMLElement>('[data-split]');
  if (title) gsap.to(splitWords(title), { opacity: 1, y: 0, duration: 0.9, ease: 'expo.out', stagger: 0.06, delay: 0.1 });

  // 2. Read-along: pinned while the words light up in scroll order (scrubbed, ease none inside).
  const statement = document.querySelector<HTMLElement>('[data-readalong]');
  if (statement) {
    const words = splitWords(statement);
    const path = document.querySelector<SVGPathElement>('.pulse-line path');
    const len = path?.getTotalLength() ?? 0;
    if (path) gsap.set(path, { strokeDasharray: len, strokeDashoffset: len });
    const tl = gsap.timeline({ scrollTrigger: { trigger: '.read-pin', start: 'top top', end: '+=140%', scrub: 0.6, pin: true } });
    tl.to(words, { opacity: 1, ease: 'none', stagger: 0.1, duration: 0.3 }, 0);
    if (path) tl.to(path, { strokeDashoffset: 0, ease: 'none', duration: words.length * 0.1 }, 0);
  }

  // 3. Horizontal run of tempos: vertical scroll drives x; ease must be 'none' for a 1:1 mapping.
  const track = document.querySelector<HTMLElement>('.tempo-track');
  if (track) {
    gsap.to(track, {
      x: () => -(track.scrollWidth - document.documentElement.clientWidth),
      ease: 'none',
      scrollTrigger: { trigger: '.tempos', start: 'top top', end: () => '+=' + (track.scrollWidth - innerWidth), scrub: 0.5, pin: true, invalidateOnRefresh: true },
    });
  }

  document.fonts?.ready.then(() => ScrollTrigger.refresh());
  return () => { killLenis(); document.documentElement.classList.remove('js-motion'); };
});
