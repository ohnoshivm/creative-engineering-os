# Signal study

An isolated capability demonstration for Creative Engineering OS; no client, services or commercial proof is implied.

Concept: a single interference surface makes the relationship between a hand, a wave and a scroll position visible.
Chosen direction: Signal study (a tactile wave instrument). Alternatives: a typographic phase diagram (too little 3D), a luminous particle volume (too much GPU work for this small demonstration). Scope authority: the user requested an autonomous isolated capability demo; the integration owner assigned this direction on 2026-10-20. This is not a client concept approval.

## Research

Reviewed primary source pages on 2026-10-20. These were text/documentation reads, not visual reconstructions.
- https://lusion.co/ — interaction as the subject; transfer to one manipulable surface; never copy its objects, camera paths or compositions. Visual mechanism remains an inference.
- https://www.14islands.com/ — focused design and technology studies; transfer to a brief authored experiment; never copy projects, brand or assets. Motion details unverified.
- https://tympanus.net/codrops/ — experiments organised around one technique; transfer to one interference function; no copied demos/shaders.
- https://threejs.org/docs/ — ShaderMaterial, geometry and renderer ownership; use documented primitives, no copied scene.
- https://gsap.com/docs/v3/Plugins/ScrollTrigger/ — native scroll progress as input, no scroll hijacking.

## Tokens and layout

Palette: ice #edf3fa (page), ink #172d52 (text), cobalt #234bda (wave), mist #cddbef (canvas ground), white #ffffff (control).
Type: locally installed Helvetica Neue / Arial for a quiet scientific instrument; display clamp(4rem, 10vw, 9.5rem), section clamp(2rem, 4vw, 4rem), body clamp(1rem, 1.5vw, 1.2rem). Tight display tracking, normal body spacing, <65 character body measure.
Spacing: 8/16/24/40/64/96; 5vw page gutters, max 1600px. One asymmetric opening title, full-width instrument, then a quiet two-column explanation. Mobile stacks controls, keeps the surface landscape and never squeezes text over the canvas. Radius 4px only on controls; no ornamental shadows.
Material: a cobalt etched sheet, analytically shaded from the wave derivative with pale contours. No HDR textures or decorative lighting rigs.
Motion: GSAP 800ms expo.out title entrance; scroll continuously maps phase, pointer maps local amplitude. One gsap.ticker loop. Native page scroll is the only scroll engine. Reduced motion and explicit pause render stills; controls update a still without tween travel.
Interaction: pointer bends the surface; touch pans the page normally; labelled range control offers a keyboard equivalent to the pointer; pause button stops ambient motion; link advances to reading section. Offscreen/hidden tabs stop drawing. WebGL failure exposes an SVG poster.

## Architecture and plan

Vite + TypeScript, existing GSAP and Three.js. Semantic HTML owns all content and controls. One shader plane and one renderer, zero texture downloads. Shader uniforms own deformation; scroll store and range input own the target amplitude. DPR <=1.5, one draw call, no postprocessing.
1. Prototype title + surface at 1440 and 390; inspect before writing supporting sections.
2. Add short reading section and accessible controls.
3. Production build; test console, scroll/pointer/range/pause, reduced-motion, no-WebGL, axe and responsive dimensions.
4. Inspect screenshots at 1440/1024/768/390, refine, record lab frame timings and asset sizes. No deployment.

Budgets: initial JS gzip <50KB; deferred graphics gzip <180KB; one draw call; no external fonts/textures; zero serious/critical axe issues. Frame time target p95 <=25ms on local desktop; throttle evidence reported separately, no field-performance claims.

## Prototype and refinement decisions

The title and shader prototype was rendered at 1440×900 and390×844 before the reading section was added. Actual images: `docs/QA/prototype-{desktop,mobile}.png`. Review found surface edge cropping and tightly packed phone contours: camera distance increased, mobile lines64→40. Final captures verify the entire surface stays inside its field.

A subsequent visual pass found the offscreen fixed skip link could appear in scrolled full-page captures. It now uses absolute offscreen positioning, preserving keyboard focus and keeping the field clear.

Independent audit requested the controls fit within desktop/tablet height and input instructions match the device. Stage height is now `clamp(260px,34vw,450px)`, with the phone override320px. Reduced-motion instruction: “Still view. Adjust Surface tension below.” Coarse-pointer instruction explains the tension control and native scroll. Desktop retains pointer guidance.

Reusable principle: an accessible control can be the primary instrument input while pointer movement is an enhancement. Project-specific choice: analytical normals and contour lines make a single wave mesh legible without a downloaded lighting environment.
