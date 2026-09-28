// Display preferences. The theme is shared with the iOS state (`themePreference`);
// font, size and line length are web-only. A copy lives in localStorage so the
// inline script in BaseLayout can apply it before first paint (no theme flash).
import type { ThemePreference } from './state/types';

export type ReadingFont = 'sans' | 'serif';
export type Measure = 'narrow' | 'normal' | 'wide';

export interface WebPrefs {
  theme: ThemePreference;
  font: ReadingFont;
  size: number;
  measure: Measure;
}

export const PREFS_KEY = 'prep.prefs';
export const DEFAULT_PREFS: WebPrefs = { theme: 'system', font: 'sans', size: 18, measure: 'normal' };

export function readWebPrefs(): WebPrefs {
  try {
    return { ...DEFAULT_PREFS, ...JSON.parse(localStorage.getItem(PREFS_KEY) ?? '{}') };
  } catch {
    return { ...DEFAULT_PREFS };
  }
}

export function resolveTheme(theme: ThemePreference): 'light' | 'dark' | 'sepia' {
  if (theme !== 'system') return theme;
  return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

export function applyPrefs(prefs: WebPrefs, theme: ThemePreference = prefs.theme): WebPrefs {
  const next = { ...prefs, theme };
  try {
    localStorage.setItem(PREFS_KEY, JSON.stringify(next));
  } catch {
    /* storage unavailable: still apply for this page */
  }
  const root = document.documentElement;
  root.dataset.theme = resolveTheme(theme);
  root.dataset.font = next.font;
  root.dataset.measure = next.measure;
  root.style.setProperty('--read-size', `${next.size}px`);
  return next;
}

if (typeof window !== 'undefined') {
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const prefs = readWebPrefs();
    if (prefs.theme === 'system') applyPrefs(prefs);
  });
}
