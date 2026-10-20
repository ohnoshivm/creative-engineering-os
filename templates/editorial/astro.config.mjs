import { defineConfig } from 'astro/config';

// Static output: every page is HTML on disk; JS ships only where a <script> asks for it.
export default defineConfig({
  output: 'static',
  build: { inlineStylesheets: 'auto' },
});
