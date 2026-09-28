// State mutations, mirroring StudyStateStore.swift.
import { update } from './store';
import { isoNow, makeDefaultState, makeWeek, newId, type MockResult, type ReadingState, type UserStudyState, type WeekProgress } from './types';

function readingState(s: UserStudyState, documentID: string): ReadingState {
  return (s.readingStates[documentID] ??= {
    documentID,
    estimatedProgress: 0,
    explicitlyCompleted: false,
    lastOpenedAt: isoNow(),
  });
}

export const actions = {
  markOpened: (documentID: string) =>
    update((s) => {
      readingState(s, documentID).lastOpenedAt = isoNow();
    }),

  updateReadingPosition: (documentID: string, sectionID: string | undefined, anchor: string | undefined, progress: number) =>
    update((s) => {
      const rs = readingState(s, documentID);
      rs.lastSectionID = sectionID;
      rs.scrollAnchor = anchor;
      rs.estimatedProgress = Math.max(rs.estimatedProgress, Math.min(1, Math.max(0, progress)));
      rs.lastOpenedAt = isoNow();
    }),

  toggleCompleted: (documentID: string) =>
    update((s) => {
      const rs = readingState(s, documentID);
      rs.explicitlyCompleted = !rs.explicitlyCompleted;
    }),

  addBookmark: (documentID: string, sectionID: string | undefined, title: string) =>
    update((s) => {
      const now = isoNow();
      s.bookmarks.unshift({ id: newId(), documentID, sectionID, title, note: '', createdAt: now, updatedAt: now });
    }),

  removeBookmark: (id: string) =>
    update((s) => {
      s.bookmarks = s.bookmarks.filter((b) => b.id !== id);
    }),

  updateBookmarkNote: (id: string, note: string) =>
    update((s) => {
      const b = s.bookmarks.find((x) => x.id === id);
      if (b) {
        b.note = note;
        b.updatedAt = isoNow();
      }
    }),

  updateWeek: (week: number, patch: Partial<WeekProgress>) =>
    update((s) => {
      const current = s.weeklyProgress[week] ?? makeWeek(week);
      const next = { ...current, ...patch, week };
      next.independentlySolved = Math.min(next.independentlySolved, next.attempted);
      s.weeklyProgress[week] = next;
    }),

  addMock: (week: number, mock: Omit<MockResult, 'id'>) =>
    update((s) => {
      const wp = (s.weeklyProgress[week] ??= makeWeek(week));
      wp.mocks.push({ ...mock, id: newId() });
    }),

  removeMock: (week: number, id: string) =>
    update((s) => {
      const wp = s.weeklyProgress[week];
      if (wp) wp.mocks = wp.mocks.filter((m) => m.id !== id);
    }),

  toggleChecklist: (id: string) =>
    update((s) => {
      const item = s.dailyChecklist.find((c) => c.id === id);
      if (item) item.isDone = !item.isDone;
    }),

  addChecklistItem: (title: string, category: string) =>
    update((s) => {
      s.dailyChecklist.push({ id: newId(), title, isDone: false, category });
    }),

  removeChecklistItem: (id: string) =>
    update((s) => {
      s.dailyChecklist = s.dailyChecklist.filter((c) => c.id !== id);
    }),

  resetChecklist: () =>
    update((s) => {
      s.dailyChecklist.forEach((c) => (c.isDone = false));
    }),

  addSlowPattern: (pattern: string) =>
    update((s) => {
      if (!s.slowPatterns.includes(pattern)) s.slowPatterns.push(pattern);
    }),

  removeSlowPattern: (pattern: string) =>
    update((s) => {
      s.slowPatterns = s.slowPatterns.filter((p) => p !== pattern);
    }),

  setDates: (startDate: string | undefined, interviewDate: string | undefined) =>
    update((s) => {
      s.startDate = startDate;
      s.interviewDate = interviewDate;
    }),

  setTheme: (theme: UserStudyState['themePreference']) =>
    update((s) => {
      s.themePreference = theme;
    }),

  resetReadingPositions: () =>
    update((s) => {
      s.readingStates = {};
    }),

  resetTracker: () =>
    update((s) => {
      const def = makeDefaultState();
      s.weeklyProgress = def.weeklyProgress;
      s.dailyChecklist = def.dailyChecklist;
    }),

  resetAll: () =>
    update((s) => {
      Object.assign(s, makeDefaultState());
    }),
};
