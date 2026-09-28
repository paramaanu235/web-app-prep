import { expect, test } from './fixtures';

test('palette opens with / and navigates to a code identifier', async ({ page }) => {
  await page.goto('');
  await page.keyboard.press('/');
  const palette = page.getByRole('dialog', { name: 'Search' });
  await expect(palette).toBeVisible();
  await palette.getByRole('combobox').fill('select_for_update');
  const first = palette.getByRole('option').first();
  await expect(first).toContainText('select_for_update');
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/docs\/django\.cheatsheet\/#django\.cheatsheet-/);
});

test('palette opens with the header button and ⌘K / Ctrl+K', async ({ page }) => {
  await page.goto('library/');
  await page.getByRole('button', { name: /Search/ }).click();
  await expect(page.getByRole('dialog', { name: 'Search' })).toBeVisible();
  await page.keyboard.press('Escape');
  await page.keyboard.press('ControlOrMeta+k');
  await expect(page.getByRole('dialog', { name: 'Search' })).toBeVisible();
});

test('search page filters by format and keeps the query in the URL', async ({ page }) => {
  await page.goto('search/?q=PriorityQueue');
  await expect(page.getByRole('searchbox')).toHaveValue('PriorityQueue');
  await expect(page.getByRole('status')).toContainText('results');
  await page.getByLabel('Format').selectOption('java');
  const hits = page.locator('a.hit');
  await expect(hits.first()).toBeVisible();
  for (const href of await hits.evaluateAll((as) => as.map((a) => a.getAttribute('href')))) {
    expect(href).toMatch(/docs\/java\.templates\.(source|test)\/#.*-line-\d+$/);
  }
  await page.getByRole('searchbox').fill('Googleyness');
  await expect(page).toHaveURL(/\?q=Googleyness$/);
});
