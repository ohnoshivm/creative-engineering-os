# shadcn/ui

## Scope and source

This integration uses shadcn as a project-local source generator: the CLI copies editable component code into a React project. It does not add a shared CEOS component runtime. Use it when a user asks for a React interface component that should live in and follow that project's design system.

The official [`shadcn-ui/ui`](https://github.com/shadcn-ui/ui) checkout is pinned at [`ba1503c64472b82256d9de95e2e62c5901a38e8b`](https://github.com/shadcn-ui/ui/tree/ba1503c64472b82256d9de95e2e62c5901a38e8b). GitHub identifies the repository as MIT licensed; the pinned checkout contains `LICENSE.md`, and its `shadcn@4.22.1` package is also MIT licensed and requires Node `>=20.18.1`. The project-local CLI is provider agnostic; only npm usage was exercised here. The upstream Agent Skill is already linked into several local skill roots; see the registration audit below. Those links existed when this work resumed; their provenance is unknown, and they were left untouched. No MCP server was registered during this continuation.

## Verified fixture

The reproducible fixture is outside the CEOS repository at `~/creative-engineering-os-upstreams/shadcn-ui-fixture`. It uses React 19.3.1, Vite 8.3.5, Tailwind CSS 4.3.3, TypeScript 7.0.2, and the pinned CLI. Its `components.json` selects the `new-york` style with neutral base tokens, project-owned aliases and CSS, and Tailwind v4; the CLI fetched the `new-york-v4` registry source. It does not initialize or edit a CEOS template.

The fixture pins package versions and keeps a lockfile. Its `.npmrc` enables exact saves and disables lifecycle scripts. Runtime dependencies include React, `radix-ui`, `cn`, `class-variance-authority`, and `lucide-react`; the local CLI and axe-core are development dependencies. The lockfile records MIT, Apache-2.0, ISC, and MPL-2.0 licenses for the direct packages; the CLI itself is MIT. See the [evidence record](../../integrations/evidence/shadcn-ui.json) for exact versions and lockfile hash.

## Install and use

Keep the CLI local to the consuming project. First configure the project's CSS entry, aliases, Tailwind setup, and `components.json` to match its own tokens. Review those files before running a setup command that might initialize or replace them.

```sh
npm install --save-exact class-variance-authority@0.7.1 lucide-react@1.61.0
npm install --save-dev --save-exact shadcn@4.22.1
./node_modules/.bin/shadcn add button dialog --dry-run --view
./node_modules/.bin/shadcn add button dialog --yes
```

Review generated files and dependencies before applying them. The recorded run used `./node_modules/.bin/shadcn add button dialog --dry-run --view`, then `./node_modules/.bin/shadcn add button dialog --yes`. Button was included because Dialog's optional footer composition imports it. The dry run previewed both files without writing them; applying the request created both files and added `cn@0.5.0` and `radix-ui@1.8.1`. The exact registry URLs were `https://ui.shadcn.com/r/styles/new-york-v4/button.json` and `https://ui.shadcn.com/r/styles/new-york-v4/dialog.json`; each fetched item matched the pinned source at verification time. The CLI rewrote Dialog's internal Button import for the fixture alias and omitted the client directive because `rsc` is false. At this pinned registry revision, generated imports also use `class-variance-authority` and `lucide-react` while registry package metadata declares only `cn` and `radix-ui`; the fixture explicitly pinned the first two packages before adding components. Inspect imports as well as registry metadata.

## Existing skill and registration audit

The initial audit classified shadcn/ui as `REFERENCE_ONLY` because it had no pinned checkout or operational component test at that point. The current local audit found the upstream `skills/shadcn` directory symlinked into `~/.claude/skills/shadcn`, `~/.agents/skills/shadcn`, and `~/.config/opencode/skills/shadcn`. All three resolve to the single pinned checkout and the same `SKILL.md` hash; their symlink timestamps are later than the initial audit, but their provenance is unknown. No direct `~/.codex/skills/shadcn` entry was found. Runtime discovery of these links was not separately exercised.

No shadcn MCP registration was found in those skill roots. The upstream skill contains MCP documentation, which is not itself a server registration; provider configuration was not read or changed. Other local skills mention shadcn for narrower work such as design-token analysis, complex artifact guidance, or Radix-to-Base UI migration. They are contextual references, not duplicate general shadcn registrations. The upstream skill recommends `npx shadcn@latest`; this guide's reproducible path uses the project's pinned local `shadcn@4.22.1` binary to preserve the consuming project's lockfile and version choice.

## Update and security

Components are source files owned by the consuming project, so review updates against local edits. Pin the CLI and lockfile, inspect a specific update with `--dry-run --diff --view`, then apply only after review. Back up or commit local component changes before any overwrite.

The CLI can write component source and project configuration, add dependencies, and invoke the detected package manager. Registry files are executable source; use the official registry or review another registry before use. The upstream root and CLI package manifests have no `preinstall`, `install`, `postinstall`, or `prepare` hooks, and the checkout has no tracked `.husky` hooks. The fixture's `.npmrc` sets `ignore-scripts=true` and `save-exact=true`; do not assume another project's package scripts are disabled. The CLI package also contains an `mcp:inspect` helper, but this task did not run it or create an MCP registration.

The full fixture dependency audit found seven high-severity issues in the development CLI dependency graph, including the `braces` stack-exhaustion advisory. The production dependency audit found zero vulnerabilities. npm's suggested forced fix would replace `shadcn@4.22.1` with breaking `shadcn@1.0.0`; it was not applied. Recheck audit status before adopting or updating the CLI.

## Verification and limits

The fixture completed `npm ci` and its production build. Playwright CLI used the named `shadcn-ui` session against the production preview: the Dialog opened with focus inside, Tab remained inside, Escape closed it, and focus returned to the trigger. Desktop, tablet, and mobile screenshots were inspected. The production browser console had zero errors and warnings. axe-core reported zero violations with the Dialog closed and open; the open scan marked `aria-hidden-focus` incomplete for the hidden app root and Radix focus guards. Screen-reader testing was not performed. The session was closed and no fixture preview server remains listening on port 4174.

The prior local audit recorded no global shadcn CLI. A later read-only check found `/opt/homebrew/bin/shadcn` at version 4.22.1 with a binary modification time after that audit. This task did not install, invoke, or alter the global binary; fixture commands used `./node_modules/.bin/shadcn`. Its attribution is unknown. No provider settings or CEOS templates changed.

## Rollback

Remove the external fixture directory to undo the fixture. In a consuming project, restore its manifest, lockfile, config/CSS if changed, and generated files from the prior commit or a private backup. Remove only this guide and its evidence JSON to remove the CEOS integration record. Retain the upstream checkout while the observed skill symlinks point into it; removing the checkout would break those existing links. The fixture and CEOS record paths were new, so no backup was needed for those additions.
