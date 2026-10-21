# Rollback guide

Rollback is per integration. Keep the pinned review checkouts unless the owner separately decides they are no longer needed. Restore backed-up skill files from their private paths before removing a source tree. The backup files are not part of CEOS and their contents are intentionally not reproduced here.

## Upstream integrations

| ID | Rollback |
|---|---|
| `impeccable` | Restore the 7 `agents/` files to `~/.agents/skills/impeccable/` and the 7 `opencode/` files to `~/.config/opencode/skills/impeccable/` from `~/.local/state/creative-engineering-os/integration-v2-20261021/backups/impeccable-v4.7-cze_q06l/`. The existing Claude symlink follows the `.agents` tree. Keep the backup manifest at its recorded path; do not print or edit backup contents. |
| `ui-ux-pro-max` | No active skill tree was changed and no backup was created. Leave the existing OpenCode tree, `.agents` symlink, and Claude plugin in place. If undoing only the CEOS record, remove its guide/evidence/manifest entry after review; do not create a manual Claude skill copy. |
| `react-bits` | Remove the four thin-shim links only if intentionally undoing the global-install record: `~/.agents/skills/react-bits`, `~/.config/opencode/skills/react-bits`, `~/.claude/skills/react-bits`, and `~/.gemini/antigravity/skills/react-bits`. Remove only the integration's component index or fixture artifacts when their owner confirms they are no longer needed. Keep `~/creative-engineering-os-upstreams/react-bits.broken-20261021T131508Z`; it is only a cleanup candidate. |
| `pmndrs-examples` | Remove the four thin-shim links only if intentionally undoing the global-install record: the same four roots under `pmndrs-examples`. The CEOS index and generator can be removed only as a scoped rollback after reviewing their callers. Keep the 232 MB `~/creative-engineering-os-upstreams/pmndrs-examples-validation` directory; do not use a broad cleanup command. |
| `gsap-skills` | No official `gsap-*` skill tree needs restoration. To undo the duplicate-scope edit, copy `~/.local/state/creative-engineering-os/integration-v2-20261021/backups/gsap-skills/agents-gsap-SKILL.md.before` back to `~/.agents/skills/gsap/SKILL.md`. |
| `superpowers` | Remove only the four new direct links if intentionally undoing this integration: the `test-driven-development` and `verification-before-completion` links under `~/.agents/skills/` and `~/.config/opencode/skills/`. Keep the pre-existing Claude plugin, its managed cache, and the pinned checkout. No backup was created. Do not add or remove `using-superpowers` through this rollback. |
| `shadcn-ui` | The three observed `shadcn` and `migrate-radix-to-base` skill-link pairs under `~/.claude/skills/`, `~/.agents/skills/`, and `~/.config/opencode/skills/` had unknown provenance and were preserved; do not remove them as a CEOS rollback. The evidence records `npm uninstall -g shadcn` as the global CLI inverse if intentionally undoing the separately recorded global install. In a consuming project, restore its package files, `components.json`, CSS/config, and generated component source from that project's commit or backup. |

## Router and CEOS records

The router's local Python files and route data are separate from the seven upstream checkouts. Review their own diff before rolling them back; this integration owner did not modify `scripts/ceos-route.py` or `integrations/routes.json`.

For tracked CEOS paths, use a path-specific Git restore after reviewing the diff:

```sh
git diff -- scripts/verify.sh
git restore -- scripts/verify.sh
```

The manifest, lock, and integration docs are local records. Remove only the exact record files being rolled back; do not use `git clean -fd` or remove the whole `integrations/` or `docs/integrations/` directory. `scripts/integrations.py`, `scripts/integrations/generate_manifest.py`, and `tests/integrations.test.py` had uncommitted scaffolding before this integration work, so retain those files and revert only the integration-owner edits. The existing CI workflow already runs the manifest and integration tests; no workflow change was made for this integration owner.

## Known outside-CEOS state

The pre-existing gstack link `gstack-review` → `../qa/sections/exploratory.md` is outside CEOS and is recorded for awareness only. Do not change it as part of this rollback. Likewise, leave unknown-provenance shadcn skill links, the React Bits broken checkout, and the pmndrs validation directory untouched unless their separate owners request cleanup.
