# Start here — Creative Engineering OS

Read this file first if you are an AI agent (or a human) about to build or review a website with this toolkit.

## What this is

Creative Engineering OS is a **method plus a library** for building original, premium websites with AI agents.
It is not a theme and not a template gallery. It gives you 14 stage-by-stage studio skills, a shelf of 386 reference
skills you open only when needed, four tested starter projects, browser QA tools, and written quality standards.

For substantial and flagship builds, the concept and signature moment are approved and seen in a real browser before
bulk sections are built. Small scoped changes use only the stages and checks they need. References are calibration,
never templates to copy.

## Folder map

| Path | Contents | How to use it |
|---|---|---|
| `skills/` | 14 core `ceos-*` skills (the studio method) | Load the one a stage needs. Start with `ceos-start-here` |
| `library/` | 386 third-party reference skills, each with its upstream licence | Not auto-loaded. Browse `library/CATALOG.md`, then open one `library/skills/<name>/SKILL.md` |
| `templates/` | `editorial`, `motion-heavy`, `immersive-3d`, `experimental-graphics` | Copy one with `scripts/new-project.sh <template> <dest>` |
| `tooling/` | `visual-audit/capture.mjs` (screens, axe, console), `perf/frame-probe.mjs` | Run during review |
| `standards/` | `STANDARD.md`, the quality floor; `QA-REPORT.md` | Read once per project |
| `agents/` | `creative-auditor.md`, a read-only independent critic | Run before anything is called done |

Paths are relative to the toolkit root, the folder containing this file.

## Route through a project

Run the local task router for a specialist recommendation, or open `ceos-studio-workflow` when you need to plan the
stages:

```sh
python3 <toolkit>/scripts/ceos-route.py "Implement a GSAP ScrollTrigger timeline" --project .
```

It recommends one primary capability. Add `--need-secondary` only when the route's explicitly described second
contribution is useful. It does not load skills, dispatch agents, install dependencies, or change provider settings.
Use `integrations/ROUTING.md` for the full matrix, detection limits, and mode rules.

Choose the lightest mode that fits the task:

1. **FAST** — one local change, such as a CSS spacing or color fix. Inspect the affected state and run the relevant
   check. Skip concept options, signature-moment prototypes, and broad QA gates unless scope expands. Preserve applicable
   input validation, security, accessibility, keyboard/focus, reduced-motion, and error-handling checks.
2. **STANDARD** — the default for a feature or page. Use the relevant CEOS stages for research, direction, UX, motion,
   architecture, and prototype; then build and inspect changed behavior in a real browser with appropriate quality
   checks.
3. **FLAGSHIP** — for a launch, rebrand, immersive experience, or other high-impact scope. Run the full path: research;
   distinct concepts and owner decision; art direction, UX, motion, and architecture as needed; a desktop-and-phone
   signature prototype before bulk sections; build; responsive browser QA; independent critique; technical review;
   refinement; and production-artifact/rollback verification.

Escalate FAST when behavior, dependencies, or direction choices appear. Escalate STANDARD for launch/rebrand work,
shared multi-route systems, immersive signature moments, or multi-team handoffs. A mode override can be supplied to the
router.

## Use it with Claude Code

Install as a plugin, then start from the router:

```text
/plugin install creative-engineering-os --marketplace ohnoshivm/creative-engineering-os
/creative-engineering-os:ceos-start-here
```

Do not also install manual copies of the same skills, or they will load twice.

## Use it with Codex, OpenCode, Antigravity, Cursor or any other LLM

1. Clone or download the repository.
2. Read `START-HERE.md` (this file) in full.
3. Open `skills/ceos-start-here/SKILL.md`, then load each `skills/<name>/SKILL.md` as instructions when its stage starts.
4. For a specialist technique, search `library/CATALOG.md` and open that one `library/skills/<name>/SKILL.md`.

The installer can link skills into several clients: `python3 scripts/ceos.py install --client all --mcp` (plan only, then add `--apply`).

## First commands

```sh
python3 scripts/ceos.py doctor                           # what is installed and what is missing
python3 scripts/ceos-route.py "Fix a small CSS spacing issue" --project .
./scripts/new-project.sh editorial ~/Projects/my-site    # copy a starter
cd ~/Projects/my-site && npm ci && npm run dev
node <toolkit>/tooling/visual-audit/capture.mjs --url http://localhost:4321 --out docs/QA/first-look
```

Run the toolkit's own checks from its root:

```sh
python3 tests/verify-structure.py
python3 tests/repository-hygiene.py
node --test tests/mirror.test.mjs
```

## Ground rules

- Original work only. Do not copy layouts, assets, copy or brand identity from references.
- No invented proof: no fake clients, numbers, testimonials, awards or locations. Mark placeholders.
- Evidence before claims. Use real rendered evidence, interactions, keyboard checks, console output, and measurements in
  proportion to scope; substantial page work uses the project's documented responsive QA sizes.
- Respect `prefers-reduced-motion` and make the page work without JavaScript or WebGL.
- Library skills are references. If one conflicts with an approved direction or a core skill, the approved direction wins.
- Prefer native platform features when they satisfy the approved direction; do not add a dependency just to satisfy a route.
- CEOS owns creative orchestration and direction. The existing project engineering orchestration policy wins; in gstack-led work,
  Superpowers is limited to narrow TDD and verification roles. Do not run two orchestrators.
- Load only the primary specialist skill needed at the current stage. Load a second only when its role is explicitly needed.

## Where to go next

- `SYSTEM.md`: how the parts fit together.
- `docs/USE.md`: the workflow in detail. `docs/INSTALL.md`: setup.
- `llms.txt`: a machine-readable index of this toolkit.
- `library/CATALOG.md`: every library skill by discipline. `library/UPSTREAM.md`: 484 more skills listed but not redistributed.
- `THIRD_PARTY_NOTICES.md` and `library/NOTICES.md`: licences for bundled third-party material.

Built by **ohnoshivm** — with **3rd Wrong** (design) × **AgentKindLabs** (AI & agents). See [CREDITS.md](CREDITS.md).
