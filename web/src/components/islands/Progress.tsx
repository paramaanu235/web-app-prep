import { useEffect, useState } from 'preact/hooks';
import { actions } from '../../lib/state/actions';
import { currentWeek, formatDate, fromDateInput, toDateInput } from '../../lib/state/derive';
import { icons } from '../../lib/icons';
import { isoNow, WEEK_STATUSES, type WeekProgress } from '../../lib/state/types';
import { Checklist } from './Checklist';
import { useStudyState } from './hooks';
import { Loading } from './Loading';

const CONFIDENCE = ['High uncertainty', 'Need scaffolding', 'Steady foundation', 'Fluent & robust', 'Senior interview ready'];
const MOCK_TYPES = ['Coding', 'System Design', 'Behavioral'];
const MOCK_SCORES = ['No hire / major gaps', 'Lean no hire', 'Lean hire / meets bar', 'Strong hire'];

function NumberField({ label, value, step = 1, min = 0, max, onChange }: {
  label: string;
  value: number;
  step?: number;
  min?: number;
  max?: number;
  onChange: (v: number) => void;
}) {
  return (
    <label class="field">
      <span>{label}</span>
      <input
        type="number"
        inputMode="decimal"
        value={value}
        step={step}
        min={min}
        max={max}
        onChange={(e) => {
          const v = Number(e.currentTarget.value);
          if (Number.isFinite(v)) onChange(Math.max(min, max === undefined ? v : Math.min(max, v)));
        }}
      />
    </label>
  );
}

function MockForm({ week }: { week: number }) {
  const blank = { date: toDateInput(isoNow()), type: 'Coding', score: 3, strengths: '', misses: '', nextDrill: '' };
  const [mock, setMock] = useState(blank);
  const set = (patch: Partial<typeof mock>) => setMock({ ...mock, ...patch });
  return (
    <form
      class="stack"
      onSubmit={(e) => {
        e.preventDefault();
        actions.addMock(week, { ...mock, date: fromDateInput(mock.date) ?? isoNow() });
        setMock(blank);
      }}
    >
      <div class="form-grid">
        <label class="field">
          <span>Date</span>
          <input type="date" value={mock.date} onInput={(e) => set({ date: e.currentTarget.value })} />
        </label>
        <label class="field">
          <span>Type</span>
          <select value={mock.type} onChange={(e) => set({ type: e.currentTarget.value })}>
            {MOCK_TYPES.map((t) => <option key={t}>{t}</option>)}
          </select>
        </label>
        <label class="field">
          <span>Score</span>
          <select value={mock.score} onChange={(e) => set({ score: Number(e.currentTarget.value) })}>
            {MOCK_SCORES.map((s, i) => <option key={s} value={i + 1}>{i + 1} · {s}</option>)}
          </select>
        </label>
      </div>
      <label class="field"><span>What went well</span><input type="text" value={mock.strengths} onInput={(e) => set({ strengths: e.currentTarget.value })} /></label>
      <label class="field"><span>Misses / hesitations</span><input type="text" value={mock.misses} onInput={(e) => set({ misses: e.currentTarget.value })} /></label>
      <label class="field"><span>Next targeted drill</span><input type="text" value={mock.nextDrill} onInput={(e) => set({ nextDrill: e.currentTarget.value })} /></label>
      <div><button class="btn" type="submit">Log mock interview</button></div>
    </form>
  );
}

function WeekEditor({ wp }: { wp: WeekProgress }) {
  const patch = (p: Partial<WeekProgress>) => actions.updateWeek(wp.week, p);
  return (
    <section class="week-editor" aria-labelledby="week-editor-title">
      <h3 id="week-editor-title">Week {wp.week}</h3>
      <div class="stack" style={{ gap: '20px' }}>
        <div class="segmented" role="group" aria-label="Status">
          {WEEK_STATUSES.map((s) => (
            <button key={s} type="button" aria-pressed={wp.status === s} onClick={() => patch({ status: s })}>{s}</button>
          ))}
        </div>
        <div class="form-grid">
          <NumberField label="Completed hours" value={wp.completedHours} step={0.5} max={168} onChange={(v) => patch({ completedHours: v })} />
          <NumberField label="Planned hours" value={wp.plannedHours} step={0.5} max={168} onChange={(v) => patch({ plannedHours: v })} />
          <NumberField label="Problems attempted" value={wp.attempted} onChange={(v) => patch({ attempted: v })} />
          <NumberField label="Solved independently" value={wp.independentlySolved} max={wp.attempted} onChange={(v) => patch({ independentlySolved: v })} />
          <NumberField label="System design sessions" value={wp.systemDesignSessions} onChange={(v) => patch({ systemDesignSessions: v })} />
          <NumberField label="STAR stories practiced" value={wp.behavioralStoriesPracticed} onChange={(v) => patch({ behavioralStoriesPracticed: v })} />
        </div>
        <label class="field">
          <span>Confidence</span>
          <select value={wp.confidence} onChange={(e) => patch({ confidence: Number(e.currentTarget.value) })}>
            {CONFIDENCE.map((c, i) => <option key={c} value={i + 1}>{i + 1} · {c}</option>)}
          </select>
        </label>
        <label class="field">
          <span>Notes</span>
          <textarea value={wp.notes} onChange={(e) => patch({ notes: e.currentTarget.value })} placeholder="What clicked, what didn’t, what to revisit…" />
        </label>

        <div>
          <h4 class="section-title" style={{ marginTop: '8px' }}>Mock interviews</h4>
          {wp.mocks.length === 0 ? (
            <p class="muted" style={{ fontSize: '14px' }}>No mocks logged this week.</p>
          ) : (
            <ul class="divider-list" style={{ marginBottom: '16px' }}>
              {wp.mocks.map((m) => (
                <li key={m.id} class="row" style={{ padding: '12px 0', alignItems: 'flex-start', flexWrap: 'nowrap' }}>
                  <div style={{ flex: 1, fontSize: '14px' }}>
                    <strong>{m.type}</strong> · {m.score}/4 · <span class="muted">{formatDate(m.date)}</span>
                    {m.strengths && <div><span class="muted">Went well:</span> {m.strengths}</div>}
                    {m.misses && <div><span class="muted">Misses:</span> {m.misses}</div>}
                    {m.nextDrill && <div><span class="muted">Next drill:</span> {m.nextDrill}</div>}
                  </div>
                  <button class="icon-btn" type="button" aria-label="Delete mock" onClick={() => actions.removeMock(wp.week, m.id)} dangerouslySetInnerHTML={{ __html: icons.trash }} />
                </li>
              ))}
            </ul>
          )}
          <MockForm week={wp.week} />
        </div>
      </div>
    </section>
  );
}

export default function Progress({ base, trackerDocId }: { base: string; trackerDocId?: string }) {
  const state = useStudyState();
  const [selected, setSelected] = useState<number | null>(null);
  const [pattern, setPattern] = useState('');

  useEffect(() => {
    const w = Number(new URLSearchParams(location.search).get('week'));
    if (w >= 1 && w <= 12) setSelected(w);
  }, []);

  if (!state) return <Loading />;

  const now = currentWeek(state);
  const weeks = Array.from({ length: 12 }, (_, i) => state.weeklyProgress[i + 1]!).filter(Boolean);
  const totals = weeks.reduce(
    (t, w) => ({
      hours: t.hours + w.completedHours,
      planned: t.planned + w.plannedHours,
      solved: t.solved + w.independentlySolved,
      attempted: t.attempted + w.attempted,
      mocks: t.mocks + w.mocks.length,
    }),
    { hours: 0, planned: 0, solved: 0, attempted: 0, mocks: 0 },
  );
  const active = selected ?? now;
  const wp = state.weeklyProgress[active];

  return (
    <div class="page">
      <header class="page-header">
        <h1>Progress</h1>
        <p>
          {state.startDate ? `Started ${formatDate(state.startDate)} · currently week ${now}` : <>Set a start date in <a href={`${base}settings/#dates`}>settings</a> to track the current week.</>}
          {trackerDocId && <> · <a href={`${base}docs/${trackerDocId}/`}>Open the tracker document</a></>}
        </p>
      </header>

      <div class="stat-row">
        <div class="stat"><b>{totals.hours}</b><span>of {totals.planned} planned hours</span></div>
        <div class="stat"><b>{totals.solved}</b><span>of {totals.attempted} solved independently</span></div>
        <div class="stat"><b>{totals.mocks}</b><span>mock interviews</span></div>
        <div class="stat"><b>{weeks.filter((w) => w.status === 'Completed').length}/12</b><span>weeks completed</span></div>
      </div>

      <h2 class="section-title">12-week plan</h2>
      <div class="week-grid">
        {weeks.map((w) => (
          <button
            key={w.week}
            type="button"
            class={`week-tile${w.week === now && state.startDate ? ' current' : ''}`}
            aria-pressed={w.week === active}
            onClick={() => {
              setSelected(w.week);
              history.replaceState(null, '', `?week=${w.week}`);
            }}
          >
            <b>Week {w.week}</b>
            <span><span class="status-dot" data-status={w.status} />{w.status}</span>
            <span>{w.completedHours} / {w.plannedHours} h</span>
          </button>
        ))}
      </div>
      {wp && <WeekEditor key={wp.week} wp={wp} />}

      <h2 class="section-title">Daily checklist</h2>
      <Checklist items={state.dailyChecklist} editable />

      <h2 class="section-title">Slow patterns · review first</h2>
      <ul class="divider-list">
        {state.slowPatterns.map((p) => (
          <li key={p} class="row" style={{ padding: '10px 0', justifyContent: 'space-between' }}>
            <span>{p}</span>
            <button class="icon-btn" type="button" aria-label={`Remove ${p}`} onClick={() => actions.removeSlowPattern(p)} dangerouslySetInnerHTML={{ __html: icons.trash }} />
          </li>
        ))}
      </ul>
      <form
        class="row"
        style={{ marginTop: '12px' }}
        onSubmit={(e) => {
          e.preventDefault();
          if (pattern.trim()) actions.addSlowPattern(pattern.trim());
          setPattern('');
        }}
      >
        <input type="text" placeholder="Add a pattern, e.g. Monotonic Stack" aria-label="New slow pattern" value={pattern} onInput={(e) => setPattern(e.currentTarget.value)} style={{ flex: '1 1 240px', width: 'auto' }} />
        <button class="btn" type="submit">Add</button>
      </form>
    </div>
  );
}
