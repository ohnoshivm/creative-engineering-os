# Creative Engineering Standard

Research → concept → art direction → UX → motion specification → architecture → prototype → build → browser review → independent critique → technical audit → refinement → deployment.
Scale artifacts to the job; preserve the evidence gates. Follow project/user authorization and use one orchestrator per stage. Existing project conventions take precedence over starter choices.

1. Original idea: write the concept, audience, purpose and primary action. Agree a direction before a substantial client build. Study references for principles; never reuse their identity, assets, copy or layouts.
2. Art direction: define typography hierarchy, palette roles, spacing/type scales, grid, material/light, responsive rules and interaction language before bulk code. Typography is composition. Avoid template grids, filler proof, decorative effects and arbitrary gradients.
3. Prototype: render the signature moment at desktop and phone sizes before multiplying sections. Select the smallest stack that supports the idea. No speculative dependencies.
4. Architecture: name state, scroll and render-loop owners. One scroll engine. Dispose GPU resources, observers, timelines and handlers. Keep content semantic and usable without graphics.
5. Motion: every animation serves hierarchy, story or feedback. Specify trigger, timing, easing, interruption and static alternative. Honor reduced motion, offscreen/hidden tabs and touch. Native scroll is the default.
6. Access: keyboard and visible focus, labels, meaningful order, contrast, useful alternatives, responsive touch targets. Automated axe checks supplement manual keyboard/touch checks.
7. Verify: production build, relevant tests, real rendered desktop/tablet/mobile evidence, exercised interactions and clean console. Look at screenshots; record concrete defects, fix and recapture. No claim that build success proves visual quality.
8. Measure: record lab LCP/CLS, frame distributions, transfer/bundle size and heap where appropriate. Measure before optimization. Headless laptop timings are not physical mobile GPU or field CWV evidence; INP needs real interactions/field data.
9. Security: review input, auth, paths, commands, outbound calls and forms. No secrets in artifacts. Audit dependencies; configure host security headers at release. Never run downloaded scripts before inspection.
10. Release: exercise the production artifact, record commit/URL/checks and rollback. No deploy implied by a local build. Missing checks are explicitly “not verified”.

## Independent review

One integration owner, path-based ownership, short artifact handoffs. Delegate only independent work. Use the provider's supported native or T3 child mechanism; model availability comes from the live catalog. Never introduce account routing or custom billing for roles. Auditor reviews actual output independently and returns findings to the owner; read-only agent permissions cannot by themselves sandbox shell or MCP writes.

## Defect report

Use [QA-REPORT.md](QA-REPORT.md). Severity: P0 broken or unsafe primary flow; P1 material usability/accessibility/rendering failure; P2 craft/performance defect; P3 refinement. Each finding includes screenshot/measurement, expected behavior, exact corrective action and a recheck result. No P0/P1 may remain at release without an explicit owner decision.

## Learning

Record one reusable principle and one project-specific decision after release. Update dependencies/skills deliberately, with lockfiles, a before/after diff, tests and rollback. Keep projects visually distinct.
