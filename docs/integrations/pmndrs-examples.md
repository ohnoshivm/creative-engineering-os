# PMNDRS Examples

## Source and scope

The searchable reference index is generated from the official [pmndrs/examples](https://github.com/pmndrs/examples) repository, pinned at [`9905cd7b3d030a0ba5c6d327e15fe30ab648abb6`](https://github.com/pmndrs/examples/tree/9905cd7b3d030a0ba5c6d327e15fe30ab648abb6). The source repository is MIT licensed. During verification, upstream `main` had advanced to `541599ac5ad913de85796403c1c6927ada3b303c`; the index remains on the reviewed pin until a newer commit is deliberately reviewed.

[`integrations/indexes/pmndrs-examples.json`](../../integrations/indexes/pmndrs-examples.json) contains 200 examples with a non-empty `package.json` `scripts.dev` command. Each entry carries its upstream `pmndrs.json` title, description, technique tags, libraries, authors, source, published date, notes and asset attribution, plus package name/version, dev command and exact runtime/development dependency ranges from `package.json`. The top-level `license` is the repository's MIT code license; each upstream asset record retains its own creator, source, license and notes.

The repository-local PMNDRS capability skill points agents to this index. The index itself does not install packages or change client settings, and it does not verify every listed example by building it. Search by `tags`, `libraries`, `authors`, dependency name, input signal or title when a task needs a concrete R3F implementation reference or a pmndrs technique example.

## Derived fields

The generator only derives `input`, `complexity`, `renderer` and `vanilla_portability`:

- `input` maps upstream tags to broad signals: interaction/event/raycast/selection/annotation/autofocus/highlight/intersection tags map to `pointer`; `scroll` and `audio` map directly; `controls` and `game` remain unspecified; entries without a mapped tag are `not-tagged`. It does not inspect event handlers or infer keyboard controls from source code.
- `complexity` is a metadata triage estimate. `high` means a high-cost technique tag (`bvh`, `custom-renderer`, `gpgpu`, `physics`, `postprocessing`, `shader`, `ssgi`, `ssr`, or `webgpu`) or at least five related libraries; `medium` means at least four tags or at least four related libraries; otherwise it is `low`. This is not a code-size, performance or runtime measurement.
- `renderer` is `r3f` when `@react-three/fiber` appears in the runtime dependencies or related libraries, `vanilla-three` when only a Three.js runtime is declared, and `other-or-unknown` otherwise. `vanilla_portability` is `rewrite-required` for R3F, `native` for vanilla Three.js, and `unclassified` otherwise.

All 200 indexed entries currently classify as R3F and require adaptation to vanilla Three.js. The upstream tags and package declarations are authoritative; these derived fields are only a first-pass search aid.

## Regenerate

Use Python 3 and Git; the generator uses only the standard library. The source checkout must have the exact pinned revision, official Git origin and no tracked changes.

```sh
git clone --filter=blob:none --no-checkout https://github.com/pmndrs/examples.git /path/to/pmndrs-examples
git -C /path/to/pmndrs-examples fetch --depth=1 origin 9905cd7b3d030a0ba5c6d327e15fe30ab648abb6
git -C /path/to/pmndrs-examples checkout --detach 9905cd7b3d030a0ba5c6d327e15fe30ab648abb6
git -C /path/to/pmndrs-examples sparse-checkout init --no-cone
git -C /path/to/pmndrs-examples sparse-checkout set --no-cone '/LICENSE' '/schemas/pmndrs.schema.json' '/examples/*/pmndrs.json' '/examples/*/package.json'
python3 scripts/integrations/pmndrs_examples_index.py --source /path/to/pmndrs-examples
```

The generator refuses another revision, a different origin, tracked source edits, or an unexpected entry count. It emits sorted UTF-8 JSON without a generated timestamp, so the same pinned checkout produces byte-identical output. The upstream repo is a workspace; inspect the selected example's scripts and dependencies before installing anything. Do not install the whole example set or add runtime packages globally.

To update, review a specific upstream commit and its repository and asset licenses, change the generator's revision and expected inventory, regenerate the index, rerun its test, and update this evidence record. There is no floating-branch update.

## Verification

- The sparse, shallow/blobless review checkout is clean at the recorded revision. The upstream `LICENSE` says MIT and the pinned `schemas/pmndrs.schema.json` was reviewed.
- The index contains 200 unique slugs, each backed by both metadata files and a non-empty `scripts.dev` command. The generator was run twice to separate output files; both compared byte-for-byte with the checked-in index (SHA-256 `69c7487b6c2f5e05acda86f2f770d5dd67a0ec7fd0d3d90cce45e842f2720b19`). The deterministic derivation test passes with `python3 tests/integrations/pmndrs_examples_index_test.py`.
- One small source example, `examples/basic-example`, was copied to an isolated validation directory. Its metadata, package file, HTML entry, React entry, scene, CSS, TypeScript configs and Vite config match the pinned source byte-for-byte. It has no model or texture assets (`assets: []`) and draws two boxes using R3F.
- Dependencies for that isolated copy were installed locally with lifecycle scripts disabled. `npm run build` passed `tsc` and Vite production bundling. Vite reported a 1,122.92 kB minified JavaScript chunk, above its 500 kB warning threshold.
- The production preview rendered in headless Chromium 155 at 1280×800. Playwright observed a live WebGL2 context (`WebGL 2.0 (OpenGL ES 3.0 Chromium)`) on an Apple M3 Metal renderer through ANGLE. Clicking the first box at (500, 400) enlarged it and changed it from orange to pink. All requested files returned HTTP 200, there were zero JavaScript errors, and the only console warning was the upstream `THREE.Clock` deprecation. Captures and logs are under the state reports directory recorded in the evidence JSON.

## Limitations and rollback

Only `basic-example` was built and exercised in a browser; the other 199 entries are indexed from source metadata and package scripts, not individually run. The browser check covers one desktop viewport and one interaction, not mobile, reduced-motion, no-WebGL, performance, or other hardware. The build warning indicates a large bundle for this one example. Asset records preserve upstream attribution but are not an independent rights audit; some upstream projects may have incomplete asset metadata. The input and complexity fields are intentionally heuristic.

To roll back the index work, remove only this guide, its evidence and index JSON, `scripts/integrations/pmndrs_examples_index.py`, and `tests/integrations/pmndrs_examples_index_test.py`. The source and validation checkouts are outside the CEOS repository; no client settings, provider registrations, runtime packages, or shared routing files were changed.
