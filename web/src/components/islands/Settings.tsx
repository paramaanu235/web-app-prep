import { useEffect, useState } from 'preact/hooks';
import { actions } from '../../lib/state/actions';
import { decodeState, encodeState, EXPORT_FILENAME, type ImportResult } from '../../lib/state/codec';
import { fromDateInput, toDateInput } from '../../lib/state/derive';
import { applyPrefs, readWebPrefs, type Measure, type ReadingFont, type WebPrefs } from '../../lib/prefs';
import { isPersistent, replaceState } from '../../lib/state/store';
import { THEMES, type ThemePreference } from '../../lib/state/types';
import { useStudyState } from './hooks';

function Segmented<T extends string>({ label, value, options, onChange }: {
  label: string;
  value: T;
  options: { value: T; label: string }[];
  onChange: (v: T) => void;
}) {
  return (
    <div class="segmented" role="group" aria-label={label}>
      {options.map((o) => (
        <button key={o.value} type="button" aria-pressed={value === o.value} onClick={() => onChange(o.value)}>{o.label}</button>
      ))}
    </div>
  );
}

const cap = (s: string) => s[0]!.toUpperCase() + s.slice(1);

export default function Settings({ integrity }: { integrity: { documents: number; lines: number; builtAt: string } }) {
  const state = useStudyState();
  const [prefs, setPrefs] = useState<WebPrefs | null>(null);
  const [pending, setPending] = useState<ImportResult | null>(null);
  const [message, setMessage] = useState('');

  useEffect(() => setPrefs(readWebPrefs()), []);
  if (!state || !prefs) return <div class="page page-narrow" aria-busy="true" style={{ minHeight: '60vh' }} />;

  const setPref = (patch: Partial<WebPrefs>) => setPrefs(applyPrefs({ ...prefs, ...patch }, state.themePreference));
  const setTheme = (theme: ThemePreference) => {
    setPrefs(applyPrefs(prefs, theme));
    actions.setTheme(theme);
  };

  const exportState = () => {
    const url = URL.createObjectURL(new Blob([encodeState(state)], { type: 'application/json' }));
    const a = Object.assign(document.createElement('a'), { href: url, download: EXPORT_FILENAME });
    a.click();
    URL.revokeObjectURL(url);
  };

  const confirmThen = (text: string, fn: () => unknown) => () => {
    if (confirm(text)) {
      fn();
      setMessage('Done.');
    }
  };

  return (
    <div class="page page-narrow">
      <header class="page-header">
        <h1>Settings</h1>
        <p>Everything is stored in this browser. Export a backup to move it between devices or to the iOS app.</p>
      </header>

      <h2 class="section-title">Reading</h2>
      <div class="setting-row">
        <div><h3>Theme</h3><p>Shared with the iOS app when you import or export.</p></div>
        <Segmented label="Theme" value={state.themePreference} options={THEMES.map((t) => ({ value: t, label: cap(t) }))} onChange={setTheme} />
      </div>
      <div class="setting-row">
        <div><h3>Reading font</h3><p>Headings, code and the interface stay sans-serif.</p></div>
        <Segmented<ReadingFont> label="Reading font" value={prefs.font} options={[{ value: 'sans', label: 'Sans' }, { value: 'serif', label: 'Serif' }]} onChange={(font) => setPref({ font })} />
      </div>
      <div class="setting-row">
        <div><h3>Text size</h3><p>{prefs.size}px</p></div>
        <input type="range" min={15} max={23} step={1} value={prefs.size} aria-label="Text size" onInput={(e) => setPref({ size: Number(e.currentTarget.value) })} style={{ width: '200px', accentColor: 'var(--accent)' }} />
      </div>
      <div class="setting-row">
        <div><h3>Line length</h3><p>Shorter lines are easier to track; wider fits more.</p></div>
        <Segmented<Measure> label="Line length" value={prefs.measure} options={[{ value: 'narrow', label: 'Narrow' }, { value: 'normal', label: 'Normal' }, { value: 'wide', label: 'Wide' }]} onChange={(measure) => setPref({ measure })} />
      </div>

      <h2 class="section-title" id="dates">Study dates</h2>
      <div class="form-grid" style={{ padding: '8px 0 16px' }}>
        <label class="field">
          <span>Start date (week 1)</span>
          <input type="date" value={toDateInput(state.startDate)} onChange={(e) => actions.setDates(fromDateInput(e.currentTarget.value), state.interviewDate)} />
        </label>
        <label class="field">
          <span>Interview date</span>
          <input type="date" value={toDateInput(state.interviewDate)} onChange={(e) => actions.setDates(state.startDate, fromDateInput(e.currentTarget.value))} />
        </label>
      </div>

      <h2 class="section-title">Backup</h2>
      {!isPersistent() && <p class="notice error">This browser is blocking storage, so changes will be lost when you close the tab. Export a backup to keep them.</p>}
      <div class="setting-row">
        <div><h3>Export</h3><p>Downloads <code>{EXPORT_FILENAME}</code>, the same format the iOS app uses.</p></div>
        <button class="btn" type="button" onClick={exportState}>Export JSON</button>
      </div>
      <div class="setting-row">
        <div><h3>Import</h3><p>Replaces everything here with a backup from the web or iOS app.</p></div>
        <label class="btn">
          Choose file…
          <input
            type="file"
            accept="application/json,.json"
            class="visually-hidden"
            onChange={async (e) => {
              const file = e.currentTarget.files?.[0];
              e.currentTarget.value = '';
              if (file) setPending(decodeState(await file.text()));
            }}
          />
        </label>
      </div>
      {pending && (
        <div class={`notice${pending.ok ? '' : ' error'}`} role="status" style={{ marginTop: '12px' }}>
          {pending.ok ? (
            <div class="stack">
              <span>
                Backup contains {pending.summary.bookmarkCount} bookmarks, {pending.summary.trackedWeeksCount} tracked weeks,{' '}
                {pending.summary.checklistCount} checklist items and progress for {pending.summary.readingCount} documents.
              </span>
              <div class="row">
                <button class="btn primary" type="button" onClick={async () => { await replaceState(pending.state); setPending(null); setMessage('Backup imported.'); }}>Replace my data</button>
                <button class="btn" type="button" onClick={() => setPending(null)}>Cancel</button>
              </div>
            </div>
          ) : (
            <span>Couldn’t import: {pending.error}</span>
          )}
        </div>
      )}

      <h2 class="section-title">Reset</h2>
      <div class="row">
        <button class="btn danger" type="button" onClick={confirmThen('Clear reading positions for all documents?', actions.resetReadingPositions)}>Reading positions</button>
        <button class="btn danger" type="button" onClick={confirmThen('Reset the 12-week tracker and checklist?', actions.resetTracker)}>Tracker &amp; checklist</button>
        <button class="btn danger" type="button" onClick={confirmThen('Erase all study data in this browser? Export a backup first if you need it.', actions.resetAll)}>Everything</button>
      </div>
      {message && <p class="muted" role="status" style={{ fontSize: '14px' }}>{message}</p>}

      <h2 class="section-title">About</h2>
      <p class="muted" style={{ fontSize: '14px', maxWidth: '65ch' }}>
        {integrity.documents} canonical documents ({integrity.lines.toLocaleString()} lines), each verified against its SHA-256 in the content manifest when this site was built on {integrity.builtAt}. Pages and search keep working offline once visited.
      </p>
    </div>
  );
}
