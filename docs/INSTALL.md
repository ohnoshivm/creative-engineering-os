# Install and restore

## Prerequisites

Tested on macOS/Apple Silicon with Python3.14, Node26 and Google Chrome. The portable setup uses Python3.11+ (stdlib TOML), Node22.22.0+ (the strictest pinned starter engine), npm, Git, zsh and rsync. Other macOS versions/Linux need their own browser/tool checks; Windows requires a compatible Unix environment and is not certified here.

Install missing prerequisites through their official supported installers. If Homebrew is already installed, inspect Brewfile and run `brew bundle --file Brewfile` when you want its listed packages/apps. This is optional and may install global software. The setup script never installs Homebrew, uses sudo, resets a config or signs into an account.

Clone the GitHub repo into `~/creative-engineering-os`, or extract a versioned release there. Run `python3 scripts/ceos.py doctor`. Inspect scripts before applying them.

## Multi-client setup

```sh
python3 scripts/ceos.py install --client all --mcp
python3 scripts/ceos.py install --client all --mcp --apply
python3 scripts/ceos.py dependencies --apply
```

Default is a read-only plan. With --apply the installer adds missing owned skill links, auditor adapters and optionally only chrome-devtools. It preserves existing target paths/entries. It refuses symlinked MCP config files and stops on invalid config instead of overwriting it. Backups of configs it changes go under `~/.local/state/creative-engineering-os/backups` with restrictive permissions. It does not export or display their contents. Setup is additive, not a transaction across every client; if a later client fails, earlier owned additions remain and can be removed deliberately.

The dependencies action runs npm ci separately in tooling, four templates and the demo. Exact transitive trees are locked. npm may run publisher install scripts; review dependencies as you would any development project. No global npm install occurs. Chromium is not downloaded by default: browser tests use installed Google Chrome. For recordings, install only Playwright's helper from tooling: `npx playwright install ffmpeg`.

Restart your agent client. Test with the studio-workflow skill. `scripts/verify.sh` checks source contracts; `python3 tests/verify-structure.py --installed` additionally verifies the39 core links when all clients use this checkout.

## Plugin alternative

Use docs/PLUGINS.md for Claude Code. Choose either plugin discovery or manual Claude links. Installing both can duplicate skills/server tools. Codex/OpenCode/Antigravity need their client-specific setup; installing a Claude plugin does not configure them.

## Restore the wider ecosystem

`manifests/ecosystem-skills.json`, `ecosystem-plugins.json`, `ecosystem-mcp.json` and `tools.json` describe the discovered setup without credentials. The13 original studio skills are already included. For upstream skills/plugins, use the verified source, revision and publisher's installer where recorded; inspect licenses and source before executing. A name/hash alone is not a downloadable or trusted dependency. Unknown provenance requires the original source or separate private personal backup; this public package cannot reproduce it byte-for-byte.

Only Chrome DevTools has an automatic, credential-free MCP adapter. ChatCut/app-provided node_repl need their host app; rea/gsc/custom Shopify definitions need their original local implementation; Stitch/DataForSEO/Analytics/Whop need supported vendor setup and the user's own auth. No dummy token or copied account config is installed.

## Roll back

- Run scripts/unlink-skills.sh to remove only core skill links pointing into this checkout. It leaves third-party/real directories untouched. OpenCode shares the ~/.agents/skills discovery directory with Codex.
- Remove the Claude auditor link and OpenCode adapter link only after checking their targets still point into this checkout.
- Remove only the added chrome-devtools server, using `claude mcp remove chrome-devtools --scope user`, `codex mcp remove chrome-devtools`, or the matching single JSON entry for OpenCode/Antigravity. Preserve any later user edits; do not blindly restore an entire before-copy.
- For plugin installation, use Claude's supported plugin uninstall. No accounts or subscriptions need migration.
- Dependency folders/build artifacts can be discarded within the created checkout after preserving wanted evidence. Do not clear unrelated global caches.
