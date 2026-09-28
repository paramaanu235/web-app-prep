import { test as base, expect } from '@playwright/test';

/** Fails any test whose page logs a console error or throws. */
export const test = base.extend<{ consoleErrors: string[] }>({
  consoleErrors: [
    async ({ page }, use) => {
      const errors: string[] = [];
      page.on('console', (msg) => msg.type() === 'error' && errors.push(msg.text()));
      page.on('pageerror', (err) => errors.push(err.message));
      await use(errors);
      expect(errors, 'console errors').toEqual([]);
    },
    { auto: true },
  ],
});

export { expect };

export const DOCS = {
  patterns: 'java.design.patterns',
  templates: 'java.templates.source',
  plan: 'codex.primary.plan',
  quickRef: 'quick.reference',
};
