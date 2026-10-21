# GSAP Skills

## Source and installation

Use the official GreenSock Agent Skills from [greensock/gsap-skills](https://github.com/greensock/gsap-skills), pinned at commit [aed9cfd3277740755f6bfc1155c7aa645403b760](https://github.com/greensock/gsap-skills/tree/aed9cfd3277740755f6bfc1155c7aa645403b760). The repository reports MIT licensing; its LICENSE file and GitHub metadata agree. The upstream skill tree has no semver release used here, so the commit is the version identifier.

All eight official skills were already installed under the local OpenCode skills directory, with matching links under the Agent Skills directory. Their SKILL.md files and the eight vendored CEOS reference copies match the pinned commit byte for byte. No reinstall, update, plugin, runtime package, or dependency was needed. The skills contain guidance only; they do not install GSAP into a project.

Upstream documents both the skills CLI and manual provider-directory installation. The CLI installer was not run. For a future update, review a specific upstream commit and license first, back up any destination files privately, then copy only the needed skill directories into the provider’s native skill directory. Do not add a native plugin and manual copies of the same skills together.

Upstream names the skills CLI as supporting 40+ agents and documents manual directories for Claude Code, Cursor, OpenCode, Codex, Antigravity, and Pi. On this machine the Codex/T3 session catalog exposed all eight skills. The OpenCode files and paths exist, but its installed CLI has no read-only skill discovery command, so OpenCode runtime discovery remains unverified.

## Skill routing

| Skill | Use for |
| --- | --- |
| gsap-core | Tweens, easing, stagger, responsive animation, and reduced motion |
| gsap-timeline | Sequencing and timeline position parameters |
| gsap-scrolltrigger | Scroll-linked motion, pinning, scrubbing, refresh, and cleanup |
| gsap-plugins | Plugin registration and GSAP plugin APIs |
| gsap-utils | GSAP utility methods |
| gsap-react | React and Next.js lifecycle, useGSAP, scoping, and cleanup |
| gsap-frameworks | Vue, Svelte, and other framework lifecycle and cleanup |
| gsap-performance | Transform use, batching, and animation performance |

## Authority, motion, and access

The approved project direction and CEOS motion/accessibility principles decide whether an animation belongs and how it should feel. For GSAP API behavior, lifecycle, plugin support, and version-specific details, use these official skills and current GSAP documentation ahead of generic design guidance or older GSAP examples.

The pinned core skill documents gsap.matchMedia() for responsive variants and the prefers-reduced-motion media query. Its reduced-motion example uses minimal or skipped animation and can be reverted with mm.revert(). React and framework skills require scoped cleanup through useGSAP or a context with ctx.revert(); ScrollTrigger guidance covers cleanup and refresh after content changes. Keep page content useful when animation is absent.

The integration adds no motion runtime and cannot prove an animation works in a browser. A project using GSAP still needs its own production preview, reduced-motion, keyboard, responsive, console, and performance checks.

## Duplicate handling

The separate generic skill at ~/.agents/skills/gsap had broad triggers that competed with the official skills. It remains installed with all its teaching content and demo assets. Its activation description and use scope now limit it to explicit requests about its own bundled demo or reference assets; general GSAP API and implementation work routes to the official gsap-* skills. The original file has a private before-backup recorded in [the evidence file](../../integrations/evidence/gsap-skills.json).

Vendored copies under library/skills/gsap-* remain intact as reference material. The unrelated gsap entry in library/UPSTREAM.md remains a catalog reference and is not an active install.

## Update and rollback

For updates, pin and review an upstream commit, compare its license and skill content, then back up only files that will change before copying. Record the revision, destination paths, and changed behavior in the evidence file.

To roll back the local duplicate-scope adjustment, restore the private backup to ~/.agents/skills/gsap/SKILL.md. The official skill files and provider links were not changed. To remove this repository record, revert only this guide and integrations/evidence/gsap-skills.json; do not reset unrelated working-tree changes.
