# Reference verification record

Date: **2026-10-20**. Method: live web retrieval of first-party pages/repositories; agent-reach web workflow was loaded and a Jina Reader retrieval of WebGL Fundamentals succeeded. Official documentation retrieval was used as the focused fallback for the remaining links. `agent-reach check-update` reported v1.5.0 current. No social-platform login or cookie access was needed.

This record documents retrieval, not a visual inspection or runtime audit. No course was completed; no shader, package, demo or browser extension was installed or executed as part of this reference-library pass. Exercises are proposed.

## Learning sources

| Requested source | Outcome |
| --- | --- |
| practicaltypography.com | First-party book index and content retrieved; payment/support request visible |
| typewolf.com | First-party font/site resources and paid guide listing retrieved |
| fontsinuse.com | First-party archive and category/typeface index retrieved |
| siteinspire.com | First-party inspiration index retrieved |
| awwwards.com | First-party awards/discovery index retrieved |
| hoverstat.es | First-party editorial index retrieved |
| tympanus.net/codrops | First-party tutorial/editorial index retrieved |
| threejs.org/examples | First-party examples index shell retrieved; individual example rendering unverified |
| shadertoy.com and /terms | Retrieval tool returned “(402) Payment Required”; not evidence the site itself charges for access. Resource and per-work terms require browser recheck |
| webglfundamentals.org | First-party learning index retrieved with both web retrieval and Jina Reader |
| webgpufundamentals.org | First-party learning index retrieved; the extraction reported missing WebGPU features in its retrieval browser. This does not establish target-device support |
| thebookofshaders.com | First-party contents retrieved, including unfinished/unlinked chapter headings |
| natureofcode.com | First-party book contents, free online access statement and print links retrieved |
| github.com/mattdesl/canvas-sketch | Official repository retrieved; MIT and beta description visible |
| web.dev | First-party documentation index retrieved |
| developer.chrome.com/docs/devtools | First-party DevTools index retrieved |
| playwright.dev | First-party framework/docs entry retrieved |
| developer.mozilla.org | Redirected to /en-US/; documentation entry retrieved |
| threejs-journey.com | First-party course landing/curriculum retrieved |
| theatrejs.com | Canonical www.theatrejs.com page, latest docs and theatre-js/theatre repository retrieved; core/Studio licensing differs |
| rive.app | First-party product, web runtime docs, pricing and rive-app/rive-wasm repository retrieved |

## Benchmarks

| Requested source | Outcome |
| --- | --- |
| lusion.co | First-party studio text and project index retrieved |
| buttermax.net | Title retrieved; zero body lines in extraction |
| 14islands.com | Redirected to www.14islands.com; studio text/project index retrieved |
| active-theory.com | Redirected to ww19.active-theory.com; parking/privacy content. Excluded as trusted studio URL |
| activetheory.net | Corrected candidate: Active Theory title and “Please enable javascript” shell retrieved; actual experience remains unverified |
| resn.co.nz | Studio title and image-only shell retrieved |
| makemepulse.com | Redirected to www.makemepulse.com; first-party studio/project text retrieved |
| locomotive.ca | Redirected to /en; first-party studio/project text retrieved |
| dogstudio.co | First-party studio/project text retrieved |
| immersive-g.com | First-party studio/project descriptions retrieved |

## Optional tool sources

Live first-party docs/repositories were retrieved for Motion, Lenis, Tempus, OGL, React Three Fiber, Three.js WebGPURenderer/TSL/KTX2Loader, canvas-sketch, oframe/ogpu, KTX-Software, Theatre.js, Rive and BabylonJS/Spector.js. Exact URLs and adoption decisions are in [OPTIONAL-TOOLING.md](../docs/OPTIONAL-TOOLING.md).

OGL's standalone LICENSE link did not retrieve; the official package.json did and states Unlicense. Spector's project site retrieved once and timed out on a later request; its repository retrieved successfully. No claims here substitute for checking the licenses and integrity of exact downloaded artifacts.

## Reverification checklist

- Reopen canonical URLs and record redirects; flag parked or reassigned domains.
- Check the specific docs/release/package rather than assuming the current site matches a project's installed version.
- Read applicable code, content, font and asset licenses separately before reuse.
- For visual or motion claims, inspect the real rendered site with screenshots and reproducible interaction steps.
- For performance claims, retain trace/metric evidence, target browser/device, scene and test conditions.
