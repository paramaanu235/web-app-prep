// Runs on every page: shared-state theme sync, mobile menu, platform key hints,
// and offline support.
import { applyPrefs, readWebPrefs } from '../lib/prefs';
import { loadState } from '../lib/state/store';

loadState().then((state) => applyPrefs(readWebPrefs(), state.themePreference));

const menuButton = document.querySelector<HTMLButtonElement>('[data-menu]');
const nav = document.getElementById('site-nav');
menuButton?.addEventListener('click', () => {
  const open = nav?.classList.toggle('open') ?? false;
  menuButton.setAttribute('aria-expanded', String(open));
});

// Search shortcuts live here rather than in the palette island so a keypress or
// click before hydration isn't lost: the request is flagged and replayed on mount.
function isTyping(target: EventTarget | null): boolean {
  const el = target as HTMLElement | null;
  return !!el && (el.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(el.tagName));
}
function requestSearch() {
  document.documentElement.dataset.searchRequested = '';
  document.dispatchEvent(new Event('open-search'));
}
document.addEventListener('keydown', (e) => {
  if ((e.key === 'k' && (e.metaKey || e.ctrlKey)) || (e.key === '/' && !isTyping(e.target) && !document.querySelector('dialog[open]'))) {
    e.preventDefault();
    requestSearch();
  }
});
document.addEventListener('click', (e) => {
  if ((e.target as HTMLElement).closest('[data-open-search]')) requestSearch();
});

if (!/Mac|iPhone|iPad/.test(navigator.platform)) {
  document.querySelectorAll('[data-mod-key]').forEach((el) => (el.textContent = 'Ctrl K'));
}

// Offline support. Registration waits until the page has loaded and gone idle,
// because installing precaches the whole site and would compete with first paint.
if ('serviceWorker' in navigator && import.meta.env.PROD) {
  const base = document.body.dataset.base ?? '/';
  const register = () => navigator.serviceWorker.register(`${base}sw.js`, { scope: base }).catch(() => {});
  const whenIdle = () => ('requestIdleCallback' in window ? requestIdleCallback(register, { timeout: 5000 }) : setTimeout(register, 2000));
  if (document.readyState === 'complete') whenIdle();
  else addEventListener('load', whenIdle, { once: true });
}
