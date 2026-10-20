---
name: ceos-realtime-3d
description: Architects and art-directs realtime 3D for websites with Three.js, React Three Fiber or OGL — scene graph, cameras and camera direction, PBR materials and lighting, environment maps, textures and colour management, render targets and post-processing, instancing, GPU memory and disposal, render-loop ownership, DOM/canvas coordination, adaptive quality and mobile. Use when building a WebGL/3D hero or scene, choosing three vs R3F vs OGL, fixing a 3D scene that looks cheap or runs slowly, or syncing 3D with scroll and HTML.
---

# Realtime 3D (Three.js / R3F / OGL)

## Purpose

3D that looks lit and art-directed — not "default PBR on grey" — and that runs within a budget on real devices.
For basic API recipes see `threejs`; for shaders `ceos-shader-engineering`; for assets `ceos-3d-asset-pipeline`.

## Choosing the library

- **three.js**: default for websites; mature, large ecosystem (loaders, PMREM, post, TSL/WebGPU renderer).
- **R3F (+ drei)**: when the app is React and scenes are component-shaped; keep the frame loop in `useFrame`, avoid
  React state updates per frame.
- **OGL**: tiny (~tens of KB), for a few custom-shader meshes/planes with no need for three's ecosystem.
- **Raw WebGL2 / WebGPU**: only for research or extreme constraints.

## Look development (what makes it premium)

- **Colour pipeline**: `renderer.outputColorSpace = SRGBColorSpace`; colour textures in sRGB, data textures linear;
  pick one tone mapping (ACES Filmic, AgX or Neutral) and set exposure deliberately.
- **Light with an environment**: image-based lighting via PMREM. Without an HDRI, build an environment *scene in code*
  (emissive panels = softboxes) and PMREM it — this is how chrome/glass get believable reflections. Add 1–2
  directional/rect lights for shape; shadows only where they ground the object (contact shadows or baked AO).
- **Materials**: `MeshPhysicalMaterial` for clearcoat, transmission, iridescence, sheen; metal needs a contrasty
  environment to read as metal; roughness variation (maps) beats perfect uniform values.
- **Camera**: choose focal length deliberately (30–40° vertical FOV for product-like, wider for spaces); move on
  splines/eased paths; never default orbit-spin. Compose for the text that sits over it.
- **Post**: few, purposeful passes — tone mapping, subtle bloom on true highlights, film grain/dither against
  banding, optional DOF. Use `pmndrs/postprocessing` (merges effects into fewer passes) or three's `EffectComposer`.

## Architecture

- One renderer, one canvas (fixed, behind or within the layout), one loop; scenes/sections swap render "profiles"
  rather than creating new renderers.
- **DOM-synced objects**: measure DOM rects (on resize/scroll), map to world units with an orthographic or matched
  perspective camera so GL planes track HTML elements exactly; HTML remains the accessible content.
- **Scroll**: read the scroll store; map section progress → scene parameters; don't move the camera with unscrubbed
  tweens that fight the user.
- **Instancing** (`InstancedMesh`, `BatchedMesh`) for repeated objects; merge static geometry; texture atlases.
- **Render targets** for feedback/trails/transitions: size them to the viewport × DPR cap, half-res when blurred,
  `dispose()` on resize/unmount.

## Performance and robustness

- DPR cap 1.5–2 desktop, ≤ 1.5 mobile; optional pixel cap (e.g. 2560×1440 total); dynamic resolution if frame time
  rises (measure with `renderer.info` + frame timings).
- Device tiering: probe `renderer.capabilities`, `WEBGL_debug_renderer_info` (where allowed), and measured frame time
  during the first seconds; choose quality tier (post on/off, shadow off, particle counts).
- Compile shaders early (`renderer.compileAsync`) behind the poster to avoid first-interaction freezes.
- Pause rendering offscreen/hidden tab; `renderer.setAnimationLoop(null)`.
- Dispose geometries, materials, textures, render targets, PMREM outputs; check `renderer.info.memory` returns to
  baseline after unmount.
- Handle `webglcontextlost`/`restored`. **No-WebGL path**: detect failure (`getContext` returns null) and show the
  designed poster + full HTML content. Never block the page on a loader.

## Verification

Screenshots of the scene at 1440 and 390; frame-time p50/p95 in an isolated run (desktop + 4× CPU throttle);
`renderer.info` draw calls/triangles/textures logged; reload with `--disable-3d-apis` shows the poster and content;
reduced-motion renders a still.

## Failure criteria

Grey "default" lighting; un-tone-mapped colour; uniform plastic materials; 300+ draw calls without reason; multiple
renderers; unbounded DPR; first-click shader compile freeze; GL objects that drift from their DOM anchors; content
only in canvas; infinite loader without WebGL.
