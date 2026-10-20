# Template D — Experimental graphics lab

Vite + TypeScript + three.js (renderer + render targets only) + raw GLSL 3. For inventing techniques before they go
into a production site.

```bash
~/creative-engineering-os/scripts/new-project.sh experimental-graphics ~/labs/my-lab
npm install && npm run dev                    # http://localhost:5173/?exp=raymarch | feedback
npm test                                      # decoded pixels, gamma, keyboard, reduced motion, axe, no-JS/WebGL
npm run test:visual                           # reviewed deterministic raymarch + feedback baselines
```

- `src/experiments/lib.ts` — `Experiment` contract (frame/resize/destroy) and `fullscreenMaterial()` (GLSL3
  `RawShaderMaterial`; `// @common` pulls in `shaders/common.glsl`: hash, smooth-min, interleaved-gradient dither).
- `raymarch` — SDF sphere tracing with smooth-min unions, tetrahedron normals, Fresnel; DPR capped at 1.25.
- `feedback` — multi-pass ping-pong on half-float targets (falls back to 8-bit without `EXT_color_buffer_float`).
- Add an experiment: create `src/experiments/<name>.ts`, register it in `REGISTRY` in `main.ts`, add a button.
- Live frame-time readout (p50/p95 every 60 frames). For GPU-level capture use the Spector.js browser extension.
- `?exp=raymarch&still` freezes time at 2 seconds; `?exp=feedback&still` computes 120 fixed simulation steps
  before presenting one static frame. Used for visual regression, not representative of animation performance.
- Raymarch lighting uses linear values and the raw fragment shader applies one gamma encoding at output;
  `RawShaderMaterial` injects no Three colour-output chunk. A decoded corner-pixel assertion guards against a
  missing or doubled transform. Feedback targets hold linear simulation state; its display pass is an authored
  raw colour output, with no additional renderer transform.

## WebGPU / TSL (optional, not installed by default)

three's `WebGPURenderer` (`three/webgpu`) + TSL node materials and compute shaders run on WebGPU with a WebGL2
backend fallback. Try them in a branch of this lab first:
`import { WebGPURenderer } from 'three/webgpu'; await renderer.init();` — keep production on WebGL2 until the
audience's browsers are verified.

## Licensing reminder

Shadertoy code is CC BY-NC-SA by default unless the author says otherwise — re-derive techniques, don't paste.

## Verification server

Production preview uses `http://localhost:4177`. Playwright builds and starts its own preview, and fails if that
port is already occupied; stop a manually started preview before running tests. This prevents a test suite from
quietly exercising another template.
