import { DOCS, expect, test } from './fixtures';

test('pages and search keep working offline after the first visit', async ({ page, context }) => {
  await page.goto('');
  // Wait until the service worker has installed and precached everything.
  await page.evaluate(async () => {
    const reg = await navigator.serviceWorker.ready;
    if (!navigator.serviceWorker.controller) {
      await new Promise((resolve) => navigator.serviceWorker.addEventListener('controllerchange', resolve, { once: true }));
    }
    return reg.active?.state;
  });
  // Load a page so its hashed JS/CSS land in the runtime cache.
  await page.goto(`docs/${DOCS.quickRef}/`);

  await context.setOffline(true);
  await page.goto(`docs/${DOCS.templates}/`);
  await expect(page.locator('#doc-content .line').first()).toBeVisible();
  await page.goto('library/');
  await expect(page.locator('a.doc-row')).toHaveCount(18);

  await page.keyboard.press('/');
  await page.getByRole('combobox').fill('Union-Find');
  await expect(page.getByRole('option').first()).toBeVisible();
  await context.setOffline(false);
});
