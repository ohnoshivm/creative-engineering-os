# Benchmarks — what to study each for

These are standards of ambition. Study the principle; never reproduce the work. Observations here are general and
public; verify specifics in a real browser before relying on them.

| Studio / site | Study it for | Never copy |
|---|---|---|
| lusion.co | Realtime 3D hero that reacts physically to pointer; quiet editorial UI framing a loud world; post-processing as grading; continuity objects carried across sections | Its sculptural objects, camera paths, palette-cycling interaction, finale tunnel |
| buttermax.net | DOM as layout engine + WebGL as renderer; each project as a distinct physical object; colour taken from project data; ink/fluid feedback on input | Device flipbooks, butter fluid, wordmark treatment |
| 14islands.com | Portfolio hierarchy: full-bleed work, scannable index, clear contact; pacing between visual case studies and plain navigation | Layouts and copy |
| active-theory.com | Ambitious realtime experiences, custom engines, experimental navigation | Scenes, assets |
| resn.co.nz | Playful, story-led interaction; personality in micro-interactions | Characters, concepts |
| makemepulse.com | Brand-campaign interactivity, WebGL storytelling | Campaign concepts |
| locomotive.ca | Scroll craft and editorial typography (and the origin of Locomotive Scroll); restrained motion | Type compositions |
| dogstudio.co | Cinematic transitions, 3D used for mood, strong art direction | The 3D objects / transitions |
| immersive-g.com | Immersive 3D product storytelling, high material quality | Scenes |
| tympanus.net/codrops | Documented techniques with source (shaders, transitions, scroll) — the best *learning* source on the list | Demos verbatim in production |

Stage 1 forensic findings for Lusion/Buttermax (from the Pixelard project) worth remembering:
both fail without WebGL, both ignore `prefers-reduced-motion`, both have weak keyboard support, average fps hides
0.3–1.3 s freezes, and both homepages convert poorly. Beating them on robustness is achievable and differentiating.
