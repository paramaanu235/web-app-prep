// Mirrors ios/GoogleInterviewPrep/GoogleInterviewPrep/Models/StudyState.swift.
// Dates are ISO-8601 strings without fractional seconds (Swift's `.iso8601`).

export type WeekStatus = 'Not Started' | 'In Progress' | 'Completed';
export const WEEK_STATUSES: WeekStatus[] = ['Not Started', 'In Progress', 'Completed'];
export type ThemePreference = 'system' | 'light' | 'dark' | 'sepia';
export const THEMES: ThemePreference[] = ['system', 'light', 'dark', 'sepia'];

export interface MockResult {
  id: string;
  date: string;
  type: string; // "Coding" | "System Design" | "Behavioral"
  score: number; // 1 (Needs Practice) … 4 (Strong Hire)
  strengths: string;
  misses: string;
  nextDrill: string;
}

export interface ChecklistItem {
  id: string;
  title: string;
  isDone: boolean;
  category: string;
}

export interface ReadingState {
  documentID: string;
  lastSectionID?: string;
  scrollAnchor?: string;
  estimatedProgress: number; // 0…1
  explicitlyCompleted: boolean;
  lastOpenedAt: string;
}

export interface Bookmark {
  id: string;
  documentID: string;
  sectionID?: string;
  codeBlockID?: string;
  exactQuoteHash?: string;
  title: string;
  note: string;
  createdAt: string;
  updatedAt: string;
}

export interface WeekProgress {
  week: number;
  status: WeekStatus;
  plannedHours: number;
  completedHours: number;
  attempted: number;
  independentlySolved: number;
  mocks: MockResult[];
  systemDesignSessions: number;
  behavioralStoriesPracticed: number;
  confidence: number; // 1…5
  notes: string;
}

export interface UserStudyState {
  version: number;
  startDate?: string;
  interviewDate?: string;
  readingStates: Record<string, ReadingState>;
  bookmarks: Bookmark[];
  /** Keyed by week number. Swift encodes this dictionary as a flat `[1, {…}, 2, {…}]` array; see codec.ts. */
  weeklyProgress: Record<number, WeekProgress>;
  dailyChecklist: ChecklistItem[];
  slowPatterns: string[];
  themePreference: ThemePreference;
  bodyFontSize: number;
  codeFontSize: number;
  keepScreenAwake: boolean;
}

export function isoNow(date = new Date()): string {
  return date.toISOString().replace(/\.\d{3}Z$/, 'Z');
}

export function newId(): string {
  // Swift's UUID().uuidString is upper-case.
  return crypto.randomUUID().toUpperCase();
}

export function makeWeek(week: number): WeekProgress {
  return {
    week,
    status: 'Not Started',
    plannedHours: week === 12 ? 10 : 18,
    completedHours: 0,
    attempted: 0,
    independentlySolved: 0,
    mocks: [],
    systemDesignSessions: 0,
    behavioralStoriesPracticed: 0,
    confidence: 3,
    notes: '',
  };
}

export function makeDefaultChecklist(): ChecklistItem[] {
  return [
    ['Complete 1 timed Medium problem (40 min)', 'Daily DSA'],
    ['Review invariant and space complexity', 'Daily DSA'],
    ['Log tricky edge-cases / mistakes', 'Error Log'],
    ['Rehearse 1 system design architecture or 1 STAR story', 'Design / Story'],
  ].map(([title, category]) => ({ id: newId(), title: title!, isDone: false, category: category! }));
}

export function makeDefaultState(): UserStudyState {
  const weeklyProgress: Record<number, WeekProgress> = {};
  for (let w = 1; w <= 12; w++) weeklyProgress[w] = makeWeek(w);
  return {
    version: 1,
    readingStates: {},
    bookmarks: [],
    weeklyProgress,
    dailyChecklist: makeDefaultChecklist(),
    slowPatterns: ['Monotonic Queue', 'Segment Tree', '0-1 BFS', 'Topological Sort Cycle Detection'],
    themePreference: 'system',
    bodyFontSize: 16,
    codeFontSize: 13.5,
    keepScreenAwake: false,
  };
}
