# Controlled upstream update procedure

Update one repository per change. Do not bulk-update all seven upstreams. `scripts/integrations.py verify` and `status` are read-only and never fetch; use the explicit `--installed` check when you want local checkout and registered-skill integrity checked.

1. Select one ID from [`manifest.json`](../../integrations/manifest.json) and [`UPSTREAM-LOCK.json`](../../integrations/UPSTREAM-LOCK.json). Review the official release page or repository history for a newer commit; compare the exact candidate against the locked full SHA. Do not move the lock just because `main` advanced.
2. Read the release notes and the full relevant diff. Check for API or format breaks, license changes, new packages, install lifecycle scripts, executable hooks, provider integrations, network behavior, and writes or deletes. For components, inspect selected registry payloads and transitive dependencies.
3. Review the candidate in an isolated worktree or disposable checkout. Do not replace active skill trees or change provider registrations during this review. Keep the prior pinned checkout available for rollback.
4. Run the operational check that matches the integration, then compare the result with its evidence record. Rebuild and capture screenshots when the change affects rendered behavior. Inspect the screenshots; record viewport, interaction, console, accessibility, and reduced-motion results where relevant.
5. If the update is accepted, update that integration's evidence and guide, its `UPSTREAM-LOCK.json` revision and skill hashes, then regenerate `manifest.json` with `python3 scripts/integrations/generate_manifest.py`. Review the exact diff. Never make `verify` rewrite records.
6. Run `python3 -I tests/integrations.test.py`, `python3 -I tests/integrations-routing.test.py`, `python3 -I tests/integrations-manifest.test.py`, and the repository checks from [`verify.yml`](../../.github/workflows/verify.yml). Run `python3 -I scripts/integrations.py verify --installed` after replacing the pinned checkout or any registered tree.
7. Record changed paths, test output, limitations, and rollback steps. Keep client config and runtime package updates separate from skill/reference updates; they need their own review and authorization.

## Operational checks by integration

| ID | Re-run after an update |
|---|---|
| `impeccable` | Compare native skill trees, verify the launcher checksum, then repeat the linked-stylesheet detector fixture. Run the pinned Cargo regression test when the required toolchain is available; its previous run was unavailable. |
| `ui-ux-pro-max` | Run the upstream Python test suite, `validate_data.py`, `smoke-stacks.sh`, and the installed design-system, UX, and stack retrieval probes. Check the active OpenCode tree and use the existing Claude plugin manager only if its version is intentionally updated. |
| `react-bits` | Regenerate the compact index, compare the selected component against the exact registry payload hash, run the isolated production build, then repeat reduced-motion, keyboard, cleanup, responsive, console, axe, and screenshot checks. |
| `pmndrs-examples` | Run `python3 tests/integrations/pmndrs_examples_index_test.py`; regenerate the index from the exact pin; build and inspect a selected production example. Do not infer all-example runtime support from one fixture. |
| `gsap-skills` | Compare all eight skill hashes and registered links. When a consuming page is available, exercise its production animation, reduced-motion, responsive, cleanup, console, and performance checks. |
| `superpowers` | Verify only the TDD and verification links against the pinned source and rerun the small RED/GREEN example. Keep `using-superpowers` and its startup hook out of the integration while gstack owns engineering orchestration. |
| `shadcn-ui` | Pin the project-local CLI; inspect component output with `--dry-run --view` or `--dry-run --diff`; review imports and dependencies; then rebuild, exercise production keyboard/focus behavior, inspect responsive screenshots, and rerun axe. |

If an operational check cannot run, record it as not verified. A successful source comparison does not establish runtime discovery or rendered behavior.
