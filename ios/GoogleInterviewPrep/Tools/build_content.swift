import Foundation
import CryptoKit

struct ManifestDocument: Codable {
    let id: String
    let title: String
    let sourceFilename: String
    let format: String
    let primaryCategory: String
    let categoryIDs: [String]
    let order: Int
    let isHistorical: Bool
    let sha256: String
    let byteCount: Int
    let lineCountAtManifestBuild: Int
    let summary: String?
}

struct Manifest: Codable {
    let version: Int
    let builtAt: String
    let documents: [ManifestDocument]
}

struct ExtractedSection: Codable {
    let id: String
    let documentID: String
    let title: String
    let headingLevel: Int
    let parentSectionID: String?
    let anchor: String
    let plainText: String
    let searchTerms: [String]
}

struct ExtractedCodeBlock: Codable {
    let id: String
    let documentID: String
    let sectionID: String
    let language: String
    let code: String
    let startLine: Int
    let endLine: Int
}

struct DocumentIntegrity: Codable {
    let id: String
    let filename: String
    let sha256: String
    let byteCount: Int
    let lineCount: Int
    let headingCount: Int
    let codeBlockCount: Int
    let indexedCharacterCount: Int
    let format: String
    let isHistorical: Bool
    let verifiedMatch: Bool
}

struct IntegrityReport: Codable {
    let generatedAt: String
    let totalDocuments: Int
    let totalLines: Int
    let totalBytes: Int
    let allHashesMatch: Bool
    let smokeTermsPresent: [String: Bool]
    let documents: [DocumentIntegrity]
}

struct SearchIndexEntry: Codable {
    let documentID: String
    let sectionID: String
    let title: String
    let headingLevel: Int
    let anchor: String
    let categoryIDs: [String]
    let format: String
    let isHistorical: Bool
    let tokens: [String]
    let preview: String
    let plainText: String
}

struct SearchIndex: Codable {
    let generatedAt: String
    let totalEntries: Int
    let entries: [SearchIndexEntry]
}

let scriptURL = URL(fileURLWithPath: #filePath)
let toolsDir = scriptURL.deletingLastPathComponent()
let projectRoot = toolsDir.deletingLastPathComponent() // ios/GoogleInterviewPrep
let workspaceRoot = projectRoot.deletingLastPathComponent().deletingLastPathComponent() // workspace root

print("Project Root: \(projectRoot.path)")
print("Workspace Root: \(workspaceRoot.path)")

let manifestURL = projectRoot.appendingPathComponent("GoogleInterviewPrep/Resources/ContentManifest.json")
guard let manifestData = try? Data(contentsOf: manifestURL) else {
    fatalError("Could not read manifest at \(manifestURL.path)")
}

let decoder = JSONDecoder()
guard let manifest = try? decoder.decode(Manifest.self, from: manifestData) else {
    fatalError("Failed to decode ContentManifest.json")
}

// Check Canonical Root Coverage:
// Every .md and .java in workspaceRoot (except antigravity_ios_app_plan.md) must be in manifest
let fm = FileManager.default
guard let rootContents = try? fm.contentsOfDirectory(atPath: workspaceRoot.path) else {
    fatalError("Could not list workspace root")
}
let canonicalRootFiles = rootContents.filter {
    ($0.hasSuffix(".md") || $0.hasSuffix(".java")) && $0 != "antigravity_ios_app_plan.md"
}

let manifestFilenames = Set(manifest.documents.map { $0.sourceFilename })
for rootFile in canonicalRootFiles {
    if !manifestFilenames.contains(rootFile) {
        fatalError("Canonical root file not represented in ContentManifest.json: \(rootFile)")
    }
}
for doc in manifest.documents {
    if !canonicalRootFiles.contains(doc.sourceFilename) {
        fatalError("Manifest entry does not exist in workspace root: \(doc.sourceFilename)")
    }
}
print("✓ Verified canonical root coverage: all \(canonicalRootFiles.count) canonical files matched.")

let studyContentURL = projectRoot.appendingPathComponent("GoogleInterviewPrep/Resources/StudyContent")
try? fm.createDirectory(at: studyContentURL, withIntermediateDirectories: true)

var allHashesMatch = true
var totalLines = 0
var totalBytes = 0
var docIntegrities = [DocumentIntegrity]()
var allSections = [ExtractedSection]()
var allSearchEntries = [SearchIndexEntry]()
var seenDocIDs = Set<String>()
var seenSourceFilenames = Set<String>()
var seenAnchors = Set<String>()

func slugify(_ text: String) -> String {
    let allowed = CharacterSet.alphanumerics
    var result = ""
    for scalar in text.unicodeScalars {
        if allowed.contains(scalar) {
            result.append(Character(scalar).lowercased())
        } else if scalar == " " || scalar == "-" || scalar == "_" {
            if !result.hasSuffix("-") && !result.isEmpty {
                result.append("-")
            }
        }
    }
    while result.hasSuffix("-") {
        result.removeLast()
    }
    return result.isEmpty ? "section" : result
}

func tokenize(_ text: String) -> [String] {
    var tokens = Set<String>()
    let pattern = #"[a-zA-Z0-9_\-@\./:]+"#
    if let regex = try? NSRegularExpression(pattern: pattern) {
        let nsString = text as NSString
        let matches = regex.matches(in: text, range: NSRange(location: 0, length: nsString.length))
        for match in matches {
            let token = nsString.substring(with: match.range).trimmingCharacters(in: CharacterSet(charactersIn: "-.:/"))
            if token.count >= 2 {
                tokens.insert(token.lowercased())
                if token.contains("_") || token.contains("-") || token.hasPrefix("@") {
                    tokens.insert(token)
                }
            }
        }
    }
    return Array(tokens)
}

print("Processing \(manifest.documents.count) documents...")

for doc in manifest.documents {
    if seenDocIDs.contains(doc.id) {
        fatalError("Duplicate document ID found: \(doc.id)")
    }
    seenDocIDs.insert(doc.id)

    if seenSourceFilenames.contains(doc.sourceFilename) {
        fatalError("Duplicate source filename in manifest: \(doc.sourceFilename)")
    }
    seenSourceFilenames.insert(doc.sourceFilename)
    
    let sourceURL = workspaceRoot.appendingPathComponent(doc.sourceFilename)
    guard fm.fileExists(atPath: sourceURL.path) else {
        fatalError("Source file not found: \(sourceURL.path)")
    }
    
    guard let fileData = try? Data(contentsOf: sourceURL) else {
        fatalError("Could not read source file: \(sourceURL.path)")
    }
    
    guard let contentString = String(data: fileData, encoding: .utf8) else {
        fatalError("Source file is not valid UTF-8: \(sourceURL.path)")
    }
    
    let computedHash = SHA256.hash(data: fileData).map { String(format: "%02x", $0) }.joined()
    let hashMatches = (computedHash == doc.sha256)
    if !hashMatches {
        allHashesMatch = false
        print("Hash mismatch for \(doc.sourceFilename): expected \(doc.sha256), got \(computedHash)")
        fatalError("Content integrity failure for \(doc.sourceFilename)")
    }
    
    let destURL = studyContentURL.appendingPathComponent(doc.sourceFilename)
    try fileData.write(to: destURL, options: .atomic)
    
    let lines = contentString.components(separatedBy: "\n")
    let lineCount = fileData.filter { $0 == 0x0A }.count
    totalLines += lineCount
    totalBytes += fileData.count
    
    var headings = [ExtractedSection]()
    var codeBlocks = [ExtractedCodeBlock]()
    var indexedChars = 0
    
    if doc.format == "markdown" {
        var inCodeBlock = false
        var currentFenceType = ""
        var currentFenceLength = 0
        var currentHeading: (title: String, level: Int, anchor: String, id: String)? = nil
        var currentSectionText = ""
        var codeBlockLines = [String]()
        var codeBlockStart = 0
        var codeBlockLang = ""
        var headingSlugCounts = [String: Int]()
        
        func finishSection() {
            guard let h = currentHeading else { return }
            let terms = tokenize(currentSectionText + " " + h.title)
            let preview = String(currentSectionText.prefix(200)).replacingOccurrences(of: "\n", with: " ")
            let section = ExtractedSection(
                id: h.id,
                documentID: doc.id,
                title: h.title,
                headingLevel: h.level,
                parentSectionID: nil,
                anchor: h.anchor,
                plainText: currentSectionText,
                searchTerms: terms
            )
            headings.append(section)
            allSections.append(section)
            
            allSearchEntries.append(SearchIndexEntry(
                documentID: doc.id,
                sectionID: h.id,
                title: h.title,
                headingLevel: h.level,
                anchor: h.anchor,
                categoryIDs: doc.categoryIDs,
                format: doc.format,
                isHistorical: doc.isHistorical,
                tokens: terms,
                preview: preview,
                plainText: currentSectionText
            ))
            currentSectionText = ""
        }
        
        let topAnchor = "\(doc.id)-top"
        if seenAnchors.contains(topAnchor) {
            fatalError("Anchor collision detected: \(topAnchor)")
        }
        seenAnchors.insert(topAnchor)
        currentHeading = (title: doc.title, level: 1, anchor: topAnchor, id: "\(doc.id).overview")
        
        for (idx, line) in lines.enumerated() {
            let trimmed = line.trimmingCharacters(in: .whitespaces)
            let isBacktickFence = trimmed.hasPrefix("```")
            let isTildeFence = trimmed.hasPrefix("~~~")
            
            if isBacktickFence || isTildeFence {
                let fenceChar = isBacktickFence ? "`" : "~"
                let count = trimmed.prefix(while: { String($0) == fenceChar }).count
                
                if inCodeBlock {
                    // Enforce matching delimiter and length to close
                    if fenceChar == currentFenceType && count >= currentFenceLength {
                        let code = codeBlockLines.joined(separator: "\n")
                        let blockID = "\(doc.id)-code-\(codeBlocks.count + 1)"
                        if seenAnchors.contains(blockID) {
                            fatalError("Code block ID collision: \(blockID)")
                        }
                        seenAnchors.insert(blockID)
                        
                        let block = ExtractedCodeBlock(
                            id: blockID,
                            documentID: doc.id,
                            sectionID: currentHeading?.id ?? "\(doc.id).overview",
                            language: codeBlockLang,
                            code: code,
                            startLine: codeBlockStart,
                            endLine: idx + 1
                        )
                        codeBlocks.append(block)
                        currentSectionText += "\n" + code
                        inCodeBlock = false
                        codeBlockLines = []
                    } else {
                        codeBlockLines.append(line)
                    }
                } else {
                    inCodeBlock = true
                    currentFenceType = fenceChar
                    currentFenceLength = count
                    let remaining = trimmed.dropFirst(count).trimmingCharacters(in: .whitespaces)
                    codeBlockLang = remaining.components(separatedBy: .whitespaces).first ?? ""
                    codeBlockStart = idx + 1
                    codeBlockLines = []
                }
                continue
            }
            
            if inCodeBlock {
                codeBlockLines.append(line)
            } else {
                var isHeading = false
                var level = 0
                var headingTitle = ""
                
                if trimmed.hasPrefix("# ") {
                    level = 1
                    headingTitle = String(trimmed.dropFirst(2))
                    isHeading = true
                } else if trimmed.hasPrefix("## ") {
                    level = 2
                    headingTitle = String(trimmed.dropFirst(3))
                    isHeading = true
                } else if trimmed.hasPrefix("### ") {
                    level = 3
                    headingTitle = String(trimmed.dropFirst(4))
                    isHeading = true
                } else if trimmed.hasPrefix("#### ") {
                    level = 4
                    headingTitle = String(trimmed.dropFirst(5))
                    isHeading = true
                } else if trimmed.hasPrefix("**") && (trimmed.hasSuffix("**") || trimmed.hasSuffix("**:")) && trimmed.count <= 75 && !trimmed.contains("→") {
                    let stripped = trimmed.replacingOccurrences(of: "**", with: "").trimmingCharacters(in: CharacterSet(charactersIn: ": "))
                    if stripped.range(of: #"^[0-9]\.\s+"#, options: .regularExpression) != nil {
                        level = 2
                        headingTitle = stripped
                        isHeading = true
                    } else if stripped.hasPrefix("Phase-two gate") || stripped.hasPrefix("Final readiness gate") {
                        level = 3
                        headingTitle = stripped
                        isHeading = true
                    }
                }
                
                if isHeading {
                    finishSection()
                    let baseSlug = slugify(headingTitle)
                    let count = (headingSlugCounts[baseSlug] ?? 0) + 1
                    headingSlugCounts[baseSlug] = count
                    let slug = count == 1 ? baseSlug : "\(baseSlug)-\(count)"
                    let anchor = "\(doc.id)-\(slug)"
                    let sectionID = "\(doc.id).\(slug)"
                    if seenAnchors.contains(anchor) {
                        fatalError("Anchor collision detected: \(anchor)")
                    }
                    seenAnchors.insert(anchor)
                    currentHeading = (title: headingTitle, level: level, anchor: anchor, id: sectionID)
                } else {
                    currentSectionText += "\n" + line
                }
            }
            indexedChars += line.count
        }
        
        // Enforce no unclosed code blocks
        if inCodeBlock {
            fatalError("Unclosed code block in \(doc.sourceFilename) starting at line \(codeBlockStart)")
        }
        
        finishSection()
    } else if doc.format == "java" {
        let topAnchor = "\(doc.id)-top"
        if seenAnchors.contains(topAnchor) {
            fatalError("Anchor collision detected: \(topAnchor)")
        }
        seenAnchors.insert(topAnchor)
        let mainSectionID = "\(doc.id).overview"
        let fullTerms = tokenize(contentString)
        
        let overviewSection = ExtractedSection(
            id: mainSectionID,
            documentID: doc.id,
            title: doc.title,
            headingLevel: 1,
            parentSectionID: nil,
            anchor: topAnchor,
            plainText: contentString,
            searchTerms: fullTerms
        )
        headings.append(overviewSection)
        allSections.append(overviewSection)
        
        allSearchEntries.append(SearchIndexEntry(
            documentID: doc.id,
            sectionID: mainSectionID,
            title: doc.title,
            headingLevel: 1,
            anchor: topAnchor,
            categoryIDs: doc.categoryIDs,
            format: doc.format,
            isHistorical: doc.isHistorical,
            tokens: fullTerms,
            preview: String(contentString.prefix(200)).replacingOccurrences(of: "\n", with: " "),
            plainText: contentString
        ))
        
        var detected: [(title: String, line: Int)] = []
        for (idx, line) in lines.enumerated() {
            let trimmed = line.trimmingCharacters(in: .whitespaces)
            var symbolTitle: String? = nil
            if trimmed.contains("class ") || trimmed.contains("interface ") || trimmed.contains("record ") {
                symbolTitle = trimmed.components(separatedBy: "{").first?.trimmingCharacters(in: .whitespaces)
            } else if (trimmed.hasPrefix("public ") || trimmed.hasPrefix("static ") || trimmed.hasPrefix("private ") || trimmed.hasPrefix("protected ")) && trimmed.contains("(") && trimmed.contains(")") {
                symbolTitle = trimmed.components(separatedBy: "{").first?.trimmingCharacters(in: .whitespaces)
            } else if trimmed.contains("@Test") || trimmed.hasPrefix("void test") {
                symbolTitle = trimmed
            }
            
            if let sym = symbolTitle, sym.count < 100 {
                detected.append((title: sym, line: idx + 1))
            }
        }
        
        for (i, d) in detected.enumerated() {
            let nextLine = (i + 1 < detected.count) ? detected[i + 1].line - 1 : lines.count
            let blockLines = lines[(d.line - 1)..<nextLine]
            let blockText = blockLines.joined(separator: "\n")
            let slug = slugify(d.title)
            let anchor = "\(doc.id)-line-\(d.line)"
            let secID = "\(doc.id).\(slug)-\(d.line)"
            let symTerms = tokenize(d.title + " " + blockText)
            if seenAnchors.contains(anchor) {
                fatalError("Anchor collision detected: \(anchor)")
            }
            seenAnchors.insert(anchor)
            
            let sec = ExtractedSection(
                id: secID,
                documentID: doc.id,
                title: d.title,
                headingLevel: 2,
                parentSectionID: mainSectionID,
                anchor: anchor,
                plainText: blockText,
                searchTerms: symTerms
            )
            headings.append(sec)
            allSections.append(sec)
            
            allSearchEntries.append(SearchIndexEntry(
                documentID: doc.id,
                sectionID: secID,
                title: d.title,
                headingLevel: 2,
                anchor: anchor,
                categoryIDs: doc.categoryIDs,
                format: doc.format,
                isHistorical: doc.isHistorical,
                tokens: symTerms,
                preview: lines[d.line - 1],
                plainText: blockText
            ))
            indexedChars += blockText.count
        }
    }
    
    let item = DocumentIntegrity(
        id: doc.id,
        filename: doc.sourceFilename,
        sha256: computedHash,
        byteCount: fileData.count,
        lineCount: lineCount,
        headingCount: headings.count,
        codeBlockCount: codeBlocks.count,
        indexedCharacterCount: indexedChars,
        format: doc.format,
        isHistorical: doc.isHistorical,
        verifiedMatch: hashMatches
    )
    docIntegrities.append(item)
    print("✓ [\(doc.id)] \(doc.sourceFilename): \(lineCount) lines, \(headings.count) sections, \(codeBlocks.count) code blocks")
}

// Check smoke-test vocabulary: FAIL if any missing
let smokeVocab = [
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

var smokeResults = [String: Bool]()
for term in smokeVocab {
    let lowerTerm = term.lowercased()
    let found = allSearchEntries.contains { entry in
        entry.tokens.contains(lowerTerm) || entry.tokens.contains(term) || entry.title.lowercased().contains(lowerTerm) || entry.plainText.lowercased().contains(lowerTerm)
    }
    smokeResults[term] = found
    if !found {
        fatalError("FATAL: Required smoke test vocabulary term missing: \(term)")
    } else {
        print("✓ Smoke test term verified: \(term)")
    }
}

let searchIndex = SearchIndex(
    generatedAt: ISO8601DateFormatter().string(from: Date()),
    totalEntries: allSearchEntries.count,
    entries: allSearchEntries
)

let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted]

let searchIndexURL = projectRoot.appendingPathComponent("GoogleInterviewPrep/Resources/SearchIndex.json")
let searchIndexData = try encoder.encode(searchIndex)
try searchIndexData.write(to: searchIndexURL, options: .atomic)
print("Wrote SearchIndex.json with \(allSearchEntries.count) entries.")

let integrityReport = IntegrityReport(
    generatedAt: ISO8601DateFormatter().string(from: Date()),
    totalDocuments: docIntegrities.count,
    totalLines: totalLines,
    totalBytes: totalBytes,
    allHashesMatch: allHashesMatch,
    smokeTermsPresent: smokeResults,
    documents: docIntegrities
)

let reportURL = projectRoot.appendingPathComponent("GoogleInterviewPrep/Resources/IntegrityReport.json")
let reportData = try encoder.encode(integrityReport)
try reportData.write(to: reportURL, options: .atomic)
print("Wrote IntegrityReport.json: \(docIntegrities.count) documents, \(totalLines) lines, \(totalBytes) bytes.")
print("Build content passed all integrity guarantees!")