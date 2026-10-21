# Pre-install audit

Initial inspection: 2026-10-21. Checkout: `~/creative-engineering-os`. Machine-readable registration inventory and configuration fingerprints: [pre-install-state.json](pre-install-state.json). No credentials or provider values were recorded.

Existing edit: `agents/creative-auditor.md`; preserve it. The repository has 14 core skills, a vendored reference library, four starters, Python installer/doctor, browser/performance tooling, and CI. Reference copies are not native installations. Shared provider configuration must remain unchanged unless a narrowly owned, backed-up integration addition is necessary. No new MCP server is required.

| Capability | Initial classification | Evidence / next check |
|---|---|---|
| Impeccable | ACTIVE / REFERENCE_ONLY | Native `.agents/skills/impeccable`, Claude link, separate OpenCode copy; bundled library commands. Check upstream completeness and provenance before replacing. |
| UI UX Pro Max | ACTIVE / REFERENCE_ONLY | OpenCode source, `.agents` link, enabled Claude plugin; retain plugin and avoid Claude manual duplicate. Retrieval assets require execution checks. |
| React Bits | MISSING | No external pinned checkout or central registration found; project-only use. |
| pmndrs/examples | MISSING | No external pinned checkout or searchable example index found. |
| GSAP official skills | ACTIVE / REFERENCE_ONLY | Eight OpenCode sources linked into Claude and Codex discovery; generic GSAP skills are separate guidance. Compare exact upstream before changes. |
| Superpowers | REFERENCE_ONLY | Bundled workflow skills exist; native installation not yet demonstrated. Startup ownership needs explicit reconciliation with gstack. |
| shadcn/ui | REFERENCE_ONLY | Existing UI guidance may reference it; no pinned external checkout or operational component test yet. Runtime stays project-level. |

Classification detail (ACTIVE, REFERENCE_ONLY, DUPLICATE, OUTDATED, MISSING, INCOMPATIBLE), upstream revisions, licenses, supporting assets, and provider discovery are completed by seven scoped specialist audit records in `integrations/evidence/`. The original library is preserved. Newer upstream commits alone do not establish that a working installation needs replacement.

## Shared environment and conflicts

Inspected metadata for Claude settings/plugins, Codex TOML, OpenCode JSON, Antigravity config, and all five local discovery roots. Configuration fingerprints and registration destinations are in the inventory. Existing MCP configuration is left in place; no redundant browser process is needed. Provider/auth values and backups are never printed.

`~/gstack/setup --status` reports installed Claude/OpenCode integration, with one broken Claude section reference (`gstack-review` → `../qa/sections/exploratory.md`). This predates this integration. Existing global project policy assigns stage orchestration to gstack and narrow TDD/verification roles to Superpowers. CEOS continues to own creative orchestration; the router must respect project-specific engineering ownership and never enable two automatic orchestrators.

Codex supports `.agents/skills`; Claude supports plugins and skill directories; OpenCode uses its existing skills directory; Antigravity has existing CEOS links but live account execution was previously blocked. Filesystem discoverability will be distinguished from a successful fresh model invocation.

## Baseline revisions and checks

The library catalog records Impeccable `dad8dbb3aac21ad1fa236c110315ef4abece23e8`, UI UX Pro Max `56ea9cf174ed86786187daa9de0e6247cb0747e4`, GSAP skills `aed9cfd3277740755f6bfc1155c7aa645403b760`, and Superpowers `bb92a77741419a4ab5f06e711a283343f1ada0c3`. These are reference pins, not proof of native completeness. No bundled React Bits, pmndrs, or shadcn source pin exists. The private/local inventory contains 536 discovery entries and fingerprints of seven settings/auth files; values are never printed.

Baseline: four script tests and one mirror security test pass. `verify-structure.py --installed` fails its old assumption that every Claude core skill is a manual symlink; the enabled plugin must be recognized without creating duplicate registrations. No baseline snapshot is regenerated.
