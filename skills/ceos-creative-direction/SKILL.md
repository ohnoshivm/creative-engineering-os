---
name: ceos-creative-direction
description: Researches benchmark digital experiences for principles (not looks), generates genuinely different website concepts, writes the creative narrative, tests originality against imitation, and produces a CONCEPT.md that requires owner approval before large implementation. Use when starting a site, when a design feels generic or derivative, when choosing between directions, or when asked for "something like <famous site>".
---

# Creative direction

## Purpose

Turn a brief into one defensible idea that only this client could own, expressed as a visual system that the rest of
the team can build. Prevent the two classic failures: the generic template and the reference clone.

## Expert knowledge to apply

- **Concept ≠ style.** A style ("dark, glassy, 3D") is available to everyone; a concept is a mapping from something
  true about the subject to a device on the page. Write it as: *"On this site, <a thing only this client has>
  becomes <a compositional / interactive device>."*
- **Competitor test.** Substitute the nearest competitor's name. If the sentence still works, the idea belongs to the
  category, not the client. Rewrite.
- **Sources of ideas, in order of strength:** the client's output (what they make), their object/shape, their name,
  their place, their ritual or process, an artefact from their world (ticket, label, manual, test card), their
  opposite (borrow a feeling from another category).
- **Benchmarks are calibration for ambition and craft**, not layouts. From each benchmark extract: the *principle*
  (why it works), the *mechanism* (how, as far as observable), the *transfer* (what that principle becomes for this
  subject), and the *never-copy list* (its signature objects, compositions, copy, shaders, assets).
- **Narrative.** A homepage is a short film with a reader in control: hook → claim → proof → depth → invitation. Each
  scene earns its place with a claim; delete scenes without one.
- **Pacing.** Alternate intensity: spectacle, quiet reading, spectacle. Two loud scenes back to back cancel out.

## Inputs

Brief, audience, the one conversion action, real assets inventory, constraints, named benchmarks, client vocabulary.

## Decision procedure

1. **Inventory the subject** (8–12 items only this client has: name meaning, logo object, materials, numbers,
   process, place, constraint, artefacts). Write them down.
2. **Research** 5–8 references (client-named benchmarks + 2 outside the category). For each, record principle /
   mechanism / transfer / never-copy. Use real browser observation where possible (`ceos-visual-audit` tools); label
   inferences as inferences.
3. **Generate three concepts** that differ in *form, motion and pacing*, not just colour. Each: idea sentence,
   signature moment (the one thing people will describe to a friend), page arc (5–8 scenes with their claim), visual
   territory (type, palette roles, material/image direction), interaction model, risk, cost (design + GPU + build).
4. **Run tests on each**: competitor test; screenshot test (does a still frame already say something?); phone test
   (does the idea survive 390 px and a thumb?); no-animation test (is it still a good page with motion off?);
   honesty test (does it need invented proof?).
5. **Recommend one**, saying what it gives up. Borrow at most one idea from a rejected concept, explicitly.
6. **Write `docs/CONCEPT.md`** and stop for approval. Large implementation does not start without it.

## Implementation standards for CONCEPT.md

```md
# Concept — <name>
Idea: On this site, <X> becomes <Y>.
Signature moment: <one paragraph, what the visitor does and sees>
Arc: <scene → claim → proof device> × 5–8
Territory: type (faces + roles), palette roles (ground/ink/accent/fields), imagery, material, sound (if any)
Interaction model: pointer / touch / keyboard / scroll — what each does
What we take from references (principles) · What we never copy (list)
Risks and costs · Rejected concepts and why
Approval: <owner, date> ← required before build
```

## Verification

- Idea sentence passes the competitor test (show the substituted sentence failing).
- Each concept has a different signature moment and a different arc.
- References are cited with URL + what was observed; nothing is described as a reference's "code" without evidence.

## Failure criteria

- Concepts that are colour/variant swaps of one layout.
- "Inspired by X" that reproduces X's hero composition, object or camera move.
- A concept that only works as a video (fails the phone or no-animation test).
- Starting the build without recorded approval.

## References

- `references/benchmarks.md` (this skill folder) — what each benchmark studio is worth studying for.
- `~/creative-engineering-os/references/catalog.md` — verified learning sources.
