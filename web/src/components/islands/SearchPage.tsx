import { useEffect, useMemo, useState } from 'preact/hooks';
import { loadEngine, type SearchEngine } from '../../lib/search/engine';
import { Highlight } from './Highlight';
import { useDebounced } from './hooks';

interface Props {
  base: string;
  categories: { id: string; name: string }[];
}

export default function SearchPage({ base, categories }: Props) {
  const [engine, setEngine] = useState<SearchEngine | null>(null);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');
  const [category, setCategory] = useState('');
  const [format, setFormat] = useState('');
  const [includeHistorical, setIncludeHistorical] = useState(false);
  const debounced = useDebounced(query, 120);

  useEffect(() => {
    setQuery(new URLSearchParams(location.search).get('q') ?? '');
    loadEngine(base).then(setEngine, (e: Error) => setError(e.message));
  }, []);

  useEffect(() => {
    const url = debounced.trim() ? `?q=${encodeURIComponent(debounced.trim())}` : location.pathname;
    history.replaceState(null, '', url);
  }, [debounced]);

  const hits = useMemo(
    () => (engine ? engine.search(debounced, { category: category || null, format: format || null, includeHistorical }) : []),
    [engine, debounced, category, format, includeHistorical],
  );

  return (
    <div class="page page-narrow">
      <header class="page-header">
        <h1>Search</h1>
        <p>Matches titles, prose and code identifiers like <code>select_for_update</code> or <code>@Transactional</code>.</p>
      </header>
      <div class="stack" style={{ marginBottom: '24px' }}>
        <input type="search" aria-label="Search query" placeholder="Search…" value={query} autoFocus onInput={(e) => setQuery(e.currentTarget.value)} style={{ fontSize: '17px', padding: '12px 14px' }} />
        <div class="row">
          <select aria-label="Category" value={category} onChange={(e) => setCategory(e.currentTarget.value)} style={{ width: 'auto' }}>
            <option value="">All categories</option>
            {categories.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
          <select aria-label="Format" value={format} onChange={(e) => setFormat(e.currentTarget.value)} style={{ width: 'auto' }}>
            <option value="">All formats</option>
            <option value="markdown">Notes</option>
            <option value="java">Java source</option>
          </select>
          <label class="row" style={{ fontSize: '14px', gap: '6px' }}>
            <input type="checkbox" checked={includeHistorical} onChange={(e) => setIncludeHistorical(e.currentTarget.checked)} /> Include historical
          </label>
        </div>
      </div>

      {error ? (
        <p class="notice error">Search is unavailable: {error}</p>
      ) : !debounced.trim() ? null : !engine ? (
        <p class="muted">Loading index…</p>
      ) : hits.length === 0 ? (
        <p class="empty">No matches for “{debounced}”.</p>
      ) : (
        <>
          <p class="muted" style={{ fontSize: '14px' }} role="status">{hits.length}{hits.length === 60 ? '+' : ''} results</p>
          <ul class="divider-list">
            {hits.map((hit) => (
              <li key={hit.entry.s + hit.anchor}>
                <a class="hit" href={`${base}docs/${hit.entry.d}/#${hit.anchor}`}>
                  <div class="hit-title"><Highlight text={hit.entry.t} query={debounced} /></div>
                  <div class="hit-doc">{hit.docTitle}</div>
                  {hit.snippet && <div class="hit-snippet"><Highlight text={hit.snippet} query={debounced} /></div>}
                </a>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
