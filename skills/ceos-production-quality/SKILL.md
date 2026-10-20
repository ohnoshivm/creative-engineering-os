---
name: ceos-production-quality
description: Production verification for creative websites — Playwright smoke and interaction tests, visual regression snapshots, automated accessibility (axe-core) plus keyboard checks, responsive and cross-browser runs, console/error budgets, build verification, basic security review and deployment/release validation with rollback. Use before merging or deploying, when adding tests to a creative site, when setting up CI for a template, or when verifying a release actually works.
---

# Production quality

## Gates (all templates ship these)

| Gate | Command | Pass |
|---|---|---|
| Type/lint | `npm run check` | 0 errors |
| Build | `npm run build` | exits 0; no unexpected chunk > budget |
| Smoke | `npm test` (Playwright) | page loads at 1440 + 390, h1 visible, primary CTA reachable by keyboard, **0 console errors** |
| A11y | included in `npm test` via `@axe-core/playwright` | 0 serious/critical violations |
| Reduced motion | test project with `reducedMotion: 'reduce'` | content complete, no scroll-driven motion |
| No-WebGL (3D templates) | Chromium with `--disable-3d-apis` | poster + full content, no uncaught errors |
| Visual regression | `npm run test:visual` | diffs reviewed; update snapshots only intentionally |
| Lab perf | `npm run lhci` | budgets in `lighthouserc.json` |

Playwright uses the installed Google Chrome (`channel: 'chrome'`) — no browser download. Add WebKit (`npx playwright
install webkit`) per project when Safari coverage matters (recommended before launch).

## Visual regression practice

`expect(page).toHaveScreenshot()` with animations disabled (`animations: 'disabled'`, reduced motion, fixed seed,
fonts loaded, WebGL frame frozen via a `?still` flag). Mask dynamic regions. Review diffs as images, never by
blindly updating.

## Security review (static sites and light backends)

Headers: CSP (allow only needed origins; avoid `unsafe-inline` where possible), `X-Content-Type-Options`,
`Referrer-Policy`, `Permissions-Policy`, HSTS on the host. Third-party scripts listed and justified; SRI for CDN
scripts; forms: server-side validation, rate limiting, honeypot, no secrets in client bundles (`npm run build` +
grep `dist/` for keys), dependency audit (`npm audit --omit=dev`), no `.env` committed.

## Release validation

Build the production artefact, serve it (`npm run preview`), run the full test suite against it, then deploy to a
preview URL and run smoke + Lighthouse against that URL. Record: commit, URL, results, rollback command (previous
deployment id / git tag).

## Failure criteria

Tests only against dev server; snapshots updated without review; axe run but keyboard never tried; console errors
"known and ignored"; no rollback path; secrets in the bundle.
