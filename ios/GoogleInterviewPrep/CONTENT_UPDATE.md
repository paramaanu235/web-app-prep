# Canonical Content Update Workflow

The 18 Markdown and Java files in the repository root are the sole canonical source of truth for study materials. To update, amend, or audit content:

## 1. Edit the Source Document
Amend the Markdown (`.md`) or Java (`.java`) file directly in the workspace root.

## 2. Audit Hashes and Line Counts
Calculate the new SHA-256 hash and line count:
```bash
shasum -a 256 <filename>
wc -l <filename>
```

## 3. Update the Manifest
Edit `ios/GoogleInterviewPrep/GoogleInterviewPrep/Resources/ContentManifest.json`:
- Update `sha256` with the newly computed hash.
- Update `lineCountAtManifestBuild` with the new line count.
- Update `byteCount` with the new file size.

## 4. Run the Content Builder
Rebuild the bundled content, section anchors, and search index:
```bash
swift -module-cache-path scratch/module-cache ios/GoogleInterviewPrep/Tools/build_content.swift
```

## 5. Run Verification Tests
Verify content integrity and smoke-test vocabulary:
```bash
xcodebuild test \
  -project ios/GoogleInterviewPrep/GoogleInterviewPrep.xcodeproj \
  -scheme GoogleInterviewPrep \
  -destination 'platform=iOS Simulator,name=iPhone 17' \
  -only-testing:GoogleInterviewPrepTests
```

## 6. Review Git Diff
Review `git diff` to ensure:
- Only intentional source files changed.
- `ContentManifest.json`, `SearchIndex.json`, and `IntegrityReport.json` match the new source content.
