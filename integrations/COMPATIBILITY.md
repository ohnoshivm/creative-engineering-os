# Router compatibility

The generated integration inventory is in [`manifest.json`](manifest.json); regenerate it with `python3 scripts/integrations/generate_manifest.py` and verify byte identity with `python3 scripts/integrations/generate_manifest.py --check`.

The router is a local Python standard-library CLI. It makes no network calls, runs no install hooks, and has no runtime package dependency. It requires the CEOS checkout and Python 3.9+. It recommends capabilities only; the host agent remains responsible for loading a selected skill and following the active project policy.

## Capability availability

Baseline classifications below come from `docs/integrations/PRE-INSTALL-AUDIT.md` and `pre-install-state.json` (2026-10-21). The router checks the current filesystem and package metadata on each invocation; baseline state does not override that check.

| Capability | Baseline | Router handling |
|---|---|---|
| CEOS core skills | Active in this checkout | Detects exact skill directories and repository-owned tool paths. |
| Impeccable | Active / reference-only; pre-existing discovery paths | Uses existing registration; does not add copies or alter plugins. |
| UI/UX Pro Max | Active / reference-only; plugin and skill paths exist | Uses existing registration; plugin-only availability can be declared with `--available`. |
| GSAP skills | Active / reference-only; multiple skills exist | Detects exact GSAP skill names; does not add GSAP runtime packages. |
| React Bits | Local project integration present | Detects the repository-local skill path; never selects it without an existing React runtime. |
| pmndrs/examples | Local project integration present | Detects the repository-local example skill; requires an existing React runtime. Otherwise routes to CEOS 3D. |
| Superpowers | Narrow native TDD and verification skills are available | Routes only to TDD and verification roles. Existing project engineering orchestration remains authoritative. |
| shadcn/ui | Project-level source component generator verified with limitations | Requires an existing React runtime. Declare `--available shadcn` when its CLI is available; the router does not install components or dependencies. UI/UX Pro Max is the non-React fallback. |

Existing duplicate skill paths are baseline state, not router-created registrations. The CLI reports only its selected primary and optional secondary, not every detected skill path. It never reads provider configuration, authentication files, credential values, or backups. A plugin without a discoverable skill directory is not inferred; use repeated `--available <capability-id>` flags when that host capability is known to be available.

## Framework checks and limits

Framework detection reads dependency names from all four package dependency groups and recognizes framework config filenames. React runtime detection specifically requires a declared `react` or `react-dom` dependency, including in hybrid Astro/Svelte/Vue projects; a `--framework` override cannot assert React by itself, and a `no React` task constraint disables React-only routes. No package manager runs and no source scan is performed.

Phrase matching is deterministic; use a route ID from `routes.json` when wording is ambiguous. Framework inference cannot prove that a skill loaded in the host. FAST mode scales concept and QA gates without dropping checks that protect changed behavior. Browser rendering, interaction behavior, accessibility, and visual quality still require the project's actual browser QA workflow.
