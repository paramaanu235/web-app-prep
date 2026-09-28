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

if (!/Mac|iPhone|iPad/.test(navigator.platform)) {
  document.querySelectorAll('[data-mod-key]').forEach((el) => (el.textContent = 'Ctrl K'));
}

if ('serviceWorker' in navigator && import.meta.env.PROD) {
  const base = document.body.dataset.base ?? '/';
  navigator.serviceWorker.register(`${base}sw.js`, { scope: base }).catch(() => {});
}
