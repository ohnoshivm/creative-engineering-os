# Quality checklist (all templates)

Copy into the project as `CHECKLIST.md` and tick with evidence (screenshot path, test output, measurement).

## Concept and design
- [ ] Approved concept (`docs/CONCEPT.md`) — idea sentence passes the competitor test
- [ ] Type: ≤ 5 sizes; body 16 px+; 45–75 ch; headlines ≤ 3 lines at 1440/768/390
- [ ] Grid: equal outer margins; ≤ 3 shared left edges per page; section rhythm consistent
- [ ] Colour roles respected; every text pair passes contrast (axe + spot checks)
- [ ] Phone layout re-composed, not shrunk
- [ ] No generic tells (see ceos-visual-audit)

## Motion
- [ ] Motion tokens used everywhere; one signature move
- [ ] Interruptible; no scroll hijack; no motion during reading
- [ ] Reduced-motion run: all content visible, no travel/parallax/auto-advance

## Graphics (if any)
- [ ] Poster/fallback without WebGL; no loader that can hang
- [ ] DPR capped; paused offscreen; `destroy()` frees GPU (renderer.info back to baseline)
- [ ] No first-interaction shader-compile freeze
- [ ] Assets optimised and within budget (inspect table attached)

## Engineering
- [ ] `npm run build` clean; `npm test` green on all projects; console clean
- [ ] axe: 0 serious/critical; keyboard walk of every journey with visible focus
- [ ] Lighthouse CI budgets met (or written exception)
- [ ] Frame probe: p95 frame time within budget; no frame > 100 ms after interactive
- [ ] Production build tested via preview / preview deployment; rollback path written
