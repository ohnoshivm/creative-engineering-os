# Superpowers integration

**Upstream:** [`obra/superpowers`](https://github.com/obra/superpowers), MIT, pinned for this integration to `b739a8af570e10a95898f2bdf6cec97467fa6c12` (version 7.0.0). The local review checkout is `~/creative-engineering-os-upstreams/superpowers` and was clean at that revision.

## CEOS use

The existing global policy gives gstack engineering-stage orchestration and gives CEOS creative direction, design, motion, and creative QA ownership. Superpowers supplies only two narrow methods here: test-driven development and verification before completion. `systematic-debugging`, planning, parallel-agent, review, and branch-finishing skills are not part of this install. Do not load `using-superpowers` as a second startup router.

The two selected skills are native Markdown `SKILL.md` files with YAML frontmatter. The Codex and OpenCode links point at the pinned checkout. They have no runtime library dependencies. TDD applies before feature or bug-fix implementation; verification applies before completion claims. No planning or debugging workflow is added, so gstack remains the engineering orchestrator.

Upstream `AGENTS.md` says a full Superpowers integration requires the `using-superpowers` bootstrap at session start and treats manual skill copies without bootstrap as incomplete. This integration deliberately omits that bootstrap to avoid a second orchestrator. The new registrations therefore verify native skill discovery only; they do not claim upstream's automatic skill triggering.

## Provider state

| Provider | Registration and result |
|---|---|
| Claude Code | Existing `superpowers@synced` plugin remains active at 6.4.2, matching official tag `v6.4.2` (commit `8ca22dba9a94f28898bbce59f2537ff4d87c747d`). It contains all 15 upstream skills and a SessionStart hook that injects `using-superpowers` on startup, clear, and compact. No direct personal skill copy was left behind, avoiding duplicate TDD/verification registrations. This existing broad hook cannot be narrowed without changing the provider plugin; it is a known limitation. A second synchronized cache copy exists at `~/.claude/plugins/synced/e8f7d314-c5d3-4449-9eb1-2db6c2deb1ee_70db48fd-6f33-488b-aa9b-363b884f48b5/6ba53849-2ee0-4cf0-957e-31c122ea1dd1`; Claude lists only the path above as loaded, and the extra copy is retained as an inactive app-managed cache. |
| Codex | Added two skill-directory links under `~/.agents/skills`: TDD and verification. The official Codex marketplace lists Superpowers 6.4.2 as available but not installed; there is no plugin-plus-manual duplicate. The Codex plugin manifest has no hooks, but the full plugin is intentionally not installed. |
| OpenCode 2.1.2 | Added the same two native personal skill links under `~/.config/opencode/skills`. The standard user plugin directory was absent. The CLI first reported no plugins, then failed with `Database is not empty and has no session table`; treat plugin inventory as unverified. No plugin was added. The upstream OpenCode plugin registers all skills and injects the `using-superpowers` bootstrap, which would compete with gstack routing. |
| Antigravity | Not installed. Upstream documents `agy plugin install https://github.com/obra/superpowers`, but `agy` is unavailable here and the existing environment record says Antigravity execution is blocked at Google's account verification. No account or provider setting was changed. |

The new links expose only `test-driven-development` and `verification-before-completion`; they do not include `using-superpowers`, `systematic-debugging`, planning, parallel-agent, code-review, or branch-finishing skills. Existing Superpowers entries under `library/skills/` stay intact as on-demand references. Fourteen of those 15 vendored skill files match upstream HEAD by SHA-256; `diagnosing-superpowers` differs. The library has no recorded source revision, so that file is not represented as current.

The installed gstack version is 1.91.121.0 at local commit `d258bcffb0cb7bda5f133f3e957f932d816d282f`; it is active in Claude and OpenCode and has no exact same-name skill directories. Its repo already contains uncommitted changes and was left untouched. `gstack setup --status` reports all 25 OpenCode links resolving and one of 43 Claude links broken: `gstack-review/SKILL.md` refers to `../qa/sections/exploratory.md`. This is pre-existing and outside this integration.

## Install, update, rollback

The selected Codex and OpenCode registrations are symlinks from each provider's native skill directory to the exact pinned upstream checkout. No provider configuration, plugin list, startup instruction, or authentication state was edited. The active Claude plugin was preserved rather than duplicated or reinstalled.

To update, review a newer official commit and its provider hooks first, then repoint these links only after pinning a clean reviewed checkout. Do not reset or overwrite a dirty upstream checkout. The upstream all-in-one OpenCode plugin installs through V1 `plugin` or V2 `plugins` configuration; it registers every skill and injects bootstrap context. Claude uses the official marketplace `/plugin install superpowers@claude-plugins-official`; Antigravity uses the `agy` command above; Codex app and CLI use the official plugin marketplace. Those all-in-one routes were not used for the new registrations.

Rollback removes only the two new links from each of the Codex and OpenCode provider directories. No direct Claude skill links remain because its existing plugin already exposes both skills. The two CEOS artifacts can be removed independently. No backup was needed because the four destination skill paths and both CEOS artifact paths were absent before creation; no existing skill tree or provider configuration was changed. The pinned checkout, vendored library, Claude plugin, and gstack remain in place.

## Verification and limits

The official HEAD was rechecked with GitHub API and matched the local clean checkout. `claude plugin list` reports the existing plugin loaded; `codex plugin list` reports the marketplace plugin not installed. OpenCode plugin inventory is not conclusive because its CLI hit the local database error above. The two new links in each of Codex and OpenCode resolve to upstream directories, have matching frontmatter names, and match the pinned source hashes. A deterministic standard-library RED/GREEN check was run outside the repository; it demonstrates the test loop, not model invocation of the Superpowers skill.

These checks establish provider-native filesystem discovery, not fresh agent invocation. This T3/Codex session did not reload after the links were created; OpenCode's 2.1.2 CLI has no skill-list command and its plugin inventory hit the local database error, so no model-driven invocation was attempted. Claude's plugin is confirmed loaded but no individual skill invocation was run. Antigravity is not runtime-verified because `agy` is unavailable and account verification is blocked. Raw, secret-free logs are under `~/.local/state/creative-engineering-os/integration-v2-20261021/reports/superpowers/`.
