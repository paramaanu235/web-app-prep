import type { APIRoute } from 'astro';
import { loadContent } from '../content-pipeline';

// Service worker for offline reading. Every page and the search index are
// precached on install; hashed assets under _astro/ are cached on first use.
// The cache name changes with each build so old content is dropped.
export const GET: APIRoute = async () => {
  const base = import.meta.env.BASE_URL;
  const content = await loadContent();
  const pages = ['', 'library/', 'search/', 'progress/', 'saved/', 'settings/', ...content.docs.map((d) => `docs/${d.meta.id}/`)];
  const precache = [...pages, 'search-index.json', 'favicon.svg', 'manifest.webmanifest'].map((p) => base + p);
  const version = `prep-${Date.now().toString(36)}`;

  const script = `
const CACHE = ${JSON.stringify(version)};
const PRECACHE = ${JSON.stringify(precache)};

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE).then((c) => c.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith('prep-') && k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);
  if (req.method !== 'GET' || url.origin !== location.origin) return;

  if (req.mode === 'navigate') {
    // Network first so new deploys show up; cache when offline.
    event.respondWith(
      fetch(req)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req, { ignoreSearch: true }).then((r) => r || caches.match(${JSON.stringify(base)}))),
    );
    return;
  }

  // Static assets: cache first, then network (and remember it).
  event.respondWith(
    caches.match(req).then((cached) =>
      cached ||
      fetch(req).then((res) => {
        if (res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
        }
        return res;
      }),
    ),
  );
});
`;
  return new Response(script.trimStart(), { headers: { 'Content-Type': 'text/javascript' } });
};
