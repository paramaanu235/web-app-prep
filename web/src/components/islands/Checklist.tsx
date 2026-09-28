import { useState } from 'preact/hooks';
import { actions } from '../../lib/state/actions';
import { icons } from '../../lib/icons';
import type { ChecklistItem } from '../../lib/state/types';

const CATEGORIES = ['Daily DSA', 'System Design', 'Behavioral', 'Error Log'];

export function Checklist({ items, editable = false }: { items: ChecklistItem[]; editable?: boolean }) {
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState(CATEGORIES[0]!);
  const done = items.filter((i) => i.isDone).length;

  const add = (e: Event) => {
    e.preventDefault();
    if (!title.trim()) return;
    actions.addChecklistItem(title.trim(), category);
    setTitle('');
  };

  return (
    <div>
      <ul class="divider-list">
        {items.map((item) => (
          <li key={item.id}>
            <label class={`check-item${item.isDone ? ' done' : ''}`}>
              <input type="checkbox" checked={item.isDone} onChange={() => actions.toggleChecklist(item.id)} />
              <span>
                <span class="check-title">{item.title}</span>
                <small>{item.category}</small>
              </span>
              {editable && (
                <button
                  class="icon-btn"
                  type="button"
                  aria-label={`Remove “${item.title}”`}
                  onClick={(e) => {
                    e.preventDefault();
                    actions.removeChecklistItem(item.id);
                  }}
                  dangerouslySetInnerHTML={{ __html: icons.trash }}
                />
              )}
            </label>
          </li>
        ))}
      </ul>
      <div class="row" style={{ justifyContent: 'space-between', marginTop: '12px' }}>
        <span class="muted" style={{ fontSize: '14px' }}>
          {done} of {items.length} done
        </span>
        {done > 0 && (
          <button class="btn" type="button" onClick={() => actions.resetChecklist()}>
            Start a new day
          </button>
        )}
      </div>
      {editable && (
        <form class="row" style={{ marginTop: '16px' }} onSubmit={add}>
          <input
            type="text"
            placeholder="Add a drill…"
            aria-label="New checklist item"
            value={title}
            onInput={(e) => setTitle(e.currentTarget.value)}
            style={{ flex: '1 1 220px', width: 'auto' }}
          />
          <select aria-label="Category" value={category} onChange={(e) => setCategory(e.currentTarget.value)} style={{ width: 'auto' }}>
            {CATEGORIES.map((c) => (
              <option key={c}>{c}</option>
            ))}
          </select>
          <button class="btn" type="submit">
            Add
          </button>
        </form>
      )}
    </div>
  );
}
