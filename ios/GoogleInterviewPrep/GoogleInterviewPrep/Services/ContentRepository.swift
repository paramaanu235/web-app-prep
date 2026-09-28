import Foundation
import Combine
import CryptoKit

public struct IntegrityReportData: Codable, Sendable {
    public let totalLines: Int
    public let totalBytes: Int
    public let generatedAt: String
    public let allHashesMatch: Bool
    public let smokeTermsPresent: [String: Bool]
}

public final class ContentRepository: @unchecked Sendable {
    public let manifest: ManifestData
    public let documents: [ContentDocument]
    public let documentsByID: [String: ContentDocument]
    public let bundle: Bundle

    private var _searchIndex: SearchIndexData?
    private let searchIndexLock = NSLock()

    public var searchIndex: SearchIndexData {
        searchIndexLock.lock()
        defer { searchIndexLock.unlock() }
        if let existing = _searchIndex {
            return existing
        }
        if let url = bundle.url(forResource: "SearchIndex", withExtension: "json"),
           let data = try? Data(contentsOf: url),
           let decoded = try? JSONDecoder().decode(SearchIndexData.self, from: data) {
            _searchIndex = decoded
            return decoded
        }
        let empty = SearchIndexData(generatedAt: "", totalEntries: 0, entries: [])
        _searchIndex = empty
        return empty
    }

    public init(bundle: Bundle = .main) {
        self.bundle = bundle

        // Load Manifest
        if let url = bundle.url(forResource: "ContentManifest", withExtension: "json"),
           let data = try? Data(contentsOf: url),
           let decoded = try? JSONDecoder().decode(ManifestData.self, from: data) {
            self.manifest = decoded
        } else {
            // Fallback empty manifest for previews or tests
            self.manifest = ManifestData(version: 1, builtAt: "", documents: [])
        }
        self.documents = manifest.documents
        var dict: [String: ContentDocument] = [:]
        for doc in manifest.documents {
            dict[doc.id] = doc
        }
        self.documentsByID = dict
    }

    public func document(withID id: String) -> ContentDocument? {
        return documentsByID[id]
    }

    public func loadIntegrityReport() -> IntegrityReportData? {
        if let url = bundle.url(forResource: "IntegrityReport", withExtension: "json"),
           let data = try? Data(contentsOf: url),
           let report = try? JSONDecoder().decode(IntegrityReportData.self, from: data) {
            return report
        }
        return nil
    }

    public func verifyLiveBundleIntegrity() -> (matched: Int, total: Int, allMatch: Bool) {
        var matched = 0
        for doc in documents {
            guard let content = content(for: doc) else { continue }
            let data = Data(content.utf8)
            let hash = SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined()
            if hash == doc.sha256 {
                matched += 1
            }
        }
        return (matched, documents.count, matched == documents.count && documents.count > 0)
    }

    public static func loadContent(for document: ContentDocument, bundle: Bundle = .main) -> String? {
        let name = (document.sourceFilename as NSString).deletingPathExtension
        let ext = (document.sourceFilename as NSString).pathExtension

        // Try direct resource in bundle
        if let url = bundle.url(forResource: name, withExtension: ext) ??
                     bundle.url(forResource: name, withExtension: ext, subdirectory: "StudyContent"),
           let text = try? String(contentsOf: url, encoding: .utf8) {
            return text
        }
        return nil
    }

    public func content(for document: ContentDocument) -> String? {
        Self.loadContent(for: document, bundle: bundle)
    }

    // Category groupings matching plan section 3
    public var startHereDocuments: [ContentDocument] {
        documents.filter { $0.categoryIDs.contains("start_here") }
    }

    public var prep12WeekDocuments: [ContentDocument] {
        documents.filter { $0.categoryIDs.contains("plans") }
    }

    public var dsaDocuments: [ContentDocument] {
        documents.filter { $0.categoryIDs.contains("dsa") }
    }

    public var javaDocuments: [ContentDocument] {
        documents.filter { $0.categoryIDs.contains("java") }
    }

    public var backendDocuments: [ContentDocument] {
        documents.filter { $0.categoryIDs.contains("backend") }
    }

    public var behavioralDocuments: [ContentDocument] {
        documents.filter { $0.categoryIDs.contains("behavioral") }
    }

    public var archiveDocuments: [ContentDocument] {
        documents.filter { $0.categoryIDs.contains("archive") }
    }

    public var pythonDocuments: [ContentDocument] {
        documents.filter { $0.categoryIDs.contains("python") }
    }

    public var systemDesignSections: [SearchIndexEntry] {
        searchIndex.entries.filter {
            $0.title.localizedCaseInsensitiveContains("System Design") ||
            $0.anchor.contains("system-design")
        }
    }
}