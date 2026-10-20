---
name: ceos-studio-workflow
description: Orchestrates a premium website project end to end — research, concept, art direction, UX, motion spec, architecture, prototype, build, real-browser review, critique, audit, refinement, deploy — with explicit quality gates and agent handoffs. Use at the start of any new website, landing page, portfolio or immersive web experience, when planning which creative/engineering skill to load next, or when deciding whether work is ready to ship.
---

# Studio workflow (Creative Engineering OS)

The spine of every project. It decides **what happens next and what must be true before moving on**. It does not
replace the specialist skills; it routes to them.

## When to use

- Kicking off any website or web experience.
- Unsure which specialist skill applies.
- Someone is about to say "done" — run the gates first.

## Inputs

Brief (subject, audience, the one action the site must drive), real assets available (photos, video, logo, copy,
proof), constraints (stack, deadline, hosting, budget for fonts/licences), benchmarks named by the client.

## The loop

| # | Stage | Owner role | Skill to load | Exit gate (all must be true) |
|---|---|---|---|---|
| 1 | Research | Creative Director | `ceos-creative-direction` §Research | 5–8 references analysed for *principles*, each with "what to take / what never to copy" |
| 2 | Concept | Creative Director | `ceos-creative-direction` | 3 distinct concepts, one recommended, **owner approval recorded** |
| 3 | Art direction | Art & Motion Director | `ceos-art-direction` | Type system, palette roles, grid, image direction written as tokens |
| 4 | UX | UX Architect | `ceos-interaction-architecture` | Sitemap, journeys, every interactive state listed incl. keyboard/touch/reduced-motion |
| 5 | Motion spec | Art & Motion Director | `ceos-motion-direction` | Motion tokens + per-scene spec (trigger, duration, easing, interruption, reduced alt) |
| 6 | Architecture | Frontend Architect | `ceos-frontend-architecture` (+ `ceos-realtime-3d` if 3D) | Stack decision with reasons; render-loop and state ownership named; budgets set |
| 7 | Prototype | Graphics / Frontend | relevant build skills | The **signature moment** runs in a browser at 1440 and 390 before any bulk sections |
| 8 | Build | Frontend Architect (integration owner) | build skills | All content in semantic HTML; no placeholder proof shipped |
| 9 | Real-browser review | Quality Engineer | `ceos-production-quality` | Screenshots at 1440/1024/768/390, console clean, interactions exercised |
| 10 | Creative critique | Independent Creative Auditor | `ceos-visual-audit` | Report in standard format; no P0/P1 open |
| 11 | Technical audit | Quality & Performance | `ceos-performance-engineering` | Budgets met or exceptions signed off; axe 0 serious/critical |
| 12 | Refinement | owners of defects | — | Each fixed defect re-verified with new evidence |
| 13 | Deploy | Frontend Architect | `ceos-production-quality` §Release | Production build exercised; rollback path written |

Small projects merge roles; the gates do not shrink.

## Decision procedure

1. Classify the project to pick a template (`templates/`): editorial (type-led, light JS) · motion-heavy (scroll
   choreography, 2D) · immersive-3d (realtime scene is the hero) · experimental-graphics (research a new technique).
   Choose the *lightest* one that can carry the concept.
2. Never start stage 7 without an approved concept (stage 2). Never start bulk sections (stage 8) before the signature
   moment survives a real-browser look at desktop and phone.
3. Parallelise only independent work (e.g. asset pipeline vs. copy deck). One integration owner merges; agents never
   edit the same file concurrently.
4. Every stage writes its artefact to the project's `docs/` (`CONCEPT.md`, `ART_DIRECTION.md`, `UX.md`, `MOTION_SPEC.md`,
   `ARCHITECTURE.md`, `QA/<date>-report.md`) and appends decisions to `DECISIONS.md`.

## Handoff format (paste into the next agent's task)

```md
## Handoff: <stage> → <next stage>
Artefact: docs/<FILE>.md (commit <sha>)
Decided: <3–6 bullets, each a decision, not a description>
Constraints the next owner must respect: <bullets>
Open questions (owner = who answers): <bullets>
Done when: <the next stage's exit gate, copied verbatim>
Files you own: <paths>  ·  Files you must not edit: <paths>
```

## Standards

- Read `~/creative-engineering-os/standards/STANDARD.md` once per project; it is the non-negotiable floor.
- Evidence beats assertion: any "works", "fast", "accessible", "beautiful" claim cites a screenshot, trace, test
  output or measurement.

## Failure criteria (stop and fix before continuing)

- A stage exit gate is "probably" met.
- Visual claims without screenshots; perf claims without a trace; a11y claims without axe + keyboard pass.
- The page reads as a template (see `ceos-visual-audit` §Generic tells).
- "Done" declared because the build passes.

## Output

At each gate: a short status block — stage, artefact path, gate checklist with ✅/❌, evidence links, next owner.
