# Creative Engineering OS

A local studio toolkit for original websites: shared specialist skills, disciplined review gates, four focused starters, browser diagnostics and an independently reviewed graphics demonstration. Existing providers, routing and authentication are preserved. Source lives here; client skills link to it.

## Start a project

```sh
~/creative-engineering-os/scripts/new-project.sh editorial ~/Projects/my-site
cd ~/Projects/my-site
npm ci
npm run dev
```

Choose `editorial` (Astro/type), `motion-heavy` (GSAP/Lenis), `immersive-3d` (Three.js) or `experimental-graphics` (raw GLSL). Start with the `ceos-studio-workflow` skill. The generated AGENTS.md and CLAUDE.md point to the shared standard. Agree the concept, prototype the signature moment, then build and inspect.

## Verify

```sh
~/creative-engineering-os/scripts/verify.sh
python3 ~/creative-engineering-os/tests/scripts.test.py
node --test ~/creative-engineering-os/tests/mirror.test.mjs
# From a project:
npm run build
npm test
npm run test:visual
```

The templates test production previews with installed Chrome. Review screenshots before creating a project's new baselines. Never blindly accept changed snapshots. Real device/Safari and field performance checks remain release work.

## Read next

- [System and compatibility](SYSTEM.md)
- [Operating guide](docs/OPERATING.md)
- [Verification results and limitations](docs/VERIFICATION.md)
- [Exact installation inventory](docs/INVENTORY.json)
- [Skills inventory](docs/SKILLS.md) · [agent ownership and handoffs](agents/TEAM.md)
- [Reference library](references/README.md) · [optional tooling decisions](docs/OPTIONAL-TOOLING.md)
- [Standard](standards/STANDARD.md) · [QA report](standards/QA-REPORT.md)
- [Rollback](docs/ROLLBACK.md) · [maintenance](docs/MAINTENANCE.md)
- [Demo](demo/signal-study/README.md) · [demo verification](docs/DEMO-VERIFICATION.md)

This toolkit provides capabilities and evidence, not an automatic guarantee of world-class design. Pixelard's website remains a separate project; it was paused for this setup.
