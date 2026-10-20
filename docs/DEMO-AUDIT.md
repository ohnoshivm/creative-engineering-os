# Independent demo audit — 20 October 2026

Scope: isolated Signal study capability demonstration; reviewed by an independent native specialist who did not produce the implementation. Captures: `demo/signal-study/docs/QA/final/`. Working tree build; generated baseline commit was internal to the demo and is superseded by the OS source commit.

Initial verdict: FIX THEN SHIP; no P0/P1 observed. Two P2 findings sent to the implementation owner:

| ID | Evidence | Finding | Correction / recheck |
|---|---|---|---|
| V-01 |390-reduced-first.png; live reduced-motion .stage data-phase remained0.000 after 500px scroll | Instructions promised pointer/scroll deformation while reduced view is static; mobile needs touch-specific instruction | Adaptive reduced/coarse guidance implemented; regression checks passed in final28-pass smoke suite |
| V-02 |1440-first.png; pause bottom y903.3, controls bottom y940.8 at 1440×900 | Instrument controls clip below desktop entry view | Stage max height450px; controls bottom890.8 at 1440×900 and749.4 at 1024×768, verified by final viewport tests |

Independent checks: actual1440/1024/768/390 + reduced screenshots inspected; skip link focuses main, range ArrowRight40→41, visible3px outline, Space toggles Pause/Resume. Capture report shows no horizontal overflow, unnamed controls, small targets, console errors or axe violations. Composition follows the concept and consistent gutters; scores8/10 for concept/type/composition/color/graphics/interaction/responsive. Temporal motion quality was not independently verified. T3 snapshot calls failed twice; reviewer used installed Playwright CLI and local images.

Limits: no originality certification, no field CWV/physical-device certification. Heading-line-count heuristic overestimated some mixed-markup H2s; screenshot evidence supersedes that heuristic. Owner recheck below is completion evidence; it is distinguished from the initial independent review.

## Owner refinement recheck

The owner supplied final-refinement.json and refreshed captures after both fixes. Integration owner inspected actual final desktop/tablet/reduced-phone images, and final regression results record28 smoke passes,3 visual comparisons and zero console/axe/overflow findings. P2 findings V-01/V-02 are resolved. Initial independent verdict is preserved above; this recheck is not a second independent motion audit. Evidence: ../demo/signal-study/docs/QA/final-refinement.json and final/ captures.
