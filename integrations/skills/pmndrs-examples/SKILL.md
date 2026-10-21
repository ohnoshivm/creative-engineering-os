---
name: pmndrs-examples
description: Search and adapt pinned pmndrs examples for Three.js, React Three Fiber, drei, or WebGL scene work; use only when implementing those renderers.
---

# pmndrs examples

Use the pinned reference checkout at `~/creative-engineering-os-upstreams/pmndrs-examples`.
Search its curated index first: `integrations/indexes/pmndrs-examples.json`.

For example, search tags, libraries, titles, and descriptions with:

```sh
jq -r '.examples[] | select((.tags + .libraries | join(" ")) | test("shader|gltf|physics|controls"; "i")) | [.slug, .path, .title] | @tsv' integrations/indexes/pmndrs-examples.json
```

Read only the matching example's source and the files it directly needs. Copy one example into the project when useful, then adapt it to that project's versions and structure. Keep dependencies project-scoped; never install example dependencies globally or modify the pinned checkout or index.
