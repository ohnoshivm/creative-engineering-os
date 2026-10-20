---
name: ceos-motion-direction
description: Designs and engineers motion as a coordinated system — motion tokens, easing and timing, choreography and sequencing, scroll choreography with GSAP ScrollTrigger, kinetic typography, SVG animation, cinematic and route transitions, gesture- and physics-driven motion, interruption and cleanup, reduced-motion alternatives, and frame scheduling/profiling. Use when animating anything on a website, writing a motion spec, choosing GSAP vs CSS vs WAAPI vs Motion, fixing janky or "cheap-feeling" animation, or adding smooth scroll.
---

# Motion direction and animation engineering

## Purpose

Motion that *means* something (hierarchy, causality, continuity, feedback) and feels authored — and engineering that
keeps it at frame rate, interruptible and accessible. For API details load `gsap-core`, `gsap-timeline`,
`gsap-scrolltrigger`, `gsap-performance` or `motion`; this skill decides *what* and *how well*.

## What separates good motion from merely working motion

1. **Purpose** — every move answers: what changed, where did it come from, what should I look at next?
2. **One signature** — a single memorable move per page; everything else supports it quietly.
3. **Consistent physics** — a small set of easings and durations reused everywhere (tokens), not per-element taste.
4. **Spatial continuity** — elements travel from where they were to where they go; no teleports, no unrelated fades.
5. **Choreography** — overlap and stagger create hierarchy (lead element first, supporting 60–120 ms later); nothing
   all-at-once, nothing one-by-one forever.
6. **Responsiveness** — input-driven motion starts within one frame and can be interrupted/reversed from any state.
7. **Restraint at rest** — idle motion is slow and small; the page is calm when the user is reading.

## Motion tokens (start here, tune per brand)

| Token | Value | Use |
|---|---|---|
| `--dur-micro` | 120–180 ms | press, hover, toggles |
| `--dur-ui` | 240–360 ms | menus, panels, small reveals |
| `--dur-move` | 500–800 ms | element travel, section entrances |
| `--dur-scene` | 900–1600 ms | page/scene transitions (never block input this long) |
| `--ease-out` | `cubic-bezier(.16,1,.3,1)` (expo-ish out) | arrivals |
| `--ease-in-out` | `cubic-bezier(.65,0,.35,1)` | travel between two rest states |
| `--ease-in` | `cubic-bezier(.7,0,.84,0)` | exits (shorter than entrances) |
| stagger | 40–90 ms | lists, words, lines |
| scroll scrub smoothing | `scrub: 0.4–1` | scroll-linked scenes |

Exits ≈ 70 % of entrance duration. Distances scale duration (√distance), not linear.

## Choosing the tool

- **CSS transitions / `@keyframes`**: state changes, hovers, simple reveals (compositor-friendly, zero JS).
- **CSS scroll-driven animations** (`animation-timeline: view()/scroll()`): simple scroll-linked effects where
  supported; feature-detect, fall back to static.
- **WAAPI**: programmatic one-offs without a library.
- **GSAP + ScrollTrigger**: timelines, sequencing, scrubbed scroll scenes, pinning, SVG/morph plugins, complex
  choreography. One `gsap.context()`/`useGSAP` per component for cleanup.
- **Motion (motion.dev)**: React gesture/layout/spring animations.
- **Springs / second-order dynamics**: pointer-following, drag release, physical UI. A critically damped spring or
  second-order system (frequency f, damping ζ, response r) gives natural follow without overshoot when ζ≥1.
- **Lenis**: only when smooth scroll is part of the concept; then make it the *only* scroll engine, drive
  ScrollTrigger from it (`lenis.on('scroll', ScrollTrigger.update)` + `gsap.ticker`), keep keyboard and anchors working.
- **Tempus**: only when several systems (Lenis, GSAP, a WebGL loop) must share one RAF and you've measured drift.

## Engineering rules

- Animate `transform` and `opacity` (and `filter`/`clip-path` sparingly). Never animate layout properties per frame.
- One RAF owner per page (GSAP ticker or your loop); WebGL reads scroll/pointer state, doesn't own extra RAFs.
- Read layout once, write many (avoid forced reflow); `will-change` only during the animation.
- Scroll scenes: scrub with `ease: "none"` inside the scrubbed timeline; pin the wrapper, animate children; create
  triggers top-to-bottom; `ScrollTrigger.refresh()` after fonts/images load.
- Interruption: every timeline can reverse or be killed mid-flight; use `overwrite: "auto"`; guard double triggers.
- Cleanup: kill timelines/ScrollTriggers/listeners on unmount or route change.
- Never hide content with JS-set initial states that fail open: set `from` states in JS *after* the script runs (or
  with a `.js` class), so no-JS shows content.

## Reduced motion (designed, not deleted)

`@media (prefers-reduced-motion: reduce)` and `gsap.matchMedia()`:
- keep fades/colour changes ≤ 200 ms; remove travel, parallax, zoom, scrubbed camera moves, auto-advance, smoothing;
- replace scroll scenes with their key frames as static compositions;
- 3D: render a still frame or idle without camera motion.

## Motion spec format (per scene)

`ID · trigger (load/scroll range/hover/click/drag) · elements · from → to · duration/easing or scroll mapping ·
stagger/overlap · interruption behaviour · reduced-motion alternative · perf notes`.

## Verification

- Record the interaction (CDP screencast / Playwright video) and inspect frames; sample transforms per frame to check
  the easing curve and duration against the spec.
- Performance panel: no long tasks > 50 ms during the move; no layout/paint storms; 60 fps on a mid laptop, stable
  on 4× CPU throttle.
- Reduced-motion run screenshots show complete content.

## Failure criteria

Fade-up on every section; different easing per element; scroll hijack; content invisible without JS; animations
that can't be interrupted; motion during reading; multiple RAF loops; jank on scroll start.
