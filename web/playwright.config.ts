import { defineConfig, devices } from '@playwright/test';

const PORT = 4322;
// Set E2E_BASE_URL (e.g. https://paramaanu235.github.io/web-app-prep/) to test a deployed site.
const REMOTE = process.env.E2E_BASE_URL;

// By default runs against the production build (`astro preview`) so the service
// worker and base path behave as they do on GitHub Pages.
export default defineConfig({
  testDir: 'e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [['github'], ['list']] : 'list',
  use: {
    baseURL: REMOTE ?? `http://localhost:${PORT}/web-app-prep/`,
    trace: 'retain-on-failure',
  },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'], viewport: { width: 1440, height: 900 } }, grepInvert: /@mobile/ },
    { name: 'mobile', use: { ...devices['Pixel 7'] }, grep: /@mobile/ },
  ],
  webServer: REMOTE
    ? undefined
    : {
        command: `npm run build && npx astro preview --port ${PORT} --ignore-lock`,
        url: `http://localhost:${PORT}/web-app-prep/`,
        reuseExistingServer: !process.env.CI,
        timeout: 180_000,
      },
});
