import os

tests_dir = "ios/GoogleInterviewPrep/GoogleInterviewPrepTests"
uitests_dir = "ios/GoogleInterviewPrep/GoogleInterviewPrepUITests"
os.makedirs(tests_dir, exist_ok=True)
os.makedirs(uitests_dir, exist_ok=True)

# 1. ContentIntegrityTests.swift
integrity_test = r"""import XCTest
import CryptoKit
@testable import GoogleInterviewPrep

final class ContentIntegrityTests: XCTestCase {
    var repository: ContentRepository!

    override func setUp() {
        super.setUp()
        repository = ContentRepository()
    }

    func testManifestContainsExactlyEighteenDocuments() {
        XCTAssertEqual(repository.documents.count, 18, "Must contain exactly 18 unique canonical documents")
        let uniqueIDs = Set(repository.documents.map { $0.id })
        XCTAssertEqual(uniqueIDs.count, 18, "All 18 document IDs must be unique")
    }

    func testContentIntegrityAndLineCounts() {
        var totalLines = 0
        var totalBytes = 0

        for doc in repository.documents {
            guard let content = repository.content(for: doc) else {
                XCTFail("Failed to load content for \(doc.sourceFilename)")
                continue
            }

            XCTAssertFalse(content.isEmpty, "\(doc.sourceFilename) should not be empty")

            let data = Data(content.utf8)
            let hash = SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
            XCTAssertEqual(hash, doc.sha256, "SHA-256 hash mismatch for \(doc.sourceFilename)")

            let lines = content.components(separatedBy: "\n")
            let lineCount = lines.last == "" ? lines.count - 1 : lines.count
            totalLines += lineCount
            totalBytes += data.count

            XCTAssertEqual(lineCount, doc.lineCountAtManifestBuild, "Line count mismatch for \(doc.sourceFilename)")
        }

        XCTAssertEqual(totalLines, 10833, "Total baseline line count across all 18 files must equal exactly 10,833")
    }

    func testHistoricalBadgeOnPythonSnippetReview() {
        let historicalDoc = repository.document(withID: "grok.python.review")
        XCTAssertNotNil(historicalDoc)
        XCTAssertTrue(historicalDoc?.isHistorical == true, "grok_python_snippets_review.md must be marked isHistorical = true")

        let otherDocs = repository.documents.filter { $0.id != "grok.python.review" }
        for doc in otherDocs {
            XCTAssertFalse(doc.isHistorical, "\(doc.sourceFilename) must not be marked historical")
        }
    }

    func testCategoryResolution() {
        XCTAssertFalse(repository.startHereDocuments.isEmpty)
        XCTAssertFalse(repository.prep12WeekDocuments.isEmpty)
        XCTAssertFalse(repository.dsaDocuments.isEmpty)
        XCTAssertFalse(repository.javaDocuments.isEmpty)
        XCTAssertFalse(repository.backendDocuments.isEmpty)
        XCTAssertFalse(repository.behavioralDocuments.isEmpty)
        XCTAssertFalse(repository.archiveDocuments.isEmpty)
    }

    @MainActor
    func testSmokeTestVocabulary() {
        let searchService = SearchService(repository: repository)
        let vocabulary = [
            "FETCH_PEERS",
            "OAuth2PasswordBearer",
            "spring-boot-starter-webmvc",
            "reverseKGroup",
            "minimum covering window",
            "Union-Find",
            "Bigtable",
            "BigQuery",
            "Googleyness",
            "STAR",
            "Java 17",
            "Visitor"
        ]

        for word in vocabulary {
            searchService.performSearch(query: word, category: nil, format: nil, includeHistorical: true)
            XCTAssertFalse(searchService.results.isEmpty, "Search for '\(word)' should return at least 1 matching section")
        }
    }
}
"""

with open(f"{tests_dir}/ContentIntegrityTests.swift", "w", encoding="utf-8") as f:
    f.write(integrity_test.strip())
print("Wrote ContentIntegrityTests.swift")

# 2. StudyStateStoreTests.swift
state_test = r"""import XCTest
@testable import GoogleInterviewPrep

@MainActor
final class StudyStateStoreTests: XCTestCase {
    var tempDirectory: URL!
    var store: StudyStateStore!

    override func setUp() {
        super.setUp()
        tempDirectory = FileManager.default.temporaryDirectory.appendingPathComponent(UUID().uuidString, isDirectory: true)
        try? FileManager.default.createDirectory(at: tempDirectory, withIntermediateDirectories: true)
        store = StudyStateStore(customDirectory: tempDirectory)
    }

    override func tearDown() {
        try? FileManager.default.removeItem(at: tempDirectory)
        super.tearDown()
    }

    func testBookmarkCreationAndPersistence() {
        store.addBookmark(documentID: "quick.reference", sectionID: "qr-sec-1", title: "Test Bookmark", note: "Takeaway")
        XCTAssertEqual(store.state.bookmarks.count, 1)
        XCTAssertEqual(store.state.bookmarks.first?.title, "Test Bookmark")

        // Reload from disk
        let reloaded = StudyStateStore(customDirectory: tempDirectory)
        XCTAssertEqual(reloaded.state.bookmarks.count, 1)
        XCTAssertEqual(reloaded.state.bookmarks.first?.title, "Test Bookmark")
    }

    func testReadingStateUpdateAndCompletion() {
        store.updateReadingPosition(documentID: "codex.primary.plan", sectionID: "sec-1", anchor: "anchor-1", estimatedProgress: 0.4)
        var reading = store.readingState(for: "codex.primary.plan")
        XCTAssertEqual(reading.lastSectionID, "sec-1")
        XCTAssertEqual(reading.estimatedProgress, 0.4)
        XCTAssertFalse(reading.explicitlyCompleted)

        store.toggleExplicitCompletion(documentID: "codex.primary.plan")
        reading = store.readingState(for: "codex.primary.plan")
        XCTAssertTrue(reading.explicitlyCompleted)
    }

    func testDestructiveResetScopes() {
        store.addBookmark(documentID: "test.doc", title: "Keep me")
        store.updateReadingPosition(documentID: "test.doc", sectionID: "s1", anchor: "a1", estimatedProgress: 0.9)

        // Reset only reading positions
        store.resetReadingPositions()
        XCTAssertTrue(store.state.readingStates.isEmpty)
        XCTAssertEqual(store.state.bookmarks.count, 1, "Bookmarks must survive reading position reset")

        // Reset all
        store.resetAllState()
        XCTAssertTrue(store.state.bookmarks.isEmpty)
        XCTAssertEqual(store.state.weeklyProgress.count, 12)
    }
}
"""

with open(f"{tests_dir}/StudyStateStoreTests.swift", "w", encoding="utf-8") as f:
    f.write(state_test.strip())
print("Wrote StudyStateStoreTests.swift")

# 3. SearchServiceTests.swift
search_test = r"""import XCTest
@testable import GoogleInterviewPrep

@MainActor
final class SearchServiceTests: XCTestCase {
    var repository: ContentRepository!
    var searchService: SearchService!

    override func setUp() {
        super.setUp()
        repository = ContentRepository()
        searchService = SearchService(repository: repository)
    }

    func testPunctuationAndSymbolSearch() {
        // Test @Transactional
        searchService.performSearch(query: "@Transactional", category: nil, format: nil, includeHistorical: false)
        XCTAssertFalse(searchService.results.isEmpty)
        XCTAssertTrue(searchService.results.contains { $0.documentID == "spring.boot.cheatsheet" || $0.documentID == "java.interview.snippets" })

        // Test select_for_update
        searchService.performSearch(query: "select_for_update", category: nil, format: nil, includeHistorical: false)
        XCTAssertFalse(searchService.results.isEmpty)

        // Test 0-1 BFS
        searchService.performSearch(query: "0-1 BFS", category: nil, format: nil, includeHistorical: false)
        XCTAssertFalse(searchService.results.isEmpty)
    }

    func testFormatAndCategoryFilter() {
        // Search "class" in Java format only
        searchService.performSearch(query: "class", category: nil, format: "java", includeHistorical: false)
        for r in searchService.results {
            XCTAssertEqual(r.format, "java")
        }
    }
}
"""

with open(f"{tests_dir}/SearchServiceTests.swift", "w", encoding="utf-8") as f:
    f.write(search_test.strip())
print("Wrote SearchServiceTests.swift")

# 4. ProgressTrackerTests.swift
progress_test = r"""import XCTest
@testable import GoogleInterviewPrep

final class ProgressTrackerTests: XCTestCase {
    func testExportImportRoundTrip() {
        var state = UserStudyState.makeDefault()
        state.bookmarks.append(Bookmark(documentID: "quick.reference", title: "Important Rubric"))
        state.weeklyProgress[1]?.completedHours = 14.5
        state.weeklyProgress[1]?.status = .inProgress

        guard let exportURL = ExportImportService.exportState(state: state),
              let data = try? Data(contentsOf: exportURL) else {
            XCTFail("Export failed")
            return
        }

        let (importedState, summary) = ExportImportService.validateImportData(data)
        XCTAssertTrue(summary.isValid)
        XCTAssertEqual(summary.bookmarkCount, 1)
        XCTAssertNotNil(importedState)
        XCTAssertEqual(importedState?.weeklyProgress[1]?.completedHours, 14.5)
    }

    func testInvalidJSONImportRejected() {
        let invalidData = Data("{\"broken\": true}".utf8)
        let (state, summary) = ExportImportService.validateImportData(invalidData)
        XCTAssertFalse(summary.isValid)
        XCTAssertNil(state)
        XCTAssertNotNil(summary.errorMessage)
    }
}
"""

with open(f"{tests_dir}/ProgressTrackerTests.swift", "w", encoding="utf-8") as f:
    f.write(progress_test.strip())
print("Wrote ProgressTrackerTests.swift")

# 5. GoogleInterviewPrepUITests.swift
ui_test = r"""import XCTest

final class GoogleInterviewPrepUITests: XCTestCase {
    override func setUpWithError() throws {
        continueAfterFailure = false
    }

    func testLibraryAllDocumentsAndSmokeSearch() throws {
        let app = XCUIApplication()
        app.launch()

        // 1. Verify Home tab
        XCTAssertTrue(app.navigationBars["Home"].waitForExistence(timeout: 5))

        // 2. Navigate to Library
        let libraryTab = app.tabBars.buttons["Library"]
        if libraryTab.exists {
            libraryTab.tap()
            XCTAssertTrue(app.navigationBars["Library"].waitForExistence(timeout: 3))

            // Tap "View All 18 Documents"
            let viewAllButton = app.buttons["View All 18 Documents"]
            if viewAllButton.waitForExistence(timeout: 3) {
                viewAllButton.tap()
                XCTAssertTrue(app.navigationBars["All Documents (18)"].waitForExistence(timeout: 3))
            }
        }

        // 3. Navigate to Search tab
        let searchTab = app.tabBars.buttons["Search"]
        if searchTab.exists {
            searchTab.tap()
            let searchField = app.searchFields.firstMatch
            if searchField.waitForExistence(timeout: 3) {
                searchField.tap()
                searchField.typeText("DB_CASCADE\n")
            }
        }
    }
}
"""

with open(f"{uitests_dir}/GoogleInterviewPrepUITests.swift", "w", encoding="utf-8") as f:
    f.write(ui_test.strip())
print("Wrote GoogleInterviewPrepUITests.swift")
