import AxeBuilder from '@axe-core/playwright';
import { DOCS, expect, test } from './fixtures';

const PAGES = ['', 'library/', 'progress/', 'saved/', 'search/?q=heap', 'settings/', `docs/${DOCS.patterns}/`, `docs/${DOCS.templates}/`, 'docs/spring.boot.cheatsheet/'];

for (const theme of ['light', 'dark', 'sepia'] as const) {
  test.describe(`${theme} theme`, () => {
    test.beforeEach(async ({ page }) => {
      await page.goto('settings/');
      await page.getByRole('group', { name: 'Theme' }).getByRole('button', { name: theme, exact: false }).click();
      await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
    });

    for (const path of PAGES) {
      test(`/${path} has no WCAG A/AA violations`, async ({ page }) => {
        await page.goto(path);
        await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
        await expect(page.locator('[aria-busy="true"]')).toHaveCount(0);
        const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
        const summary = results.violations.map((v) => `${v.id} (${v.impact}): ${v.nodes.length} × ${v.nodes[0]?.target.join(' ')}`);
        expect(summary).toEqual([]);
      });
    }
  });
}

test('search palette is accessible when open', async ({ page }) => {
  await page.goto('');
  await page.keyboard.press('/');
  await page.getByRole('combobox').fill('heap');
  await page.getByRole('option').first().waitFor();
  const results = await new AxeBuilder({ page }).include('dialog.palette').withTags(['wcag2a', 'wcag2aa']).analyze();
  expect(results.violations.map((v) => v.id)).toEqual([]);
});
