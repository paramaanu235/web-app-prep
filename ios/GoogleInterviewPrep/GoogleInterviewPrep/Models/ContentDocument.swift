import Foundation

public enum ContentFormat: String, Codable, Sendable {
    case markdown
    case java
}

public struct ContentDocument: Codable, Identifiable, Hashable, Sendable {
    public let id: String
    public let title: String
    public let sourceFilename: String
    public let format: ContentFormat
    public let primaryCategory: String
    public let categoryIDs: [String]
    public let order: Int
    public let isHistorical: Bool
    public let sha256: String
    public let byteCount: Int
    public let lineCountAtManifestBuild: Int
    public let summary: String?

    public init(
        id: String,
        title: String,
        sourceFilename: String,
        format: ContentFormat,
        primaryCategory: String,
        categoryIDs: [String],
        order: Int,
        isHistorical: Bool,
        sha256: String,
        byteCount: Int,
        lineCountAtManifestBuild: Int,
        summary: String? = nil
    ) {
        self.id = id
        self.title = title
        self.sourceFilename = sourceFilename
        self.format = format
        self.primaryCategory = primaryCategory
        self.categoryIDs = categoryIDs
        self.order = order
        self.isHistorical = isHistorical
        self.sha256 = sha256
        self.byteCount = byteCount
        self.lineCountAtManifestBuild = lineCountAtManifestBuild
        self.summary = summary
    }
}

public struct ManifestData: Codable {
    public let version: Int
    public let builtAt: String
    public let documents: [ContentDocument]
}