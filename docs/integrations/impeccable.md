# Impeccable integration

**Status:** The native skill copies are updated to 4.7.0. The standalone detector runs with engine 0.1.16, but its published binary does not include the pinned source's linked stylesheet ignore fix.

## Source and formats

- Official repository: [pbakaus/impeccable](https://github.com/pbakaus/impeccable), pinned at [`dad8dbb3aac21ad1fa236c110315ef4abece23e8`](https://github.com/pbakaus/impeccable/commit/dad8dbb3aac21ad1fa236c110315ef4abece23e8), Impeccable 4.7.0, Apache-2.0.
- The clean upstream checkout is at `~/creative-engineering-os-upstreams/impeccable`.
- The pinned source provides native skill trees and a Claude plugin. This machine uses `~/.agents/skills/impeccable` for Codex and the shared Claude skill symlink, plus `~/.config/opencode/skills/impeccable` for OpenCode. The official Claude plugin is 4.7.0 and is not installed; no plugin-plus-manual duplicate was found.
- The vendored [reference skill](../../library/skills/impeccable/SKILL.md) remains unchanged and on demand.

The skill triggers for requests to design, redesign, critique, audit, polish, simplify, harden, animate, or otherwise improve web and native interfaces. Its scope includes websites, dashboards, forms, settings, onboarding, empty states, and iOS/Android UI. The deterministic engine scans HTML/HTM, CSS-family, JS/TS-family, Astro, Vue, and Svelte source; the HTML engine can be opted into for template files. URL scans need an installed compatible browser.

## Native commands and analysis boundary

Provider workflows include `shape`, `init`, `document`, `extract`, `critique`, `audit`, `polish`, `bolder`, `quieter`, `distill`, `harden`, `onboard`, `animate`, `colorize`, `typeset`, `layout`, `delight`, `overdrive`, `clarify`, `adapt`, `optimize`, `live`, and `generate`, plus `doctor`, `hooks`, and `pin/unpin`. `craft` is a deprecated alias.

Use the native skill surface (`$impeccable <command>` in Codex; `/impeccable <command>` in Claude Code/OpenCode). The launcher is at `<skill-base-dir>/scripts/impeccable`:

```sh
<skill-base-dir>/scripts/impeccable context
<skill-base-dir>/scripts/impeccable detect src/page.html --json
<skill-base-dir>/scripts/impeccable detect https://example.com --json
<skill-base-dir>/scripts/impeccable detect --cdp 9222 --target <page-match> --json
```

`detect` is deterministic. `critique`, `audit`, and the other skill workflows are prompts for the provider model; they are not deterministic standalone programs. A clean detector result is not visual QA or a complete accessibility review.

## Version audit and update

| Install | Before | After | Discovery state |
|---|---:|---:|---|
| Codex `~/.agents/skills/impeccable` | 4.6.0 / engine 0.1.15 | 4.7.0 / engine 0.1.16 | Present in the current injected skill catalog before the update; fresh post-update reload not verified |
| Claude `~/.claude/skills/impeccable` | 4.6.0 | shared symlink to 4.7.0 tree | On-disk link verified; no fresh Claude invocation |
| OpenCode `~/.config/opencode/skills/impeccable` | 4.6.0 / engine 0.1.15 | 4.7.0 / engine 0.1.16 | Native files and front matter verified on disk; runtime discovery not invoked |
| Claude plugin | none found | not installed | Avoids a second registration beside the shared skill |

The active `.agents` and OpenCode trees now match their pinned upstream provider trees. The provider-specific skill metadata was preserved. The update backed up 14 files before changing them; no provider settings, auth, subscriptions, T3 settings, or MCP registrations changed.

The upstream launcher uses a self-contained platform binary and verifies a `.sha256` sidecar before caching a new binary. Its source build is separate and needs Node >=18.19.0, Bun 1.3.13, and Rust/Cargo. The official `npx impeccable install/update` installer was inspected but not run; a manual native-tree update avoided broader provider hook/config changes. No global binary cache was installed during verification.

**Rollback:** restore the 7 files under `agents/` in `~/.local/state/creative-engineering-os/integration-v2-20261021/backups/impeccable-v4.7-cze_q06l` to `~/.agents/skills/impeccable/`, and the 7 files under `opencode/` to `~/.config/opencode/skills/impeccable/`. The Claude symlink follows the restored `.agents` tree. The backup manifest is `.../manifest.json`.

## Operational verification and limitation

The official `engine-v0.1.16` Darwin arm64 asset (17,192,672 bytes) matched its published SHA-256 (`5c00c3130b961f3aa1066f04ed0e1f58e87808ad153efa00f1c44184800084f2`). The updated launcher checksum path passed using that asset from a temporary `file://` base; `engine-probe` returned `impeccable-engine 0.1.16`.

A temporary page linked `src/vendor/lib.css`, with `detector.ignoreFiles: ["src/vendor/**"]`. `detect --no-config --json src/page.html` returned `low-contrast` and `gradient-text` (exit 2). With config enabled, both still appeared (exit 2), although a direct scan of the ignored CSS file returned `[]` (exit 0). This does not satisfy the pinned source regression test's expected behavior. The test is present at `crates/html/tests/ignored_linked_stylesheet.rs`, but could not be run because Cargo is unavailable.

The pinned fix commit is dated 2026-10-20; the published `engine-v0.1.16` release is dated 2026-10-19. That ordering and the detector result indicate the published binary predates the fix. The source fix is therefore not operationally verified in the released engine. Raw detector output and download/checksum logs are under `~/.local/state/creative-engineering-os/integration-v2-20261021/reports/impeccable/`.
