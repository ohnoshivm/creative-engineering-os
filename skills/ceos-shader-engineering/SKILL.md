---
name: ceos-shader-engineering
description: Writes, debugs and optimises GPU shaders for the web — GLSL ES 3.0 and WGSL, Three.js ShaderMaterial/onBeforeCompile and TSL (WebGPU), coordinate spaces, procedural noise and textures, signed distance fields and raymarching, vertex displacement, image and page transitions, GPGPU particles, multi-pass/ping-pong rendering, precision and cross-browser fallbacks. Use when a visual effect needs a custom shader, when building transitions, distortion, fluid or particle simulations, raymarched forms, or when a shader is slow, banding, or broken on some GPUs.
---

# Shader engineering

## Purpose

Custom GPU effects that are art-directable, fast and portable.

## Core knowledge

**Spaces**: object → world (`modelMatrix`) → view (`viewMatrix`) → clip (`projectionMatrix`) → NDC → screen. Do
lighting in one space consistently (view or world). Screen UV = `gl_FragCoord.xy / resolution`; correct aspect
before computing distances.

**Procedural toolkit**: hash functions (integer hashes over `sin`-fract for stability), value/simplex/gradient noise,
fBm, domain warping, Voronoi/cellular, SDF primitives (`sdSphere`, `sdBox`, `sdRoundBox`, `sdTorus`), operators
(union/intersection/subtraction, **smooth min** for organic blends, repetition, twist/bend), antialiased edges with
`fwidth` + `smoothstep`.

**Raymarching**: sphere tracing over an SDF (max ~64–128 steps, epsilon scaled by distance), normals by central
differences or tetrahedron technique, soft shadows and AO by short marches, early-out bounds (march only inside a
proxy box mesh rather than full screen). Budget: fragment cost × pixels — render at reduced resolution and upscale
if needed.

**Vertex work**: displacement along normals with recomputed normals (finite differences in the shader or analytic
derivatives), morph targets for authored deformation, instanced attributes for per-instance variation.

**Transitions**: mix two textures by a mask (noise threshold with soft edge, directional wipe, displacement-driven
UV offset), drive the uniform from GSAP; keep both textures resident only during the transition.

**GPGPU / multi-pass**: ping-pong render targets (float/half-float) for position/velocity simulations; `GPUComputationRenderer`
in three; on WebGPU, compute shaders (WGSL / TSL `compute()`). Check `EXT_color_buffer_float`/half-float support
and fall back.

**WebGPU / TSL**: three's `WebGPURenderer` (falls back to WebGL2 backend) and TSL node materials let one shader graph
target both. Use for compute-heavy work; keep a WebGL2 path for production until your audience coverage is verified.

## Implementation standards

- Uniforms named by meaning (`uProgress`, `uPointer`, `uTime`), time in seconds, all animation driven from JS state.
- `precision highp float;` in fragment shaders that do position/noise math (mobile mediump causes artefacts).
- Dither the final colour (blue-noise or interleaved gradient noise) to remove banding on gradients.
- Avoid dynamic branching on divergent data in hot loops; unroll small fixed loops; prefer `mix`/`step`.
- Shader source in `.glsl` files (Vite `?raw` import) with `#include`-style chunks; one shared noise library.
- Hot-reload during development; a debug view mode (normals, UVs, SDF steps heat-map).

## Debugging

Visualise intermediates as colours; isolate with a fullscreen quad; check compile logs (`renderer.debug.checkShaderErrors`);
Spector.js to capture a frame (draw calls, uniforms, textures, render targets); test on a second GPU vendor
(Apple + Android/Intel) and Safari for precision and extension differences.

## Verification

Visual: screenshots at two resolutions + a recorded transition. Performance: GPU frame time (DevTools Performance with
GPU track, or EXT_disjoint_timer_query where available), steady 60 fps at target DPR on a mid laptop; fallback
quality tier verified. Correctness: no NaNs/black pixels at extremes (uProgress 0/1, tiny/huge viewports).

## Failure criteria

Full-screen raymarching at full DPR on phones; banding; aspect-stretched noise; uniforms animated in-shader with
hard-coded speeds; no fallback when float textures are unsupported; copied Shadertoy code without licence check
(Shadertoy default licence is CC BY-NC-SA — not usable commercially unless the author states otherwise).

## References

The Book of Shaders; WebGL2 Fundamentals; WebGPU Fundamentals; Inigo Quilez articles (SDF functions, smooth min);
three.js examples (webgl_gpgpu_*, webgpu_*); Codrops shader tutorials.
