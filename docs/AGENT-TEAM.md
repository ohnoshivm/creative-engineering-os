# Studio roles and handoffs

A small project can apply roles inline. Delegate only independent work through supported native or T3 child-task APIs; a top-level conversation is not a child task. Choose live available providers/models, preserve existing auth/routing and avoid billing changes. One integration owner owns merging and final evidence.

| Role | Ownership | Skills |
|---|---|---|
| Creative director | Brief, references, original concept and approval | ceos-creative-direction |
| UX architect | IA, journeys, keyboard/touch/states | ceos-interaction-architecture |
| Art and motion director | Type/grid/palette/material, motion spec | ceos-art-direction, ceos-motion-direction |
| Frontend architect | Stack, state/frame/scroll ownership, integration | ceos-frontend-architecture |
| Graphics/shader engineer | Geometry/materials/shaders/assets | ceos-realtime-3d, ceos-shader-engineering, ceos-3d-asset-pipeline, ceos-creative-coding |
| Quality/performance engineer | Browser evidence, access and measured budgets | ceos-production-quality, ceos-performance-engineering |
| Independent auditor | Critique of actual output against approved direction | ceos-visual-audit |

The bundle registers the creative-auditor adapter for Claude/OpenCode. Other rows are portable role briefs, not a claim that every host supports named subagent registration. Use the role/skills in a supported child prompt or inline. This avoids silently overwriting existing specialist agents.

Handoffs contain the artifact/commit, decisions, constraints, open questions, exit gate, owned paths and paths that must not be edited. Never give two concurrent agents the same files. The auditor does not fix its own review target: owner supplies captures and persists the returned report; write/edit/shell tools are restricted. Plugin/MCP access and tool policies are not an OS sandbox.
