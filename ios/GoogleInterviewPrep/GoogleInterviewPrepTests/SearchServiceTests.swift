import XCTest
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

    func testJavaSearchReturnsExactLineAnchor() {
        // Search for code inside a Java method body
        searchService.performSearch(query: "Arrays.copyOfRange", category: nil, format: "java", includeHistorical: false)
        XCTAssertFalse(searchService.results.isEmpty, "Should find match in Java templates")
        let first = searchService.results.first!
        XCTAssertEqual(first.format, "java")
        XCTAssertTrue(first.anchor.contains("-line-"), "Anchor must be a specific line anchor: \(first.anchor)")
        if let range = first.anchor.range(of: #"-line-(\d+)$"#, options: .regularExpression) {
            let lineStr = String(first.anchor[range]).replacingOccurrences(of: "-line-", with: "")
            let lineNum = Int(lineStr) ?? 0
            XCTAssertGreaterThan(lineNum, 1, "Must deep-link to the actual matching line in method body, not line 1")
        } else {
            XCTFail("Anchor did not match line pattern: \(first.anchor)")
        }
    }
}