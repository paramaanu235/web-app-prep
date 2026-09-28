import { useEffect, useState } from 'preact/hooks';
import { getState, loadState, subscribe } from '../../lib/state/store';
import type { UserStudyState } from '../../lib/state/types';

export function useStudyState(): UserStudyState | null {
  const [state, setState] = useState(getState());
  useEffect(() => {
    let alive = true;
    loadState().then((s) => alive && setState(s));
    const unsubscribe = subscribe(setState);
    return () => {
      alive = false;
      unsubscribe();
    };
  }, []);
  return state;
}

export function useDebounced<T>(value: T, ms: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const t = setTimeout(() => setDebounced(value), ms);
    return () => clearTimeout(t);
  }, [value, ms]);
  return debounced;
}
