import type { APIRoute } from 'astro';
import { loadContent } from '../content-pipeline';

// Compact search index, fetched lazily by the search palette and /search page.
export const GET: APIRoute = async () => {
  const content = await loadContent();
  const docs = Object.fromEntries(content.docs.map((d) => [d.meta.id, d.meta.title]));
  return new Response(JSON.stringify({ docs, entries: content.searchEntries }), {
    headers: { 'Content-Type': 'application/json' },
  });
};
