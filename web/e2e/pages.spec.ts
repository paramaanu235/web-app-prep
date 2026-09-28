import { readFileSync } from 'node:fs';
import { DOCS, expect, test } from './fixtures';

const manifest = JSON.parse(
  readFileSync(new URL('../../ios/GoogleInterviewPrep/GoogleInterviewPrep/Resources/ContentManifest.json', import.meta.url), 'utf8'),
) as { documents: { id: string; title: string }[] };

const APP_PAGES = [
  ['', /^Week \d+ of 12$/],
  ['library/', 'Library'],
  ['progress/', 'Progress'],
  ['saved/', 'Saved'],
  ['search/', 'Search'],
  ['settings/', 'Settings'],
] as const;

for (const [path, heading] of APP_PAGES) {
  test(`/${path} renders`, async ({ page }) => {
    await page.goto(path);
    await expect(page.getByRole('heading', { level: 1 })).toHaveText(heading);
  });
}

test('every document renders with its sections', async ({ page }) => {
  for (const doc of manifest.documents) {
    const res = await page.goto(`docs/${doc.id}/`);
    expect(res?.status(), doc.id).toBe(200);
    await expect(page).toHaveTitle(`${doc.title} · Interview Prep`);
    await expect(page.locator('#doc-content')).not.toBeEmpty();
    expect(await page.locator('.doc-toc .toc a').count(), `${doc.id} TOC`).toBeGreaterThan(0);
  }
});

test('library lists all 18 documents and links resolve', async ({ page }) => {
  await page.goto('library/');
  const rows = page.locator('a.doc-row');
  await expect(rows).toHaveCount(manifest.documents.length);
  await rows.first().click();
  await expect(page).toHaveURL(new RegExp(`docs/${DOCS.quickRef}/$`));
});

test('unknown paths show the 404 page', async ({ page, consoleErrors }) => {
  const res = await page.goto('no-such-page/');
  expect(res?.status()).toBe(404);
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Page not found');
  consoleErrors.length = 0; // the 404 response itself is logged as a resource error
});
