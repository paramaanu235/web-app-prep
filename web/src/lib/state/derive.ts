import { isoNow, type UserStudyState } from './types';

const DAY = 86_400_000;

function startOfDay(d: Date): number {
  return new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime();
}

/** Calendar-day difference `to - from` in the viewer's time zone. */
export function daysBetween(from: Date, to: Date): number {
  return Math.round((startOfDay(to) - startOfDay(from)) / DAY);
}

export function currentWeek(state: UserStudyState, now = new Date()): number {
  if (!state.startDate) return 1;
  const days = daysBetween(new Date(state.startDate), now);
  return Math.max(1, Math.min(12, Math.floor(days / 7) + 1));
}

export function daysUntilInterview(state: UserStudyState, now = new Date()): number | null {
  return state.interviewDate ? daysBetween(now, new Date(state.interviewDate)) : null;
}

/** ISO timestamp -> `YYYY-MM-DD` (local) for <input type="date">. */
export function toDateInput(iso: string | undefined): string {
  if (!iso) return '';
  const d = new Date(iso);
  const pad = (n: number) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

/** `YYYY-MM-DD` -> ISO timestamp at local midnight. */
export function fromDateInput(value: string): string | undefined {
  const m = value.match(/^(\d{4})-(\d{2})-(\d{2})$/);
  return m ? isoNow(new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]))) : undefined;
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' });
}

export function readingProgress(state: UserStudyState, docId: string): { progress: number; done: boolean; opened: boolean } {
  const rs = state.readingStates[docId];
  if (!rs) return { progress: 0, done: false, opened: false };
  return { progress: rs.explicitlyCompleted ? 1 : rs.estimatedProgress, done: rs.explicitlyCompleted, opened: true };
}

/** Link to a document section by its section id; the reader resolves it to the anchor. */
export function sectionHref(base: string, documentID: string, sectionID?: string): string {
  const doc = `${base}docs/${documentID}/`;
  return sectionID ? `${doc}?section=${encodeURIComponent(sectionID)}` : doc;
}
