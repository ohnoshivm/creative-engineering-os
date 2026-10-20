# Use the studio

1. Give the agent a brief: audience, outcome, primary action, real content/assets, constraints and reference principles. Load ceos-studio-workflow, then the discipline skill for the current stage.
2. Agree an original concept. Record type hierarchy, palette, spacing, grid, material/light, motion, interactions and responsive rules. References are inspiration; do not copy identities, layouts, assets or copy.
3. Create the lightest starter:

```sh
./scripts/new-project.sh editorial ~/Projects/my-original-site
cd ~/Projects/my-original-site
npm ci
npm run dev
```

The generator refuses existing directories and template traversal. It copies source/lockfiles, excludes dependencies/raw reports/baselines, initializes Git and writes project instructions. Prototype the signature moment at desktop/phone before bulk implementation.

4. Build and verify: npm run build, npm test, real desktop/tablet/mobile screenshots, interactions, keyboard, reduced-motion/fallbacks, console and axe. npm run test:visual compares reviewed baselines; on a new project capture/review before explicitly creating them. Existing starter baselines are OS/browser-dependent and intentionally omitted from generated projects.
5. Run shared capture/perf tools against a production preview. From the toolkit root:

```sh
node tooling/visual-audit/capture.mjs --url http://localhost:4174 --out /path/to/project/docs/QA/review
node tooling/perf/frame-probe.mjs --url http://localhost:4174 --out /path/to/project/docs/QA/perf.json
```

Use the actual project's port. Starters use4321/4174/4176/4177 and refuse server reuse so tests cannot silently inspect the wrong app. Capture screenshots do not replace actual scroll/hover/navigation checks. rAF distributions are scheduling observations, not GPU time or field INP.

6. Give approved direction and captures to an independent auditor. Use standards/QA-REPORT.md: evidence, severity, exact corrective action and recheck. Fix real defects and inspect again. A build is not a visual-quality verdict.
7. Measure before optimizing. Review inputs, paths, commands, dependencies and deployment headers as relevant. Release only the exercised artifact with a recorded rollback. This toolkit does not grant permission to publish another client's site.

## Roles and example prompts

- Direction: “Use ceos-creative-direction to propose a distinctive concept from this brief and available assets.”
- Motion: “Use ceos-motion-direction to specify triggers, timing/easing, interruption and reduced-motion alternatives for the approved scene.”
- Graphics: “Use ceos-realtime-3d and ceos-shader-engineering for the signature material; name frame ownership and performance budgets.”
- Quality: “Use ceos-production-quality and ceos-visual-audit on this production URL and approved direction; return concrete evidence-backed defects.”

Use supported native/T3 delegation only for independent paths; one integration owner merges. Model/provider availability comes from the live host catalog, not a fixed list in this repo.
