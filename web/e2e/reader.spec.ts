import { DOCS, expect, test } from './fixtures';

test.use({ permissions: ['clipboard-read', 'clipboard-write'] });

test('table of contents follows scrolling and links jump to sections', async ({ page }) => {
  await page.goto(`docs/${DOCS.patterns}/`);
  const toc = page.locator('.doc-toc');
  await toc.getByRole('link', { name: '4. Builder', exact: true }).click();
  await expect(page).toHaveURL(/#java\.design\.patterns-4-builder$/);
  await expect(page.locator('#java\\.design\\.patterns-4-builder')).toBeInViewport();
  await expect(toc.locator('a[aria-current="true"]')).toHaveText('4. Builder');
});

test('code blocks copy and wrap', async ({ page }) => {
  await page.goto(`docs/${DOCS.patterns}/`);
  const figure = page.locator('figure.code').first();
  await figure.getByRole('button', { name: 'Copy' }).click();
  await expect(figure.getByRole('button', { name: 'Copied' })).toBeVisible();
  const copied = await page.evaluate(() => navigator.clipboard.readText());
  expect(copied).toBe(await figure.locator('pre').innerText());

  const wrap = figure.getByRole('button', { name: 'Wrap' });
  await wrap.click();
  await expect(figure).toHaveClass(/wrap/);
  await expect(wrap).toHaveAttribute('aria-pressed', 'true');
});

test('GitHub-style in-page links resolve to iOS anchors', async ({ page }) => {
  await page.goto(`docs/${DOCS.patterns}/`);
  const hrefs = await page.locator('#doc-content a[href^="#"]').evaluateAll((as) => as.map((a) => a.getAttribute('href')!.slice(1)));
  expect(hrefs.length).toBeGreaterThan(20);
  for (const id of hrefs) expect(await page.locator(`[id="${id}"]`).count(), id).toBe(1);
});

test('bookmarking a section shows it on the Saved page with a note', async ({ page }) => {
  await page.goto(`docs/${DOCS.patterns}/#java.design.patterns-4-builder`);
  const heading = page.locator('#java\\.design\\.patterns-4-builder');
  await heading.hover();
  const bookmark = heading.getByRole('button', { name: 'Bookmark this section' });
  await bookmark.click();
  await expect(bookmark).toHaveAttribute('aria-pressed', 'true');

  await page.goto('saved/');
  await expect(page.getByText('1 bookmark.', { exact: false })).toBeVisible();
  await page.getByRole('button', { name: 'Add note' }).click();
  await page.getByLabel('Note').fill('Revisit telescoping constructors');
  await page.getByRole('button', { name: 'Save note' }).click();
  await expect(page.getByText('Revisit telescoping constructors')).toBeVisible();

  await page.getByRole('link', { name: '4. Builder' }).click();
  await expect(page).toHaveURL(/docs\/java\.design\.patterns\/#java\.design\.patterns-4-builder$/);
  await expect(heading).toBeInViewport();
});

test('keyboard shortcuts move between sections and bookmark', async ({ page }) => {
  await page.goto(`docs/${DOCS.patterns}/`);
  await page.keyboard.press('j');
  await page.keyboard.press('j');
  await expect(page).toHaveURL(/#java\.design\.patterns-/);
  await page.keyboard.press('b');
  await page.goto('saved/');
  await expect(page.locator('.hit-title')).toHaveCount(1);
  await page.goto(`docs/${DOCS.patterns}/`);
  await page.keyboard.press('?');
  await expect(page.getByRole('dialog', { name: 'Keyboard shortcuts' })).toBeVisible();
});

test('mark as read shows in the library', async ({ page }) => {
  await page.goto(`docs/${DOCS.plan}/`);
  await page.getByRole('button', { name: 'Mark as read' }).click();
  await expect(page.getByRole('button', { name: 'Read ✓' })).toBeVisible();
  await page.goto('library/');
  await expect(page.locator(`[data-progress-doc="${DOCS.plan}"] .badge.done`)).toHaveText('Read');
});

test('reading position is offered on return', async ({ page }) => {
  await page.goto(`docs/${DOCS.patterns}/#java.design.patterns-10-decorator`);
  await page.waitForTimeout(1800); // position is saved after 1.5 s
  await page.goto(`docs/${DOCS.patterns}/`);
  const note = page.locator('[data-resume]');
  await expect(note).toBeVisible();
  await expect(note).toContainText('10. Decorator');
  await note.getByRole('link', { name: 'Resume' }).click();
  await expect(page.locator('#java\\.design\\.patterns-10-decorator')).toBeInViewport();
});

test('Java viewer highlights linked lines and outlines symbols', async ({ page }) => {
  await page.goto(`docs/${DOCS.templates}/#java.templates.source-line-120`);
  const line = page.locator('#java\\.templates\\.source-line-120');
  await expect(line).toBeInViewport();
  expect(await line.evaluate((el) => getComputedStyle(el).backgroundColor)).not.toBe('rgba(0, 0, 0, 0)');
  await expect(page.locator('.doc-toc .toc-title')).toHaveText('Outline');
});

test('section deep links (?section=) resolve to anchors', async ({ page }) => {
  await page.goto(`docs/${DOCS.patterns}/?section=java.design.patterns.10-decorator`);
  await expect(page).toHaveURL(/docs\/java\.design\.patterns\/#java\.design\.patterns-10-decorator$/);
});

test('contents sheet and menu work on phones @mobile', async ({ page }) => {
  await page.goto(`docs/${DOCS.patterns}/`);
  await expect(page.locator('.doc-toc')).toBeHidden();
  await page.getByRole('button', { name: 'Contents' }).click();
  const sheet = page.getByRole('dialog', { name: 'Contents' });
  await sheet.getByRole('link', { name: '4. Builder', exact: true }).click();
  await expect(sheet).toBeHidden();
  await expect(page.locator('#java\\.design\\.patterns-4-builder')).toBeInViewport();

  await page.getByRole('button', { name: 'Menu' }).click();
  await page.getByRole('navigation', { name: 'Main' }).getByRole('link', { name: 'Progress' }).click();
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Progress');
});

test('pages never scroll sideways on phones @mobile', async ({ page }) => {
  for (const path of ['', 'library/', 'progress/', 'settings/', `docs/${DOCS.patterns}/`, `docs/${DOCS.templates}/`, 'docs/java.interview.snippets/']) {
    await page.goto(path);
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(overflow, path).toBeLessThanOrEqual(0);
  }
});
