import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    target: 'es2022',
    // three.js is ~530 KB min / 130 KB gz in its own lazily loaded chunk; that is expected.
    chunkSizeWarningLimit: 600,
    rollupOptions: {
      output: {
        // three.js in its own chunk: loaded only after first paint, only when WebGL is available.
        manualChunks: (id) => (id.includes('node_modules/three') ? 'three' : undefined),
      },
    },
  },
});
