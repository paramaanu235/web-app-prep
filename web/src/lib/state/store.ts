// Browser-side study state: IndexedDB persistence, in-memory cache, change
// notifications, and cross-tab sync. Falls back to memory-only storage when
// IndexedDB is unavailable (e.g. some private browsing modes).
import { get, set } from 'idb-keyval';
import { makeDefaultState, type UserStudyState } from './types';
import { applyPrefs, readWebPrefs } from '../prefs';

const KEY = 'userStudyState';
type Listener = (state: UserStudyState) => void;

let state: UserStudyState | null = null;
let loading: Promise<UserStudyState> | null = null;
let persistent = true;
const listeners = new Set<Listener>();
// Browser-only: in SSR (Node) an open BroadcastChannel would keep the build process alive.
const channel = typeof window !== 'undefined' && 'BroadcastChannel' in window ? new BroadcastChannel('study-state') : null;

async function readStored(): Promise<UserStudyState> {
  try {
    const stored = await get<UserStudyState>(KEY);
    return stored ?? makeDefaultState();
  } catch {
    persistent = false;
    return makeDefaultState();
  }
}

export function loadState(): Promise<UserStudyState> {
  loading ??= readStored().then((s) => (state = s));
  return loading;
}

export function getState(): UserStudyState | null {
  return state;
}

export function isPersistent(): boolean {
  return persistent;
}

export function subscribe(listener: Listener): () => void {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

function notify() {
  if (state) listeners.forEach((l) => l(state!));
}

export async function replaceState(next: UserStudyState): Promise<void> {
  state = next;
  applyPrefs(readWebPrefs(), next.themePreference);
  notify();
  try {
    if (persistent) await set(KEY, next);
  } catch {
    persistent = false;
  }
  channel?.postMessage('changed');
}

export async function update(mutate: (draft: UserStudyState) => void): Promise<void> {
  const current = await loadState().then(() => state!);
  const draft = structuredClone(current);
  mutate(draft);
  await replaceState(draft);
}

channel?.addEventListener('message', async () => {
  state = await readStored();
  applyPrefs(readWebPrefs(), state.themePreference);
  notify();
});
