# Final verification — 20 October 2026

This completes the safe local installation scope. Capabilities with blocked or untested host/device behavior are labeled explicitly. No public deployment or Pixelard website implementation is included.

## Capability matrix

| Capability | Status | Actual evidence / limit |
|---|---|---|
| Central source, ownership, standards and operating/rollback guides | WORKING | Repository source, AGENTS.md/CLAUDE.md, stage gates and report template; local link/hygiene checks |
|13 original specialist skills /39 owned links | WORKING for Claude/Codex/OpenCode; Antigravity runtime BLOCKED | Structural schemas pass; live Codex/T3 catalog; isolated OpenCode discovers13 once each; Antigravity account gate |
| Four production starters | WORKING locally | [Template results](TEMPLATE-VERIFICATION.md), production builds/smoke/visual/axe and real inspected screenshots |
| Original isolated graphics demo | WORKING locally | [Demo evidence](DEMO-VERIFICATION.md), [independent critique](DEMO-AUDIT.md); scoped refinements rechecked |
| Native / T3 child orchestration | WORKING in Codex/T3 | Three same-provider specialist tasks executed; cross-provider Antigravity task attempted using live catalog and existing auth |
| Independent auditor registration | PARTIALLY WORKING | Claude owned file/tool constraints validated; no Claude model invocation. OpenCode parser resolves edit/bash/task deny. Existing agents preserved |
| Chrome DevTools MCP server | WORKING | [Smoke JSON](MCP-SMOKE.json): initialize/tools-list, navigation, DOM click, snapshot, network/console and performance trace; screenshot check included in final run |
| Claude / OpenCode MCP connection | WORKING | Native `claude mcp get chrome-devtools`: Connected; isolated-data `opencode mcp list`: connected |
| Codex MCP host activation | PARTIALLY WORKING | Native `codex mcp get ... --json` confirms config; independent server smoke passes. Fresh Codex host required to expose added tools; this running host was not restarted |
| Antigravity host activation | BLOCKED | T3 child attempt returns “Verify your account to continue.” No authentication flow changed/completed |
| T3 collaborative browser | PARTIALLY WORKING | Open/navigation to localhost succeeds; resize/snapshot experienced host disconnect. Playwright CLI/test runner supplied actual browser evidence |
| Blender + GLB/meshopt | WORKING | [Asset smoke](ASSET-SMOKE.json): factory-default disposable cube export → inspect → optimize → re-inspect; EXT_meshopt_compression confirmed |
| axe and local Lighthouse | WORKING | Project-scoped axe in browser tests; globally existing Lighthouse used for local measurements |
| Lighthouse CI service/upload | OPTIONAL / NOT VERIFIED | Pinned autorun script exists in applicable starters; remote CI is not configured |
| KTX/toktx encoder | NOT INSTALLED | No admin installer/sudo; optional workflow documented. Real KTX texture encoding/transcoding not tested |
| R3F/OGL/Motion/Tempus/Theatre/Rive/WebGPU/OGPU/Spector | OPTIONAL | Primary-source evaluation and scoped experiments in [optional tools](OPTIONAL-TOOLING.md), no blanket installs |
| Existing provider/auth preservation | WORKING within checked scope | [Comparison](CONFIG-PRESERVATION.json): only owned MCP addition, pre-existing definitions/settings unchanged;2 known auth files same hashes. All subscription logins were not re-exercised |
| Default OpenCode database | BLOCKED pre-existing condition | CLI/schema mismatch; diagnostic checks use throwaway data only. No migration/reset performed |
| gstack readiness | PARTIALLY WORKING pre-existing condition | `~/gstack/setup --status` exit1: Claude install broken section link. Existing installation not rewritten |
| Hosted/Safari/physical mobile/field CWV | NOT VERIFIED | No deployment, WebKit test or physical-device lab/field measurements performed |

Five production builds passed (four starters + demo). Final browser suites: **92 smoke passes** (64 starters +28 demo), **20 visual comparisons** (17 starters +3 demo). Explicit capability/project skips and all per-suite counts are recorded in the linked reports. Root helper coverage adds4 script tests and1 security-helper test. Final source hygiene:162 text files,0 targeted secret-pattern findings,0 broken local Markdown links.

## Commands executed in this continuation

- `scripts/verify.sh`:13 skill schemas,39 resolving links,4 locked starter contracts, standard/team artifacts and git backup exclusion passed; installed core tools located.
- `python3 tests/scripts.test.py`:4 tests passed. Creation with spaces, name/lock sync, baseline/artifact exclusion, existing destination preservation, traversal/dangling-path rejection, foreign-link protection and idempotence covered.
- `node --test tests/mirror.test.mjs`:1 security-focused test passed. Intended mirror file allowed; missing/malformed/traversal/symlink escape rejected. An initial expected-path assertion failed on macOS `/var`→`/private/var` canonicalization, corrected to compare real paths.
- `python3 tests/asset-smoke.py`: all 4 export/inspect/optimize/inspect steps exit0.1936-byte cube becomes1948bytes with meshopt extension; proof of pipeline, not an optimization benefit for a tiny cube.
- `python3 tests/mcp-smoke.py`:32 tools advertised; isolated server diagnostics passed. No logged-in user browser was attached. Server schema requires pageId; harness was adapted from actual tools/list response.
- `npm audit --omit=dev --json` in tooling:0 vulnerabilities; each starter and demo audited separately in their reports. No automatic audit-fix or global package upgrades.
- `tests/repository-hygiene.py`: source-only secret-prefix/private-key pattern scan and local Markdown links. This bounded scan does not certify absence of every possible secret. Backups/auth/config files are excluded from repository content.
- Template and demo production check/build/smoke/visual/capture/Lighthouse commands: exact totals, corrected failures and limitations in their separate reports.
- Client configuration comparison and metadata-only inventory generated [INVENTORY.json](INVENTORY.json), [CLIENT-VERIFICATION.json](CLIENT-VERIFICATION.json), [CONFIG-PRESERVATION.json](CONFIG-PRESERVATION.json).

## Refinement and evidence interpretation

The template pass fixed reduced-motion GPU-buffer resize clearing, strengthened decoded-pixel shader checks so DOM text cannot make an empty canvas pass, and separated production-preview ports with server reuse disabled. Independent demo review caught mismatched input guidance and below-fold desktop controls; its owner corrected and rechecked them. No visual baseline was updated merely to silence an unexplained failure.

Concurrent browser workloads contaminated an early3D Lighthouse run. It is retained/labeled and superseded by an isolated run; local frame/Lighthouse figures are not field INP or physical-mobile GPU evidence. Temporal motion review and robust leak/context-loss/device tests remain project release gates.

A previous session reported a credential-output incident. No value is repeated or stored in this repository; user-controlled revocation/rotation was not performed. This report does not claim that the entire historical thread was free of credential exposure. Existing Token Harbor files/routing were not reactivated or modified.

## Release state

Local toolkit only; no production site deployed. Source is committed after final checks. See [rollback](ROLLBACK.md) for owned integration removal without restoring whole account config files, and [maintenance](MAINTENANCE.md) for deliberate upgrades. Remaining account/device checks are explicit limitations, not silent success claims.
