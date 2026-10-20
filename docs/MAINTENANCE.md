# Maintenance

Monthly, or before adopting a new tool, review first-party release notes, license changes, engine/peer compatibility and dependency advisories. Do not run a bulk global update or switch providers as a maintenance shortcut.

1. Commit a clean source baseline; privately back up only client files to be modified. Record package/tool versions and current test results.
2. Update one stack or tool at a time in a branch. Keep versions and lockfiles in sync. Inspect third-party package/repository source before executing new installation scripts.
3. Run `scripts/verify.sh`, script/security helper tests and the relevant template's production build, smoke and visual suites. Review actual diffs before baseline changes. Re-run responsive, reduced, noJS/noWebGL and console/axe checks.
4. For render/motion changes, repeat controlled measurements and inspect recordings. Use physical devices/browser engines before releases. Never upgrade a renderer solely for a fashionable API.
5. Reload each client and verify discovery/connectivity. Keep existing subscriptions, provider routing and auth files untouched. Compare parsed config excluding the intentionally owned addition. Never dump full config/log/environment/auth data into a report.
6. Refresh resource dates and original summaries; remove dead links, distinguish JS shells from inspected experiences. Review optional-tool decisions when a real project warrants them.
7. Archive reports with date, commit and environment. Record regressions and a tested rollback. Restrict access to backups and diagnostic captures; consider their retention deliberately.

Current exceptions to revisit: Antigravity Google account verification before runtime checks, default OpenCode database migration (host-supported repair only), gstack install broken link, KTX encoder availability, broader Safari/physical-device verification. The earlier session reported a credential-output incident; user-controlled credential revocation remains outside this install. Never repeat the value in documentation.
