# Installation inventory

Exact machine-readable versions, installed paths and pinned project dependencies: [INVENTORY.json](INVENTORY.json). Verified 20 October 2026.

| Tool | Version | Location |
|---|---|---|
| node | v26.11.1 | `/opt/homebrew/bin/node` |
| npm | 11.20.0 | `/opt/homebrew/bin/npm` |
| bun | 1.4.3 | `/opt/homebrew/bin/bun` |
| git | git version 2.50.1 (Apple Git-155) | `/usr/bin/git` |
| gh | gh version 2.96.0 (2026-07-02) | `/opt/homebrew/bin/gh` |
| uv | uv 0.12.1 (Homebrew 2026-07-31 aarch64-apple-darwin) | `/opt/homebrew/bin/uv` |
| playwright-cli | 0.1.22 | `/opt/homebrew/bin/playwright-cli` |
| lighthouse | 13.5.0 | `/opt/homebrew/bin/lighthouse` |
| blender | Blender 5.2.2 LTS | `/opt/homebrew/bin/blender` |
| claude | 2.1.304 (Claude Code) | `/Users/hustle/.local/bin/claude` |
| codex | codex-cli 0.163.0 | `/opt/homebrew/bin/codex` |
| opencode | 1.19.3 | `/Users/hustle/.opencode/bin/opencode` |

## Pinned template/tool packages

| Package | Version | License in installed metadata | Scope |
|---|---|---|---|
| playwright | 1.64.1 | Apache-2.0 | Project/template/tooling only |
| @axe-core/playwright | 4.14.0 | MPL-2.0 | Project/template/tooling only |
| astro | 7.4.1 | MIT | Project/template/tooling only |
| gsap | 3.15.0 | Standard 'no charge' license: https://gsap.com/standard-license. | Project/template/tooling only |
| @playwright/test | 1.64.1 | Apache-2.0 | Project/template/tooling only |
| typescript | 5.9.3 | Apache-2.0 | Project/template/tooling only |
| three | 0.186.1 | MIT | Project/template/tooling only |
| @types/three | 0.186.0 | MIT | Project/template/tooling only |
| vite | 8.3.4 | MIT | Project/template/tooling only |
| lenis | 1.3.27 | MIT | Project/template/tooling only |

## Additions and evaluated tools

- Blender 5.2.2LTS installed by prior setup phase via Homebrew cask; version and disposable GLB export tested. Existing Node/npm/bun/Chrome/CLIs preserved.
- Chrome DevTools MCP 1.11.0 (Apache-2.0, https://github.com/ChromeDevTools/chrome-devtools-mcp) pinned and run on demand through npx. Four client adapters, independent stdio diagnostic smoke, Claude/OpenCode connection checks.
- glTF-Transform CLI 4.5.1 (MIT, https://gltf-transform.dev/) run on demand. Disposable Blender GLB inspect/meshopt-optimize/reinspect passed. Tiny cube1948bytes vs1936before: this verifies encoding, not a size-improvement claim.
- meshoptimizer extension exercised through glTF-Transform; no separate global meshoptimizer CLI needed.
- @lhci/cli0.15.1 configured in applicable template scripts; Lighthouse 13.5.0 itself used for measured browser audits. CI-host autorun/remote upload not configured or verified.
- axe integration runs project-local in Playwright. Separate global axe CLI not needed.
- KTX/toktx encoder NOT INSTALLED; previous phase found installer requires admin. No sudo used. Compression/transcoder workflow documented, physical texture-pipeline verification remains pending.
- Spector.js, R3F, OGL, Motion, Tempus, Theatre, Rive, WebGPU/TSL, canvas-sketch/OGPU: evaluated, optional recipes; see [OPTIONAL-TOOLING.md](OPTIONAL-TOOLING.md). No speculative global installs.
- No new model-provider API billing, account routing, Token Harbor activation, browser extension, paid service or extra browser MCP.

For installed dependency metadata, lockfiles are the repeatable source. Audit results are point-in-time and do not cover global/npm-cache dependencies or all transitive on-demand CLI packages. Registry printed a deprecation notice from a transitive glob dependency in glTF-Transform; no global package upgrade or audit-fix was attempted.
