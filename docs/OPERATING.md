# Operating guide

1. Create the lightest appropriate starter with `scripts/new-project.sh <template> <new-directory>`; it refuses existing destinations and copies no dependencies, build artifacts or snapshot baselines. Run `npm ci`. Runtime package versions remain pinned. Git is initialized, not committed or published automatically.
2. Load `ceos-studio-workflow`, then only the discipline skills needed. Write a short brief and research principles with sources and anti-copy boundaries. Get the concept agreed before substantial client implementation. Record type/grid/palette/motion/responsive decisions as tokens.
3. Prototype one representative scene. Inspect 1440 and390 before bulk sections. Choose native scroll unless interpolation earns its cost; one scroll/render owner. Build content/fallbacks and keyboard/reduced-motion states together with graphics.
4. Use the host's supported orchestration. In T3 discover live provider/model capability before delegation; same-provider native children when supported, T3 tasks otherwise. Delegate independent paths only and retain task IDs. An ordinary top-level thread is not a child task. Roles/ownership are in agents/TEAM.md.
5. Build and exercise the production artifact (`npm run build`, `npm test`). Template configs launch their own preview and refuse an occupied port. `npm run test:visual` compares reviewed baselines; for a new project, first capture and inspect images, then intentionally run `npm run test:update-snapshots`.
6. For broader evidence, keep the production preview running and run:

```sh
node ~/creative-engineering-os/tooling/visual-audit/capture.mjs \
  --url http://localhost:4174 --out docs/QA/2026-10-20
node ~/creative-engineering-os/tooling/perf/frame-probe.mjs \
  --url http://localhost:4174 --out docs/QA/perf.json
# Optional --video requires Playwright's ffmpeg artifact:
# cd ~/creative-engineering-os/tooling && npx playwright install ffmpeg
```

Use the URL/port from the current starter, not this example unconditionally. The capture script takes first/full screenshots at 1440/1024/768/390 plus reduced views and records axe, errors and DOM measurements. Full-page images do not replace scroll/hover/navigation interaction evidence. Wrapped-heading counts are heuristic when markup mixes span line-height rules; verify visually.

7. Hand images and approved direction to the independent auditor. It returns a concrete defect report; integration owner saves it, fixes problems, reruns relevant checks and attaches new evidence. Static screenshots cannot prove temporal motion quality.
8. Measure lab performance on an otherwise quiet machine. Record environment, DPR, network/CPU settings, LCP/CLS/frame percentiles/bytes and failures. rAF intervals are not GPU time or field INP. Real touch/Safari/device checks remain necessary for a public launch.
9. Run relevant security/dependency review. Avoid secrets in screenshots, HARs or bundles. Configure production headers, validate forms on the server, and verify the hosted artifact only when deployment is authorized. Record commit/URL and rollback.

## Starter selection

| Template | Stack | Use |
|---|---|---|
| editorial | Astro + TS + targeted GSAP | Type/content-led sites with minimal JS |
| motion-heavy | Vite + TS + GSAP + Lenis | Scroll choreography; owns one ticker/scroll engine |
| immersive-3d | Vite + TS + Three + GSAP | Scene/material/light with semantic HTML and fallback |
| experimental-graphics | Vite + TS + Three RawShaderMaterial | Raymarching and ping-pong feedback R&D, not blanket production defaults |

React/R3F, Motion, OGL, WebGPU, Theatre and Rive remain project decisions. Follow existing project conventions instead of migrating them into a starter.
