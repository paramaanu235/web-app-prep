# Antigravity plan: local Google Interview Prep iOS app

## 1. Objective

Build a polished, offline-first iPhone app named **Google Interview Prep** from the study material in this directory. The app must preserve every source document and source-code file, arrange them into a useful study library, provide full-text search and personal progress tracking, and install locally on the owner's iPhone through Xcode.

The app is a private study tool. It needs no account, backend, analytics, ads, network connection, cloud database, App Store submission, or in-app purchase.

### Non-negotiable outcomes

1. Every one of the 18 source artifacts in the manifest below is bundled and reachable in the UI.
2. Source content is copied byte-for-byte. Do not summarize, rewrite, deduplicate, or silently omit overlapping documents.
3. Markdown headings, tables, lists, links, fenced code, inline code, and long code blocks render clearly on an iPhone.
4. Java and Python material is searchable, readable, bookmarkable, and available offline.
5. User state—reading progress, bookmarks, notes, weekly check-ins, and mock results—persists across app launches.
6. A content-integrity test fails the build if a manifest entry is missing, duplicated, empty, renamed without updating the manifest, or altered during packaging.
7. The repository includes exact instructions for installing and reopening the app locally on a physical iPhone.

---

## 2. Instructions to Antigravity

Treat this Markdown file as the implementation specification. Work through the phases in order and continue until the Definition of Done passes. Make reasonable UI implementation choices within this scope; do not replace source material with generated summaries.

Create the app in:

```text
ios/GoogleInterviewPrep/
```

Do not edit the 18 canonical source files in the workspace root. The build pipeline may copy them into the Xcode project. Generated app files, indexes, HTML, and manifests belong under `ios/GoogleInterviewPrep/`.

Use:

- Swift 6-compatible source
- SwiftUI
- iPhone deployment target iOS 16.4 or later
- `NavigationStack` and native accessibility/dynamic-type support
- XCTest for unit/integrity tests and XCUITest for the critical navigation flow
- Codable JSON stored in Application Support for user state, so the app does not require iOS 17 SwiftData
- `WKWebView` for faithful document rendering
- locally bundled Markdown/rendering and syntax-highlighting assets; never load JavaScript, CSS, fonts, or content from a CDN at runtime

The Xcode project must build without a paid third-party service. Prefer Apple frameworks. If a build-time package is used, pin its exact version and document it. Keep runtime content fully offline.

---

## 3. Canonical source manifest

The current canonical input is 18 files, 496 KB total, and 10,833 lines. Store this list in a machine-readable `ContentManifest.json`; do not discover inputs with a broad glob after app files have been added.

Line counts below are an audit baseline, not a permanent validation rule. SHA-256 hashes should be regenerated deliberately whenever a canonical source file is amended, then reviewed in the manifest diff.

| Order | File | Lines | Category | Display title | Treatment |
|---:|---|---:|---|---|---|
| 1 | `quick_reference.md` | 68 | Start Here | Quick Reference | Featured home entry |
| 2 | `codex_proposed_plan.md` | 282 | Plans | Primary 12-Week Plan | Mark as primary plan |
| 3 | `gemini_proposed_plan.md` | 340 | Plans | Alternate Plan — Gemini | Preserve in full |
| 4 | `grok_proposed_plan.md` | 256 | Plans | Alternate Plan — Grok | Preserve in full |
| 5 | `weekly_tracker.md` | 85 | Progress | 12-Week Tracker | Document plus native tracker views |
| 6 | `star_story_bank.md` | 125 | Behavioral | STAR Story Bank | Document plus editable story forms |
| 7 | `grok_coding_questions.md` | 376 | DSA Practice | Google L4/L5 Coding Questions | Preserve week grouping |
| 8 | `amazon_dsa_questions.md` | 402 | DSA Practice | Amazon DSA Questions | Keep separate from Google material |
| 9 | `grok_python_snippets.md` | 1,607 | Python | Python Interview Muscle Memory | Large code reference |
| 10 | `java_interview_cheatsheet.md` | 1,771 | Java | Java Interview Snippets | Large code reference, 53 sections |
| 11 | `JavaInterviewTemplates.java` | 935 | Java | Java Interview Templates — Source | Raw Java source viewer |
| 12 | `JavaInterviewTemplatesTest.java` | 225 | Java | Java Template Tests — Source | Raw Java source viewer |
| 13 | `java_design_pattern_cheatsheet.md` | 1,462 | Java | Java Design Patterns | Preserve all 33 patterns |
| 14 | `java_8_vs_17_interview_guide.md` | 799 | Java | Java 8 to 17 Interview Guide | Preserve version/reference sections |
| 15 | `django_cheatsheet.md` | 617 | Backend | Django Cheat Sheet | Preserve official-reference links |
| 16 | `fastapi_cheatsheet.md` | 600 | Backend | FastAPI Cheat Sheet | Preserve official-reference links |
| 17 | `spring_boot_cheatsheet.md` | 709 | Backend | Spring Boot Cheat Sheet | Preserve official-reference links |
| 18 | `grok_python_snippets_review.md` | 174 | Archive & Reviews | Historical Python Snippet Review | Clearly label as historical; do not treat old findings as current source truth |

### Content grouping shown in the app

```text
Start Here
└── Quick Reference

12-Week Preparation
├── Primary 12-Week Plan
├── Alternate Plan — Gemini
├── Alternate Plan — Grok
└── 12-Week Tracker

DSA Practice
├── Google L4/L5 Coding Questions
├── Amazon DSA Questions
├── Python Interview Muscle Memory
└── Java Interview Snippets

Java & Design
├── Java Interview Snippets
├── Java Interview Templates — Source
├── Java Template Tests — Source
├── Java Design Patterns
└── Java 8 to 17 Interview Guide

Backend Frameworks
├── Django Cheat Sheet
├── FastAPI Cheat Sheet
└── Spring Boot Cheat Sheet

System Design
└── Deep link to the System Design sections in the primary and alternate plans

Behavioral
└── STAR Story Bank

Archive & Reviews
└── Historical Python Snippet Review
```

It is acceptable for one canonical document to appear in more than one navigation collection, such as Java Interview Snippets under DSA and Java. There must still be one underlying document ID, one reading state, and one search index entry.

---

## 4. Product structure

Use a five-tab layout:

### Home

- Current preparation week and days remaining, configured locally by interview date
- “Continue reading” card
- This week's plan milestones
- Today checklist
- Quick Reference shortcut
- Recent bookmarks
- Upcoming mock or review item
- A content status line such as “18 documents available offline”

The user can set or change the interview date in Settings. If no date is set, show week selection without inventing a date. Compute the current week from a user-selected preparation start date, capped to weeks 1–12.

### Library

- Category list in the order specified above
- Document cards with title, short static description, section count, reading percentage, and last-opened position
- Collapsible table of contents generated from Markdown headings
- Filters for Plans, DSA, Python, Java, Backend, System Design, Behavioral, and Archive
- “All Documents” view proving that all 18 unique documents are present

### Search

- Full-text search across document title, section path, prose, inline code, and fenced-code content
- Results grouped by document and section
- Match snippets with highlighted terms
- Filters by category, language, and source type (`Markdown`, `Java`)
- Selecting a result opens the document at the matching heading or line anchor
- Search must work in airplane mode and should be debounced

The corpus is small enough for an in-memory normalized index generated at build time. Avoid introducing a database search dependency unless profiling proves it necessary. Preserve code identifiers during tokenization: searching `select_for_update`, `CompletableFuture`, `DB_CASCADE`, `0-1 BFS`, or `@Transactional` must find the expected material.

### Progress

- Native 12-week dashboard derived from `weekly_tracker.md`
- Each week: status, planned hours, completed hours, problems attempted, problems solved independently, mocks, system-design practices, behavioral stories, confidence, and notes
- Daily checklist matching the source tracker: timed problem, review, error log, system design/behavioral block as appropriate
- Mock log: date, coding/design/behavioral type, score, strengths, misses, next drill
- Slow-pattern list and design-writeup checklist
- Export all user-entered progress as JSON through the iOS share sheet
- Import validates a schema version and asks before replacing existing local state

Do not infer completion merely because a document was scrolled. Reading percentage and explicit completion are separate fields.

### Saved

- Bookmarked documents, sections, code blocks, and search results
- User notes attached to a document section or code block
- Filter by category and sort by most recent or source order
- Copy code button preserves the exact code text and line breaks

### Settings

- Preparation start date and interview date
- Theme: system/light/dark
- Code font size and body text size adjustment, in addition to Dynamic Type
- Reset only reading positions, only tracker data, or all local user state; each requires a clear destructive confirmation
- Content version, manifest date, document count, and integrity status
- Export/import
- Local-install help

---

## 5. Document reader requirements

### Markdown

Render Markdown inside `WKWebView` using a local HTML shell and vendored renderer/highlighter assets. The renderer must support:

- H1–H4 headings with stable anchors
- tables that can horizontally scroll without making the whole page overflow
- fenced code with language label, wrapping toggle, horizontal scrolling, and copy button
- inline code
- nested lists and task lists
- block quotes and horizontal rules
- external HTTPS links, opened through an explicit user action in the system browser
- absolute workspace file links displayed as text when they cannot resolve on the phone

Sanitize rendered HTML and block arbitrary network navigation inside the web view. Load only app-bundled files. Apply iOS theme colors through CSS variables and update correctly when appearance changes.

### Raw Java source

Display `.java` files as syntax-highlighted source with:

- line numbers
- find-in-document
- copy selection and copy entire file
- jump-to-symbol/section using a lightweight build-time index of class and method declarations
- optional line wrapping

The raw source must remain byte-identical to the canonical file in the app bundle. A separately generated highlighted representation is fine.

### Reader navigation and state

- Native table-of-contents drawer
- Previous/next section controls
- Restore the last section and scroll anchor per document
- Bookmark current section or individual code block
- Add a note without modifying the source
- Display source filename and “historical” badge where relevant
- Keep the screen awake only if the user enables an optional study-session toggle; default behavior follows system settings

---

## 6. Data model

Use stable string IDs so state survives content rebuilds.

```swift
struct ContentDocument: Codable, Identifiable {
    let id: String                    // e.g. "java.interview.snippets"
    let title: String
    let sourceFilename: String
    let format: ContentFormat         // markdown or java
    let primaryCategory: String
    let categoryIDs: [String]
    let order: Int
    let isHistorical: Bool
    let sha256: String
    let byteCount: Int
    let lineCountAtManifestBuild: Int
}

struct ContentSection: Codable, Identifiable {
    let id: String                    // document ID + stable slug + collision suffix
    let documentID: String
    let title: String
    let headingLevel: Int
    let parentSectionID: String?
    let anchor: String
    let plainText: String
    let searchTerms: [String]
}

struct ReadingState: Codable {
    let documentID: String
    var lastSectionID: String?
    var scrollAnchor: String?
    var estimatedProgress: Double
    var explicitlyCompleted: Bool
    var lastOpenedAt: Date
}

struct Bookmark: Codable, Identifiable {
    let id: UUID
    let documentID: String
    let sectionID: String?
    let codeBlockID: String?
    let exactQuoteHash: String?
    var note: String
    let createdAt: Date
    var updatedAt: Date
}

struct WeekProgress: Codable, Identifiable {
    let week: Int
    var status: WeekStatus
    var plannedHours: Double
    var completedHours: Double
    var attempted: Int
    var independentlySolved: Int
    var mocks: [MockResult]
    var systemDesignSessions: Int
    var behavioralStoriesPracticed: Int
    var confidence: Int
    var notes: String
}
```

Persist one versioned `UserStudyState.json` atomically: write to a temporary file, validate it, then replace the previous state. Keep one recoverable previous version. Never store canonical study content inside mutable user state.

---

## 7. Content pipeline and integrity

Create a deterministic build tool under:

```text
ios/GoogleInterviewPrep/Tools/build_content.swift
```

It must:

1. Resolve the workspace root explicitly.
2. Read only the 18 paths declared in `ContentManifest.json`.
3. Reject missing, unreadable, duplicate, empty, non-UTF-8, or unexpected file types.
4. Normalize nothing in the copied source: preserve bytes and line endings.
5. Verify each source SHA-256 against the reviewed manifest.
6. Copy canonical bytes into `GoogleInterviewPrep/Resources/StudyContent/`.
7. Parse headings and fenced-code boundaries without treating `#` inside code blocks as headings.
8. Generate stable heading/code-block anchors and a compact search index.
9. Generate an `IntegrityReport.json` with filename, hash, bytes, lines, heading count, code-block count, and indexed character count.
10. Fail on duplicate stable IDs or anchors.

When a source document is intentionally edited, provide a command that reports the old/new hash and requires the developer to update the manifest explicitly. Do not silently accept hash drift.

### Integrity tests

Add tests that assert:

- exactly 18 unique canonical document IDs exist
- every declared file exists both at the canonical path and in the built app resources
- canonical and bundled SHA-256 values match
- bundled content can be decoded as UTF-8 and is nonempty
- all 10,833 baseline lines are represented for the initial build; later intentional content changes update the recorded line counts
- Markdown fenced-code delimiters are balanced where the source expects balanced fences
- all Markdown headings outside fences appear in the generated table of contents
- raw Java line counts and bytes match exactly
- all category references resolve to a document
- all internal document/section deep links resolve
- the historical review file is present and visibly marked historical
- searches for a fixed smoke-test vocabulary reach the intended documents

Smoke-test vocabulary:

```text
FETCH_PEERS
OAuth2PasswordBearer
spring-boot-starter-webmvc
reverseKGroup
minimum covering window
Union-Find
Bigtable
BigQuery
Googleyness
STAR
Java 17
Visitor
```

---

## 8. Project layout

```text
ios/GoogleInterviewPrep/
├── GoogleInterviewPrep.xcodeproj
├── GoogleInterviewPrep/
│   ├── App/
│   │   ├── GoogleInterviewPrepApp.swift
│   │   └── AppEnvironment.swift
│   ├── Models/
│   ├── Services/
│   │   ├── ContentRepository.swift
│   │   ├── SearchIndex.swift
│   │   ├── StudyStateStore.swift
│   │   └── ExportImportService.swift
│   ├── Features/
│   │   ├── Home/
│   │   ├── Library/
│   │   ├── Reader/
│   │   ├── Search/
│   │   ├── Progress/
│   │   ├── Saved/
│   │   └── Settings/
│   ├── Components/
│   ├── Resources/
│   │   ├── ContentManifest.json
│   │   ├── StudyContent/
│   │   ├── SearchIndex.json
│   │   ├── IntegrityReport.json
│   │   └── Web/
│   │       ├── reader.html
│   │       ├── reader.css
│   │       ├── markdown-renderer.min.js
│   │       └── syntax-highlighter.min.js
│   └── Preview Content/
├── GoogleInterviewPrepTests/
├── GoogleInterviewPrepUITests/
├── Tools/
│   └── build_content.swift
├── README.md
└── CONTENT_UPDATE.md
```

Keep views small and inject services through `AppEnvironment`. Make `ContentRepository` read-only. Keep user state operations behind `StudyStateStore` so UI tests can use a temporary store.

---

## 9. UI and accessibility standard

- Use a restrained system-native visual style suitable for long study sessions.
- Support light and dark mode, Dynamic Type, VoiceOver labels, Reduce Motion, and sufficient contrast.
- Minimum touch targets: 44×44 points.
- Long titles wrap; they do not truncate essential distinctions such as “primary” versus “historical.”
- Use a monospaced font for source code, with adjustable size.
- Preserve selection and copy inside readers.
- Avoid horizontal scrolling for prose. Tables and non-wrapped code may scroll within their own containers.
- Show an empty state and recovery action for every list/search screen.
- Do not use color alone to represent progress or category.
- Do not place framework implementation details in learner-facing copy.

App icon and accent color can be simple and original: an abstract `{ }`/path motif without Google trademarks or copied logos.

---

## 10. Implementation phases

### Phase 0 — Environment and skeleton

- Verify Xcode and an iOS simulator are available.
- Create the app target, unit-test target, and UI-test target.
- Set a unique placeholder bundle identifier such as `dev.apoorv.GoogleInterviewPrep`, which the owner can change for signing.
- Add a CI-style local command that builds for an iPhone simulator.
- Commit no signing certificate, provisioning profile, Apple ID, or secret.

Exit check: the empty app builds and launches in the simulator.

### Phase 1 — Content ingestion

- Create the explicit manifest with the 18 canonical files and reviewed hashes.
- Implement the deterministic content builder.
- Add the resources to the app target.
- Generate the integrity report and search/section indexes.
- Add content-integrity tests before building UI beyond a diagnostic list.

Exit check: test output reports 18/18 sources, zero missing files, zero hash mismatches, and zero duplicate IDs.

### Phase 2 — Library and readers

- Implement category navigation and All Documents.
- Implement Markdown and raw Java readers.
- Add table of contents, anchor navigation, theme adaptation, selection, copying, and reading-position restoration.
- Test very long files, tables, and all code-block languages present in the corpus.

Exit check: every document opens; a UI test traverses all 18 entries and asserts a nonempty reader title/content marker.

### Phase 3 — Search and saved content

- Load the generated offline index.
- Implement ranked title/heading/body/code matching.
- Add category filters and section deep links.
- Add document/section/code bookmarks and notes.

Exit check: all smoke-test vocabulary searches return the expected source; airplane-mode simulator behavior is unchanged.

### Phase 4 — Tracker and home dashboard

- Implement week calculation and interview-date settings.
- Translate tracker fields into native forms while keeping the full original tracker document accessible.
- Add mock log, slow patterns, daily checklist, and Home summary.
- Add JSON export/import with schema validation and replacement confirmation.

Exit check: state persists after force-quit/relaunch; invalid imports do not damage current state.

### Phase 5 — Quality and physical-device pass

- Test iPhone SE-size and current large iPhone simulators in light/dark mode and large accessibility text.
- Run VoiceOver review of tabs, search, reader controls, tracker fields, and destructive confirmations.
- Profile launch, search latency, memory use, and scrolling in the two largest documents.
- Remove all network dependence and verify web-view navigation policy.
- Build and run on the owner's physical iPhone.

Exit check: Definition of Done below passes and README installation steps work from a clean checkout.

---

## 11. Test matrix

### Unit tests

- Manifest decoding and schema/version rejection
- Stable slug/anchor collisions
- Heading parsing around fenced code
- Search normalization for punctuation-heavy identifiers
- Search ranking and category filters
- week/date boundary behavior, including dates before and after the 12-week window
- atomic state save and previous-state recovery
- bookmark identity after app relaunch
- import merge/replace validation
- destructive reset scopes

### Content tests

- all integrity assertions from section 7
- Markdown fixture containing table, nested list, inline code, fenced Java/Python, links, and duplicate headings
- Java fixture with nested classes and overloaded methods
- source text containing HTML special characters and script-like input renders as text/code rather than executable content

### UI tests

1. Launch → All Documents → confirm 18 unique documents.
2. Open each document → confirm title and nonempty rendered content.
3. Search `DB_CASCADE` → open Django section.
4. Search `@Transactional` → open Spring/Java results.
5. Bookmark a Java code block, add a note, relaunch, confirm both remain.
6. Change code size and appearance, confirm reader updates.
7. Fill a weekly check-in, export state, reset tracker, import state, confirm restoration.
8. Open historical review and confirm its historical badge.
9. Attempt an external link and confirm it requires explicit system-browser handoff.
10. Run with networking disabled and repeat library/search/reader flows.

### Performance targets

- Warm launch to usable Home: under 1 second on a recent physical iPhone when feasible
- Search update for this corpus: under 150 ms after debounce
- No main-thread parsing of all Markdown during launch
- Smooth reader scrolling without rendering the entire library at once
- No crash or state corruption after repeated background/foreground transitions

Targets must be measured and reported with device/simulator details; do not claim them solely from implementation inspection.

---

## 12. Local iPhone installation

Document these steps in the generated project README and verify them on the actual project:

1. Install the current stable Xcode supported by macOS.
2. Open `ios/GoogleInterviewPrep/GoogleInterviewPrep.xcodeproj`.
3. In Xcode Settings → Accounts, sign in with the owner's Apple ID if needed.
4. Select the app target → Signing & Capabilities → enable automatic signing and select the owner's Personal Team or paid team.
5. Change the bundle identifier if it conflicts with an existing identifier.
6. Connect the iPhone, trust the Mac, select the phone as the run destination, and enable Developer Mode if iOS requests it.
7. Press Run. Follow any device prompt to trust/approve the developer identity.
8. Disconnect the phone and verify the entire library, search, bookmarks, and tracker work in airplane mode.

Personal/free signing can require periodic re-signing through Xcode according to Apple's current provisioning rules. The app must keep user state in the Application Support directory and support JSON export so progress can be backed up before reinstalling. A paid developer account/TestFlight can be documented as an optional distribution route, but it is outside the required local-only delivery.

Do not add App Store submission, public distribution, iCloud, or TestFlight work to the required scope.

---

## 13. Content update workflow

The canonical Markdown and Java files remain the source of truth. Document this update process in `CONTENT_UPDATE.md`:

1. Amend and validate the source file in the workspace root.
2. Run the content audit command to view changed hash, line count, heading count, and code-block count.
3. Review the source diff.
4. Explicitly update that manifest entry's hash/metadata.
5. Run the content builder.
6. Run integrity, unit, and search smoke tests.
7. Build/run the app; confirm old bookmarks resolve or are reported as orphaned with a recovery UI.

Never edit only the app-bundled copy. Generated copies should have a header or build rule making that clear.

---

## 14. Definition of Done

The task is complete only when all of these are true:

- [ ] The iOS project opens and builds without manual source-file repair.
- [ ] The app launches in a simulator and on the owner's physical iPhone.
- [ ] All 18 manifest entries are present in All Documents.
- [ ] Canonical and bundled hashes match for all 18 files.
- [ ] All original Markdown prose and code, plus both raw Java files, remain accessible.
- [ ] Library categories and cross-category references match this plan.
- [ ] Markdown tables and code blocks are usable on a small iPhone screen.
- [ ] Full-text search includes code and passes every smoke-test vocabulary case.
- [ ] Search result deep links land in the correct section.
- [ ] Reading position, explicit completion, bookmarks, notes, and tracker state persist.
- [ ] Tracker JSON export/import works and rejects invalid schema/data safely.
- [ ] Historical review content is visibly distinguished from current reference content.
- [ ] No runtime network request is needed for content, rendering, search, or persistence.
- [ ] External links cannot navigate silently inside the content web view.
- [ ] Light/dark mode, Dynamic Type, VoiceOver, and small-screen checks pass.
- [ ] Unit, content-integrity, and critical UI tests pass.
- [ ] README explains build, physical-device signing, offline verification, backup, reinstall, and content updates.
- [ ] Final handoff states the tested Xcode version, simulator/device and iOS versions, document count, integrity result, test totals, known limitations, and exact installation path.

### Required final evidence from Antigravity

Return a concise build report containing:

```text
Project path:
Xcode / Swift version:
Deployment target:
Simulator build result:
Physical iPhone run result:
Canonical documents found: 18/18
Bundled hash matches: 18/18
Indexed documents/sections/code blocks:
Unit tests:
UI tests:
Offline verification:
Accessibility checks:
Known limitations:
```

Do not report the app as complete if the physical-device run was not performed. Report it as “simulator-complete; device installation pending” and leave the verified local-install steps ready for the owner.

---

## Appendix A — initial reviewed SHA-256 baseline

Use these hashes for the first `ContentManifest.json`. Regenerate and explicitly review only when the corresponding canonical source is intentionally amended.

```text
JavaInterviewTemplates.java          53300a1255926b290e9b4ac7e569bf2ce578c57781286c4c3bf7b60556636415
JavaInterviewTemplatesTest.java      0bb1439c6cd73013b45241ddb7db7aa9bf122dd4ec4732766918590a53d9c145
amazon_dsa_questions.md              aa434a891fc780dfddc7ff35453a08848237c43fa963bef565c1a28f1147b4d2
codex_proposed_plan.md               939512e0d4fc2b5a6c8e0daca8e08ef6c689bb6945c23fd2ac27cda9ac003712
django_cheatsheet.md                 4802254719e818c910e7e46a6707a23806af93053ef5cc204da38a7b88e9786e
fastapi_cheatsheet.md                4745c328e881ed5369d7ebdf15a1a3ccaba53cd3b9dca1ede96a661598d6d4a9
gemini_proposed_plan.md              7e0d4cc5b236626a1a67aaaf798ba366dee60e87fd5a10d8f2705c0237fef4e0
grok_coding_questions.md             e82214f0b6465e797e075bdbfb038c2455d5de7606509ac57f7aaa9dbc91ce99
grok_proposed_plan.md                57d4cd07ebf03011b612e2d6b30f0d6bbcc08c6496c38cf3efdc4d157a986ab6
grok_python_snippets.md              66d75962661d8b886dbc2de3eb9f33f75dff101271b0972278f01218b61dd646
grok_python_snippets_review.md       a812c0b3ec7fed867771b05e5dc8783ae3dfa0d7c13a1e11c720965b7877a985
java_8_vs_17_interview_guide.md      e53e391520ff77f39d8554a5b52a4ee0209b99f5fbc98eb5d042318389053255
java_design_pattern_cheatsheet.md    9ec00b8ba2b1de9ebbe4e669450e21568d8a85d2843d7c498dc8ec2b2040210f
java_interview_cheatsheet.md         8ceb1fa537bdfabeea20ff803a4adcf74269d554adae2675837c9c2cc234559d
quick_reference.md                   20317101474254fc0d174b34fde2658965b9a4341899cbfe1213722024dc82e9
spring_boot_cheatsheet.md            e437c1ef1d4d44a07c27a350ac26a6b5558b7a1d5619cc9528202629f997b67b
star_story_bank.md                   b10d30bd3850fe6b23dab21d4254580c8203e08f20fb1612050c9fe5868e61e1
weekly_tracker.md                    3a12279f700d951e4aff53bca8edf3d1db05c5f9845e0fd7fcbaa0e671055354
```
