# React Bits

## Source and license

Use the official [DavidHDev/react-bits repository](https://github.com/DavidHDev/react-bits/tree/e12c22192ac7b4b452c5e2feb9b586d74765d696), pinned at commit e12c22192ac7b4b452c5e2feb9b586d74765d696 (2026-10-19, “add landing updates”). The upstream checkout remains at ~/creative-engineering-os-upstreams/react-bits outside the CEOS tree and outside automatic skill discovery.

The root [LICENSE.md](https://github.com/DavidHDev/react-bits/blob/e12c22192ac7b4b452c5e2feb9b586d74765d696/LICENSE.md) is **MIT + Commons Clause License Condition v1.0**; GitHub's SPDX field is null because this is a custom condition. It permits use, including commercial use, as part of an application, website, or product. It prohibits selling, sublicensing, or redistributing the components themselves alone, in a bundle, or as a port. No per-component license override file was found in the pinned checkout. React Bits Pro is a separate paid catalog and is not included in the free component index.

## Installation and catalog

The upstream README documents two source-install paths:

    npx shadcn@latest add @react-bits/SplitText-TS-TW
    npx jsrepo@latest add https://reactbits.dev/r/SplitText-TS-TW

The shadcn alias is configured in a consumer's components.json as @react-bits: https://reactbits.dev/r/{name}.json. This task exercised shadcn with a fixed CLI version; jsrepo was reviewed from the README but not run.

The ShinyText registry item declares empty npm and registry dependency arrays and has no install hook metadata. The upstream website package has no preinstall/install/postinstall/prepare lifecycle scripts; its predev and prebuild hooks run pro:summary, which were not executed. The large root dependency list is for the React Bits website, not required by this source-installed component.

The compact catalog is INTEGRATION-COMPONENT-INDEX.json (`~/creative-engineering-os-upstreams/react-bits/INTEGRATION-COMPONENT-INDEX.json`): 217 components across Text Animations, Animations, Components, Micro, and Backgrounds, with 868 JS/TS × CSS/Tailwind entries and each registry item's npm dependencies. The README count table totals 216 (Micro=34), while the pinned public/llms.txt itemized list and registry contain 217 (Micro=35); the index follows the itemized catalog.

## Recommended use

React Bits is an **external pinned implementation reference**, not a global runtime or CEOS skill installation. Use it only when the project already has React. Read each registry item's dependency list, accessibility behavior, cleanup, licensing, and source before installation. The upstream README documents shadcn MCP use with Claude Code, Cursor, Codex, VS Code, and Antigravity; these are upstream support claims, not fresh agent-runtime tests in this integration.

No provider, plugin, MCP, or host config was changed. The parent-owned CEOS route/manifest can register this as an optional React-only source reference; it should not be recommended for non-React projects.

## Verified component: ShinyText

The isolated React/Vite fixture at ~/creative-engineering-os-upstreams/react-bits-fixture was installed through the official CLI:

    npx --yes shadcn@4.22.1 add @react-bits/ShinyText-JS-CSS

The CLI reported two files and no npm dependencies. Its JSX output differed from the pinned registry payload in two expressions, including the transparent-color fallback; the fixture was restored from the exact pinned public/r/ShinyText-JS-CSS.json payload and SHA-256 checked. See restore-pinned-component.py (`~/creative-engineering-os-upstreams/.tests/react-bits/restore-pinned-component.py`). The direct unauthenticated GET to reactbits.dev/r/... returned HTTP 403, but the official CLI install succeeded and GitHub's current main commit and raw registry item matched the pinned source hashes.

Production build: npm run build passed with Vite 8.3.5 (17 modules). Output was 226.83 kB JavaScript (71.61 kB gzip) and 2.04 kB CSS (0.91 kB gzip). Vite reports that "use client" is not preserved; this does not affect this client-only Vite fixture. The earlier CountUp source and its motion@12.43.0 dependency were preserved from the interrupted work, but the ShinyText page does not import CountUp and its code is absent from the built bundle.

In the named Playwright CLI session react-bits, the production page rendered the semantic h1 text and the sweep updated styles in normal motion. With prefers-reduced-motion: reduce, the background stayed unchanged and no RAF remained after the initial settle. Keyboard Tab/Enter reached the native Headline shimmer button; removing ShinyText returned its text, zeroed the tracked RAF, removed all three pointer listeners, and disconnected its observer. Re-mount also succeeded. Desktop 1440×900, tablet 768×1024, and mobile 390×844 had no horizontal overflow. Visual inspection found no clipping or alignment defect; the headline remains one line at all three widths. Console errors/warnings: zero.

Axe reported 0 violations, 26 passes, and one incomplete color-contrast check because the text uses a gradient. Manual contrast against the fixture background measured 7.97:1 for the base text and 15.81:1 for the shine stop; the button text and border measured 12.77:1 and 4.26:1.

Screenshots: desktop (`~/creative-engineering-os-upstreams/.tests/react-bits/shinytext-desktop.png`), tablet (`~/creative-engineering-os-upstreams/.tests/react-bits/shinytext-tablet.png`), mobile (`~/creative-engineering-os-upstreams/.tests/react-bits/shinytext-mobile.png`), reduced motion (`~/creative-engineering-os-upstreams/.tests/react-bits/shinytext-reduced.png`). Browser script and results: verify-browser.js (`~/creative-engineering-os-upstreams/.tests/react-bits/verify-browser.js`) and verification.json (`~/creative-engineering-os-upstreams/.tests/react-bits/verification.json`).

### Accessibility and performance limits

ShinyText leaves the text in ordinary DOM content, adds no hidden duplicate for its main text, and marks the optional glow duplicate aria-hidden. The fixture includes a keyboard-operable button for disabling the loop. The default loop honors reduced motion. The component samples matchMedia only at mount and does not subscribe to preference changes; its followPointer branch schedules RAF without checking the reduced-motion flag. Do not enable followPointer for reduced-motion users without an explicit consumer-side decision.

The effect writes a CSS background gradient each animation frame and uses requestAnimationFrame, IntersectionObserver, a 2D canvas color parser, and three pointer listeners. Keep concurrent instances low and measure on target hardware; this run did not measure physical-device frame time or field Core Web Vitals. Axe could not automatically resolve the gradient's contrast, so the manual color-stop ratios above supplement the scan. Screen-reader/VoiceOver and forced-colors checks were not run.

## Audit, update, and rollback

The initial audit classified React Bits as **MISSING**; no duplicate integration or provider conflict was found. The failed checkout ~/creative-engineering-os-upstreams/react-bits.broken-20261021T131508Z remains untouched (30 MB) and is recorded as a cleanup candidate only; do not delete it as part of this integration.

For an update, review a specific Git commit and root license, regenerate the component index from that checkout, install with a pinned CLI, compare the CLI output to the pinned registry payload, then rebuild and repeat browser, reduced-motion, cleanup, and accessibility checks. The registry alias is floating, so hashes are required to establish a component pin.

Rollback by removing only this guide and integrations/evidence/react-bits.json, plus the untracked component index and the React Bits test artifacts/fixture changes if desired. No shared config, provider registrations, or runtime dependencies were changed. Do not remove the recorded broken checkout during rollback.
