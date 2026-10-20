# Signal study

An isolated original interaction demonstration built from Creative Engineering OS’s immersive-3d template. It is not a client site. The concept and implementation decisions are in [docs/ART_DIRECTION.md](docs/ART_DIRECTION.md); verification is in [../../docs/DEMO-VERIFICATION.md](../../docs/DEMO-VERIFICATION.md).

```sh
npm ci
npm run dev
npm run build
npm run preview
npm test
npm run test:visual
npm run audit:visual
```

Production preview uses port 4184. Smoke tests reuse that server if present; build first after changes. Without an existing server, Playwright builds and serves the production artifact. Tests use installed Google Chrome, without downloading another browser. The visual audit's optional video flag requires Playwright's ffmpeg binary (`npx playwright install ffmpeg`).

Pointer movement bends the surface, native scroll shifts phase, and the labelled range changes tension. Arrow keys provide the range's native keyboard interaction. The pause button stops ambient rendering. Reduced motion uses a still frame, with no entrance or scroll animation; tension remains adjustable. `?still` provides deterministic visual snapshots. No WebGL leaves the SVG poster. JavaScript-disabled HTML retains all reading content and anchor navigation.

One `gsap.ticker` owns animation and Three.js rendering. The scene is a single analytically shaded plane with custom vertex and fragment shaders, capped DPR, no textures and no postprocessing. Rendering stops offscreen and in hidden tabs. Modules expose cleanup for HMR. Dependency versions are inherited from the tested template; none were added.

No deployment was performed. Physical mobile GPU, Safari, field CWV/INP and hosting security headers remain outside this local demonstration.
