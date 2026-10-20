# Rollback guide

The setup is additive. Do not overwrite whole client config files from a backup if subsequent user changes exist. Backups under `backups/2026-10-20-mcp` and `backups/2026-10-20-resume` are mode700 directories with mode600 configuration copies; never publish them.

- **Skill links:** run `scripts/unlink-skills.sh`. It removes only ceos links whose literal target is inside this workspace; real directories and foreign links stay intact. Source skills remain here.
- **Claude MCP:** `claude mcp remove chrome-devtools --scope user` removes only this server. Secondary Claude account was not changed.
- **Codex MCP:** `codex mcp remove chrome-devtools` removes this server. The CLI serializes TOML and may omit explicit empty arrays on other entries; compare parsed settings against the private before snapshot. This setup restored node_repl's original explicit `args=[]` after native serialization omitted it.
- **OpenCode MCP:** remove only `mcp["chrome-devtools"]` from `~/.config/opencode/opencode.json`, preserving all providers, auth, tool policies and other servers.
- **Antigravity MCP:** remove only `mcpServers["chrome-devtools"]` from `~/.gemini/config/mcp_config.json`. It was empty before setup; do not restore an empty file if other entries have since been added.
- **Auditor:** remove `~/.claude/agents/creative-auditor.md` only if it is still the link into this repo. Remove OpenCode's `creative-auditor.md` only after comparing it to this repo's owned adapter; preserve later user edits. Existing eight agents were not changed.
- **Blender:** installed during the earlier setup via Homebrew cask. If no longer needed, use Homebrew's supported cask uninstall after preserving user assets/preferences; no automatic removal is performed.
- **Local dependencies/artifacts:** project-local node_modules/dist/reports are disposable after retaining wanted evidence. Lockfiles/source remain. On-demand npx packages live in npm's ordinary cache, not global package installs. Do not clear global caches merely to remove this system.
- **Demo/new projects:** isolated directories; no existing client project was migrated. Archive the created directory or remove it only on user instruction.
- **Whole workspace:** first unlink owned integrations and remove owned MCP entries. Archive the repo privately. Backups may contain account data and must never enter public storage.

Known pre-existing items (Token Harbor config, OpenCode database mismatch, gstack broken section link) were neither reactivated nor repaired. Rollback does not touch them.
