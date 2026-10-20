# Architecture and boundaries

The checkout is the source of truth. Small skill/agent text is linked into each client's supported discovery path; heavier runtime packages remain inside tooling, templates and the demo. Versions are pinned in package manifests/lockfiles. Application/agent credentials stay with their vendors.

The studio pipeline is research → concept → art direction → UX → motion specification → architecture → prototype → build → real browser review → independent critique → technical audit → refinement → release. One integration owner coordinates independent roles with path ownership. No site is finished because it compiles.

## Client integration

| Client | Delivery | Verification boundary |
|---|---|---|
| Claude Code | Plugin marketplace, or manual links + native JSON MCP schema | Plugin manifest and isolated install tested; no claim that a new user's model invocation/auth works |
| Codex | ~/.agents/skills + additive TOML MCP block | Installed skill discovery and server protocol tested; reload host for new MCP tools |
| OpenCode | ~/.agents/skills compatibility scan + agent adapter + native MCP schema | Discovery/parser/server connection tested; user's database/auth remain theirs |
| Antigravity | ~/.gemini/antigravity/skills + documented MCP JSON | Definitions supplied; original runtime check stopped at Google account verification |
| T3 Code | Provider skills + native browser/delegation APIs when offered | No invented T3 plugin schema and no provider-routing changes |

## Runtime ownership

DOM owns content and layout. One scroll engine and one frame owner per experience. Canvas enhances semantic content, with keyboard/reduced-motion and unsupported-graphics alternatives. Node/browser tools and Blender remain separate software; this repository does not ship their binaries.

The Claude plugin loads the 14 core studio skills, auditor and isolated Chrome diagnostics. It does not enable every third-party plugin or attach a logged-in browser. The multi-client installer is an explicit separate setup path, not a startup hook.

## Full ecosystem

The manifests distinguish bundled original content from upstream-install and unknown provenance. They include historical plugin caches as separate observations, not claims that every cached plugin is enabled. Source/license/public availability can change. See docs/ECOSYSTEM.md and THIRD_PARTY_NOTICES.md.

Public releases are generated through an allowlist into a clean publication checkout. Personal installation reports/raw captures/config snapshots and original private commit history are omitted. The source package includes original procedural demo art and reviewed visual-test baselines, not reference-site assets.

Built by **ohnoshivm** — with **3rd Wrong** (design) × **AgentKindLabs** (AI & agents).
