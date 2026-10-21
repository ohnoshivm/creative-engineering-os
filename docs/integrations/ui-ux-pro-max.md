# UI/UX Pro Max

## Scope and source

UI/UX Pro Max is a design-system and implementation knowledge base. Use it for UI research, visual direction, responsive patterns, accessibility, UX, and stack-specific guidance. It complements CEOS creative direction; it does not choose the project's concept or replace the approved direction.

The repository [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) is pinned at [`56ea9cf174ed86786187daa9de0e6247cb0747e4`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/56ea9cf174ed86786187daa9de0e6247cb0747e4), MIT on current `main`. The upstream checkout is `~/creative-engineering-os-upstreams/ui-ux-pro-max`. The v2.15.0 release tag has conflicting license metadata: its CLI README says CC-BY-NC-4.0 while its package metadata says MIT. Current `main` and repository metadata say MIT; confirm licensing before redistributing files specifically from that release tag.

## Existing registration and use

The existing OpenCode skill tree at `~/.config/opencode/skills/ui-ux-pro-max` was retained and compared with the pinned upstream. `~/.agents/skills/ui-ux-pro-max` is a symlink to that tree, so it serves Codex and other `.agents`-compatible clients. The existing Claude Marketplace plugin remains in place; no separate manual Claude skill or global CLI was added. The optional `ui-ux-pro-max-cli@2.5.0` was not installed.

Use the local Python search script through the registered skill or directly when a focused data lookup is useful:

```sh
python3 ~/.config/opencode/skills/ui-ux-pro-max/scripts/search.py \
  'healthcare patient portal appointment accessible' --design-system --json \
  --project-name 'Project name'
python3 ~/.config/opencode/skills/ui-ux-pro-max/scripts/search.py \
  'error summary keyboard focus' --domain ux --json
python3 ~/.config/opencode/skills/ui-ux-pro-max/scripts/search.py \
  'server component suspense streaming' --stack nextjs --json
```

The Python search uses the standard library and local CSV/JSON design data; it does not need the optional Node CLI. The CLI's `init` and `update` flows can contact GitHub and npm and write skill files, so they are outside this integration's normal read-only lookup path.

## Verification

The pinned OpenCode skill tree matched current upstream: all 39 data files and all 31 script/support files matched. `SKILL.md` and the two reference documents matched after the documented upstream Claude-plugin-root to OpenCode path substitution. `node cli/scripts/sync-assets.mjs --check` reported that assets are in sync.

The upstream Python suite ran 164 tests in 5.253 seconds and returned `OK`. The semantic data validator accepted 12 domain files, 22 stack files, and `ui-reasoning.csv`; all 22 registered stack smoke probes returned at least one result. The installed OpenCode-path design-system query returned valid JSON with the required project, category, pattern, style, colors, typography, key-effects, and anti-pattern fields; persistence was `null`, and no files were written. The UX and Next.js stack probes each returned three results. Exact commands and results are in [the evidence record](../../integrations/evidence/ui-ux-pro-max.json).

The existing Claude plugin cache is in a directory labelled 2.13.0. Its runtime skill, 39 data files, and 30 of 31 script/support files match current `main`; only a test fixture differs. These checks exercised local scripts and files, not a fresh Claude or OpenCode model invocation. Runtime discovery after an update remains unverified.

## Update and rollback

For an update, review a pinned upstream commit and license, privately back up the complete OpenCode tree before replacing any files, compare the tree, then copy only reviewed changes. The `.agents` link follows the OpenCode tree. If Claude metadata needs a version refresh, use its existing plugin manager; do not add a second manual Claude skill. Rerun the upstream tests, data validator, stack probes, installed retrieval probes, and the local skill-tree integrity check.

No active skill tree changed in this integration, so no backup was created. For a future OpenCode tree replacement, restore the private backup to `~/.config/opencode/skills/ui-ux-pro-max`; the `.agents` symlink will follow it. Roll back Claude through its plugin manager. Do not remove the upstream checkout while either existing registration uses it.
