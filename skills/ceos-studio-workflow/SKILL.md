---
name: ceos-studio-workflow
description: Scales the Creative Engineering OS workflow to FAST, STANDARD, or FLAGSHIP work. Selects only relevant creative and engineering stages, keeps safety and evidence checks in scope, and records compact decisions and handoffs. Use when planning multi-stage website work, deciding what must be true before the next stage, or checking if substantial work is ready to ship.
---

# Studio workflow (Creative Engineering OS)

This workflow owns creative stage selection and handoffs: **what happens next and what must be true before moving on**.
It does not replace specialist skills or take over a project's engineering orchestration.

## When to use

- Planning a website or web experience that spans multiple stages.
- Unsure which specialist applies; run `scripts/ceos-route.py` for one deterministic recommendation.
- Reviewing substantial work before calling it done.
- For a local CSS or copy fix, use FAST and verify only the affected behavior plus any checks the change touches.

## Inputs

Brief and requested outcome; current project state; framework and dependencies; real assets; time, hosting, and licence
constraints; references; existing project instructions and engineering orchestration policy.

## Choose a mode

| Mode | Scope | Workflow |
|---|---|---|
| **FAST** | One local change, such as spacing, color, or type-size correction | Inspect the relevant code and current state, make the change, then check the affected state or viewport. Skip concept options, signature-moment prototypes, and broad QA unless scope expands. Preserve applicable validation, error handling, security, accessibility, keyboard/focus, and reduced-motion checks. |
| **STANDARD** | Normal feature or page work; default when scope is unclear | Use the CEOS stages that apply to the task. Research and direction are needed when a real choice is open; UX, motion, architecture, and prototype work are needed when those concerns change. Inspect changed behavior in a real browser and run relevant quality checks. |
| **FLAGSHIP** | Launch, rebrand, immersive experience, or another high-impact scope | Run the full applicable path: research, multiple concepts and owner decision, art direction, UX, motion, architecture, a signature prototype before bulk sections, build, responsive browser review, independent critique, technical review, refinement, and production-artifact/rollback verification. |

Escalate FAST when behavior, multiple states, dependencies, or brand direction are involved. Escalate STANDARD when a
launch/rebrand, shared multi-route system, immersive signature moment, or multi-team handoff needs formal approval. A user
or project mode override takes precedence over automatic classification.

## The stages

Use only the stages relevant to the selected mode and changed surface. A stage can be merged with another for small work.

| # | Stage | Skill | Apply its gate when… |
|---|---|---|---|
| 1 | Research | `ceos-creative-direction` §Research | References or user evidence will change the direction. FLAGSHIP work records what to learn and what not to copy. |
| 2 | Concept | `ceos-creative-direction` | The task makes a new site or brand direction choice. FLAGSHIP work presents distinct concepts, one recommendation, and records owner approval before bulk build. |
| 3 | Art direction | `ceos-art-direction` | Visual direction or a shared design system changes; record relevant type, palette, grid, imagery, and responsive tokens. |
| 4 | UX | `ceos-interaction-architecture` | Routes, forms, navigation, or interactive states change; include keyboard, touch, and accessibility behavior. |
| 5 | Motion spec | `ceos-motion-direction` | Animation changes; define intent, trigger, timing, interruption, and reduced-motion behavior. |
| 6 | Architecture | `ceos-frontend-architecture` | Stack, rendering, state, asset, scroll, or lifecycle ownership changes. Use the lightest suitable stack. |
| 7 | Prototype | Relevant build skills | A risky or signature interaction needs validation. FLAGSHIP work sees the signature moment at desktop and phone widths before bulk sections. |
| 8 | Build | Relevant implementation skills | Always for implementation; preserve semantic content, error handling, and project conventions. |
| 9 | Browser review | `ceos-production-quality` and project browser tools | A rendered path, responsive behavior, or interaction changes; exercise the changed flow and inspect actual output. FLAGSHIP work uses the documented responsive set. |
| 10 | Creative critique | `ceos-visual-audit` or `creative-auditor` | Substantial visual work needs an independent review; fix P0/P1 defects and recapture. |
| 11 | Technical review | `ceos-performance-engineering` and relevant QA skills | Performance, accessibility, security, or production quality is in scope; measure rather than assume. |
| 12 | Refinement | Defect owners | Evidence shows defects; fix the cause and recheck the affected result. |
| 13 | Release verification | `ceos-production-quality` §Release | The user authorizes a release. Exercise the production artifact and record its rollback path; a router recommendation never authorizes a deploy. |

FAST work does not require stages 1–7, 10, or a full-page audit by default. It still keeps every relevant safety and
quality check. Never bypass input validation, security, data-preserving error handling, accessibility, reduced motion,
or an explicit user/project gate to save time.

## Decision procedure

1. Select FAST, STANDARD, or FLAGSHIP from the scope. `scripts/ceos-route.py` can recommend a mode and specialist without
   running tools or changing project state.
2. Preserve existing project instructions, framework, dependencies, and engineering orchestration. CEOS owns creative
   orchestration and direction. The existing project engineering orchestrator wins; in gstack-led work, gstack owns engineering
   orchestration and Superpowers is limited to narrow TDD and verification roles. Do not run two orchestrators.
3. Load only the primary specialist needed for the current stage. Load a second only when its contribution is explicit
   and needed. Check framework and constraints first; do not add React or another runtime to satisfy a skill route.
4. For substantive new work, select the lightest suitable starter (`editorial`, `motion-heavy`, `immersive-3d`, or
   `experimental-graphics`) and record the stack decision. A local fix does not need a template decision.
5. Build semantic content and meaningful fallbacks. Respect approved direction and provide a designed reduced-motion
   alternative whenever motion changes.

## Compact project state and handoff

Keep a current state note only when work spans stages or owners; a FAST change does not need a new document. Use this
compact schema in an existing project note or handoff:

```md
Task: <outcome>
Mode: <FAST | STANDARD | FLAGSHIP>
Constraints / stack: <only material constraints and current framework>
Decisions: <decision → reason>
Evidence: <check → artifact or status>
Open questions: <question → owner, or none>
Next: <stage/action → owner>
```

Keep evidence concrete: screenshot, test output, browser interaction, trace, or explicit “not verified.” Do not write an
artifact for a stage that was not needed.

## Standards and evidence

- Read `standards/STANDARD.md` once per project; apply its relevant quality floor at each stage.
- Evidence beats assertion: a visual claim needs a real render, a performance claim needs a measurement, and an
  accessibility claim needs the applicable automated and manual checks.
- For substantial page work, inspect the documented responsive sizes, interactions, keyboard/focus, console, and
  accessibility. FAST work checks the affected viewport and interaction rather than inheriting a full-page review.
- Keep references as calibration, never copies. Mark placeholders and do not invent proof.

## Failure criteria

- A required gate for the selected mode is only “probably” met.
- Visual, performance, or accessibility claims lack their relevant evidence.
- FAST mode is used even though scope expanded to behavior, multiple states, a new dependency, or brand direction.
- A data, security, accessibility, reduced-motion, or explicit quality check is bypassed.
- “Done” is declared because the build passes.

## Output

For FAST, report the change and its focused check. For STANDARD and FLAGSHIP, report the current stage, compact state,
decisions, relevant gate status, evidence, open questions, and next owner. Do not emit the full handoff at every step.
