---
name: ceos-creative-coding
description: Invents original procedural and generative visuals for the web with Canvas 2D, SVG and WebGL — noise fields, flow fields, particle systems, physics and springs, computational geometry, procedural shapes and organic animation — designed as art-directed systems, not pasted demos. Use when a site needs a custom generative background, interactive sketch, data-driven or organic visual, particle effect, procedural illustration, or when exploring a new visual technique.
---

# Creative coding

## Purpose

Build visuals from rules so they are ownable and alive. The aim is invention: a system with parameters the art
director can tune, not a copy of a CodePen.

## Expert knowledge to apply

- **Systems thinking**: a generative piece = elements + rules + parameters + randomness + time + input. Expose
  parameters (a tiny GUI or URL params) and seed every random source so results are reproducible.
- **Noise**: value/gradient (Perlin/simplex) noise for organic variation; fractal Brownian motion (sum of octaves)
  for detail; domain warping (noise of noise) for fluid organic forms; curl noise for divergence-free flow (particles
  that swirl without clumping).
- **Motion models**: Euler/semi-implicit Euler integration (`v += a·dt; p += v·dt`), damping, springs (Hooke + damper),
  verlet for constraints/cloth/rope, flocking (separation/alignment/cohesion), attraction/repulsion fields. Use
  fixed time steps for stability; decouple simulation dt from frame rate.
- **Geometry**: polar/parametric curves, superformula, Bézier/Catmull-Rom splines, Poisson-disk sampling for
  natural distributions, Voronoi/Delaunay, marching squares for metaball/contour shapes, SDFs for smooth unions.
- **Colour**: interpolate in OKLab/OKLCH; palettes from the brand, not rainbow HSL.
- **Rendering choice**: SVG for < ~1–2k crisp shapes and accessibility; Canvas 2D for thousands of simple marks and
  trails; WebGL (instancing / GPGPU) for 10k–1M particles or per-pixel effects. OffscreenCanvas + worker when the
  simulation would block the main thread.
- **Craft details**: trails via low-alpha clears or feedback textures; DPR-aware canvas sizing; anti-aliasing via
  supersampling or SDF edges; grain/dither to kill banding.

## Inputs

Concept + art direction (palette, mood), interaction intent, target devices and budget.

## Decision procedure

1. Write the rule set in one paragraph ("Each pixel is a particle pulled toward the logo outline; pointer pushes
   with a falloff; noise adds drift…").
2. Prototype in an isolated sketch (Template D lab or canvas-sketch), seeded, with exposed params.
3. Art-direct by tuning parameters against screenshots; record the chosen param set.
4. Port to production with a budget: particle count by device tier, DPR cap, pause offscreen, reduced-motion still.

## Implementation standards

Seeded PRNG (e.g. mulberry32), fixed-step simulation, typed arrays for particle state, no allocations in the hot
loop, resize handling, `destroy()`, a static fallback frame (PNG or first frame) for reduced motion / no JS.

## Verification

Same seed → same frame (screenshot diff); 60 fps on a mid laptop at target count; stays ≥ 30 fps at 4× CPU throttle
or degrades count gracefully; no memory growth over 2 minutes.

## Failure criteria

Unseeded randomness; demo code with unexplained magic numbers; "particles for decoration" unrelated to the concept;
allocations per frame; full-DPR canvases on phones; no still fallback.

## References

The Nature of Code (natureofcode.com), The Book of Shaders (noise chapters), canvas-sketch (mattdesl), Codrops.
