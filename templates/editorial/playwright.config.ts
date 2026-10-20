import { defineConfig, devices } from '@playwright/test';

// Uses the installed Google Chrome (channel: 'chrome') so no browser download is needed.
export default defineConfig({
  testDir: 'tests',
  fullyParallel: true,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: { baseURL: 'http://localhost:4321', channel: 'chrome', trace: 'retain-on-failure' },
  webServer: { command: 'npm run build && npm run preview', url: 'http://localhost:4321', reuseExistingServer: false, timeout: 120_000 },
  projects: [
    { name: 'desktop', use: { ...devices['Desktop Chrome'], channel: 'chrome', viewport: { width: 1440, height: 900 } } },
    { name: 'mobile', use: { ...devices['Pixel 7'], channel: 'chrome' } },
    { name: 'reduced-motion', use: { ...devices['Desktop Chrome'], channel: 'chrome', reducedMotion: 'reduce' } },
    { name: 'no-js', use: { ...devices['Desktop Chrome'], channel: 'chrome', javaScriptEnabled: false } },
  ],
});
