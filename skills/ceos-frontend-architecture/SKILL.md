---
name: ceos-frontend-architecture
description: Chooses and structures the frontend for creative websites — Astro vs Vite vs Next.js/React, TypeScript, modern CSS (cascade layers, container queries, custom properties), component boundaries, rendering lifecycle, animation and WebGL integration, state ownership, asset loading and maintainability. Use when starting a project's codebase, deciding a stack, integrating GSAP/Three.js into a framework, structuring components, or when an animated/3D site has leaks, double render loops or tangled state.
---

# Frontend architecture for creative sites

## Purpose

The smallest architecture that carries the concept, with explicit ownership of DOM, scroll, render loop and state.

## Stack decision (default to the lightest)

| Situation | Choose | Why |
|---|---|---|
| Content-led, editorial, few interactive islands | **Astro** (static, islands) | HTML-first, zero JS by default, great SEO |
| One-page or few-page cinematic / WebGL experience, no app state | **Vite + TypeScript** (vanilla modules) | Full control of the render loop, minimal runtime |
| Many routes + CMS + app-like features, team on React | **Next.js** (App Router) | Routing, data, image pipeline |
| React team needs declarative 3D | **React Three Fiber** inside Vite/Next | Only if the team is React-native; otherwise raw three |
| Tiny WebGL effect, no scene graph | **OGL** or raw WebGL2 | ~a few KB vs three.js |

Never default to React. Write the choice and its rejected alternatives in `docs/ARCHITECTURE.md`.

## Ownership model (write it down)

- **DOM is the layout engine.** All content, links and headings are HTML. Canvas reads DOM rects to place GL objects
  (DOM-synced planes) — never the other way round.
- **One render loop owner** (`gsap.ticker` or a single `requestAnimationFrame` scheduler) that ticks: input → scroll →
  animation → render. Pause it when the canvas is offscreen (`IntersectionObserver`) or the tab is hidden.
- **One scroll source** (native or Lenis), exposed as a read-only store (`scroll.y`, `velocity`, `progress`).
- **State**: small explicit stores (signals or a tiny observable) for app state; scene state derived from it.
  No component reaches into another's internals.
- **Lifecycle**: every module exports `init()` / `destroy()`; destroy disposes geometries, materials, textures,
  render targets, listeners, observers, timelines.

## Modern CSS baseline

`@layer reset, tokens, base, components, utilities;` · custom properties for all tokens · container queries for
components · `clamp()` type · logical properties · `:focus-visible` · `prefers-reduced-motion` and `prefers-contrast`
· `content-visibility: auto` for long below-fold sections (with `contain-intrinsic-size`).

## Loading strategy

- Ship HTML + CSS first; the hero text renders without JS.
- Load heavy 3D/JS after first paint (`import()` on idle or on intersection); show a designed poster, not a spinner.
- Budget: initial JS (excluding the 3D chunk) ≤ 150–200 KB gz; hero assets ≤ 2–3 MB; fonts ≤ 2 families, subset woff2.
- Preload only the LCP image/font. Use `fetchpriority="high"` on the LCP element.

## Project structure (vanilla Vite example)

```
src/
  main.ts            boot: feature-detect → init modules → start loop
  core/loop.ts       single RAF scheduler
  core/scroll.ts     scroll store (native or Lenis)
  core/pointer.ts    pointer store (normalised, smoothed)
  gl/                scene, materials, passes (no DOM queries except via sync helpers)
  motion/            timelines per section (gsap.context per section)
  sections/          DOM behaviour per section
  styles/            tokens.css, base.css, sections/*.css
tests/               Playwright smoke + visual
```

## Verification

`npm run build` passes with no warnings worth fixing; bundle report reviewed; route/section mount-unmount 20× shows
no growth in JS heap, WebGL contexts, listeners (DevTools Memory / `performance.memory` + `renderer.info`).

## Failure criteria

React chosen "because default"; content rendered only in canvas; two RAF loops; scroll read in several places;
no `destroy()`; heavy 3D blocking first paint; global CSS without layers fighting component styles.
