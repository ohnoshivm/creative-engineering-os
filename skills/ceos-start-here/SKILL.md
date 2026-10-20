---
name: ceos-start-here
description: Entry point and router for the Creative Engineering OS. Explains in one page what the toolkit contains (14 core studio skills, a 386-skill reference library, four tested starters, browser QA tooling, an independent auditor) and maps any website task — concept, art direction, typography, UX, motion, 3D/shaders, frontend, performance, QA, SEO/content — to the exact skill to load next. Use first whenever you start or resume website work with this toolkit, or when unsure which skill applies.
---

# Start here — Creative Engineering OS

You are working with a toolkit for building original, premium websites. It is **a method plus a library**, not a
theme. Read this page once, then load only the skills the current step needs.

## 1. What is where

| Path | What it is | Load it |
|---|---|---|
| `skills/ceos-*` (14) | The studio method — how this team works, stage by stage | By name when the stage starts |
| `library/skills/*` (386) | Third-party reference skills (permissive licences, upstream licence kept) | Only the one you need: read `library/skills/<name>/SKILL.md` |
| `library/CATALOG.md` | Every library skill by discipline with one-line "use it for" | Skim the section you need |
| `templates/` | Four tested starters: `editorial`, `motion-heavy`, `immersive-3d`, `experimental-graphics` | `scripts/new-project.sh <template> <dest>` |
| `tooling/` | `visual-audit/capture.mjs` (screens + axe + console), `perf/frame-probe.mjs` | During review |
| `standards/STANDARD.md` | The non-negotiable quality floor | Once per project |
| `agents/creative-auditor.md` | Read-only independent critic | Before anything is called done |

Paths are relative to the toolkit root (the folder that contains this `skills/` directory).

## 2. The route through a project

1. **Frame** → `ceos-studio-workflow` (stages, gates, handoffs). Always first.
2. **Concept** → `ceos-creative-direction`. Three distinct concepts, one recommended, owner approval before building.
3. **Look** → `ceos-art-direction` (type, grid, colour, imagery as tokens).
4. **Behaviour** → `ceos-interaction-architecture` (IA, journeys, every input, accessibility).
5. **Motion** → `ceos-motion-direction` (tokens, choreography, reduced motion).
6. **Stack** → `ceos-frontend-architecture` (lightest stack, one render loop, ownership).
7. **Signature moment** → `ceos-realtime-3d` / `ceos-shader-engineering` / `ceos-creative-coding` / `ceos-3d-asset-pipeline` as needed.
8. **Build** from a template; content in semantic HTML; placeholders clearly marked.
9. **Prove it** → `ceos-production-quality` (tests, axe, keyboard, no-JS/no-WebGL), `ceos-performance-engineering` (measured budgets).
10. **Critique** → `ceos-visual-audit` (or the `creative-auditor` agent). Fix P0/P1, re-capture, repeat.

Never skip 2 → 7: the concept and the signature moment are approved and seen in a real browser before bulk sections.

## 3. Task → skill router

| If the task is… | Core skill | Library skills worth opening |
|---|---|---|
| "Make it look less generic / more premium" | ceos-art-direction, ceos-visual-audit | `frontend-design`, `design-taste-frontend`, `impeccable`-family entries in CATALOG "Visual design" |
| Choose fonts, type scale, editorial layout | ceos-art-direction | CATALOG → Visual design & typography |
| Colour palette / design tokens / design system | ceos-art-direction | `ui-ux-pro-max`, `ui-styling`, design-system entries |
| Sitemap, journeys, forms, navigation, a11y | ceos-interaction-architecture | CATALOG → UX & interaction (accessibility, forms) |
| Scroll animation, page transitions, kinetic type | ceos-motion-direction | GSAP entries (`gsap-*`), `motion`, CATALOG → Motion |
| 3D hero, WebGL scene, materials, lighting | ceos-realtime-3d | CATALOG → 3D, WebGL & shaders |
| Custom shader, raymarching, particles, fluid | ceos-shader-engineering, ceos-creative-coding | template `experimental-graphics` |
| Models/textures too big, Blender → web | ceos-3d-asset-pipeline | — |
| React/Next/Vite/Astro structure, components | ceos-frontend-architecture | `react-best-practices`, CATALOG → Frontend engineering |
| Slow, janky, CWV, memory | ceos-performance-engineering | CATALOG → Quality, performance & testing |
| Tests, visual regression, release | ceos-production-quality | `playwright`/QA entries in CATALOG |
| Critique a page | ceos-visual-audit | — |
| SEO, copy, social/content | — | CATALOG → Content, SEO & growth |

If a library skill conflicts with a core skill, **the approved project direction wins, then the core skill**; say which
trade-off you made.

## 4. Rules that make the output world-class (short form of `standards/STANDARD.md`)

- One idea that belongs to this client, not the category. References are calibration, never templates.
- Type is the main material: few sizes, big contrast, measured line length, deliberate line breaks.
- One signature motion; everything else quiet; designed reduced-motion state.
- HTML first: all content and actions work without JS and without WebGL.
- Evidence or it didn't happen: screenshots at 1440/1024/768/390, axe, keyboard, console, measured performance.
- No invented proof: no fake clients, numbers, testimonials or awards.

## 5. First commands in a fresh checkout

```sh
python3 scripts/ceos.py doctor                  # what's installed / missing
./scripts/new-project.sh editorial ~/Projects/my-site && cd ~/Projects/my-site && npm ci && npm run dev
node <toolkit>/tooling/visual-audit/capture.mjs --url http://localhost:4321 --out docs/QA/first-look
```
