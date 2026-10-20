# Release validation — 1.0.0

Scope: the portable public source bundle, not an image of a logged-in Mac. Original machine snapshots/private reports/history are excluded. Validation uses an exported clean checkout and explicit temporary user roots, not real account configuration writes.

Original local core evidence: five production builds,92 browser smoke passes and20 visual comparisons, including desktop/tablet/mobile, reduced-motion and graphics-disabled/no-JS paths as applicable. Root helper tests cover source contracts, safe project generation and mirror traversal/symlink rejection. Blender→GLB→meshopt inspect/optimize/reinspect and isolated MCP navigation/DOM/snapshot/screenshot/network/console/performance trace passed. These facts describe the author-machine run; omitted raw private installation reports are not presented as public release artifacts.

Packaging verification checks dry-run no-writes, preservation of existing configs/providers and explicit empty TOML arrays, idempotent links/MCP addition, foreign path protection, malformed/symlinked config refusal, private backup permissions and actual exported required paths. Plugin manifest validation and isolated plugin installation exercise documented client behavior. Fresh npm lockfile installs/builds and export self-reproduction are checked before upload. Final totals/results are recorded below after the actual run.

Limits: model invocations/new-user accounts, hosted client integrations, physical GPUs/Safari/Firefox, field CWV/INP and deployment response headers are not certified. Antigravity's original runtime check stopped at account verification. The ten MCP names include app/machine/account-bound integrations whose original launch/auth values are intentionally absent.907 skill records and60 plugin records include aliases/content versions/historical caches; they are not907 bundled/reinstalled third-party skills. Source/license evidence is recorded separately.

Public artifact review also checks no real home/user paths, auth files, personal config snapshots, raw captures/backups, app caches, node_modules or original Git history. Unknown third-party contents are not redistributed. A bounded secret-pattern scan is useful evidence, not proof against every possible secret form.

GitHub Actions provides source/helper checks and five build jobs. Remote CI status is reported separately from local results; adding a workflow is not itself a passing run.
