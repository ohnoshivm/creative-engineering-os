# CEOS task routing

`integrations/routes.json` is the source of truth for the 19 deterministic task routes. Run the standard-library CLI from a project and pass its directory explicitly when the shell is elsewhere:

```sh
python3 <ceos-root>/scripts/ceos-route.py "Create a wireframe for the signup flow" --project .
python3 <ceos-root>/scripts/ceos-route.py "Implement a GSAP scroll sequence" --project . --need-secondary
```

The CLI returns one primary capability. It returns one secondary only when `--need-secondary` is requested; every route records the secondary's specific contribution. It does not load skills, dispatch agents, install packages, select a provider, or change settings. An incompatible preferred option is skipped. If the preferred capability is not detected and the next option is available, that option becomes primary; if neither is detected, the preferred compatible option is shown with a status note so the host can verify it.

## Route matrix

The listed order is the preference order. A secondary stays opt-in and its role is written in `routes.json`.

| Task | Primary | Secondary |
|---|---|---|
| Creative concept | CEOS Creative Direction | Impeccable |
| Art direction | CEOS Art Direction | UI/UX Pro Max |
| Design research | UI/UX Pro Max | CEOS reference library |
| Typography and layout | Impeccable | UI/UX Pro Max |
| Wireframes and UX | CEOS Interaction Architecture | UI/UX Pro Max |
| Motion direction | CEOS Motion Direction | GSAP skills |
| GSAP implementation | GSAP skills | CEOS Motion Engineering |
| React animations | React Bits | GSAP skills |
| UI components and forms | shadcn/ui | UI/UX Pro Max |
| Creative interactive elements | React Bits | CEOS Creative Coding |
| Three.js and R3F | pmndrs/examples | CEOS 3D |
| GLSL shaders | CEOS Shader Engineering | pmndrs/examples |
| Frontend architecture | CEOS Frontend Architecture | Superpowers TDD |
| Complex implementation | Superpowers TDD | CEOS Frontend Architecture |
| Debugging and verification | Superpowers verification | Existing project QA |
| Visual critique | Impeccable | CEOS Visual Auditor |
| Browser verification | Existing Playwright tools | Superpowers verification |
| Performance | CEOS Performance Engineering | Existing measurement tools |
| Final release | CEOS Production Quality | Superpowers verification |

Prefer native platform features and existing project conventions when they satisfy the approved direction. A route is a specialist hint, not a reason to add a dependency or framework. The approved project direction takes precedence over generic recommendations.

## Framework and capability detection

- Framework detection reads package names from `dependencies`, `devDependencies`, `peerDependencies`, and `optionalDependencies`, plus framework config filenames. It does not install packages or scan source code.
- A React runtime is considered present only when `react` or `react-dom` is declared in `package.json`. `--framework` can label the framework, but cannot claim a React runtime that package metadata does not show. A `no React` task constraint also disables React-only options.
- React Bits, shadcn/ui, and pmndrs/examples require an existing React runtime. React-first routes include concrete vanilla/native fallback guidance; the router never recommends adding React to satisfy a route.
- Skill availability checks exact directory names in the CEOS checkout, project skill directories, and standard local agent skill directories. Repository-local integration paths and existing browser/performance tool paths are checked directly. Provider configuration, credentials, skill contents, and backups are never read.
- Plugin-only capabilities without a discoverable skill directory can be declared with repeated `--available <capability-id>` flags. When supplied, this list replaces filesystem discovery for that invocation. Route IDs and capability IDs are in `routes.json`.
- Natural-language matching is deterministic phrase matching. Use `--task-id <route-id>` when the task wording is ambiguous.

## Work modes

- **FAST**: one local change, such as a spacing, color, or type-size fix. Inspect the affected state and run relevant checks. Skip concept options, owner approvals, signature-moment prototypes, and broad QA unless scope expands. Keep the validation, error handling, accessibility, keyboard/focus, reduced-motion, and security checks that the changed code touches.
- **STANDARD**: the default for a feature or page. Use only applicable CEOS stages, inspect changed behavior in a real browser, and run relevant quality checks.
- **FLAGSHIP**: a launch, rebrand, immersive site, or similarly high-impact scope. Run the full applicable path: research; distinct concepts and owner decision; art direction, UX, motion, and architecture as needed; a desktop-and-phone signature prototype before bulk sections; build; responsive browser QA; independent critique; technical review; refinement; and production-artifact/rollback verification.

Escalate FAST when behavior, multiple states, dependencies, or brand direction are involved. Escalate STANDARD for a launch or rebrand, shared multi-route system, immersive signature moment, or multi-team handoff. A user-specified `--mode` override takes precedence.

## Orchestration ownership

CEOS owns creative orchestration and direction. Existing project or global engineering policy owns engineering orchestration; where that policy uses gstack, gstack remains the engineering orchestrator and Superpowers is limited to TDD and verification. Never run two automatic orchestrators. The router only recommends; the host agent must follow the active project policy.

## Limits

The router cannot prove that a host loaded a skill or that the current project policy permits a tool. It cannot verify visual output, interactions, accessibility, or performance. Those still require the project's actual browser and quality checks. FAST changes avoid broad concept gates, not checks required by the changed behavior or explicit user/project instructions.
