import { useState } from 'preact/hooks';
import { actions } from '../../lib/state/actions';
import { formatDate, sectionHref } from '../../lib/state/derive';
import type { Bookmark } from '../../lib/state/types';
import { useStudyState } from './hooks';
import type { DocRef } from './Home';
import { Loading } from './Loading';

function BookmarkRow({ bookmark, base, docTitle }: { bookmark: Bookmark; base: string; docTitle: string }) {
  const [editing, setEditing] = useState(false);
  const [note, setNote] = useState(bookmark.note);

  return (
    <li style={{ padding: '14px 0' }}>
      <a class="hit-title" href={sectionHref(base, bookmark.documentID, bookmark.sectionID)}>
        {bookmark.title || docTitle}
      </a>
      <div class="hit-doc">Saved {formatDate(bookmark.createdAt)}</div>
      {editing ? (
        <form
          class="stack"
          style={{ marginTop: '10px' }}
          onSubmit={(e) => {
            e.preventDefault();
            actions.updateBookmarkNote(bookmark.id, note.trim());
            setEditing(false);
          }}
        >
          <textarea aria-label="Note" value={note} onInput={(e) => setNote(e.currentTarget.value)} autoFocus />
          <div class="row">
            <button class="btn primary" type="submit">Save note</button>
            <button class="btn" type="button" onClick={() => { setNote(bookmark.note); setEditing(false); }}>Cancel</button>
          </div>
        </form>
      ) : (
        <>
          {bookmark.note && <p style={{ margin: '8px 0 0', whiteSpace: 'pre-wrap', maxWidth: '70ch' }}>{bookmark.note}</p>}
          <div class="row" style={{ marginTop: '8px' }}>
            <button class="code-btn" type="button" onClick={() => setEditing(true)}>{bookmark.note ? 'Edit note' : 'Add note'}</button>
            <button class="code-btn" type="button" onClick={() => actions.removeBookmark(bookmark.id)}>Remove</button>
          </div>
        </>
      )}
    </li>
  );
}

export default function Saved({ base, docs }: { base: string; docs: DocRef[] }) {
  const state = useStudyState();
  if (!state) return <Loading />;

  const groups = docs
    .map((doc) => ({ doc, bookmarks: state.bookmarks.filter((b) => b.documentID === doc.id) }))
    .filter((g) => g.bookmarks.length > 0);

  return (
    <div class="page page-narrow">
      <header class="page-header">
        <h1>Saved</h1>
        <p>{state.bookmarks.length} bookmark{state.bookmarks.length === 1 ? '' : 's'}. Hover a heading while reading (or press <kbd>b</kbd>) to save it.</p>
      </header>
      {groups.length === 0 ? (
        <p class="empty">Nothing saved yet.</p>
      ) : (
        groups.map(({ doc, bookmarks }) => (
          <section key={doc.id}>
            <h2 class="section-title">{doc.title}</h2>
            <ul class="divider-list">
              {bookmarks.map((b) => <BookmarkRow key={b.id} bookmark={b} base={base} docTitle={doc.title} />)}
            </ul>
          </section>
        ))
      )}
    </div>
  );
}
