# Tool selection

Ask the local CEOS router for one primary capability:

```sh
python3 <ceos-root>/scripts/ceos-route.py "Describe the task" --project .
python3 <ceos-root>/scripts/ceos-route.py "Build a GSAP scroll sequence" --project . --need-secondary
```

Use the second form only when the route's recorded secondary contribution helps. The router recommends; it does not load skills, dispatch agents, install dependencies, or change provider settings. For the full route matrix, React detection rules, fallbacks, and work modes, see [ROUTING.md](../../integrations/ROUTING.md).

For a direct specialist choice, use the primary skill's native entry point and follow its project policy. Keep React Bits, shadcn/ui, and pmndrs/examples for projects that already declare React. Use GSAP guidance for its API and lifecycle, with CEOS owning motion direction and reduced-motion behavior. Superpowers is limited to TDD and verification under the active engineering orchestrator.
