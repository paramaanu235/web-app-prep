// Document page behaviour: code copy/wrap, scroll-spy TOC, reading progress,
// resume position, bookmarks, "mark as read", and keyboard shortcuts.
import { actions } from '../lib/state/actions';
import { getState, loadState, subscribe } from '../lib/state/store';
import type { UserStudyState } from '../lib/state/types';

const layout = document.querySelector<HTMLElement>('[data-doc-id]')!;
const docId = layout.dataset.docId!;
const content = document.getElementById('doc-content')!;
const article = layout.querySelector<HTMLElement>('.doc-main')!;
const progressBar = document.getElementById('reading-progress')!;
const tocSheet = document.getElementById('toc-sheet') as HTMLDialogElement;
const shortcuts = document.getElementById('shortcuts-dialog') as HTMLDialogElement;
const completeBtn = document.querySelector<HTMLButtonElement>('[data-complete]')!;

// Sections come from the TOC so markdown headings and Java symbols behave alike.
interface SpySection {
  id: string;
  anchor: string;
  title: string;
  el: HTMLElement;
}
const sections: SpySection[] = [...document.querySelectorAll<HTMLAnchorElement>('.doc-toc .toc a')]
  .map((a) => {
    const anchor = decodeURIComponent(a.hash.slice(1));
    const el = document.getElementById(anchor);
    return el ? { id: a.dataset.sectionId!, anchor, title: a.textContent!.trim(), el } : null;
  })
  .filter((s): s is SpySection => s !== null);
const tocLinks = [...document.querySelectorAll<HTMLAnchorElement>('.toc a')];

/* ---------- Code blocks ---------- */
content.addEventListener('click', async (e) => {
  const button = (e.target as HTMLElement).closest<HTMLButtonElement>('.code-btn[data-action]');
  if (!button) return;
  const figure = button.closest('figure.code')!;
  if (button.dataset.action === 'wrap') {
    const on = figure.classList.toggle('wrap');
    button.setAttribute('aria-pressed', String(on));
  } else {
    const text = figure.querySelector('pre')?.textContent ?? '';
    try {
      await navigator.clipboard.writeText(text);
      button.textContent = 'Copied';
    } catch {
      button.textContent = 'Copy failed';
    }
    setTimeout(() => (button.textContent = 'Copy'), 1500);
  }
});

/* ---------- Scroll spy + progress ---------- */
let current: SpySection | undefined;
let progress = 0;

function computeCurrent(): SpySection | undefined {
  const line = 96;
  let found: SpySection | undefined;
  for (const s of sections) {
    if (s.el.getBoundingClientRect().top <= line) found = s;
    else break;
  }
  return found;
}

function onScroll() {
  const rect = article.getBoundingClientRect();
  const total = rect.height - innerHeight;
  progress = total > 0 ? Math.min(1, Math.max(0, -rect.top / total)) : 1;
  progressBar.style.transform = `scaleX(${progress})`;

  const next = computeCurrent();
  if (next !== current) {
    current = next;
    for (const a of tocLinks) {
      const active = !!current && a.hash === `#${current.anchor}`;
      if (active) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    }
    const activeSidebarLink = document.querySelector<HTMLElement>('.doc-toc a[aria-current]');
    activeSidebarLink?.scrollIntoView({ block: 'nearest' });
  }
  scheduleSave();
}

let ticking = false;
addEventListener(
  'scroll',
  () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => {
      ticking = false;
      onScroll();
    });
  },
  { passive: true },
);

let saveTimer: ReturnType<typeof setTimeout> | undefined;
function save() {
  clearTimeout(saveTimer);
  saveTimer = undefined;
  actions.updateReadingPosition(docId, current?.id, current?.anchor, progress);
}
function scheduleSave() {
  if (!saveTimer) saveTimer = setTimeout(save, 1500);
}
addEventListener('pagehide', () => saveTimer && save());

/* ---------- Bookmarks & completion ---------- */
function bookmarkFor(state: UserStudyState, sectionID: string) {
  return state.bookmarks.find((b) => b.documentID === docId && b.sectionID === sectionID);
}

function toggleBookmark(sectionID: string, title: string) {
  const state = getState();
  if (!state) return;
  const existing = bookmarkFor(state, sectionID);
  if (existing) actions.removeBookmark(existing.id);
  else actions.addBookmark(docId, sectionID, title);
}

content.addEventListener('click', (e) => {
  const button = (e.target as HTMLElement).closest<HTMLButtonElement>('[data-bookmark]');
  if (!button) return;
  const heading = button.closest<HTMLElement>('[data-section-id]')!;
  toggleBookmark(heading.dataset.sectionId!, heading.dataset.sectionTitle ?? heading.textContent!.trim());
});

completeBtn.addEventListener('click', () => actions.toggleCompleted(docId));

function render(state: UserStudyState) {
  content.querySelectorAll<HTMLElement>('[data-section-id]').forEach((heading) => {
    const pressed = !!bookmarkFor(state, heading.dataset.sectionId!);
    heading.querySelector('[data-bookmark]')?.setAttribute('aria-pressed', String(pressed));
  });
  const done = !!state.readingStates[docId]?.explicitlyCompleted;
  completeBtn.setAttribute('aria-pressed', String(done));
  completeBtn.textContent = done ? 'Read ✓' : 'Mark as read';
}
subscribe(render);

/* ---------- Deep links by section id (bookmarks, iOS parity) ---------- */
const sectionParam = new URLSearchParams(location.search).get('section');
if (sectionParam) {
  const heading = content.querySelector<HTMLElement>(`[data-section-id="${CSS.escape(sectionParam)}"]`);
  const target = sections.find((s) => s.id === sectionParam)?.el ?? heading;
  history.replaceState(null, '', location.pathname + (target ? `#${target.id}` : ''));
  target?.scrollIntoView();
}

/* ---------- Resume ---------- */
loadState().then((state) => {
  render(state);
  const rs = state.readingStates[docId];
  const target = rs?.scrollAnchor ? sections.find((s) => s.anchor === rs.scrollAnchor) : undefined;
  const firstSection = sections[0];
  if (!location.hash && !sectionParam && target && target !== firstSection) {
    const note = document.querySelector<HTMLElement>('[data-resume]')!;
    note.querySelector('[data-resume-title]')!.textContent = target.title;
    note.querySelector('[data-resume-link]')!.addEventListener('click', (e) => {
      e.preventDefault();
      note.hidden = true;
      history.replaceState(null, '', `#${target.anchor}`);
      target.el.scrollIntoView();
    });
    note.querySelector('[data-resume-dismiss]')!.addEventListener('click', () => (note.hidden = true));
    note.hidden = false;
  }
  actions.markOpened(docId);
  onScroll();
});

/* ---------- Dialogs ---------- */
document.querySelector('[data-open-toc]')?.addEventListener('click', () => tocSheet.showModal());
tocSheet.addEventListener('click', (e) => {
  if (e.target === tocSheet || (e.target as HTMLElement).closest('a')) tocSheet.close();
});
document.querySelectorAll<HTMLElement>('[data-close-dialog]').forEach((b) =>
  b.addEventListener('click', () => b.closest('dialog')?.close()),
);

/* ---------- Keyboard ---------- */
function jump(delta: 1 | -1) {
  const idx = current ? sections.indexOf(current) : -1;
  const target = sections[Math.max(0, Math.min(sections.length - 1, idx + delta))];
  if (!target) return;
  history.replaceState(null, '', `#${target.anchor}`);
  target.el.scrollIntoView();
}

document.addEventListener('keydown', (e) => {
  const el = e.target as HTMLElement;
  if (e.metaKey || e.ctrlKey || e.altKey || el.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(el.tagName)) return;
  if (document.querySelector('dialog[open]')) return;
  switch (e.key) {
    case 'j':
      jump(1);
      break;
    case 'k':
      jump(-1);
      break;
    case 'b':
      if (current) toggleBookmark(current.id, current.title);
      break;
    case 't':
      if (getComputedStyle(document.querySelector('.doc-toc')!).display === 'none') tocSheet.showModal();
      else document.querySelector<HTMLElement>('.doc-toc a[aria-current], .doc-toc a')?.focus();
      break;
    case '?':
      shortcuts.showModal();
      break;
    default:
      return;
  }
  e.preventDefault();
});
