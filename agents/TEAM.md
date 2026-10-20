# Specialist agent team

Seven roles (prompt §8). Six already existed as Claude Code agents (`~/.claude/agents/`) and OpenCode agents
(`~/.config/opencode/agents/`) before this OS; they are **reused unchanged**. The missing seventh, the Independent
Creative Auditor, is added here.

| Role | Agent (Claude Code / OpenCode) | Owns | Primary skills |
|---|---|---|---|
| Creative Director | `creative-director` (existing) | Concept, narrative, originality; approval gate | ceos-creative-direction, frontend-design |
| UX Architect | `ui-ux-architect` (existing) | IA, journeys, interaction model, a11y plan | ceos-interaction-architecture |
| Art & Motion Director | `visual-designer` + `motion-director` (existing, used as one role on small jobs) | Type, colour, grid, imagery; motion tokens and spec | ceos-art-direction, ceos-motion-direction, gsap-* |
| Frontend Architect — **integration owner** | `frontend-architect` (existing) | Stack, structure, render loop, merges all work | ceos-frontend-architecture |
| Creative Graphics & Shader Engineer | `3d-webgl-engineer` (existing) | Scenes, materials, shaders, assets | ceos-realtime-3d, ceos-shader-engineering, ceos-3d-asset-pipeline, ceos-creative-coding |
| Quality & Performance Engineer | `visual-qa-engineer` + `performance-engineer` (existing) | Browser evidence, tests, budgets | ceos-production-quality, ceos-performance-engineering |
| Independent Creative Auditor | **`creative-auditor` (new)** | Read-only critique against concept + standard | ceos-visual-audit |

Codex in T3 has native child agents and T3-owned delegation. Use the live orchestrator catalog to choose an available model; apply these role briefs to supported child tasks. Antigravity roles can be applied inline when its host exposes no supported registry. Templates include project instructions; existing global instructions are preserved. T3 has its own browser and delegation capabilities, verified in the setup session, and also inherits provider skill discovery.

## Rules of engagement

1. **One integration owner** (Frontend Architect) merges; specialists hand back patches or files they exclusively own.
2. **Ownership by path**, declared in each handoff (`Files you own` / `Files you must not edit`). Two agents never
   edit the same file in parallel.
3. **Parallelise only independent work** (e.g. asset optimisation ∥ copy deck ∥ UX inventory). Concept, art
   direction and integration are sequential.
4. **Context economy**: each agent loads `standards/STANDARD.md`, its own skills, and the handoff — not the whole
   history. Artefacts live in `docs/`, so agents read files, not chat logs.
5. **No swarm**: default team size for a page is 1–3 agents. Spawn a specialist only when its skill is needed and
   the work is separable. Never add API billing; agents run on existing subscriptions.
6. **The auditor is independent**: it never audits work it produced, has no edit permission, and its report format is
   fixed (`ceos-visual-audit`).

## Handoff format

Defined in `skills/ceos-studio-workflow/SKILL.md` (§Handoff format). Completion = the receiving stage's exit gate.

## Code-review standard

Reviewers check: ownership respected; tokens instead of magic numbers; one render loop; `destroy()` paths; motion in
`matchMedia`; content in HTML; tests added/updated; evidence attached (screenshots/test output/measurements).

## Read-only auditor enforcement

Claude auditor limits tools to Read/Glob/Grep/WebFetch/WebSearch and explicitly denies write/edit/shell. OpenCode auditor denies edit/bash/task. Capture and report persistence belong to the integration owner. These are tool-level boundaries, not an OS sandbox or a guarantee about unrelated MCP servers. Existing eight OpenCode agents still have legacy `permissions:` frontmatter that may not enforce restrictions; they were preserved and should be reviewed individually before security-sensitive delegation.
