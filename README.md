# Interview Prep

Google interview preparation notes, cheat sheets and a 12-week tracker, available as:

- **Web app**: <https://paramaanu235.github.io/web-app-prep/>. Source in [`web/`](web/), plan in [`web/PLAN.md`](web/PLAN.md).
- **iOS app**: offline SwiftUI app in [`ios/GoogleInterviewPrep`](ios/GoogleInterviewPrep/README.md).

The 18 `.md` / `.java` files in the repository root are the single source of truth for both apps. Each file's SHA-256 is recorded in
`ios/GoogleInterviewPrep/GoogleInterviewPrep/Resources/ContentManifest.json`, and both builds refuse to run if a file doesn't match.
After editing content, follow [`CONTENT_UPDATE.md`](ios/GoogleInterviewPrep/CONTENT_UPDATE.md).

## Web app

```bash
cd web
npm install
npm run dev      # http://localhost:4321/web-app-prep/
npm test         # unit: integrity, iOS parity, backup format, search
npm run test:e2e # browser: Playwright + axe against the production build
npm run lighthouse -- --desktop   # needs `npx astro preview --port 4322` running
npm run build    # static site in web/dist
```

Every push to `main` runs all of the above and deploys to GitHub Pages via `.github/workflows/deploy-web.yml`, then smoke-tests the live site (including offline mode).

Study progress, bookmarks and notes stay in your browser (IndexedDB). Use **Settings → Export** to back them up; the file is the same format as the iOS app's export, so it can be imported on either one.
