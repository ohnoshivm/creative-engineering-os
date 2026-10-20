# System overview

One versioned source of truth, provider-specific integration, project-scoped runtime dependencies. Architecture details: [ARCHITECTURE.md](architecture/ARCHITECTURE.md).

| Component | Location | Purpose |
|---|---|---|
| 13 custom skills | `skills/ceos-*` | Direction, UX, motion, graphics, architecture, assets, critique and production verification |
| 39 skill links | `~/.claude/skills`, `~/.agents/skills`, `~/.gemini/antigravity/skills` | One owned link per skill per discovery directory; no overwritten third-party skills |
| Auditor | `agents/creative-auditor.md`, `agents/opencode/creative-auditor.md` | Read-only tool restrictions; owner supplies captures and persists report |
| Four templates | `templates/` | Pinned packages/lockfiles, semantic content, fallback states, build and real-browser tests |
| Shared tooling | `tooling/` | Responsive captures, axe, console/layout reports, optional video and rAF/frame/CWV lab probe |
| Chrome DevTools MCP | pinned npx `chrome-devtools-mcp@1.11.0` | On-demand isolated headless Chrome diagnostics; no logged-in browser reuse; telemetry/CrUX disabled |
| Blender | `/Applications/Blender.app`, PATH via Homebrew | Offline asset creation; glTF-Transform/meshopt run on demand, not global dependencies |
| Library and standards | `references/`, `standards/` | Primary learning sources, exercises, creative gates and evidence-backed reports |
| Demonstration | `demo/signal-study` | Independent original shader + GSAP integration study, not a client website |

## Compatibility (20 October 2026)

| Client | State | Evidence and limit |
|---|---|---|
| Claude Code primary account | WORKING skills/browser; auditor runtime PARTIALLY WORKING | Skill links + previous live discovery; native `claude mcp get chrome-devtools` reports Connected. Auditor file linked with read-only tool list; a model-run invocation was not performed. Secondary account not modified |
| Codex / this T3 session | WORKING skills/native children; MCP registration PARTIALLY WORKING | All 13 ceos skills appear in injected live catalog; native child tasks executed. `codex mcp get ... --json` confirms registration; independent stdio handshake exercises all 32 exposed tools' core categories. New MCP tools need a fresh host session; not injected into this running session |
| OpenCode | WORKING discovery/config; default database BLOCKED independently | Isolated-data `debug skill` discovers all 13; `debug agent creative-auditor` resolves deny for edit/bash/task; `mcp list` reports chrome-devtools Connected. Existing default-state schema conflict was not reset or repaired |
| Antigravity | BLOCKED runtime; config/links PARTIALLY WORKING | 13 owned skill links and documented global MCP config present; server itself passes stdio smoke. T3-owned execution attempt returned Google “Verify your account to continue.” No account changes attempted; native discovery/execution still unverified |
| T3 Code | WORKING native orchestration; browser PARTIALLY WORKING | Live capability catalog and same-provider native specialist tasks used. Preview opens/navigates local demo; resize/snapshot host disconnect occurred. Browser QA used installed Playwright workflows when preview calls failed. No T3 settings/auth/routing changed |

No subscription login or provider migration was attempted. Config comparison confirms only the chrome-devtools entry was added to the four client configs; other settings and pre-existing server definitions match the private before snapshot. Two known auth files match their pre-run hashes. This is preservation evidence, not a fresh login test of every account.

## Browser integration

The same server command is adapted to each documented config schema:

```text
npx --yes chrome-devtools-mcp@1.11.0 --isolated --headless --no-usage-statistics --no-performance-crux
```

Claude uses `~/.claude.json` user MCP servers; Codex uses `~/.codex/config.toml` (`mcp_servers`); OpenCode uses `~/.config/opencode/opencode.json` (`mcp`, local command array); Antigravity uses `~/.gemini/config/mcp_config.json` (`mcpServers`). Native commands were used for Claude and Codex. Existing server names/values were preserved. Backups are private and git-ignored. No credentials are stored in the added server definition.

The server can inspect and change its browser; isolation is not an OS filesystem sandbox. Avoid private data in diagnostic pages/captures. Existing MCP servers were not audited or reconfigured. Spector.js remains optional; no overlapping browser server/extension was added.

Official schemas and safety flags checked: [Chrome DevTools](https://github.com/ChromeDevTools/chrome-devtools-mcp), [Claude](https://code.claude.com/docs/en/mcp), [OpenCode](https://opencode.ai/docs/mcp-servers/), [Antigravity](https://antigravity.google/docs/mcp). Codex setup was checked against installed `codex mcp add --help`.
