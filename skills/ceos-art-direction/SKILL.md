---
name: ceos-art-direction
description: Turns an approved concept into a visual system — composition, grid and proportion, typographic hierarchy and type setting, colour roles and relationships, imagery and material direction, rhythm, responsive art direction — written as tokens, then critiques rendered pages against it. Use when setting typography, choosing fonts, building a type scale, designing layouts or grids, defining palettes, art-directing imagery or 3D materials, or when a design "looks off" and needs precise visual diagnosis.
---

# Art direction and visual design

## Purpose

Make the page look *decided*: every size, gap, colour and crop follows a rule that serves the concept. Produce
`docs/ART_DIRECTION.md` + CSS tokens; later, judge screenshots against them.

## Expert knowledge to apply

**Typography (after Bringhurst, Butterick's *Practical Typography*, Typewolf/Fonts In Use practice)**
- Body text first: 16–21 px on screen, line length 45–75 characters (≈66 ideal), leading 1.4–1.6 for sans, slightly
  more for serif. Never grey body text below 7:1 unless it's secondary.
- Few sizes, strong contrast between them. A page usually needs 4–5 sizes: display, heading, lead, body, small. Ratio
  between display and body on strong sites is often ≥ 5×; timid scales (1.2 everywhere) read as template.
- Display type: tighten tracking as size grows (−1 % to −5 %), leading 0.85–1.05; small text: loosen (+1–5 %), never
  tracked-out ALL CAPS as decoration.
- One family can carry a whole site (weights + optical sizes). Two families only when clearly distinct in role.
- Set headlines for line breaks deliberately: break on sense, avoid orphans/widows (`text-wrap: balance` for
  headings, `pretty` for paragraphs), check every breakpoint; a headline is ≤ 2–3 lines.
- Use real typographic characters: curly quotes, en/em dashes, proper apostrophes, `font-variant-numeric:
  tabular-nums` where numbers align, `font-feature-settings` only with a reason.
- Licences: verify web licence (OFL/Google Fonts/Fontshare free vs. paid foundries). Self-host, subset, `font-display:
  swap` + metric-matched fallback (`size-adjust`, `ascent-override`) to avoid CLS.

**Composition and grids**
- One grid, one pair of outer margins for the whole site (fluid 16–40 px), 12 columns on desktop, 4–6 on phone.
  Asymmetry inside the grid, never in the frame.
- Proportion: choose a ratio family (e.g. 1:√2, 2:3, 4:5, 16:9) for media and reuse it; consistency of crop is what
  makes a set of images feel art-directed.
- Hierarchy is built with scale, weight, space and position before colour. Squint test: the intended first, second,
  third read must survive a 4 px blur.
- Rhythm: section spacing clearly larger than intra-section spacing (desktop 120–240 px between scenes). Vary section
  compositions; neighbours never share a layout.
- Every section has one dominant element. Empty space is placed, and closed by something on its far side.

**Colour**
- Define roles, not swatches: ground, ink, muted ink, accent (action), fields (chapter colours), states. The accent
  appears on the primary action and at most one more place.
- Build in OKLCH for perceptual steps; check WCAG contrast for every text/ground pair (4.5:1 body, 3:1 large/UI).
- Brand colours that fail contrast are used as fields/graphics, not text.
- Avoid the generated-page palettes: cream + terracotta serif; black + single acid accent; violet/indigo gradients on
  white; gradient blobs.

**Imagery and material**
- One master image brief (subject, light, lens, crop, colour, mood) applied to every image; one treatment.
- For 3D: material grammar (what is chrome, what is matte, what glows), light recipe (key/fill/rim, environment),
  exposure and tone mapping chosen once.
- Never pass found/stock/generated images off as the client's work.

**Responsive art direction**
- The phone layout is its own composition, not a squeezed desktop: re-decide crops (`<picture>` art direction), type
  sizes (`clamp()`), order and what is cut.

## Inputs

Approved `CONCEPT.md`, brand assets (logo, colours, fonts), content inventory, imagery inventory.

## Decision procedure

1. Translate the concept's territory into tokens: `--font-*`, type steps (`clamp()`), `--space-*` scale (based on 4
   or 8), grid columns/margins, colour roles, radius (one value or deliberate few), motion tokens (handed to motion).
2. Specify each section's composition with an ASCII wireframe at desktop and phone, naming the dominant element.
3. Write the master image/material brief.
4. Build the first screen in the browser and critique it with the checklist below before any other section.

## Critique checklist (use with real screenshots)

Type: sizes count ≤ 5? body 16+ px and 45–75 ch? headline ≤ 3 lines at 1440/768/390? tracking scaled with size?
Grid: margins equal left/right? text blocks share ≤ 3 left edges? Colour: contrast pass for every text pair? accent
used sparingly? Hierarchy: squint test passes? Imagery: same crop family and treatment? Responsive: phone layout
re-composed, not shrunk?

Each finding: **evidence** (screenshot + coordinates/selector + measured value) → **rule violated** → **fix** (exact
token/CSS change).

## Failure criteria

Default font stacks; 7+ font sizes; centred everything; identical card grids; gradient/glow decoration; grey body
text; ALL-CAPS eyebrow above every heading; mismatched image crops; tokens bypassed with magic numbers.

## References

`references/type-and-grid.md` (this folder) · catalog entries: Practical Typography, Typewolf, Fonts In Use,
SiteInspire, Awwwards, Hoverstat.es.
