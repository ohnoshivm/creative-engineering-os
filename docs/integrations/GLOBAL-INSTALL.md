# Global UI and WebGL integrations

Installed on 2026-10-21. The source of truth is the pinned local upstream checkout where it is available; the two shim skills live in CEOS. No provider settings or MCP servers were added.

## Sources and install method

| Capability | Pinned source | Global integration |
| --- | --- | --- |
| shadcn/ui | `~/creative-engineering-os-upstreams/shadcn-ui` at `ba1503c64472b82256d9de95e2e62c5901a38e8b` | Official `shadcn` and `migrate-radix-to-base` skills are symlinked. The global npm package `shadcn@4.22.1` is installed. |
| React Bits | `~/creative-engineering-os-upstreams/react-bits` at `e12c22192ac7b4b452c5e2feb9b586d74765d696` | Thin `react-bits` shim at `integrations/skills/react-bits/SKILL.md`. Pinned README documents the shadcn registry and jsrepo install forms; no jsrepo global install. |
| pmndrs/examples | `~/creative-engineering-os-upstreams/pmndrs-examples` at `9905cd7b3d030a0ba5c6d327e15fe30ab648abb6` | Thin `pmndrs-examples` shim at `integrations/skills/pmndrs-examples/SKILL.md`; it points agents to the 200-entry index at `integrations/indexes/pmndrs-examples.json`. |

The shadcn package review found `bin: ./dist/index.js`, Node `>=20.18.1`, and no `preinstall`, `install`, or `postinstall` scripts. It was installed with scripts disabled:

```sh
npm i -g shadcn@4.22.1 --ignore-scripts
```

The installed CLI reports `4.22.1`. The official shadcn skill requires the CLI and recommends the project's package runner (such as `npx shadcn@latest`, `pnpm dlx`, or `bunx`); the global pinned `shadcn` command is available when called directly.

## Skill discovery paths

These four skill directories exist exactly once in each root:

- `shadcn` and `migrate-radix-to-base` → pinned shadcn checkout
- `react-bits` and `pmndrs-examples` → this CEOS checkout under `integrations/skills/`

They are linked in `~/.agents/skills`, `~/.config/opencode/skills`, and `~/.claude/skills`. They are also linked in `~/.gemini/antigravity/skills` because CEOS already uses that convention. `agy` is unavailable, so Antigravity discovery and invocation are unverified. No pre-existing same-named entry was found; no backup was needed.

## React Bits use

The public pinned tree contains no `SKILL.md` and no standalone React Bits MCP server or CLI. Its official README documents these project-scoped installs:

```sh
npx shadcn@latest add @react-bits/<Component>-TS-TW
npx jsrepo@latest add https://reactbits.dev/r/<Component>-TS-TW
```

The valid variant suffixes are `JS-CSS`, `JS-TW`, `TS-CSS`, and `TS-TW`. The official registry alias is `@react-bits` → `https://reactbits.dev/r/{name}.json`; add it to a project's `components.json` when needed. Choose a component for a concrete React/Next/Vite-React interaction, inspect its source and dependencies, and check keyboard access, focus behavior, accessibility, and `prefers-reduced-motion` for that component. Do not use it for non-React work or just because the library exists.

The React Bits repo documents an opt-in integration through the shadcn MCP server. For example, add the registry alias above, then run `npx shadcn@latest mcp init --client claude` from the project. On this Mac the installed pinned CLI equivalent is `shadcn mcp init --client claude`. For Codex, `shadcn mcp init --client codex` prints the official TOML setup instructions. These commands were not run.

## pmndrs/examples use

Search the curated index first, then open only the matching example and files it directly needs. For example:

```sh
jq -r '.examples[] | select((.tags + .libraries | join(" ")) | test("shader|gltf|physics|controls"; "i")) | [.slug, .path, .title] | @tsv' integrations/indexes/pmndrs-examples.json
```

Copy one example into the project when useful and adapt it to the project's versions. Keep example dependencies project-scoped; never install them globally or edit the pinned checkout/index.

## Existing Claude plugin overlap

`claude plugin list` was run read-only. The known related skills are `vercel:shadcn`, `stitch-build:shadcn-ui`, and `ui-ux-pro-max:ui-styling`. Their plugin namespaces differ from the plain `shadcn` skill name, so no same-name skill entry is displaced. The list showed Vercel enabled but noted its packaged skills are not installed; Stitch Build is enabled at user and project scope; UI UX Pro Max is enabled at user scope. No plugin or setting was changed.

## Verification and limits

`shadcn --version` and `npm ls -g shadcn --depth=0` both report `4.22.1`. Both shim skills pass the skill validator and are under 80 lines. All symlinks resolve; each provider root has one entry per skill; the two official shadcn SKILL.md files' 21 relative Markdown links resolve. The pmndrs index parses and its documented jq search returns matches.

These global skill entries are symlinks, so moving or removing a source checkout breaks that entry until it is relinked.

React Bits reached the requested commit, but its supplied worktree was sparse and had no materialized source files. Local Git's lazy fetch failed with `No route to host`; the pinned commit, tree, README, install guide, and MCP guide were read through GitHub's read-only API. No checkout worktree files were written. The shadcn and React Bits MCP paths remain opt-in and were not enabled. Native skill discovery and invocation were not tested in Codex, OpenCode, or Claude; Antigravity runtime is also unverified.

Raw command/check logs are in `~/.local/state/creative-engineering-os/integration-v2-20261021/reports/global-install/`. Exact rollback commands are in [global-install.json](../../integrations/evidence/global-install.json).
