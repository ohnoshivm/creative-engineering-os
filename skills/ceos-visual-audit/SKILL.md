---
name: ceos-visual-audit
description: Independent, evidence-based visual and creative critique of a rendered website in a real browser — originality, typography, composition, spacing, alignment, hierarchy, colour, imagery, motion quality, interaction clarity, consistency, responsive fidelity and design-to-spec accuracy — producing a prioritised defect report where every issue has evidence and a precise fix. Use after any visual change, before declaring a page done, when a page "feels off", or when asked to review/critique/QA a design.
---

# Visual quality audit

## Purpose

Judge what the browser actually renders, not what the code intends. Replace "improve the design" with defects a
developer can fix in minutes.

## Capture first (never critique from code)

```bash
node ~/creative-engineering-os/tooling/visual-audit/capture.mjs --url http://localhost:5173 --out docs/QA/<date>
```
Produces screenshots at 1440, 1024, 768, 390 (first screen + full page), console errors, a DOM type/colour/spacing
measurement JSON, axe results, and a reduced-motion screenshot set. Record key interactions as video when motion is
in scope (`--video`).

## How to look (in this order)

1. **Five-second test** (first screen at 1440 and 390): can a stranger say what this is and what to do?
2. **Squint test**: blur mentally — is the intended order of reading obvious?
3. **Concept fidelity**: does the screen express the approved idea sentence, or could it be anyone's?
4. **Type**: count sizes; check measure, leading, tracking vs size, line breaks, orphans, font loading (fallback
   flash), real quotes/dashes.
5. **Grid and spacing**: equal outer margins; shared left edges; section rhythm; consistent gaps (measure in px).
6. **Colour**: roles respected; contrast (measured); accent discipline.
7. **Imagery/3D**: one treatment; crops consistent; lighting and materials credible; no stretched/low-res assets.
8. **Motion** (from video/frames): purpose, easing consistency, choreography, interruption, idle calm, jank.
9. **Interaction clarity**: affordances, hover/focus/active states, feedback latency.
10. **Responsive fidelity**: phone is re-composed; nothing overflows; tap targets ≥ 44 px.
11. **Spec accuracy**: compare against `ART_DIRECTION.md` tokens and approved mockups (pixel diff where available).

## Generic tells (each is a finding unless the brief demands it)

Centred hero + small eyebrow + gradient blob; identical icon cards in rows of three; ALL-CAPS tracked labels above
every heading; 01/02/03 numbering on non-sequences; glassmorphism by default; purple/indigo gradients; drop shadows
on everything; fade-up on every section; stock "team at laptop" photos; default system or Inter-everywhere type;
one border-radius on every element; arrow "→" on every link.

## Report format (`docs/QA/<date>-visual-audit.md`)

```md
# Visual audit — <page> — <date> — build <sha>
Scores (0–10): Concept __ · Typography __ · Composition __ · Colour __ · Imagery/3D __ · Motion __ · Interaction __ · Responsive __
Verdict: SHIP / FIX THEN SHIP / RETHINK

| ID | Sev | Area | Evidence (file:viewport, selector, measured value) | Rule / expectation | Fix (exact change) | Verified |
|----|-----|------|-----------------------------------------------------|--------------------|--------------------|----------|
| V-01 | P1 | Type | 390-first.png: h1 wraps to 5 lines (font-size 64px at 390) | headline ≤ 3 lines | --step-display min 44px → 40px; copy cut to 4 words | ☐ |
```

Severity: **P0** broken/misleading/inaccessible · **P1** visibly below standard, fix before ship · **P2** polish ·
**P3** idea for later. Verified = re-captured screenshot path after the fix.

## Rules for the auditor

- Independence: audit someone else's output, or re-read your own with the report format — no defending choices.
- Every finding cites a screenshot path + viewport + selector or coordinates + a measurement where possible.
- Every fix is concrete (token, CSS property, copy change, asset change). No adjectives without numbers.
- Re-capture after fixes; close findings only with new evidence.

## Failure criteria

Critique without screenshots; vague findings; ignoring phone; scoring without listing defects; marking verified
without re-capture.
