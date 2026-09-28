import { currentWeek, daysUntilInterview, readingProgress, sectionHref } from '../../lib/state/derive';
import { Checklist } from './Checklist';
import { useStudyState } from './hooks';

export interface DocRef {
  id: string;
  title: string;
  summary?: string | null;
}

export default function Home({ base, docs, startHere }: { base: string; docs: DocRef[]; startHere: DocRef[] }) {
  const state = useStudyState();
  const titleOf = (id: string) => docs.find((d) => d.id === id)?.title;

  if (!state) return <div class="page page-narrow" aria-busy="true" style={{ minHeight: '60vh' }} />;

  const week = currentWeek(state);
  const days = daysUntilInterview(state);
  const wp = state.weeklyProgress[week];
  const recent = Object.values(state.readingStates)
    .filter((r) => titleOf(r.documentID))
    .sort((a, b) => b.lastOpenedAt.localeCompare(a.lastOpenedAt))
    .slice(0, 3);
  const bookmarks = state.bookmarks.slice(0, 4);

  return (
    <div class="page page-narrow">
      <header class="page-header">
        <div class="eyebrow">Google interview preparation</div>
        <h1>Week {week} of 12</h1>
        <p>
          {days === null ? (
            <>
              No interview date yet · <a href={`${base}settings/#dates`}>set your dates</a>
            </>
          ) : days > 0 ? (
            `${days} day${days === 1 ? '' : 's'} until your interview`
          ) : days === 0 ? (
            'Interview day. You’ve got this.'
          ) : (
            'Interview date has passed'
          )}
        </p>
      </header>

      {wp && (
        <div class="stat-row">
          <div class="stat">
            <b>
              {wp.completedHours}
              <span class="muted" style={{ fontSize: '1rem', fontWeight: 400 }}> / {wp.plannedHours} h</span>
            </b>
            <span>Hours this week</span>
          </div>
          <div class="stat">
            <b>
              {wp.independentlySolved}
              <span class="muted" style={{ fontSize: '1rem', fontWeight: 400 }}> / {wp.attempted}</span>
            </b>
            <span>Solved independently</span>
          </div>
          <div class="stat">
            <b>{wp.status}</b>
            <span>
              <a href={`${base}progress/?week=${week}`}>Update week {week}</a>
            </span>
          </div>
        </div>
      )}

      {recent.length > 0 && (
        <section>
          <h2 class="section-title">Continue reading</h2>
          <ul class="divider-list">
            {recent.map((r) => {
              const { progress } = readingProgress(state, r.documentID);
              const anchor = r.scrollAnchor ? `#${r.scrollAnchor}` : '';
              return (
                <li key={r.documentID}>
                  <a class="doc-row" href={`${base}docs/${r.documentID}/${anchor}`}>
                    <span class="doc-row-title">{titleOf(r.documentID)}</span>
                    <span class="doc-row-meta">
                      {Math.round(progress * 100)}%
                      <span class="progress-track" aria-hidden="true">
                        <span class="progress-fill" style={{ width: `${Math.round(progress * 100)}%` }} />
                      </span>
                    </span>
                  </a>
                </li>
              );
            })}
          </ul>
        </section>
      )}

      <section>
        <h2 class="section-title">Today’s drills</h2>
        <Checklist items={state.dailyChecklist} />
      </section>

      <section>
        <h2 class="section-title">Start here</h2>
        <ul class="divider-list">
          {startHere.map((d) => (
            <li key={d.id}>
              <a class="doc-row" href={`${base}docs/${d.id}/`}>
                <span class="doc-row-title">{d.title}</span>
                {d.summary && <span class="doc-row-summary">{d.summary}</span>}
              </a>
            </li>
          ))}
        </ul>
      </section>

      {bookmarks.length > 0 && (
        <section>
          <h2 class="section-title">Recent bookmarks</h2>
          <ul class="divider-list">
            {bookmarks.map((b) => (
              <li key={b.id}>
                <a class="doc-row" href={sectionHref(base, b.documentID, b.sectionID)}>
                  <span class="doc-row-title">{b.title || titleOf(b.documentID)}</span>
                  <span class="doc-row-summary">{b.note || titleOf(b.documentID)}</span>
                </a>
              </li>
            ))}
          </ul>
          <p style={{ fontSize: '14px' }}>
            <a href={`${base}saved/`}>All bookmarks</a>
          </p>
        </section>
      )}
    </div>
  );
}
