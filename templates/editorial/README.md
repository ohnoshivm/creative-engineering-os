# Template A — Editorial

Astro (static) + TypeScript + one targeted GSAP moment. For premium, type-led sites: studios, essays, portfolios,
journals. Ships zero JS except the title reveal (≈ GSAP core).

```bash
~/creative-engineering-os/scripts/new-project.sh editorial ~/projects/my-journal
npm install && npm run dev        # http://localhost:4321
npm test                          # desktop, mobile, reduced-motion, no-JS; axe; keyboard; measure check
npm run check                     # sync Astro types, check TypeScript scripts/tests
npm run test:visual               # screenshot regression
npm run build && npm run preview  # static dist/
npm run lhci
```

- `src/styles/global.css` — cascade layers; tokens (5 type steps, paper/ink/soft/mark), 12-column page grid with
  subgrid article, margin notes that fold into the flow on phones.
- `src/scripts/title-reveal.ts` — the single orchestrated moment, fails open, skipped under reduced motion.
- Fonts: Charter (system on Apple devices) as a placeholder. Replace with the licensed faces; add
  `@font-face` with metric-matched fallbacks (see `ceos-art-direction` references).

## Verification server

Production preview uses `http://localhost:4321`. Playwright builds and starts its own preview, and fails if that
port is already occupied; stop a manually started preview before running tests. This prevents a test suite from
quietly exercising another template.
