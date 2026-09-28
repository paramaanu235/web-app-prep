import XCTest
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

    func testSepiaThemePersists() {
        store.updatePreferences(theme: "sepia")
        XCTAssertEqual(store.state.themePreference, "sepia")

        let reloaded = StudyStateStore(customDirectory: tempDirectory)
        XCTAssertEqual(reloaded.state.themePreference, "sepia")
    }
}
