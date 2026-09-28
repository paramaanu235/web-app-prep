// Lighthouse audit for the main pages.
//   node scripts/lighthouse.mjs [baseUrl] [--desktop] [--min=95] [--skip-perf]
// Defaults to the local preview server. Exits non-zero when a score is below --min.
// --skip-perf leaves performance out of the pass/fail check (shared CI runners make it noisy).
import { chromium } from '@playwright/test';
import * as chromeLauncher from 'chrome-launcher';
import lighthouse from 'lighthouse';
import desktopConfig from 'lighthouse/core/config/desktop-config.js';

const args = process.argv.slice(2);
const base = args.find((a) => !a.startsWith('--')) ?? 'http://localhost:4322/web-app-prep/';
const desktop = args.includes('--desktop');
const min = Number(args.find((a) => a.startsWith('--min='))?.slice(6) ?? 95);
const skipPerf = args.includes('--skip-perf');
const PAGES = ['', 'library/', 'docs/java.design.patterns/', 'docs/java.templates.source/', 'progress/', 'search/?q=heap', 'settings/'];
const CATEGORIES = ['performance', 'accessibility', 'best-practices', 'seo'];

const chrome = await chromeLauncher.launch({ chromePath: chromium.executablePath(), chromeFlags: ['--headless=new', '--no-sandbox'] });
let failed = false;
try {
  console.log(`${desktop ? 'Desktop' : 'Mobile'} · ${base}\n`);
  console.log(['page'.padEnd(34), ...CATEGORIES.map((c) => c.slice(0, 12).padStart(13))].join(''));
  for (const path of PAGES) {
    const result = await lighthouse(base + path, { port: chrome.port, output: 'json', logLevel: 'error', onlyCategories: CATEGORIES }, desktop ? desktopConfig : undefined);
    const scores = CATEGORIES.map((c) => Math.round((result.lhr.categories[c]?.score ?? 0) * 100));
    const low = CATEGORIES.filter((c, i) => scores[i] < min && !(skipPerf && c === 'performance'));
    if (low.length) failed = true;
    console.log(['/' + path.padEnd(33), ...scores.map((s) => String(s).padStart(13))].join('') + (low.length ? `   ✗ ${low.join(', ')}` : ''));
    for (const c of low) {
      for (const ref of result.lhr.categories[c].auditRefs) {
        const audit = result.lhr.audits[ref.id];
        if (ref.weight > 0 && audit.score !== null && audit.score < 0.9) console.log(`      ${c}: ${audit.id} — ${audit.title}${audit.displayValue ? ` (${audit.displayValue})` : ''}`);
      }
    }
  }
} finally {
  await chrome.kill();
}
process.exit(failed ? 1 : 0);
