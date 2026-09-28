import Foundation

public struct SearchIndexEntry: Codable, Identifiable, Hashable, Sendable {
    public let documentID: String
    public let sectionID: String
    public let title: String
    public let headingLevel: Int
    public let anchor: String
    public let categoryIDs: [String]
    public let format: String
    public let isHistorical: Bool
    public let tokens: [String]
    public let preview: String
    public let plainText: String

    public var id: String { sectionID }
}

public struct SearchIndexData: Codable, Sendable {
    public let generatedAt: String
    public let totalEntries: Int
    public let entries: [SearchIndexEntry]
}

public struct SearchResult: Identifiable, Hashable, Sendable {
    public let id: String
    public let documentID: String
    public let documentTitle: String
    public let sectionID: String
    public let sectionTitle: String
    public let anchor: String
    public let preview: String
    public let matchScore: Int
    public let categoryIDs: [String]
    public let format: String
    public let isHistorical: Bool
}