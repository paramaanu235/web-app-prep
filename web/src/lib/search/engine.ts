// Port of ios/.../Services/SearchService.swift `performSearch`, so the same
// query ranks the same sections on web and iOS.
import type { WebSearchEntry } from '../../content-pipeline/types';

export interface SearchFilters {
  category?: string | null;
  format?: string | null;
  includeHistorical?: boolean;
}

export interface SearchHit {
  entry: WebSearchEntry;
  docTitle: string;
  anchor: string;
  snippet: string;
  score: number;
}

interface Prepared extends WebSearchEntry {
  titleLower: string;
  docTitleLower: string;
  textLower: string;
  tokensLower: string[];
}

export class SearchEngine {
  private entries: Prepared[];
  private docTitles: Record<string, string>;

  constructor(entries: WebSearchEntry[], docTitles: Record<string, string>) {
    this.entries = entries.map((e) => ({
      ...e,
      titleLower: e.t.toLowerCase(),
      docTitleLower: (docTitles[e.d] ?? '').toLowerCase(),
      textLower: e.x.toLowerCase(),
      tokensLower: e.k.map((k) => k.toLowerCase()),
    }));
    this.docTitles = docTitles;
  }

  search(query: string, filters: SearchFilters = {}, limit = 60): SearchHit[] {
    const trimmed = query.trim();
    if (!trimmed) return [];
    const lower = trimmed.toLowerCase();
    const queryTokens = lower.split(/[^\p{L}\p{M}\p{N}]+/u).filter(Boolean);
    const hits: SearchHit[] = [];

    for (const e of this.entries) {
      if (!filters.includeHistorical && e.h) continue;
      if (filters.category && !e.c.includes(filters.category)) continue;
      if (filters.format && e.f !== filters.format.toLowerCase()) continue;

      let score = 0;
      if (e.titleLower === lower || e.docTitleLower === lower) score += 150;
      else if (e.titleLower.includes(lower)) score += 80;
      else if (e.docTitleLower.includes(lower)) score += 40;

      const phraseAt = e.textLower.indexOf(lower);
      if (phraseAt >= 0) score += 60;

      if (queryTokens.length && queryTokens.every((q) => e.titleLower.includes(q) || e.textLower.includes(q) || e.k.includes(q))) {
        score += 50;
      }

      for (let i = 0; i < e.k.length; i++) {
        const tokenLower = e.tokensLower[i]!;
        if (e.k[i] === trimmed || tokenLower === lower) score += 50;
        else if (tokenLower.includes(lower)) score += 20;
      }
      if (score <= 0) continue;

      let snippet = e.p;
      if (phraseAt >= 0) {
        const start = Math.max(0, phraseAt - 50);
        const end = Math.min(e.x.length, phraseAt + trimmed.length + 70);
        snippet = (start > 0 ? '…' : '') + e.x.slice(start, end).replaceAll('\n', ' ') + (end < e.x.length ? '…' : '');
      }

      let anchor = e.a;
      if (e.f === 'java') {
        let at = phraseAt;
        if (at < 0) {
          const first = queryTokens.find((q) => e.textLower.includes(q));
          at = first ? e.textLower.indexOf(first) : -1;
        }
        const offset = at >= 0 ? e.x.slice(0, at).split('\n').length - 1 : 0;
        const base = Number(e.a.match(/-line-(\d+)$/)?.[1] ?? 1);
        anchor = `${e.d}-line-${base + offset}`;
      }

      hits.push({ entry: e, docTitle: this.docTitles[e.d] ?? e.d, anchor, snippet: snippet.trim(), score });
    }

    hits.sort((a, b) => b.score - a.score);
    return hits.slice(0, limit);
  }
}

let enginePromise: Promise<SearchEngine> | undefined;

/** Lazily fetches the prebuilt index (src/pages/search-index.json.ts) on first use. */
export function loadEngine(base: string): Promise<SearchEngine> {
  enginePromise ??= fetch(`${base}search-index.json`)
    .then((r) => {
      if (!r.ok) throw new Error(`Search index request failed (${r.status})`);
      return r.json() as Promise<{ docs: Record<string, string>; entries: WebSearchEntry[] }>;
    })
    .then((data) => new SearchEngine(data.entries, data.docs))
    .catch((err) => {
      enginePromise = undefined;
      throw err;
    });
  return enginePromise;
}
