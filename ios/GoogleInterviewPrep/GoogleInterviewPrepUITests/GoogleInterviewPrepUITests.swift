import XCTest

final class GoogleInterviewPrepUITests: XCTestCase {
    override func setUpWithError() throws {
        continueAfterFailure = false
    }

    func testLibraryAllDocumentsAndSmokeSearch() throws {
        let app = XCUIApplication()
        app.launch()

        // 1. Verify Home tab
        XCTAssertTrue(app.navigationBars["Home"].waitForExistence(timeout: 5), "Home navigation bar must appear on launch")

        // 2. Navigate to Library
        let libraryTab = app.tabBars.buttons["Library"]
        XCTAssertTrue(libraryTab.waitForExistence(timeout: 5), "Library tab must exist")
        libraryTab.tap()
        XCTAssertTrue(app.navigationBars["Library"].waitForExistence(timeout: 5), "Library navigation bar must appear")

        // 3. Tap "View All 18 Documents" using accessibilityIdentifier
        let viewAllButton = app.buttons["viewAllDocumentsButton"]
        XCTAssertTrue(viewAllButton.waitForExistence(timeout: 5), "View All 18 Documents button must exist")
        viewAllButton.tap()

        // 4. Verify All Documents shows 18 total
        XCTAssertTrue(app.navigationBars["All Documents (18)"].waitForExistence(timeout: 5), "All Documents view with exactly 18 entries must open")

        // 5. Navigate to Search tab
        let searchTab = app.tabBars.buttons["Search"]
        XCTAssertTrue(searchTab.waitForExistence(timeout: 5), "Search tab must exist")
        searchTab.tap()

        let searchField = app.searchFields.firstMatch
        XCTAssertTrue(searchField.waitForExistence(timeout: 5), "Search field must exist")
        searchField.tap()
        searchField.typeText("DB_CASCADE\n")

        // 6. Unconditionally assert that search result appears and navigates to the document
        let djangoResult = app.cells.firstMatch
        XCTAssertTrue(djangoResult.waitForExistence(timeout: 5), "Search for 'DB_CASCADE' must return matching document cells")
        djangoResult.tap()

        XCTAssertTrue(app.navigationBars["Django Cheat Sheet"].waitForExistence(timeout: 5), "Selecting search result must navigate into Django Cheat Sheet reader")
    }
}
