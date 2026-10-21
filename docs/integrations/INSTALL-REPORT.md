# Creative Engineering OS V2 integration report

**Date:** 2026-10-21  
**Scope:** seven pinned upstream integrations plus the local CEOS task router. The parent integration records are [`manifest.json`](../../integrations/manifest.json) and [`UPSTREAM-LOCK.json`](../../integrations/UPSTREAM-LOCK.json); detailed evidence remains in the per-capability JSON files.

## A–H integration state

| | State | Version / full commit | Path | Agents supported by evidence | Verification and limits |
|---|---|---|---|---|---|
| **A. Impeccable** | Updated | Skill 4.7.0, engine 0.1.16; `dad8dbb3aac21ad1fa236c110315ef4abece23e8` | `~/creative-engineering-os-upstreams/impeccable`; active native trees under `.agents`, OpenCode, and the shared Claude skill path | Claude, Codex, OpenCode, Antigravity per upstream support evidence; this machine has active Claude/Codex/OpenCode paths, no Antigravity path | **Partial.** Provider trees match the pin, launcher checksum/probe passed. The published engine did not apply the pinned linked-stylesheet ignore fix; Cargo source regression test was unavailable. [Evidence](../../integrations/evidence/impeccable.json) |
| **B. UI/UX Pro Max** | Already present; aligned to pinned `main` | `56ea9cf174ed86786187daa9de0e6247cb0747e4`; release metadata records v2.15.0 at a different commit | `~/creative-engineering-os-upstreams/ui-ux-pro-max`; active OpenCode tree with `.agents` symlink and existing Claude plugin cache | Claude, Codex, OpenCode | **Passed with limitations.** Local retrieval, source comparison, data validation, and upstream tests passed. No fresh provider model invocation; Claude cache directory is labelled 2.13.0. The v2.15.0 tag has conflicting CLI README/package license statements. [Evidence](../../integrations/evidence/ui-ux-pro-max.json) |
| **C. React Bits** | Installed as a thin source-reference shim and component index | `e12c22192ac7b4b452c5e2feb9b586d74765d696` | `~/creative-engineering-os-upstreams/react-bits`; CEOS shim `integrations/skills/react-bits/SKILL.md`; 217-entry index in the pinned checkout | Claude, Codex, OpenCode, Antigravity; four local shim links are recorded, but model invocation was not tested | **Passed with limitations.** The ShinyText fixture built and passed production browser, keyboard, responsive, reduced-motion, cleanup, and axe checks. It is reference-only: existing React projects only; the upstream license includes a Commons Clause. [Evidence](../../integrations/evidence/react-bits.json), [global registration record](../../integrations/evidence/global-install.json) |
| **D. pmndrs/examples** | Installed as a searchable reference index and thin shim | `9905cd7b3d030a0ba5c6d327e15fe30ab648abb6` | `~/creative-engineering-os-upstreams/pmndrs-examples`; `integrations/indexes/pmndrs-examples.json`; CEOS shim `integrations/skills/pmndrs-examples/SKILL.md` | Claude, Codex, OpenCode, Antigravity; four local shim links are recorded, but per-client invocation was not tested | **Passed with limitations.** The index has 200 examples; one production example built and responded to a click. The other 199 were not individually run; mobile, reduced motion, no-WebGL fallback, and performance remain unverified. [Evidence](../../integrations/evidence/pmndrs-examples.json), [global registration record](../../integrations/evidence/global-install.json) |
| **E. GSAP skills** | Already present; duplicate generic activation narrowed | `aed9cfd3277740755f6bfc1155c7aa645403b760`; eight official skills | `~/creative-engineering-os-upstreams/gsap-skills`; active `.agents` and OpenCode skills | Claude, Codex, OpenCode, Antigravity per upstream support evidence; Codex catalog and native files were observed, Antigravity was not runtime-tested | **Passed with limitations.** All eight official skill files and vendored references match the pin. No consuming page was available to verify animation or reduced-motion behavior. OpenCode has no available skill-list diagnostic. [Evidence](../../integrations/evidence/gsap-skills.json) |
| **F. Superpowers** | Installed narrowly: TDD and verification links for Codex/OpenCode; existing Claude plugin retained | v7.0.0; `b739a8af570e10a95898f2bdf6cec97467fa6c12` | `~/creative-engineering-os-upstreams/superpowers`; four direct links across `.agents` and OpenCode; pre-existing Claude plugin remains manager-owned | Claude, Codex, OpenCode; no Antigravity runtime | **Partial.** The selected links and one RED/GREEN microcheck passed. Fresh model-driven selection was not tested. Upstream auto-trigger behavior requires `using-superpowers`; it is intentionally omitted so gstack stays the engineering orchestrator. [Evidence](../../integrations/evidence/superpowers.json) |
| **G. shadcn/ui** | Project-level source generator verified; existing skill links retained | Repository `ba1503c64472b82256d9de95e2e62c5901a38e8b`; CLI 4.22.1 | `~/creative-engineering-os-upstreams/shadcn-ui`; isolated fixture `~/creative-engineering-os-upstreams/shadcn-ui-fixture`; observed `shadcn` links in Claude, `.agents`, and OpenCode roots | Claude, Codex, OpenCode; skill runtime discovery was not separately tested | **Passed with limitations.** Fixture build, production dialog interactions, responsive screenshots, console, and axe passed. Seven high-severity findings were reported in the development CLI dependency graph; no forced downgrade was applied. The three skill links had unknown provenance and were not changed. [Evidence](../../integrations/evidence/shadcn-ui.json), [global install record](../../integrations/evidence/global-install.json) |
| **H. CEOS router** | Installed internal capability | Base CEOS revision `f43aa700883e032bfd5fc0241a7bfea2c49c327b`; route files are uncommitted and are not represented by that commit | `scripts/ceos-route.py`, `integrations/routes.json`, `integrations/ROUTING.md` | Claude, Codex, OpenCode, Antigravity as local Python CLI consumers; no provider dispatch or skill loading | **Passed with limitations.** Seven routing test methods cover 19 routes; all eight requested scenarios selected the expected primary. The router does not prove model skill loading or browser behavior. [Evidence](../../integrations/evidence/router.json) |

The manifest records full revisions, local paths, license, integration type, agent IDs, technologies, triggers, dependencies, verification status, update method, and rollback method. The lock records each observed checkout SHA and hashes both the active `SKILL.md` and full tree for registered skill roots. All seven upstream checkout HEADs matched their evidence pins during this run. The React Bits checkout has an untracked `INTEGRATION-COMPONENT-INDEX.json`; it was preserved. The router base checkout is modified by the pre-existing integration work.

## Integration architecture and routing

CEOS owns creative direction and orchestration. Impeccable supplies deterministic critique and interface commands. UI/UX Pro Max supplies local design knowledge and search. React Bits supplies selected React component source references. pmndrs/examples supplies searchable R3F examples. GSAP skills are the motion API and lifecycle authority while CEOS retains motion direction and accessibility. Superpowers is limited to TDD and completion verification under gstack. shadcn/ui copies editable source into an existing React project; it is not a shared CEOS component runtime.

Use the local router for one primary recommendation. A secondary is opt-in:

```sh
python3 scripts/ceos-route.py "Build a GSAP scroll sequence" --project .
python3 scripts/ceos-route.py "Build a GSAP scroll sequence" --project . --need-secondary
python3 scripts/integrations.py verify
python3 scripts/integrations.py status
```

The first router example selected `gsap`; the opt-in secondary is CEOS motion. Use [ROUTING.md](../../integrations/ROUTING.md) for the complete matrix, framework checks, and fallbacks. [TOOL-SELECTION.md](TOOL-SELECTION.md) is the short human guide.

### Eight requested route scenarios

These were run through `scripts/ceos-route.py` with temporary project metadata; the three React cases declared an existing React runtime.

| Request | Selected route | Primary capability |
|---|---|---|
| Improve homepage visual hierarchy | `visual-critique` | `impeccable` |
| Create a responsive editorial layout | `typography` | `impeccable` |
| Create an animated headline | `react-animations` | `react-bits` |
| Build a GSAP scroll sequence | `gsap-implementation` | `gsap` |
| Build an accessible dialog component | `components-forms` | `shadcn` |
| Prototype an interactive 3D object with React Three Fiber | `three-r3f` | `pmndrs-examples` |
| Debug a broken production component | `debugging-verification` | `superpowers-verification` |
| Audit an inconsistent landing page | `visual-critique` | `impeccable` |

All eight returned `available: true` in this local environment. The routing suite independently asserts these eight outcomes and the React/no-React boundaries.

## Tested examples and recorded results

| Integration | Real result from specialist evidence |
|---|---|
| Impeccable | On the linked-stylesheet fixture, the configured scan still returned `low-contrast` and `gradient-text` (exit 2); scanning the ignored CSS target directly returned no findings (exit 0). That is the published 0.1.16 binary's observed limitation, not a passing regression. [Evidence](../../integrations/evidence/impeccable.json) |
| UI/UX Pro Max | The upstream suite ran **164 tests in 5.253 seconds: OK**; the semantic validator accepted **12 domain files, 22 stack files, and `ui-reasoning.csv`**; **22/22** stack probes returned results. The healthcare design-system query returned valid JSON with expected fields and no persistence. [Evidence](../../integrations/evidence/ui-ux-pro-max.json) |
| React Bits | The index contains **217 components / 868 variants**. The production fixture built **17 modules**; browser checks recorded **15 style mutations in 250 ms**, no overflow, no browser errors/warnings, and zero axe violations plus one incomplete gradient contrast check. [Evidence](../../integrations/evidence/react-bits.json) |
| pmndrs/examples | The index has **200** unique examples. The single tested production example built **571 modules**; its minified JS chunk was **1,122.92 kB**. A click enlarged a cube and changed it orange-to-pink; there were **0 JavaScript errors** and one `THREE.Clock` deprecation warning. [Evidence](../../integrations/evidence/pmndrs-examples.json) |
| GSAP skills | **Eight** installed official skills and their vendored references matched the pinned hashes. No project animation was available to exercise in a browser. [Evidence](../../integrations/evidence/gsap-skills.json) |
| Superpowers | Four Codex/OpenCode links matched the pinned skills. The deterministic RED/GREEN microcheck finished with **1 passing test**. No model invocation was performed. [Evidence](../../integrations/evidence/superpowers.json) |
| shadcn/ui | Fixture `npm ci` added **413 packages**; production build transformed **2,041 modules**, with **23.88 kB CSS / 5.28 kB gzip** and **294.88 kB JS / 95.77 kB gzip**. Dialog keyboard/focus behavior passed; console had **0 errors and 0 warnings**; axe found **0 violations** with the dialog closed and open, with `aria-hidden-focus` incomplete on the open scan. [Evidence](../../integrations/evidence/shadcn-ui.json) |
| Router | The local routing suite contains **7 test methods**, asserts **19 route pairs**, and includes the **8** scenarios above. [Evidence](../../integrations/evidence/router.json) |

## Duplicate and conflict report

- **Consolidated:** UI/UX Pro Max has one OpenCode tree with an `.agents` symlink; Impeccable shares its `.agents` tree with Claude instead of adding a second Claude plugin; the router is the single route policy and returns one primary by default. GSAP's official eight skills are the general implementation path; the existing generic `~/.agents/skills/gsap` was narrowed to its own demo/reference use and its teaching content remains.
- **Intentionally separate:** CEOS creative direction remains separate from implementation references. gstack retains engineering orchestration; Superpowers exposes only TDD and verification. React Bits and shadcn are limited to existing React projects. pmndrs/examples remains an index/reference, not a global runtime. Vendored library copies remain on-demand references.
- **Unresolved:** the existing shadcn and `migrate-radix-to-base` links in three skill roots have unknown provenance and were preserved. The Claude UI/UX Pro Max plugin cache is labelled 2.13.0, though current runtime assets are mostly aligned; its test fixture differs. The UI/UX Pro Max v2.15.0 tag's CLI README license conflicts with its package metadata. The pre-existing Claude Superpowers plugin injects `using-superpowers` at SessionStart, which conflicts conceptually with gstack; it remains unchanged. The separate synchronized plugin cache was also retained.
- **Cleanup candidates preserved:** `~/creative-engineering-os-upstreams/react-bits.broken-20261021T131508Z` (30 MB) and `~/creative-engineering-os-upstreams/pmndrs-examples-validation` (232 MB). Neither was deleted. The pre-existing gstack broken link `gstack-review` → `../qa/sections/exploratory.md` is outside CEOS and recorded only.
- **Other operational risks:** Impeccable's published binary misses the pinned source fix. shadcn's development CLI dependency graph reported seven high-severity findings; the forced proposed downgrade to 1.0.0 was not applied. React Bits' root license includes a Commons Clause restriction on redistributing components by themselves.

## Efficiency report

The router evidence reports a **static proxy** for “Create a wireframe for the signup flow”: router output plus one primary skill totals **4,979 bytes ≈ 1,245 tokens**, compared with **66,719 bytes ≈ 16,680 tokens** for all 14 core skills (approximate tokens are `ceil(bytes / 4)`). The recorded static-proxy reduction is 92.5%. This is a static size comparison only: there is no live token telemetry, so it does **not** claim real token savings. [Router evidence](../../integrations/evidence/router.json)

## Proposed shared-config changes (not applied)

Specialist evidence reported one parent-owned action: register React Bits as a source reference for existing React projects, never as a recommendation for non-React projects, and do not add provider-global config. The central manifest records it as `reference-only`, and the existing router provides a React-gated route. **That repository-level action is complete; no shared provider configuration change is proposed or awaiting approval.**

Superpowers' upstream describes automatic triggering through the `using-superpowers` startup bootstrap. That bootstrap was intentionally omitted because gstack owns engineering orchestration. The narrow method path needs no shared config: reload a host session and explicitly invoke the TDD or verification skill when the project policy calls for it. Automatic upstream bootstrap would require a shared startup/policy change and would reintroduce the orchestrator conflict, so it is not proposed.

## Maintenance pointers

- [Controlled per-repository update procedure](UPDATE-PROCEDURE.md); never bulk-update all seven.
- [Rollback guide](ROLLBACK.md), including the private Impeccable and GSAP backup locations recorded in evidence.
- [Tool selection](TOOL-SELECTION.md) and [full router behavior](../../integrations/ROUTING.md).
- [Compatibility limits](../../integrations/COMPATIBILITY.md) and each per-capability evidence JSON.

## Repository regression

The CI source commands in `verify.yml` passed: structure, installer, routing (**7 tests**), integration (**10 tests**), generated manifest (**2 tests**), mirror security (**1 test**), and repository hygiene (**0 secret-pattern findings / 0 broken Markdown links**). The existing `tests/scripts.test.py` (**4 tests**) and pmndrs index test (**1 test**) also passed. `scripts/verify.sh`, `scripts/verify.sh --installed`, `scripts/integrations.py verify`, `scripts/integrations.py status`, manifest regeneration check, and `git diff --check` passed.

All five CI build targets passed `npm run build` using their existing `node_modules`. `npm ci` was not run because it would install packages and run package installation hooks; the task prohibited remote install scripts. The standalone `python3 -I tests/verify-structure.py --installed` check still fails on its pre-existing expectation that Claude has a manual `ceos-3d-asset-pipeline` link; the audit recorded this limitation. The wrapper's `--installed` mode checks the actual integration lock and registered skill trees instead.

## Final status

### Fully working in the verified scope

- The local router selected the expected primary for all eight requested scenarios; its seven-method routing suite passes.
- UI/UX Pro Max's local Python search, data validation, upstream tests, and all 22 stack smoke probes passed.
- React Bits ShinyText passed the isolated production fixture's build and recorded browser/accessibility checks.
- shadcn/ui generated and exercised the fixture Dialog successfully with the recorded keyboard, focus, responsive, console, and axe results.

### Partially working

- Impeccable's skill trees and launcher are current, but the published detector binary failed the linked-stylesheet ignore regression.
- pmndrs/examples has a verified 200-entry index and one tested example; the remaining examples and several runtime conditions are unverified.
- Superpowers' native links and narrow TDD example are verified, but fresh model-driven skill selection is not. The automatic bootstrap remains out by design.

### Installed but not operationally verified

- GSAP skills are hash-verified and discoverable in the current Codex/T3 catalog, but no consuming page exercised actual animation or reduced-motion behavior.
- Fresh provider/model invocation for UI/UX Pro Max, Impeccable, GSAP, and Superpowers was not tested; local file/search checks are not model-invocation evidence.

### Unsupported or blocked

- Antigravity live skill invocation remains blocked/unverified because `agy` is unavailable and the prior runtime check encountered Google's account verification gate. No account or provider settings were changed.
- The legacy `python3 -I tests/verify-structure.py --installed` mode still fails on the missing `~/.claude/skills/ceos-3d-asset-pipeline` link. The pre-install audit recorded this old assumption; this integration did not add provider skill links. `scripts/verify.sh --installed` runs the default structural check plus the new integration checkout/tree verification instead.
