import XCTest
import CryptoKit
import JavaScriptCore
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

            let lineCount = content.filter { $0 == "\n" }.count
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

    private func loadWebScript(named name: String) -> String {
        let fullName = name.hasSuffix(".js") ? name : (name.hasSuffix(".min") ? "\(name).js" : "\(name).min.js")
        let baseName = (fullName as NSString).deletingPathExtension
        let ext = (fullName as NSString).pathExtension

        let bundles = [
            Bundle.main,
            Bundle(for: ContentIntegrityTests.self)
        ]
        for b in bundles {
            if let url = b.url(forResource: baseName, withExtension: ext) ??
                         b.url(forResource: baseName, withExtension: ext, subdirectory: "Web") {
                if let str = try? String(contentsOf: url, encoding: .utf8), !str.isEmpty {
                    return str
                }
            }
            let directURL = b.bundleURL.appendingPathComponent(fullName)
            if let str = try? String(contentsOf: directURL, encoding: .utf8), !str.isEmpty {
                return str
            }
        }
        return ""
    }

    func testSyntaxHighlightingTokenization() {
        let script = loadWebScript(named: "syntax-highlighter")
        XCTAssertFalse(script.isEmpty, "syntax-highlighter.min.js must be loadable")

        let context = JSContext()!
        context.evaluateScript("var window = this;")
        context.evaluateScript(script)

        // 1. Strings with numbers and keyword-like tokens should not produce placeholder leaks (e.g. STR_0 or NUM_0)
        let javaSample = "String s = \"hello 123\";\nint n = 42;"
        context.setObject(javaSample, forKeyedSubscript: "code" as NSString)
        let javaRes = context.evaluateScript("window.SyntaxHighlighter.highlight(code, 'java')").toString() ?? ""

        XCTAssertFalse(javaRes.contains("STR_"), "Highlight result must not contain internal string placeholders: \(javaRes)")
        XCTAssertFalse(javaRes.contains("NUM_"), "Highlight result must not contain internal number placeholders: \(javaRes)")
        XCTAssertFalse(javaRes.contains("hl-type\">STR_"), "Placeholders must never be highlighted as types: \(javaRes)")
        XCTAssertTrue(javaRes.contains("<span class=\"hl-string\">&quot;hello 123&quot;</span>"), "String literal should be highlighted cleanly: \(javaRes)")
        XCTAssertTrue(javaRes.contains("<span class=\"hl-number\">42</span>"), "Number should be highlighted cleanly: \(javaRes)")
        XCTAssertTrue(javaRes.contains("<span class=\"hl-keyword\">int</span>"), "Keyword should be highlighted: \(javaRes)")

        // 2. URL containing // inside a string must not be truncated as a comment
        let urlSample = "String url = \"https://example.com\";"
        context.setObject(urlSample, forKeyedSubscript: "code" as NSString)
        let urlRes = context.evaluateScript("window.SyntaxHighlighter.highlight(code, 'java')").toString() ?? ""
        XCTAssertTrue(urlRes.contains("<span class=\"hl-string\">&quot;https://example.com&quot;</span>"), "URL in string must remain intact: \(urlRes)")
        XCTAssertFalse(urlRes.contains("hl-comment"), "Double slash inside string must not be highlighted as comment: \(urlRes)")

        // 3. Python string containing # must not be truncated as a comment
        let pySample = "s = \"#,#\"\nx = 10 # comment"
        context.setObject(pySample, forKeyedSubscript: "code" as NSString)
        let pyRes = context.evaluateScript("window.SyntaxHighlighter.highlight(code, 'python')").toString() ?? ""
        XCTAssertTrue(pyRes.contains("<span class=\"hl-string\">&quot;#,#&quot;</span>"), "Hash in Python string must remain intact: \(pyRes)")
        XCTAssertTrue(pyRes.contains("<span class=\"hl-comment\"># comment</span>"), "Real Python comment must be highlighted: \(pyRes)")
    }

    func testMarkdownRenderingNestedLists() {
        let hlScript = loadWebScript(named: "syntax-highlighter")
        let mdScript = loadWebScript(named: "markdown-renderer")
        XCTAssertFalse(hlScript.isEmpty, "syntax-highlighter script must not be empty")
        XCTAssertFalse(mdScript.isEmpty, "markdown-renderer script must not be empty")

        let context = JSContext()!
        context.evaluateScript("var window = this;")
        context.evaluateScript(hlScript)
        context.evaluateScript(mdScript)

        let markdown = """
        * parent
          * child
        * sibling
        """
        context.setObject(markdown, forKeyedSubscript: "md" as NSString)
        let result = context.evaluateScript("window.MarkdownRenderer.render(md, 'doc-1')").toString() ?? ""

        // Verify structurally valid nested list HTML:
        // Child <ul> must be inside parent <li>, and parent <li> closes AFTER </ul>
        XCTAssertFalse(result.contains("<li>parent</li>\n<ul>"), "Parent <li> must not close before child <ul> opens: \(result)")
        XCTAssertTrue(result.contains("<li>parent\n<ul>\n<li>child"), "Child list must be properly nested inside parent <li>: \(result)")
        XCTAssertTrue(result.contains("<li>sibling"), "Sibling list item must be properly closed: \(result)")
    }

    func testMarkdownRenderingTableEscapedPipes() {
        let hlScript = loadWebScript(named: "syntax-highlighter")
        let mdScript = loadWebScript(named: "markdown-renderer")
        let context = JSContext()!
        context.evaluateScript("var window = this;")
        context.evaluateScript(hlScript)
        context.evaluateScript(mdScript)

        let tableMd = """
        | Syntax | Note | Java 17 |
        | --- | --- | --- |
        | a\\|b | `c|d` | `split("\\\\R")` |
        """
        context.setObject(tableMd, forKeyedSubscript: "md" as NSString)
        let result = context.evaluateScript("window.MarkdownRenderer.render(md, 'doc-1')").toString() ?? ""

        XCTAssertTrue(result.contains("<td>a|b</td>") || result.contains("<td>a\\|b</td>"), "Escaped pipe should not split into an extra column: \(result)")
        XCTAssertTrue(result.contains("<code>c|d</code>"), "Backtick pipe should not split table cell: \(result)")
        XCTAssertTrue(result.contains("<code>split(&quot;\\\\R&quot;)</code>"), "Double backslashes in table inline code must be preserved: \(result)")
    }

    func testLiveBundleIntegrityVerification() {
        let live = repository.verifyLiveBundleIntegrity()
        XCTAssertEqual(live.total, 18, "Must verify all 18 documents")
        XCTAssertEqual(live.matched, 18, "All 18 documents must match their canonical SHA-256 live")
        XCTAssertTrue(live.allMatch, "Live bundle integrity check must pass")
    }
}