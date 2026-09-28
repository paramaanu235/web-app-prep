# Google Interview Prep — iOS App

Offline-first iPhone app built with Swift 6 and SwiftUI. The app bundles and preserves the 18 canonical Google interview preparation documents (10,833 lines, 496 KB) with high-fidelity reading, offline full-text search, 12-week study progress tracking, bookmarks, notes, and zero runtime network dependencies.

---

## Features

- **18 Bundled Canonical Documents**: Preserved byte-for-byte in the app bundle. Zero summaries or omitted files.
- **Offline High-Fidelity Reader**: Powered by `WKWebView` with locally bundled HTML, CSS, Markdown parser, and syntax highlighter. Horizontal scrolling for code blocks and tables. Zero CDN or network requests.
- **Java Source Viewer**: Full syntax highlighting, line numbers, find-in-file, and symbol navigation for raw `.java` files.
- **Offline Full-Text Search**: In-memory tokenized index preserving code identifiers (`select_for_update`, `@Transactional`, `0-1 BFS`, `CompletableFuture`, `DB_CASCADE`).
- **12-Week Tracker & Checklists**: Interactive tracking derived from `weekly_tracker.md`, with planned vs. completed hours, independent solves, mock logs, and confidence ratings.
- **Bookmarks & Notes**: Save sections or code blocks with personal notes.
- **Atomic State Persistence & Backup**: Saved in `Application Support` with backup recovery, plus JSON export and import via iOS share sheet.

---

## Requirements

- **macOS**: macOS 14.0 or later
- **Xcode**: Xcode 15.0 or later (Xcode 26.2 tested)
- **Swift**: Swift 5.9 / Swift 6 (Swift 6.2.3 tested)
- **Deployment Target**: iOS 16.4 or later (iPhone & iPad)
- **Network**: None required. Completely offline.

---

## Local iPhone Installation (No Paid Account Needed)

You can run this app on your physical iPhone using Apple's free local development provisioning:

1. **Open the Project**:
   ```bash
   open ios/GoogleInterviewPrep/GoogleInterviewPrep.xcodeproj
   ```
2. **Sign in to Xcode**:
   - In Xcode, go to **Xcode → Settings → Accounts**.
   - Sign in with your standard Apple ID (no paid developer program required).
3. **Configure Signing**:
   - In the Xcode Project Navigator, select the root `GoogleInterviewPrep` project.
   - Select the `GoogleInterviewPrep` target under **Targets**.
   - Go to **Signing & Capabilities**.
   - Check **Automatically manage signing**.
   - Under **Team**, select your **Personal Team** (your name).
   - If Xcode reports a bundle ID conflict, change **Bundle Identifier** to something unique (e.g. `dev.yourname.GoogleInterviewPrep`).
4. **Connect your iPhone**:
   - Connect your iPhone to your Mac using a USB-C or Lightning cable.
   - Unlock your iPhone and tap **Trust This Computer** when prompted.
5. **Enable Developer Mode on iPhone**:
   - On iOS 16+: Go to **Settings → Privacy & Security → Developer Mode**.
   - Toggle Developer Mode **ON** and restart your iPhone when prompted.
6. **Select Destination and Run**:
   - In Xcode's destination selector (top toolbar), choose your connected iPhone.
   - Press **Run (Cmd + R)**. Xcode will build and install the app onto your phone.
7. **Trust Developer Certificate (First Time Only)**:
   - When attempting to open the app for the first time, iOS will display an "Untrusted Developer" alert.
   - On your iPhone, open **Settings → General → VPN & Device Management**.
   - Under **Developer App**, tap your Apple ID and tap **Trust**.
8. **Verify Offline / Airplane Mode**:
   - Turn on **Airplane Mode** on your iPhone.
   - Open **Interview Prep**. Browse all 18 documents, perform code searches, and create bookmarks to verify complete offline operation.

> [!NOTE]
> Free developer certificates expire after 7 days, after which you simply reconnect to your Mac and press **Run** in Xcode to refresh the profile. Your study notes, bookmarks, and tracker progress will be preserved in Application Support.

---

## Backing Up & Restoring Your Study Progress

Before updating iOS or reinstalling the app:
1. Open **Settings** (gear icon on the Home tab).
2. Tap **Export Study Progress (JSON)** to share or save your `UserStudyState.json` backup.
3. You can restore your data at any time via **Import Study Progress (JSON)**.

---

## Running Tests

From the terminal in the workspace root:

```bash
# Run unit and content integrity tests
xcodebuild test \
  -project ios/GoogleInterviewPrep/GoogleInterviewPrep.xcodeproj \
  -scheme GoogleInterviewPrep \
  -destination 'platform=iOS Simulator,name=iPhone 17' \
  -only-testing:GoogleInterviewPrepTests

# Run UI tests
xcodebuild test \
  -project ios/GoogleInterviewPrep/GoogleInterviewPrep.xcodeproj \
  -scheme GoogleInterviewPrep \
  -destination 'platform=iOS Simulator,name=iPhone 17' \
  -only-testing:GoogleInterviewPrepUITests
```

---

## Updating Canonical Content

If canonical source Markdown or Java files in the workspace root are updated:
1. Run the content build tool from the project root:
   ```bash
   swift ios/GoogleInterviewPrep/Tools/build_content.swift
   ```
2. The tool validates all 18 files, recalculates SHA-256 hashes and line counts, checks for duplicate anchors and smoke vocabulary terms, and regenerates `ContentManifest.json`, `SearchIndex.json`, and `IntegrityReport.json`.
3. Re-run `GoogleInterviewPrepTests` to verify integrity and hash synchronization before deploying.

