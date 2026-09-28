import type { APIRoute } from 'astro';

export const GET: APIRoute = () => {
  const base = import.meta.env.BASE_URL;
  return new Response(
    JSON.stringify({
      name: 'Interview Prep',
      short_name: 'Prep',
      start_url: base,
      scope: base,
      display: 'standalone',
      background_color: '#fdfdfc',
      theme_color: '#fdfdfc',
      icons: [{ src: `${base}favicon.svg`, sizes: 'any', type: 'image/svg+xml' }],
    }),
    { headers: { 'Content-Type': 'application/manifest+json' } },
  );
};
