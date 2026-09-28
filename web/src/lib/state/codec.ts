// JSON import/export compatible with the iOS app's ExportImportService
// (JSONEncoder, .iso8601 dates, .sortedKeys, [Int: X] dictionaries as flat arrays).
import { THEMES, WEEK_STATUSES, isoNow, makeWeek, type UserStudyState, type WeekProgress } from './types';

export const EXPORT_FILENAME = 'GoogleInterviewPrep_Backup.json';

// Seconds between 1970-01-01 and 2001-01-01 (Swift's reference date).
const SWIFT_EPOCH_OFFSET = 978307200;

function sortKeys(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(sortKeys);
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.keys(value)
        .sort()
        .filter((k) => (value as Record<string, unknown>)[k] !== undefined && (value as Record<string, unknown>)[k] !== null)
        .map((k) => [k, sortKeys((value as Record<string, unknown>)[k])]),
    );
  }
  return value;
}

export function encodeState(state: UserStudyState): string {
  const weeks = Object.values(state.weeklyProgress).sort((a, b) => a.week - b.week);
  const swiftShape = { ...state, weeklyProgress: weeks.flatMap((w) => [w.week, w]) };
  return JSON.stringify(sortKeys(swiftShape), null, 2);
}

export interface ImportSummary {
  bookmarkCount: number;
  trackedWeeksCount: number;
  checklistCount: number;
  readingCount: number;
}

export type ImportResult = { ok: true; state: UserStudyState; summary: ImportSummary } | { ok: false; error: string };

class ImportError extends Error {}

function date(value: unknown, field: string): string {
  if (typeof value === 'number') return isoNow(new Date((value + SWIFT_EPOCH_OFFSET) * 1000));
  if (typeof value === 'string' && !Number.isNaN(Date.parse(value))) return isoNow(new Date(value));
  throw new ImportError(`${field} is not a valid date.`);
}
const optDate = (v: unknown, f: string) => (v === undefined || v === null ? undefined : date(v, f));

function num(value: unknown, field: string): number {
  if (typeof value !== 'number' || !Number.isFinite(value)) throw new ImportError(`${field} must be a number.`);
  return value;
}
function str(value: unknown, field: string): string {
  if (typeof value !== 'string') throw new ImportError(`${field} must be a string.`);
  return value;
}
function bool(value: unknown, field: string): boolean {
  if (typeof value !== 'boolean') throw new ImportError(`${field} must be true or false.`);
  return value;
}
function arr(value: unknown, field: string): unknown[] {
  if (!Array.isArray(value)) throw new ImportError(`${field} must be a list.`);
  return value;
}
function obj(value: unknown, field: string): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new ImportError(`${field} must be an object.`);
  return value as Record<string, unknown>;
}
const optStr = (v: unknown, f: string) => (v === undefined || v === null ? undefined : str(v, f));

function check(condition: boolean, message: string) {
  if (!condition) throw new ImportError(message);
}

function decodeWeek(raw: unknown, key: number): WeekProgress {
  const w = obj(raw, `weeklyProgress[${key}]`);
  const status = str(w.status, 'status');
  check((WEEK_STATUSES as string[]).includes(status), `Invalid status "${status}" for week ${key}.`);
  const week: WeekProgress = {
    week: num(w.week, 'week'),
    status: status as WeekProgress['status'],
    plannedHours: num(w.plannedHours, 'plannedHours'),
    completedHours: num(w.completedHours, 'completedHours'),
    attempted: num(w.attempted, 'attempted'),
    independentlySolved: num(w.independentlySolved, 'independentlySolved'),
    mocks: arr(w.mocks, 'mocks').map((m, i) => {
      const mock = obj(m, `mocks[${i}]`);
      return {
        id: str(mock.id, 'mock id'),
        date: date(mock.date, 'mock date'),
        type: str(mock.type, 'mock type'),
        score: num(mock.score, 'mock score'),
        strengths: str(mock.strengths, 'strengths'),
        misses: str(mock.misses, 'misses'),
        nextDrill: str(mock.nextDrill, 'nextDrill'),
      };
    }),
    systemDesignSessions: num(w.systemDesignSessions, 'systemDesignSessions'),
    behavioralStoriesPracticed: num(w.behavioralStoriesPracticed, 'behavioralStoriesPracticed'),
    confidence: num(w.confidence, 'confidence'),
    notes: str(w.notes, 'notes'),
  };
  // Same rules as ExportImportService.validateImportData.
  check(key >= 1 && key <= 12 && week.week === key, `Invalid week number: ${key}. Must be between 1 and 12.`);
  check(week.plannedHours >= 0 && week.plannedHours <= 168, `Invalid planned hours for week ${key}.`);
  check(week.completedHours >= 0 && week.completedHours <= 168, `Invalid completed hours for week ${key}.`);
  check(week.attempted >= 0 && week.independentlySolved >= 0, `Problem counts for week ${key} must be non-negative.`);
  check(week.independentlySolved <= week.attempted, `Independently solved problems cannot exceed attempted problems for week ${key}.`);
  check(week.confidence >= 1 && week.confidence <= 5, `Confidence score for week ${key} must be between 1 and 5.`);
  check(week.systemDesignSessions >= 0 && week.behavioralStoriesPracticed >= 0, `Session counts for week ${key} must be non-negative.`);
  week.mocks.forEach((m) => check(m.score >= 1 && m.score <= 4, `Mock interview score must be between 1 and 4 (got ${m.score}).`));
  return week;
}

function decodeWeeks(raw: unknown): Record<number, WeekProgress> {
  const pairs: [number, unknown][] = [];
  if (Array.isArray(raw)) {
    check(raw.length % 2 === 0, 'weeklyProgress has an odd number of entries.');
    for (let i = 0; i < raw.length; i += 2) pairs.push([num(raw[i], 'week key'), raw[i + 1]]);
  } else {
    for (const [k, v] of Object.entries(obj(raw, 'weeklyProgress'))) pairs.push([Number(k), v]);
  }
  const weeks: Record<number, WeekProgress> = {};
  for (const [key, value] of pairs) weeks[key] = decodeWeek(value, key);
  for (let w = 1; w <= 12; w++) weeks[w] ??= makeWeek(w);
  return weeks;
}

export function decodeState(json: string): ImportResult {
  try {
    let parsed: unknown;
    try {
      parsed = JSON.parse(json);
    } catch {
      throw new ImportError('The file is not valid JSON.');
    }
    const s = obj(parsed, 'root');
    const version = num(s.version, 'version');
    check(version === 1, `Unsupported schema version ${version}. Expected version 1.`);

    const readingStates: UserStudyState['readingStates'] = {};
    for (const [docID, raw] of Object.entries(obj(s.readingStates, 'readingStates'))) {
      const r = obj(raw, `readingStates.${docID}`);
      const progress = num(r.estimatedProgress, 'estimatedProgress');
      check(progress >= 0 && progress <= 1, `Invalid reading progress for ${docID}: ${progress}.`);
      readingStates[docID] = {
        documentID: str(r.documentID, 'documentID'),
        lastSectionID: optStr(r.lastSectionID, 'lastSectionID'),
        scrollAnchor: optStr(r.scrollAnchor, 'scrollAnchor'),
        estimatedProgress: progress,
        explicitlyCompleted: bool(r.explicitlyCompleted, 'explicitlyCompleted'),
        lastOpenedAt: date(r.lastOpenedAt, 'lastOpenedAt'),
      };
    }

    const theme = str(s.themePreference, 'themePreference');
    check((THEMES as string[]).includes(theme), `Invalid theme preference: ${theme}.`);
    const bodyFontSize = num(s.bodyFontSize, 'bodyFontSize');
    const codeFontSize = num(s.codeFontSize, 'codeFontSize');
    check(bodyFontSize >= 10 && bodyFontSize <= 36, `Invalid body font size: ${bodyFontSize}.`);
    check(codeFontSize >= 8 && codeFontSize <= 30, `Invalid code font size: ${codeFontSize}.`);

    const state: UserStudyState = {
      version,
      startDate: optDate(s.startDate, 'startDate'),
      interviewDate: optDate(s.interviewDate, 'interviewDate'),
      readingStates,
      bookmarks: arr(s.bookmarks, 'bookmarks').map((raw, i) => {
        const b = obj(raw, `bookmarks[${i}]`);
        return {
          id: str(b.id, 'bookmark id'),
          documentID: str(b.documentID, 'bookmark documentID'),
          sectionID: optStr(b.sectionID, 'sectionID'),
          codeBlockID: optStr(b.codeBlockID, 'codeBlockID'),
          exactQuoteHash: optStr(b.exactQuoteHash, 'exactQuoteHash'),
          title: str(b.title, 'bookmark title'),
          note: str(b.note, 'bookmark note'),
          createdAt: date(b.createdAt, 'createdAt'),
          updatedAt: date(b.updatedAt, 'updatedAt'),
        };
      }),
      weeklyProgress: decodeWeeks(s.weeklyProgress),
      dailyChecklist: arr(s.dailyChecklist, 'dailyChecklist').map((raw, i) => {
        const c = obj(raw, `dailyChecklist[${i}]`);
        return { id: str(c.id, 'id'), title: str(c.title, 'title'), isDone: bool(c.isDone, 'isDone'), category: str(c.category, 'category') };
      }),
      slowPatterns: arr(s.slowPatterns, 'slowPatterns').map((p) => str(p, 'slow pattern')),
      themePreference: theme as UserStudyState['themePreference'],
      bodyFontSize,
      codeFontSize,
      keepScreenAwake: bool(s.keepScreenAwake, 'keepScreenAwake'),
    };

    return {
      ok: true,
      state,
      summary: {
        bookmarkCount: state.bookmarks.length,
        trackedWeeksCount: Object.values(state.weeklyProgress).filter((w) => w.completedHours > 0 || w.status !== 'Not Started').length,
        checklistCount: state.dailyChecklist.length,
        readingCount: Object.keys(state.readingStates).length,
      },
    };
  } catch (error) {
    if (error instanceof ImportError) return { ok: false, error: error.message };
    throw error;
  }
}
