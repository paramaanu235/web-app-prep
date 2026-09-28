import { readFileSync, writeFileSync } from 'node:fs';
import { expect, test } from './fixtures';

test('theme choice applies instantly and survives reloads', async ({ page }) => {
  await page.goto('settings/');
  await page.getByRole('group', { name: 'Theme' }).getByRole('button', { name: 'Sepia' }).click();
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'sepia');
  await page.goto('library/');
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'sepia');
  await page.getByRole('link', { name: 'Settings' }).click();
  await page.getByRole('group', { name: 'Theme' }).getByRole('button', { name: 'Dark' }).click();
  await page.getByRole('group', { name: 'Reading font' }).getByRole('button', { name: 'Serif' }).click();
  await page.reload();
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
  await expect(page.locator('html')).toHaveAttribute('data-font', 'serif');
});

test('week edits persist and show on the home page', async ({ page }) => {
  await page.goto('progress/?week=1');
  await page.getByLabel('Completed hours').fill('6.5');
  await page.getByLabel('Completed hours').blur();
  await page.getByLabel('Problems attempted').fill('4');
  await page.getByLabel('Problems attempted').blur();
  await page.getByLabel('Solved independently').fill('3');
  await page.getByLabel('Solved independently').blur();
  await page.getByRole('group', { name: 'Status' }).getByRole('button', { name: 'In Progress' }).click();
  await page.getByLabel('What went well').fill('Clear invariants');
  await page.getByRole('button', { name: 'Log mock interview' }).click();
  await expect(page.getByText('Clear invariants')).toBeVisible();

  await page.goto('');
  await expect(page.locator('.stat').first()).toContainText('6.5');
  await expect(page.locator('.stat').nth(2)).toContainText('In Progress');
});

test('export produces an iOS-compatible backup that imports back', async ({ page }, testInfo) => {
  await page.goto('progress/?week=2');
  await page.getByLabel('Completed hours').fill('3');
  await page.getByLabel('Completed hours').blur();

  await page.goto('settings/');
  const [download] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Export JSON' }).click()]);
  expect(download.suggestedFilename()).toBe('GoogleInterviewPrep_Backup.json');
  const file = testInfo.outputPath('backup.json');
  await download.saveAs(file);
  const json = JSON.parse(readFileSync(file, 'utf8'));
  expect(Array.isArray(json.weeklyProgress)).toBe(true);
  expect(json.weeklyProgress[3].completedHours).toBe(3);
  expect(readFileSync(file, 'utf8')).not.toMatch(/\.\d{3}Z/);

  page.once('dialog', (d) => d.accept());
  await page.getByRole('button', { name: 'Everything' }).click();
  await page.goto('progress/?week=2');
  await expect(page.getByLabel('Completed hours')).toHaveValue('0');

  await page.goto('settings/');
  await page.locator('input[type=file]').setInputFiles(file);
  await expect(page.getByRole('status').first()).toContainText(`${json.dailyChecklist.length} checklist items`);
  await page.getByRole('button', { name: 'Replace my data' }).click();
  await expect(page.getByText('Backup imported.')).toBeVisible();
  await page.goto('progress/?week=2');
  await expect(page.getByLabel('Completed hours')).toHaveValue('3');
});

test('invalid backups are rejected with a reason', async ({ page }, testInfo) => {
  const file = testInfo.outputPath('bad.json');
  writeFileSync(file, JSON.stringify({ version: 2 }));
  await page.goto('settings/');
  await page.locator('input[type=file]').setInputFiles(file);
  await expect(page.getByText('Couldn’t import: Unsupported schema version 2')).toBeVisible();
});
