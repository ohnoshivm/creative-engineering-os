# Template B — Cinematic motion

Vite + TypeScript + GSAP/ScrollTrigger (+ optional Lenis). For scroll-driven 2D stories: kinetic type, pinned
scenes, horizontal sequences.

```bash
~/creative-engineering-os/scripts/new-project.sh motion-heavy ~/projects/my-story
npm install && npm run dev          # http://localhost:5173 (append ?lenis to try smooth scroll)
npm test                            # desktop, mobile, reduced-motion, no-JS; axe; read-along + horizontal run asserted
npm run test:visual
npm run build && npm run preview
```

- One `gsap.matchMedia` registers all motion; reduced motion and no-JS get the complete static page.
- Hidden start states exist only under `.js-motion` (added by JS) — content never depends on a script finishing.
- Word splitting keeps one visually hidden copy of the sentence for assistive tech; unlit words stay ≥ 3:1 contrast.
- Lenis is opt-in (`?lenis`), driven from `gsap.ticker` (one RAF), `lagSmoothing(0)`; keyboard and anchors stay native.
- The horizontal run uses `ease: 'none'` for a 1:1 scroll mapping and `invalidateOnRefresh` for resizes.

## Verification server

Production preview uses `http://localhost:4174`. Playwright builds and starts its own preview, and fails if that
port is already occupied; stop a manually started preview before running tests. This prevents a test suite from
quietly exercising another template.
