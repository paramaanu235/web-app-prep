import { useEffect, useMemo, useRef, useState } from 'preact/hooks';
import { loadEngine, type SearchEngine, type SearchHit } from '../../lib/search/engine';
import { icons } from '../../lib/icons';
import { Highlight } from './Highlight';
import { useDebounced } from './hooks';

export default function SearchPalette({ base }: { base: string }) {
  const dialog = useRef<HTMLDialogElement>(null);
  const input = useRef<HTMLInputElement>(null);
  const list = useRef<HTMLUListElement>(null);
  const [engine, setEngine] = useState<SearchEngine | null>(null);
  const [error, setError] = useState('');
  const [query, setQuery] = useState('');
  const [includeHistorical, setIncludeHistorical] = useState(false);
  const [selected, setSelected] = useState(0);
  const debounced = useDebounced(query, 80);

  const hits: SearchHit[] = useMemo(
    () => (engine ? engine.search(debounced, { includeHistorical }, 30) : []),
    [engine, debounced, includeHistorical],
  );
  const hrefFor = (hit: SearchHit) => `${base}docs/${hit.entry.d}/#${hit.anchor}`;

  const open = () => {
    if (!dialog.current?.open) dialog.current?.showModal();
    input.current?.select();
    loadEngine(base).then(setEngine, (e: Error) => setError(e.message));
  };

  useEffect(() => {
    // Requests come from src/scripts/app.ts; one may have arrived before hydration.
    const onRequest = () => {
      delete document.documentElement.dataset.searchRequested;
      open();
    };
    if (document.documentElement.dataset.searchRequested !== undefined) onRequest();
    document.addEventListener('open-search', onRequest);
    return () => document.removeEventListener('open-search', onRequest);
  }, []);

  useEffect(() => setSelected(0), [debounced, includeHistorical]);
  useEffect(() => {
    list.current?.querySelector('[aria-selected="true"]')?.scrollIntoView({ block: 'nearest' });
  }, [selected]);

  const onInputKey = (e: KeyboardEvent) => {
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelected((s) => Math.min(s + 1, hits.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelected((s) => Math.max(s - 1, 0));
    } else if (e.key === 'Enter') {
      const hit = hits[selected];
      if (hit) {
        e.preventDefault();
        dialog.current?.close();
        location.href = hrefFor(hit);
      } else if (query.trim()) {
        location.href = `${base}search/?q=${encodeURIComponent(query.trim())}`;
      }
    }
  };

  return (
    <dialog
      ref={dialog}
      class="palette"
      aria-label="Search"
      onClick={(e) => e.target === dialog.current && dialog.current?.close()}
    >
      <div class="palette-input">
        <span class="muted" dangerouslySetInnerHTML={{ __html: icons.search }} />
        <input
          ref={input}
          type="search"
          placeholder="Search notes, code, patterns…"
          aria-label="Search query"
          aria-controls="palette-results"
          aria-activedescendant={hits[selected] ? `hit-${selected}` : undefined}
          role="combobox"
          aria-expanded={hits.length > 0}
          autoComplete="off"
          spellcheck={false}
          value={query}
          onInput={(e) => setQuery(e.currentTarget.value)}
          onKeyDown={onInputKey}
        />
        <button class="icon-btn" type="button" aria-label="Close search" onClick={() => dialog.current?.close()}>
          <span dangerouslySetInnerHTML={{ __html: icons.close }} />
        </button>
      </div>
      {error ? (
        <p class="palette-empty">Search is unavailable: {error}</p>
      ) : !debounced.trim() ? (
        <p class="palette-empty">Try “select_for_update”, “Union-Find”, “@Transactional” or “STAR”.</p>
      ) : !engine ? (
        <p class="palette-empty">Loading index…</p>
      ) : hits.length === 0 ? (
        <p class="palette-empty">No matches for “{debounced}”.</p>
      ) : (
        <ul class="palette-results" id="palette-results" role="listbox" ref={list}>
          {hits.map((hit, i) => (
            <li key={hit.entry.s + hit.anchor} role="presentation">
              <a
                id={`hit-${i}`}
                role="option"
                aria-selected={i === selected}
                href={hrefFor(hit)}
                tabIndex={-1}
                onMouseMove={() => setSelected(i)}
                onClick={() => dialog.current?.close()}
              >
                <div class="hit-title">
                  <Highlight text={hit.entry.t} query={debounced} />
                </div>
                <div class="hit-doc">{hit.docTitle}</div>
                {hit.snippet && (
                  <div class="hit-snippet">
                    <Highlight text={hit.snippet} query={debounced} />
                  </div>
                )}
              </a>
            </li>
          ))}
        </ul>
      )}
      <div class="palette-foot">
        <span>
          <kbd>↑</kbd> <kbd>↓</kbd> to move · <kbd>↵</kbd> to open · <kbd>esc</kbd> to close
        </span>
        <label>
          <input type="checkbox" checked={includeHistorical} onChange={(e) => setIncludeHistorical(e.currentTarget.checked)} />
          Include historical
        </label>
      </div>
    </dialog>
  );
}
