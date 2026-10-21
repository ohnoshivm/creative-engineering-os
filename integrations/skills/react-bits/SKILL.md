---
name: react-bits
description: Find and install animated or interactive React Bits components for React, Next.js, or Vite React projects; do not use for non-React sites or merely because the library exists.
---

# React Bits

Use this only when a specific animated or interactive component serves the project. Inspect the pinned source at `~/creative-engineering-os-upstreams/react-bits`, revision `e12c22192ac7b4b452c5e2feb9b586d74765d696`. If a source file is absent from the sparse checkout, read that single file at the pinned revision through GitHub's contents API; do not change the checkout.

The official variants end in `JS-CSS`, `JS-TW`, `TS-CSS`, or `TS-TW`. Install into the project with either documented command:

```sh
npx shadcn@latest add @react-bits/<Component>-TS-TW
npx jsrepo@latest add https://reactbits.dev/r/<Component>-TS-TW
```

Replace the component and variant with the matching official registry entry. Use the project's package runner where appropriate; do not install jsrepo globally. Read the added source and dependencies, and check keyboard access, focus behavior, accessibility, and `prefers-reduced-motion` for each component.

Do not use this for non-React sites or to add motion simply because React Bits is available.
