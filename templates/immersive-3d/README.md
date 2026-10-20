# Template C — Immersive 3D

Vite + TypeScript + three.js + GSAP. For sites where a realtime scene is the hero.

## Use

```bash
~/creative-engineering-os/scripts/new-project.sh immersive-3d ~/projects/my-site
cd ~/projects/my-site && npm install
npm run dev            # http://localhost:5173
npm test               # Playwright: desktop, mobile, reduced-motion, no-WebGL (uses installed Chrome)
npm run test:visual    # screenshot regression (?still freezes the scene)
npm run build && npm run preview
npm run lhci           # Lighthouse CI against the preview build
npm run audit:visual   # full visual-audit capture (needs `npm run preview` running)
npm run assets:optimize -- in.glb out.glb   # glTF-Transform (meshopt + WebP)
```

## Architecture (read before changing)

- `index.html` holds all content and a drawn SVG poster. It renders without JS.
- `src/main.ts` boots motion, then imports the 3D stage on idle **only if WebGL2 exists**. `data-stage` on `<html>`
  reports `live` or `poster` (tests assert it).
- `src/core/loop.ts` — the only render-loop owner (adds the GL frame to `gsap.ticker`). Paused offscreen.
- `src/core/pointer.ts` — pointer store; `src/motion/sections.ts` — scroll store + reveals inside `gsap.matchMedia`.
- `src/gl/stage.ts` — renderer, code-built environment (PMREM), the example ribbon, `destroy()` that releases the GPU.
- Reduced motion or `?still` → one deterministic frame, no loop.

Replace the ribbon with your concept's object; keep the boot order, ownership and tests.
See `CHECKLIST.md` before shipping.

## Verification server

Production preview uses `http://localhost:4176`. Playwright builds and starts its own preview, and fails if that
port is already occupied; stop a manually started preview before running tests. This prevents a test suite from
quietly exercising another template.
