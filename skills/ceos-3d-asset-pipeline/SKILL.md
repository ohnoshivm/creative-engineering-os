---
name: ceos-3d-asset-pipeline
description: Produces web-ready 3D assets — Blender modelling/lookdev hand-off, baking lighting/AO, glTF/GLB export, optimisation with glTF-Transform and meshoptimizer (gltfpack), Draco/meshopt geometry compression, KTX2/Basis texture compression, animation export, and per-asset size/performance budgets. Use when bringing models or textures into a website, when a GLB is too large or slow to load, when exporting from Blender, or when setting asset budgets for a 3D site.
---

# 3D asset production pipeline

## Tools on this machine

- Blender 5.2 LTS (`/opt/homebrew/bin/blender`, Homebrew cask) — headless scripting: `blender -b file.blend --python script.py`.
- `@gltf-transform/cli` and `gltfpack` — project dev dependencies in the immersive-3d and experimental templates
  (`npm run assets:optimize`). Not installed globally on purpose.
- KTX-Software (`ktx`/`toktx`) — **not installed** (no Homebrew formula; official macOS installer is an admin .pkg).
  Install manually from github.com/KhronosGroup/KTX-Software/releases if KTX2 is needed; gltf-transform's `uastc`/
  `etc1s` commands require it. Meanwhile use WebP textures (`gltf-transform webp`) which need no extra binary.

## Pipeline

1. **Model for the camera**: polycount where silhouettes need it, flat where they don't; real-world scale (1 unit =
   1 m), +Y up, applied transforms, clean normals, UVs without overlap where baking.
2. **Lookdev in Blender** with the same environment intent as the web scene; keep materials glTF-compatible
   (Principled BSDF → glTF PBR: base colour, metallic/roughness, normal, emission, transmission, clearcoat, sheen,
   iridescence extensions).
3. **Bake** what is static (AO, lightmaps, complex shading) into textures; pack ORM (occlusion/roughness/metallic) in one texture.
4. **Export glTF 2.0 (.glb)**: +Y up, selected objects, apply modifiers, include only needed attributes.
5. **Optimise**:
   ```bash
   npx gltf-transform inspect in.glb                      # report sizes, draw calls
   npx gltf-transform optimize in.glb out.glb \
     --compress meshopt --texture-compress webp --texture-size 2048   # dedup, prune, weld, simplify, instance, compress
   npx gltfpack -i in.glb -o out.glb -cc -tc              # alternative: meshopt + (KTX2 if toktx present)
   ```
6. **Load** with `GLTFLoader` + `MeshoptDecoder` (or `DRACOLoader`) + `KTX2Loader` (if KTX2). Lazy-load per section.

## Budgets (starting point; agree per project)

| Asset | Desktop | Mobile |
|---|---|---|
| Hero model (compressed) | ≤ 1.5 MB | ≤ 0.8 MB |
| All 3D on first view | ≤ 3 MB | ≤ 1.5 MB |
| Texture max size | 2048² | 1024² |
| Triangles in view | ≤ 500k | ≤ 150k |
| Draw calls | ≤ 100 | ≤ 50 |

## Verification

`gltf-transform inspect` before/after table in the PR; the model renders identically (screenshot diff at fixed
camera) after optimisation; network panel shows sizes; load time measured from archive/throttled profile.

## Failure criteria

Shipping the raw Blender export; 4K textures on phones; unapplied scale (objects 100× size); duplicated materials
per mesh; uncompressed geometry > 1 MB; assets loaded before first paint that aren't needed for it.
