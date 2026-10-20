# Template verification — 2026-10-20

All four production artifacts built and passed browser smoke, keyboard/accessibility checks and visual comparisons in installed Google Chrome 155 on this Mac. This verifies local starter behavior; it does not certify physical-device GPU performance or a deployed site.

## Commands and results

Run inside each template: `npm run build`, `npm test -- --workers=2`, `npm run test:visual -- --workers=2`, and `npm audit --omit=dev`.

| Template | Production build | Smoke passed / intentionally skipped | Visual passed / skipped | Production advisories |
|---|---|---:|---:|---:|
| editorial | pass | 14 / 2 | 4 / 0 | 0 |
| motion-heavy | pass | 13 / 7 | 4 / 0 | 0 |
| immersive-3d | pass | 21 / 14 | 3 / 2 | 0 |
| experimental-graphics | pass | 16 / 20 | 6 / 6 | 0 |
| Total | 4 passed | 64 / 43 | 17 / 8 | 0 |

Skips are capability/project combinations: keyboard on touch, axe injection with JavaScript disabled, reduced-motion-only assertions in normal projects, graphics assertions without WebGL, and graphic baselines in fallback projects. They are not unresolved failures. TypeScript checks passed; editorial now exposes `npm run check` (`astro sync && tsc --noEmit`) for its scripts/tests. This does not replace a dedicated Astro-template semantic checker.

Existing A/B/C baselines were compared without updates. D previously had no baseline suite: six deterministic raymarch/feedback screenshots at 1440, 768 and 390 were generated with `--update-snapshots=missing`, opened and inspected individually, then all six passed a normal comparison run.

## Fixed defects and evidence

| Defect | Change | Verification |
|---|---|---|
| Reduced-motion lab canvas cleared on resize with no running loop to redraw it | Repaint a static frame after resizing; preserve `still` query while switching | Static screenshots remain identical over time; resized raymarch still contains decoded GPU colour signal |
| Reduced-motion immersive ribbon vanished after resize | Repaint current geometry after buffer/camera resize once the first frame exists | Regression first failed with only 6 quantized colours after resize; now exceeds 100 before and after; full suite and original baselines pass |
| Graphics "nonblank" test inspected compressed PNG bytes and could pass for flat output | Decode actual RGBA; hide overlapping panel during canvas capture; require visible coloured signal, dark ground and colour range | Both experiments pass at desktop/tablet/390/reduced; overlay text cannot supply the signal |
| Lab gave no useful JavaScript-disabled state and left unavailable controls active | Add visible `noscript` explanation; controls start disabled and enable after WebGL setup | JavaScript-disabled and `--disable-3d-apis` projects verify readable explanation and disabled controls |
| Immersive wordmark hit area was only 26–30px tall | Increase inline-flex link target to 44px without changing header height | `templates/immersive-3d/docs/QA/verification/final-controls.json`: 44px at 1440/768/390, no horizontal overflow; final screenshots inspected |
| Templates shared port 4174 and silently reused other running servers | Distinct defaults: editorial 4321, motion 4174, immersive 4176, lab 4177; all test servers reject occupied ports | A wrong-template lab run was correctly rejected by `data-lab`; after port isolation its 16 smoke + 6 baseline comparisons pass. Preview scripts, audit URLs, Lighthouse configs and READMEs agree |
| Lab experiment URL could select inherited object properties (`constructor`, `__proto__`, `toString`) and crash | Use a Map registry; unknown names resolve to raymarch | Regression navigates all three prototype keys plus an unknown name, asserts visible selected raymarch and no page errors |
| Immersive copy claimed offscreen GPU resource release | State actual behavior: offscreen rendering pauses; teardown releases resources | Matches IntersectionObserver loop stop and explicit `destroy()` implementation |

The failed wrong-server comparison and the deliberately failing resize regression were investigated before final passing runs. No existing snapshots were overwritten to conceal either failure.

## Gamma correctness

Raymarch is a `RawShaderMaterial` with no Three output-colour chunk. It uses linear lighting/background values and one explicit `pow(col, 1.0 / 2.2)` at final output. The decoded screenshot assertion checks an unobscured ground pixel against the expected approximately 22/23/25 RGB (tolerance <2 per channel). Missing conversion would produce approximately 1/1/2; a second conversion approximately 84–89. The assertion passes at all four graphics-capable test projects. The feedback simulation stores render-target state and its display shader writes authored raw display colour; it has no additional output transform.

`?exp=raymarch&still` uses time 2 seconds. Feedback still mode computes 120 fixed simulation steps before presenting one image. These freeze modes are visual-test fixtures, not animation benchmarks.

## Rendered inspection

Actually opened desktop, tablet and phone screenshots, including full-page captures for content and reduced states. Editorial has a 2-line desktop and 3-line tablet/phone title, readable text measure, flowing margin note and visible footer action. Motion has a 3-line title, readable contrast, keyboard action and exercised read-along/horizontal-scroll behavior. Immersive has a 2-line title, readable DOM content, no-JS/no-WebGL poster, actual scroll-triggered section reveals and a static reduced-motion ribbon. Lab has readable controls and distinct raymarch forms/feedback ink at all three widths; fullscreen graphics intentionally extend beyond portrait viewport edges.

Evidence directories (relative to repository):

- `templates/editorial/docs/QA/verification/`: 1440/1024/768/390 first/full images, reduced images, `capture.json`, Lighthouse JSON.
- `templates/motion-heavy/docs/QA/verification/`: corresponding images/measurements, scroll recordings, Lighthouse JSON.
- `templates/immersive-3d/docs/QA/verification/`: corresponding images/measurements, scroll recordings, final 1440/768/390 screenshots and 44px target measurements, Lighthouse JSON.
- `templates/experimental-graphics/docs/QA/raymarch/`: four-width/reduced captures and Lighthouse JSON; `tests/smoke.spec.ts-snapshots/` contains reviewed baselines for both experiments; `docs/no-js.png` shows the actual fallback.

Capture reports record zero console/page errors and zero axe violations at all four normal widths. No horizontal overflow or unnamed controls was recorded. The only undersized link reported was the immersive wordmark, fixed and measured afterward. Full-page screenshots of pinned/sticky interfaces can relocate their fixed header during capture; use first-screen images and live interaction checks for viewport composition.

## Local Lighthouse

Installed Lighthouse 13.5.0; production preview; desktop preset; one run per artifact. No global package install was performed. The existing Lighthouse CI thresholds (LCP ≤2500ms, CLS ≤0.05, TBT ≤200ms, accessibility ≥95) are satisfied by these measurements; `lhci autorun` itself was not run.

| Template | Performance | Accessibility | Best practices | SEO | LCP | TBT | CLS |
|---|---:|---:|---:|---:|---:|---:|---:|
| editorial | 100 | 100 | 100 | 100 | 289ms | 0ms | 0 |
| motion-heavy | 100 | 100 | 100 | 91 | 345ms | 0ms | 0 |
| immersive-3d, isolated | 100 | 100 | 100 | 91 | 512ms | 0ms | 0 |
| experimental-graphics, isolated | 100 | 100 | 100 | 91 | 373ms | 19ms | 0.00049 |

An earlier immersive run overlapped other browser suites and returned performance 72/TBT 894ms. It is retained as `lighthouse.json` for transparency and superseded by `lighthouse-isolated.json` after other browser/GPU jobs finished. Do not interpret that contention difference as a code-performance improvement. Editorial/motion scores are single local observations. The lab audit predates the final registry-only URL hardening; its complete smoke and visual suites were rerun after that change. All production dependency audits returned zero advisories at the time of the run.

Not verified: Safari/Firefox, physical mobile GPUs, GPU timer-query/frame-p95 performance, extension-denied half-float rendering on a second vendor, deployment response headers, hosted URLs and rollback. No physical-device 60fps or release certification is claimed. Playwright's required 1.4MiB FFmpeg helper was installed into its local cache for recordings; no global dependency was added.
