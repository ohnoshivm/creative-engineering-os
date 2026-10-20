---
name: ceos-performance-engineering
description: Measures and fixes performance of creative, animated and WebGL websites — Core Web Vitals (LCP, INP, CLS), DevTools performance traces, main-thread long tasks, GPU/frame-time stability, memory leaks, bundle and asset weight, loading strategy, adaptive quality and progressive enhancement. Use when a site feels slow or janky, before launch, when setting budgets, when adding heavy 3D/video/fonts, or when someone claims it's "fast" without numbers.
---

# Performance engineering

## Principle

Measure in conditions that resemble visitors, find the biggest cost, fix it, measure again. Average fps lies; look
at distributions and freezes.

## Budgets (defaults; agree per project in ARCHITECTURE.md)

LCP ≤ 2.5 s (mobile, 4× CPU, fast-4G-ish) · INP ≤ 200 ms · CLS ≤ 0.05 · initial JS (non-3D) ≤ 200 KB gz ·
first-view 3D ≤ 3 MB · frame time p95 ≤ 20 ms desktop / ≤ 33 ms mobile emulation · no single frame > 100 ms after
interactivity · heap stable over a 2-minute idle + scroll loop.

## Toolbox

- **Lighthouse** (installed globally, v13) and **Lighthouse CI** (`npx @lhci/cli`, template config) for lab CWV.
- **Chrome DevTools MCP** (`chrome-devtools-mcp`): `performance_start_trace` / `performance_analyze_insight`,
  network and console from an agent.
- **Playwright + CDP** (`tooling/perf/frame-probe.mjs`): rAF frame-interval distribution per phase (idle, pointer,
  scroll), long tasks, LCP/CLS, `Performance.getMetrics`, CPU throttling, optional HAR replay for network-independent runs.
- **web-vitals** library in the page for field-like INP/LCP reporting during tests.
- **Spector.js** (browser extension) and `renderer.info` for GPU-side inspection.

## Procedure

1. Isolate: one browser session, nothing else running; record environment (machine, browser, throttling).
2. Lab pass: Lighthouse mobile + desktop; save JSON. Note LCP element and its timeline.
3. Runtime pass: frame probe on load→idle→pointer→scroll; 2 repeats; report p50/p95/p99/max and frames > 33/50 ms.
4. Trace the worst moment (DevTools trace via MCP or Playwright `tracing`), attribute: script (which function),
   style/layout (which selector/forced reflow), paint/raster, GPU (shader compile, texture upload), GC.
5. Fix the top item; re-measure; keep before/after numbers in `docs/QA/perf-<date>.md`.

## Common creative-site fixes

Preload/prioritise the LCP image or font, not the 3D bundle · split three.js into a lazily imported chunk · compile
shaders/upload textures during the poster phase (`renderer.compileAsync`, `initTexture`) · cap DPR · pause offscreen ·
move simulation to a worker · avoid layout reads in scroll handlers · `content-visibility` for long pages · compress
textures (WebP/KTX2) and geometry (meshopt) · subset fonts · avoid video autoplay of large files above the fold ·
use `IntersectionObserver` not scroll listeners · stop GC churn (no per-frame allocations).

## Progressive enhancement checklist

HTML content first · works without JS · works without WebGL (poster + content) · reduced motion · save-data/slow
network → skip heavy assets · low-end GPU tier → fewer passes.

## Failure criteria

"It's fast on my machine"; only average fps reported; measuring while other captures run; budgets exceeded without a
written exception; leaking WebGL contexts across navigations.
