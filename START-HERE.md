# Start here — Creative Engineering OS

Read this file first if you are an AI agent (or a human) about to build or review a website with this toolkit.

## What this is

Creative Engineering OS is a **method plus a library** for building original, premium websites with AI agents.
It is not a theme and not a template gallery. It gives you 14 stage-by-stage studio skills, a shelf of 386 reference
skills you open only when needed, four tested starter projects, browser QA tools, and written quality standards.

Core rule: concept and signature moment are approved and seen in a real browser before bulk sections are built.
References are calibration, never templates to copy.

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

## The route through a project

1. **Frame** with `ceos-studio-workflow`. Always first.
2. **Concept** with `ceos-creative-direction`. Three distinct concepts, one recommended, owner approval before building.
3. **Look** with `ceos-art-direction` (type, grid, colour, imagery as tokens).
4. **Behaviour** with `ceos-interaction-architecture` (IA, journeys, every input, accessibility).
5. **Motion** with `ceos-motion-direction` (tokens, choreography, reduced motion).
6. **Stack** with `ceos-frontend-architecture` (lightest stack, one render loop, ownership).
7. **Signature moment** with `ceos-realtime-3d`, `ceos-shader-engineering`, `ceos-creative-coding` or `ceos-3d-asset-pipeline` as needed.
8. **Build** from a template. Content in semantic HTML. Placeholders clearly marked.
9. **Prove it** with `ceos-production-quality` (tests, axe, keyboard, no-JS and no-WebGL) and `ceos-performance-engineering` (measured budgets).
10. **Critique** with `ceos-visual-audit` or the `creative-auditor` agent. Fix P0/P1 issues, re-capture, repeat.

Do not skip steps 2 to 7.

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
- Evidence before claims. Real screenshots at 1440, 1024, 768 and 390 px, axe, keyboard, console and measured performance.
- Respect `prefers-reduced-motion` and make the page work without JavaScript or WebGL.
- Library skills are references. If one conflicts with an approved direction or a core skill, the approved direction wins.

## Where to go next

- `SYSTEM.md`: how the parts fit together.
- `docs/USE.md`: the workflow in detail. `docs/INSTALL.md`: setup.
- `llms.txt`: a machine-readable index of this toolkit.
- `library/CATALOG.md`: every library skill by discipline. `library/UPSTREAM.md`: 484 more skills listed but not redistributed.
- `THIRD_PARTY_NOTICES.md` and `library/NOTICES.md`: licences for bundled third-party material.
