import { describe, expect, it } from 'vitest';
import { loadManifest, readSource, sectionise } from '../src/content-pipeline';
import { SearchEngine } from '../src/lib/search/engine';
import type { WebSearchEntry } from '../src/content-pipeline/types';

const manifest = loadManifest();
const entries: WebSearchEntry[] = manifest.documents.flatMap((doc) =>
  sectionise(doc, readSource(doc).text).sections.map((s) => ({
    d: doc.id, s: s.id, t: s.title, a: s.anchor, c: doc.categoryIDs, f: doc.format, h: doc.isHistorical, k: s.tokens, p: s.preview, x: s.plainText,
  })),
);
const engine = new SearchEngine(entries, Object.fromEntries(manifest.documents.map((d) => [d.id, d.title])));

describe('search', () => {
  // Smoke vocabulary from build_content.swift.
  it.each(['FETCH_PEERS', 'OAuth2PasswordBearer', 'spring-boot-starter-webmvc', 'reverseKGroup', 'minimum covering window', 'Union-Find', 'Bigtable', 'BigQuery', 'Googleyness', 'STAR', 'Java 17', 'Visitor'])(
    'finds "%s"',
    (term) => expect(engine.search(term).length).toBeGreaterThan(0),
  );

  it('ranks the exact code identifier first', () => {
    const [top] = engine.search('select_for_update');
    expect(top!.entry.x.toLowerCase()).toContain('select_for_update');
  });

  it('points Java hits at the matching line', () => {
    const hit = engine.search('kthLargestHeap', { format: 'java' })[0];
    expect(hit?.anchor).toMatch(/-line-\d+$/);
  });

  it('hides historical documents unless asked', () => {
    const historical = entries.filter((e) => e.h).map((e) => e.d);
    expect(engine.search('python').some((h) => historical.includes(h.entry.d))).toBe(false);
    expect(engine.search('python', { includeHistorical: true }).some((h) => historical.includes(h.entry.d))).toBe(true);
  });
});
