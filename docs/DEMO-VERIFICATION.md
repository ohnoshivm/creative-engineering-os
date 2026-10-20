# Signal study — demonstration verification

An isolated original capability study in `demo/signal-study`, created from the immersive-3d template. It makes no client claims and was not deployed. Concept, reference limitations, tokens, state ownership, interaction and motion rules were written in [ART_DIRECTION.md](../demo/signal-study/docs/ART_DIRECTION.md) before implementation. The signature surface was inspected at1440×900 and390×844 before adding the reading section.

Production artifact: Vite build, localhost port4184. Browser: installed Google Chrome155.0.8059.84, headless Chromium engine on macOS26.5.1 arm64. Source is an uncommitted root-workspace demonstration; Vite asset hashes identify the exercised build. A generated nested template Git repository was removed so the demonstration can be tracked by the OS repository.

## Commands and evidence

Run in `~/creative-engineering-os/demo/signal-study`:

| Command | Actual result |
|---|---|
| From OS root: `scripts/new-project.sh immersive-3d demo/signal-study` | Created from template; no pre-existing demo files. |
| `npm ci --no-audit --no-fund` | Exit0,31 packages; inherited versions, no additional project dependencies. fsevents optional install-script warning was reported, installation succeeded. |
| `npm run check` | Exit0. |
| `npm run build` | Exit0, production Vite artifact. Final initial JS46.77KB gzip, CSS1.26KB; deferred graphics129.52KB Three +1.43KB stage. Zero textures or font downloads. |
| `npm run preview -- --port 4184` | Production preview serving HTTP200. |
| `npm test -- --workers=2` | Final:28 passed,12 intentional capability/project-specific skips; [output](../demo/signal-study/docs/QA/smoke-output.txt). |
| `npm run test:update-snapshots -- --workers=1` | Created3 deliberate still-frame baselines;1 no-WebGL visual skip. Images were opened and reviewed, then comparison passed3/3. Final intentional height/instruction update:3 passed,1 skipped; comparison rerun3 passed,1 skipped. |
| `node ../../tooling/visual-audit/capture.mjs --url http://localhost:4184 --out docs/QA/final --video` | Initial command used absolute tooling path. Installed the required Playwright ffmpeg binary. Final12 screenshots and4 viewport recordings refreshed;0 console errors/0 serious-critical axe violations. |
| `npm audit --omit=dev --json` | Exit0,0 vulnerabilities; [raw audit](../demo/signal-study/docs/QA/npm-audit.json). |
| `lighthouse http://localhost:4184 --preset=desktop --chrome-flags='--headless=new' --output=json --output-path=docs/QA/lighthouse-desktop.json --quiet` | Exit0. Performance99, accessibility100, best practices100, SEO91; LCP575.6ms, CLS0, TBT103ms. [JSON](../demo/signal-study/docs/QA/lighthouse-desktop.json). Measured before the final copy/stage-height refinements. |

The first TypeScript pass found an unused local and an unsupported `process` reference in the template-derived config change; both were removed. Initial smoke failures were ambiguous test selectors and a changing button-name locator, corrected to stable locators. These failures were not counted as product passes.

## What is exercised

Semantic HTML, responsive typography, one GSAP title entrance, native scroll-to-phase mapping, a custom vertex-displaced and analytically shaded Three.js plane, pointer bending, an equivalent keyboard range input and pause/resume. One GSAP ticker owns frames. Offscreen and hidden tabs stop rendering; preference changes update the static/live state. No smooth-scroll library, texture, HDRI or postprocessing was added.

Smoke coverage includes visible content, anchor navigation, clean console, no horizontal overflow, one live renderer/draw call, keyboard order and visible focus, range arrows and output, pause producing identical screenshots across time, pointer/scroll changes, reduced-motion stills and adjustment, no-WebGL SVG fallback, complete no-JavaScript reading content, and axe serious/critical violations. Final audit refinements add explicit instruction and viewport-fit regression checks.

[Capture data](../demo/signal-study/docs/QA/final/capture.json) includes1440×900,1024×768,768×1024 and390×844 plus reduced-motion desktop/phone. Captures were opened as images. Type stays one line at all four widths; measured heading sizes144/102.4/76.8/64px. Outer margins72/51/38/20px match. Zero measured small tap targets, zero horizontal overflow, zero unnamed controls, zero console errors and zero axe violations in the four standard captures. Reduced-motion capture axe was not rerun by that tool; the separate reduced-motion Playwright axe test passed.

| ID | Severity | Finding | Correction | Recheck |
|---|---|---|---|---|
| D01 | P2 | Prototype wave cropped at field edges;64 contours crowded on phone. | Increased camera distance and reduced phone contours to40. | Final full-page images show bounded surface with readable contours. |
| D02 | P2 | Hidden fixed skip link appeared within scrolled full-page screenshots. | Absolute offscreen link; focus moves it back into view. | Refreshed full captures no longer show it; desktop keyboard test passed. |
| D03 | P2 | Independent audit: pointer/scroll guidance unsuitable for reduced/coarse input. | Reduced still-view guidance and coarse-pointer range/scroll guidance. | Final reduced/mobile/desktop/no-WebGL instruction tests pass. |
| D04 | P2 | Independent audit: controls extended below1440×900 and1024×768. | Stage `clamp(260px,34vw,450px)`; phone override320px. | Controls bottom890.8px at1440×900 and749.4px at1024×768; regression passes. |

Creative critique: the single interference sheet is the instrument and the image; the display headline, restrained palette and quiet reading section support it without unrelated decoration. A single locally available font keeps the demo self-contained; typography is not evidence of an exclusive brand identity.

## Measured runtime

Sequential local probes used the shared frame-probe tool, production URL and readiness check `document.documentElement.dataset.stage === 'live'`. Common flags: `--settle 1000 --idle 2000 --scrollMs 3000`; desktop1440×900@1. Additional runs: `--cpu 4`; mobile `--mobile --cpu 4 --touchMode events`. Each browser closed before the next run. Browser/test activity was coordinated with the template verification agent. A separate local inspection tab was open during these early probes, so machine-wide GPU isolation was not established. The tab was subsequently closed.

| Run / raw JSON | LCP (ms) | CLS | Idle/pointer/scroll p95 (ms) | Native scroll |
|---|---:|---:|---|---:|
| [Desktop1](../demo/signal-study/docs/QA/perf-desktop-1.json) |328|0|16.7 /16.7 /16.8|756px|
| [Desktop2](../demo/signal-study/docs/QA/perf-desktop-2.json) |188|0|16.8 /16.7 /16.8|756px|
| [Desktop CPU4](../demo/signal-study/docs/QA/perf-cpu4.json) |276|0|16.8 /16.8 /16.7|756px|
| [Mobile emulation CPU4](../demo/signal-study/docs/QA/perf-mobile.json) |96|0|16.8 /16.7 /16.7|959px|

All probes had0 failed requests. Desktop1 included one50ms frame and a62ms scroll-phase long task; desktop2 and both throttled runs had no scroll-phase long tasks. Those are observed runs, not a universal60fps promise. Ending JS heap4.4–6.3MB is a snapshot, not a leak test. One draw call and16,384 triangles are exposed by renderer diagnostics and checked by smoke tests. Final changes only adjust copy and stage dimensions; these timings describe the preceding artifact rather than a new performance claim for the refinement.

## Limits

rAF intervals measure scheduling, not isolated GPU execution. No GPU timer query, physical mobile GPU, Safari/WebKit, screen-reader session, field CWV/INP, network-throttled mobile Lighthouse,2-minute heap/disposal loop or exhaustive context-loss/restoration test was run. No host was deployed, so CSP/HSTS and other hosting headers are not verified. Static review found only a bounded local range input, no forms/auth/client secrets/outbound requests, and no dangerous HTML insertion. Dependency audit is not a complete security assessment.

## Final refinement verification

Production build and TypeScript check pass after both audit fixes. Final full smoke suite:28 passed,12 explicit capability/project-specific skips. Final visual update3 passed/1 skip, followed by baseline comparison3 passed/1 skip. All12 screenshots were refreshed; desktop/tablet/mobile images and the reduced-motion phone image were opened and checked. [Viewport measurements](../demo/signal-study/docs/QA/final-refinement.json) prove pause/control visibility at both audited sizes. No P0/P1 findings remain; the two independent P2 findings are corrected and rechecked.

Final build assets: `index-oqGxquUo.js`, `index-BC4xzwx8.css`, `stage-oy1sOfKf.js`, `three-BxwHOTyG.js`. Production preview remains running at http://localhost:4184 for inspection. No deployment/rollback operation was performed; this is a local artifact.

Reusable principle: an accessible range can carry the full interaction, with pointer motion as an enhancement. Project-specific decision: one analytically shaded wave plane communicates interference without texture downloads or a lighting rig.
