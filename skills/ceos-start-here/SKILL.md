---
name: ceos-start-here
description: Progressive entry point for the Creative Engineering OS. Explains the toolkit, maps website tasks to a specialist through the deterministic local router, and scales the CEOS workflow to FAST, STANDARD, or FLAGSHIP work. Use first when starting or resuming website work with this toolkit, or when unsure which skill applies.
---

# Start here — Creative Engineering OS

You are working with a toolkit for building original, premium websites. It is **a method plus a library**, not a theme.
Read this page once, then load only the skills needed for the current task and stage.

## 1. What is where

| Path | What it is | Load it |
|---|---|---|
| `skills/ceos-*` (14) | The studio method — how this team works, stage by stage | By name when the stage starts |
| `library/skills/*` (386) | Third-party reference skills (permissive licences, upstream licence kept) | Only the one you need: read `library/skills/<name>/SKILL.md` |
| `library/CATALOG.md` | Every library skill by discipline with one-line "use it for" | Skim the section you need |
| `templates/` | Four tested starters: `editorial`, `motion-heavy`, `immersive-3d`, `experimental-graphics` | `scripts/new-project.sh <template> <dest>` |
| `tooling/` | `visual-audit/capture.mjs` (screens + axe + console), `perf/frame-probe.mjs` | During review |
| `standards/STANDARD.md` | The quality floor, scaled to the task | Read when the project starts |
| `agents/creative-auditor.md` | Read-only independent critic | Use for a substantial independent critique |

Paths are relative to the toolkit root (the folder that contains this `skills/` directory).

## 2. Route and scale the task

Run the local router for one primary recommendation:

```sh
python3 <toolkit>/scripts/ceos-route.py "Create a wireframe for the signup flow" --project .
```

The 19 routes and their preferred capabilities live in `integrations/routes.json`; the full matrix and detection rules
are in `integrations/ROUTING.md`. Add `--need-secondary` only when the route's explicitly described second contribution
is useful. Use repeated `--available <capability-id>` flags for host-provided skills that have no discoverable skill
directory. Framework detection uses package metadata and config filenames. React Bits, shadcn/ui, and pmndrs/examples
require an existing React runtime; a framework override cannot bypass the package-metadata check.

The router recommends; it does not load skills, dispatch agents, install packages, or alter provider settings. Load only
the selected skill for the current stage. Prefer native platform features and existing project conventions when they
satisfy the approved direction; do not add dependencies to satisfy a route. If guidance conflicts with approved project
direction or a core CEOS skill, the approved direction wins, then the core skill.

| Mode | Use it for | Workflow |
|---|---|---|
| **FAST** | One local change, such as a CSS spacing fix | Check the affected state and run relevant checks. Skip concept options, signature prototypes, and broad QA unless the scope grows. Keep applicable safety, accessibility, keyboard/focus, reduced-motion, and security checks. |
| **STANDARD** | Normal features and page work; default when scope is unclear | Use relevant CEOS stages, build, inspect changed behavior in a real browser, and run relevant quality checks. |
| **FLAGSHIP** | Launch, rebrand, immersive site, or other high-impact work | Run the full research, direction, prototype, build, browser review, independent critique, technical review, refinement, and release verification path. |

Escalate FAST when behavior, dependencies, or direction choices appear. Escalate STANDARD for launch/rebrand work, shared
multi-route systems, immersive signature moments, or multi-team handoffs. A `--mode` override is available.

## 3. CEOS workflow and engineering ownership

`ceos-studio-workflow` owns creative stage selection and handoffs. For FLAGSHIP work, establish the concept and owner
decision before bulk sections, and render the signature moment at desktop and phone widths. For STANDARD work, use those
gates when the task makes a direction choice or includes a signature interaction. FAST work does not inherit those gates
automatically.

CEOS owns creative orchestration and direction. Existing project engineering orchestration policy wins; in gstack-led
work, gstack owns engineering orchestration and Superpowers is limited to narrow TDD and verification roles. Do not run
two orchestrators.

## Use it with Claude Code

Install as a plugin, then start from the router:

```text
/plugin install creative-engineering-os --marketplace ohnoshivm/creative-engineering-os
/creative-engineering-os:ceos-start-here
```

Do not also install manual copies of the same skills, or they will load twice.

## Use it with Codex, OpenCode, Antigravity, Cursor, or another LLM

1. Clone or download the repository.
2. Read `START-HERE.md` in full.
3. Open this skill, then load only the skill needed when its stage starts.
4. For a specialist technique, search `library/CATALOG.md` and open that reference skill.

The installer can link skills into supported clients: `python3 scripts/ceos.py install --client all --mcp` (plan only,
then add `--apply`).

## 4. Rules that make the output world-class (short form of `standards/STANDARD.md`)

- One idea that belongs to this client, not the category. References are calibration, never templates.
- Type is the main material: few sizes, big contrast, measured line length, deliberate line breaks.
- One signature motion; everything else quiet; designed reduced-motion state.
- HTML first: all content and actions work without JS and without WebGL.
- Evidence or it didn't happen: use rendered screenshots, interaction checks, axe/keyboard, console, and measurements in
  proportion to the work; substantial page reviews use the project's documented responsive sizes.
- No invented proof: no fake clients, numbers, testimonials or awards.

## 5. First commands in a fresh checkout

```sh
python3 scripts/ceos.py doctor                  # what's installed / missing
python3 scripts/ceos-route.py "Fix a small CSS spacing issue" --project .
./scripts/new-project.sh editorial ~/Projects/my-site && cd ~/Projects/my-site && npm ci && npm run dev
node <toolkit>/tooling/visual-audit/capture.mjs --url http://localhost:4321 --out docs/QA/first-look
```
