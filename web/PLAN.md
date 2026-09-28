# Plan: Interview Prep web app

A web app with a minimal theme and strong readability, built on the same content and data as the iOS app in `ios/GoogleInterviewPrep`.

- **Live site:** <https://paramaanu235.github.io/web-app-prep/>
- **Repository:** <https://github.com/paramaanu235/web-app-prep> (the whole `prep_for_google` folder: content, `ios/`, `web/`)
- **Hosting:** GitHub Pages, deployed by GitHub Actions on every push to `main`

## 1. What we're carrying over from iOS

The iOS app is basically a reader built around 18 study files, plus some personal study state. The web app reuses its source data as-is and does not create a second copy:

| iOS piece | What it is | Web approach |
|---|---|---|
| 18 root `.md` / `.java` files | The only source of truth | Read directly at build time; never copied or edited |
| `ContentManifest.json` | Titles, categories, order, sha256, "historical" flag | Same file drives the web navigation and integrity checks |
| `build_content.swift` | Splits files into sections, builds anchors like `{docId}-{slug}` and `{docId}-line-N` | Ported to TypeScript (`src/content-pipeline/`). A test checks that all 521 section ids, anchors and token sets match the iOS `SearchIndex.json` exactly |
| `SearchService.swift` | Scored search that keeps code identifiers intact (`select_for_update`, `@Transactional`) | Scoring ported line for line (`src/lib/search/engine.ts`) |
| `UserStudyState` | Reading progress, bookmarks, 12-week tracker, checklist, mocks, theme | Same JSON shape, stored in IndexedDB; import/export works both ways with iOS |
| Home / Library / Search / Progress / Saved tabs | App sections | Routes (section 4) |

## 2. Stack

- **Astro** (static site) with **Preact** for the interactive parts. Pages are rendered to static HTML at build time and ship almost no JavaScript. Only search, the tracker, bookmarks and settings run in the browser.
- **Shiki** for syntax highlighting at build time (GitHub Light / GitHub Dark Dimmed), so no highlighting code ships to the browser.
- **remark/rehype** for Markdown, with GitHub-style tables. Heading ids are set from the ported sectioniser, matched by source line.
- **IndexedDB** (via `idb-keyval`) for study state, synced across open tabs with `BroadcastChannel`, plus JSON export/import.
- **Offline support** through a service worker generated after each build (`integrations/service-worker.ts`). It precaches every page, script, style, font and the search index, and is registered only once the page is idle so it never slows first paint.
- **Vitest** for unit tests and content checks, `astro check` for types, **Playwright + axe** for browser tests, and a **Lighthouse** script (`npm run lighthouse`).
- Fonts are self-hosted (`@fontsource`), so nothing loads from a third-party CDN.

```
web/
  src/content-pipeline/   # manifest loader, sha256 check, sectioniser, slugify/tokenize, Markdown + Java rendering
  src/lib/search/         # SearchService port
  src/lib/state/          # UserStudyState types, IndexedDB store, actions, iOS-compatible codec
  src/lib/prefs.ts        # theme / font / size / line length
  src/components/         # Astro components + Preact islands
  src/pages/              # routes, search-index.json, manifest.webmanifest
  integrations/           # post-build service worker generator
  src/scripts/            # reader behaviour (scroll-spy, bookmarks, shortcuts)
  tests/                  # Vitest
  e2e/                    # Playwright + axe
  scripts/lighthouse.mjs  # Lighthouse audit, fails below a threshold
```

## 3. GitHub Pages constraints (amendment)

Hosting on GitHub Pages changes a few things:

1. **Base path.** The site lives at `/web-app-prep/`, not `/`. `astro.config.mjs` sets `site`, `base: '/web-app-prep'` and `trailingSlash: 'always'`. Every internal link uses `import.meta.env.BASE_URL`, and the service worker is scoped to the base path.
2. **Static only.** There is no server, so every route is prerendered. Search, bookmarks and deep links resolve in the browser, using query strings (`?q=`, `?week=`, `?section=`) and hashes, which Pages serves without rewrites.
3. **404.** Astro emits `404.html`, which Pages serves for unknown paths under the site.
4. **The site is public.** GitHub Pages has no access control on personal accounts; even a private repo would still publish a public site. The study content is readable by anyone with the URL. Personal data (progress, notes, bookmarks) never leaves the browser.
5. **Deploys.** `.github/workflows/deploy-web.yml` runs on every push to `main` and on pull requests: unit tests (including the SHA-256 integrity check), `astro check`, the Playwright suite, and Lighthouse (accessibility, best practices and SEO must be ≥ 95). Only `main` deploys to Pages. A final job then smoke-tests the live site, including offline mode. A content edit without a manifest update fails the build instead of shipping mismatched content.
6. **Line endings.** `.gitattributes` marks the `.md`/`.java` files `-text` so Git never rewrites them, which would break their hashes.

## 4. Design: minimal layout, readable text

**Typography**
- Line length capped at 70ch by default (62ch narrow / 84ch wide). Body text 18px, line height 1.68, paragraph spacing 1em.
- Reading font: system sans by default, with **Source Serif 4** as an option. Headings, code and the interface are always sans. Code uses **JetBrains Mono**.
- Heading scale of about 1.25; `h2`s get a thin top rule and generous space above, so long cheat sheets are easy to skim.
- Body text contrast of at least 7:1 in every theme. One accent colour, used for links, focus rings and active states.

**Themes:** System, Light, Dark (soft `#141414`, not pure black) and Sepia. They're applied by an inline script before first paint, so there's no flash of the wrong theme.

**Layout**
- Desktop (>1240px) has three columns: document list, article, and an "On this page" table of contents that highlights the section you're reading. Below 1240px the document list is hidden; below 960px only the article shows, with a floating **Contents** button that opens a bottom sheet.
- No cards, gradients or shadows. Structure comes from spacing and 1px dividers. A thin reading-progress bar sits at the top.

**Code and tables**
- Code blocks never wrap by default. They scroll sideways and have **Copy** and **Wrap** buttons plus a language label. They can extend wider than the text measure.
- Tables scroll sideways inside a bordered container with light row striping. (A sticky header row isn't possible inside a horizontally scrolling container, so that item was dropped.)
- The Java source viewer has line numbers that don't get copied, every line linkable as `#{docId}-line-N` (the iOS anchors), and a highlighted target line. The outline in the right column lists classes and methods. Find-in-file uses the browser's own ⌘F / Ctrl+F.

**Keyboard:** `⌘K`, `Ctrl K` or `/` search · `j`/`k` next/previous section · `t` table of contents · `b` bookmark the current section · `?` help.

**Reader settings:** Theme is stored in the shared `themePreference`, so it travels with iOS backups. Font, text size and line length are web-only (`localStorage`), because iOS `bodyFontSize` means something different on a phone.

## 5. Routes

| Route | Contents |
|---|---|
| `/web-app-prep/` | Home: week N of 12, days until the interview, this week's numbers, continue reading, today's drills, start here, recent bookmarks |
| `/library/` | Documents grouped by the 7 categories, with reading progress |
| `/docs/[id]/` | Reader for both Markdown and Java (amendment: one route instead of `/docs` + `/source`). Deep links: `#anchor` or `?section={sectionID}` |
| `/search/?q=` | Full results with category, format and historical filters. `⌘K` opens the quick palette on any page |
| `/progress/?week=N` | Totals, 12-week grid, week editor (status, hours, problems, sessions, confidence, notes, mocks), checklist, slow patterns |
| `/saved/` | Bookmarks grouped by document, with notes |
| `/settings/` | Theme and typography, study dates, JSON export/import, resets, integrity info |

## 6. Things to get right (all implemented and tested)

1. **Anchor parity.** Bookmarks store `documentID`/`sectionID`. The TypeScript sectioniser reproduces Swift's output exactly, `tests/content.test.ts` compares it with the iOS `SearchIndex.json`, and every anchor was checked to exist in the rendered HTML.
2. **Swift JSON quirk.** `[Int: WeekProgress]` is encoded as a flat `[1, {…}, 2, {…}]` array. The codec reads and writes that format, and also accepts object keys.
3. **Dates.** ISO 8601 with **no fractional seconds**: Swift's `.iso8601` decoder rejects `.123Z`, so every timestamp is written without milliseconds. Import also accepts Swift reference-date numbers.
4. **Validation.** Import applies the same rules as `ExportImportService.validateImportData` (week range, hours ≤ 168, solved ≤ attempted, confidence 1–5, mock score 1–4, theme, font sizes).
5. **Integrity.** The build and the tests recompute SHA-256 for all 18 files and fail on any mismatch with the manifest.
6. **Links between documents.** GitHub-style `#1-singleton` fragments and absolute `/…/file.md:884` links are rewritten to the right document and section.
7. **Search index size.** The lazily loaded `search-index.json` is about 1.1 MB raw (about 300 KB gzipped on Pages). Search runs on the main thread over pre-lowercased entries, which takes about 3 ms per query for 521 sections, so the Web Worker from the original plan wasn't needed.

## 7. Phases

| # | Milestone | Status |
|---|---|---|
| 0 | Astro project, design tokens and themes, reading layout | ✅ Done |
| 1 | Content pipeline: manifest, hash check, sectioniser, anchors, Shiki | ✅ Done (parity test green) |
| 2 | Reader: TOC with scroll-spy, code/table handling, Java viewer, reader settings | ✅ Done |
| 3 | Search: scoring port, `⌘K` palette, results page | ✅ Done |
| 4 | State: IndexedDB store, reading progress, bookmarks, notes, iOS import/export | ✅ Done |
| 5 | Progress: home dashboard, 12-week tracker, checklist, mock log, slow patterns | ✅ Done |
| 6 | Polish: Playwright e2e + axe, Lighthouse ≥ 95, offline verification on the deployed site | ✅ Done (section 9) |
| 7 | Deploy plus CI (tests, type check, build, integrity) on GitHub Pages | ✅ Workflow in place |

## 8. Open decisions

- **Sync between devices.** v1 uses the manual JSON export/import that already works with iOS. Automatic sync would need a backend (for example Supabase, or a Cloudflare Worker with KV), because GitHub Pages is static. Deferred.
- **Keeping content private.** If the notes shouldn't be public, the site would have to move to a host with access control, such as Cloudflare Pages with Cloudflare Access. The Astro build works there unchanged apart from `site`/`base`.

## 9. Phase 6 results

**Browser tests** (`npm run test:e2e`, 56 tests, desktop + Pixel 7) run against the production build:
- every route and all 18 documents render without console errors, and unknown paths get the 404 page;
- reader: TOC scroll-spy, copy/wrap, in-page links, bookmarks and notes, `j`/`k`/`b`/`?` shortcuts, mark as read, resume position, Java line links, `?section=` deep links;
- search palette (`/`, `⌘K`, header button) and the search page filters;
- theme persistence, the week editor, mock log, and export → reset → import round trip in the iOS format; invalid backups are rejected;
- offline: after one visit, other documents, the library and search all work with the network off;
- phones: Contents sheet, menu, no sideways scrolling;
- axe (WCAG 2.1 A/AA) on 9 pages in light, dark and sepia, plus the open search palette: no violations.

**Lighthouse** (local production build, 7 pages):

| | Performance | Accessibility | Best practices | SEO |
|---|---|---|---|---|
| Mobile (throttled) | 99–100 | 100 | 100 | 100 |
| Desktop | 100 | 100 | 100 | 100 |

**Bugs the tests found and fixed**
1. Home, Progress, Saved and Settings kept `aria-busy="true"` and a 60vh min-height after loading. The store was often ready before hydration, so the first client render didn't match the server HTML and Preact left the placeholder behind. Islands now always hydrate from the placeholder state.
2. Four GitHub Light token colours (keywords, comments, strings, numbers) and one Dark Dimmed colour were below 4.5:1 on our code backgrounds, down to 2.8:1 on sepia. They're replaced with same-hue variants that pass in every theme.
3. Search matches (`<mark>`) in dark mode inherited muted text on a dark yellow background. They now use the full text colour.
4. Search palette results nested a link inside `role="option"` (axe: nested-interactive). The link is now the option.
5. Pressing `/`, `⌘K` or clicking Search before the palette hydrated did nothing. Shortcuts now live in the always-loaded app script and are replayed on hydration.
6. Offline, pages you hadn't visited online failed to load their scripts, because only visited pages' assets were cached. The service worker is now generated after the build with a full asset list, and ignores `Vary` headers when matching.
7. Home's mobile Speed Index was 12 s because the service worker precached the whole site during first load. Registration now waits for load + idle.
