# Architecture

## Principle

One source of truth on disk, linked (never copied) into each client's documented discovery path. Everything heavy
lives inside projects or templates, not globally.

```text
~/creative-engineering-os/          (git, source of truth)
  skills/ceos-*/SKILL.md  ──symlink──▶ ~/.claude/skills/ceos-*          Claude Code (both accounts optional)
                          ──symlink──▶ ~/.agents/skills/ceos-*          Codex (user scope), OpenCode (compat scan)
                          ──symlink──▶ ~/.gemini/antigravity/skills/ceos-*   Antigravity (global scope)
  agents/*.md             ──symlink──▶ ~/.claude/agents/creative-auditor.md   (only the role that was missing)
                          ──copy-adapted──▶ ~/.config/opencode/agents/creative-auditor.md
  standards/STANDARD.md   ◀── referenced from each project's CLAUDE.md / AGENTS.md
  templates/{editorial,motion-heavy,immersive-3d,experimental-graphics}   copied by scripts/new-project.sh
  tooling/                visual-audit + perf scripts shared by all templates (zero global deps)
```

T3 Code supplies its own collaborative browser and native/app-owned task orchestration. Provider skills load through the provider discovery paths; no T3 settings change is needed. Prefer live T3 preview tools, with documented Playwright workflows for reproducible suites and fallback. Use the live model catalog before delegation.

## Why `ceos-` prefix

OpenCode warns that skill names must be unique across all locations, and this machine already has ~300 skills.
Every custom skill is namespaced `ceos-*` so nothing shadows or collides with an installed skill.

## Why `~/.agents/skills` and not `~/.config/opencode/skills`

OpenCode scans `~/.config/opencode/skills`, `~/.claude/skills` and `~/.agents/skills`. Linking into all three would
register each skill up to three times in OpenCode. Linking into `~/.claude/skills` + `~/.agents/skills` covers Claude,
Codex and OpenCode with the fewest entries. (Existing third-party skills already appear in several of these
directories; that pre-existing duplication is left as is.)

## What is global vs project-local

| Global (reusable, small) | Project-local (in templates) |
|---|---|
| Skills + agents (text) | TypeScript, Vite, Astro, three, gsap; lenis in motion template only (OGL/R3F optional) |
| Chrome DevTools MCP (run on demand via npx, no global install) | @playwright/test, @axe-core/playwright, @lhci/cli |
| Blender (desktop app, via Homebrew cask) | @gltf-transform/cli, gltfpack (dev deps, run via npm scripts) |
| Existing: Node, npm, bun, Chrome, Lighthouse, playwright-cli | Theatre.js / Rive only when a project needs authoring |

Playwright in templates uses the installed Google Chrome (`channel: 'chrome'`), so no extra browser download.

## Skill map (13 custom skills, merged by responsibility)

| Skill | Covers (prompt §4) | Leans on existing skills |
|---|---|---|
| `ceos-studio-workflow` | §11 quality loop, gates, handoffs, which skill when | all below; superpowers verification |
| `ceos-creative-direction` | §4.1 | frontend-design, taste-skill (for dealing directions) |
| `ceos-art-direction` | §4.2 incl. typography/layout | impeccable, taste-skill |
| `ceos-interaction-architecture` | §4.3 | building-accessible-interfaces, web-accessibility |
| `ceos-motion-direction` | §4.4 | gsap-* (API), motion |
| `ceos-frontend-architecture` | §4.5 | vercel-react-best-practices (only for React) |
| `ceos-creative-coding` | §4.6 | — |
| `ceos-realtime-3d` | §4.7 | threejs (API basics) |
| `ceos-shader-engineering` | §4.8 | — |
| `ceos-3d-asset-pipeline` | §4.9 | optimize-3d-assets |
| `ceos-visual-audit` | §4.10 | reviewing-interface-quality |
| `ceos-performance-engineering` | §4.11 | performance, core-web-vitals |
| `ceos-production-quality` | §4.12 | playwright-cli, web-accessibility |

## Agent team

Seven roles (§8). Six already exist as Claude Code agents and are **reused, not overwritten**; the missing
Independent Creative Auditor is added. Role contracts, ownership and handoff formats: `agents/TEAM.md`.

## MCP

One addition: Chrome DevTools MCP (`chrome-devtools-mcp`, ChromeDevTools org, Apache-2.0) for traces, network and
console. Added per client through each client's own config mechanism, after a backup. No second browser MCP:
Playwright (CLI + `@playwright/test`) remains the repeatable-test path and T3 preview tools stay as they are.
