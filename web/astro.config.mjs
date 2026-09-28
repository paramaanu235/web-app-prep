// @ts-check
import { defineConfig } from 'astro/config';
import preact from '@astrojs/preact';

// Hosted on GitHub Pages as a project site: https://paramaanu235.github.io/web-app-prep/
export default defineConfig({
  site: 'https://paramaanu235.github.io',
  base: '/web-app-prep',
  trailingSlash: 'always',
  integrations: [preact()],
  build: { format: 'directory' },
});
