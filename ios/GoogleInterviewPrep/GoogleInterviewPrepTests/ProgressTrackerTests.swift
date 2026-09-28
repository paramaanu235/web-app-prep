import XCTest
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

    func testImportValidationRejectsUnsupportedSchemaVersion() {
        var state = UserStudyState.makeDefault()
        state.version = 99
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        let data = try! encoder.encode(state)
        let (result, summary) = ExportImportService.validateImportData(data)
        XCTAssertFalse(summary.isValid)
        XCTAssertNil(result)
        XCTAssertTrue(summary.errorMessage?.contains("Unsupported schema version") == true)
    }

    func testImportValidationRejectsNegativeHoursAndInvalidBounds() {
        var state = UserStudyState.makeDefault()
        state.weeklyProgress[1]?.plannedHours = -10.0
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        let data = try! encoder.encode(state)
        let (result, summary) = ExportImportService.validateImportData(data)
        XCTAssertFalse(summary.isValid)
        XCTAssertNil(result)
        XCTAssertTrue(summary.errorMessage?.contains("Invalid planned hours") == true)
    }

    func testImportValidationRejectsInvalidWeekNumber() {
        var state = UserStudyState.makeDefault()
        state.weeklyProgress[99] = WeekProgress(week: 99)
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        let data = try! encoder.encode(state)
        let (result, summary) = ExportImportService.validateImportData(data)
        XCTAssertFalse(summary.isValid)
        XCTAssertNil(result)
        XCTAssertTrue(summary.errorMessage?.contains("Invalid week number") == true)
    }

    func testImportValidationRejectsInvalidConfidenceScore() {
        var state = UserStudyState.makeDefault()
        state.weeklyProgress[1]?.confidence = 10
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        let data = try! encoder.encode(state)
        let (result, summary) = ExportImportService.validateImportData(data)
        XCTAssertFalse(summary.isValid)
        XCTAssertNil(result)
        XCTAssertTrue(summary.errorMessage?.contains("Confidence score") == true)
    }

    func testImportValidationRejectsSolvedGreaterThanAttempted() {
        var state = UserStudyState.makeDefault()
        state.weeklyProgress[1]?.attempted = 5
        state.weeklyProgress[1]?.independentlySolved = 8
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        let data = try! encoder.encode(state)
        let (result, summary) = ExportImportService.validateImportData(data)
        XCTAssertFalse(summary.isValid)
        XCTAssertNil(result)
        XCTAssertTrue(summary.errorMessage?.contains("cannot exceed attempted") == true)
    }
}