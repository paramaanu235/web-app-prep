import Foundation

public struct ContentSection: Codable, Identifiable, Hashable, Sendable {
    public let id: String
    public let documentID: String
    public let title: String
    public let headingLevel: Int
    public let parentSectionID: String?
    public let anchor: String
    public let plainText: String
    public let searchTerms: [String]

    public init(
        id: String,
        documentID: String,
        title: String,
        headingLevel: Int,
        parentSectionID: String? = nil,
        anchor: String,
        plainText: String,
        searchTerms: [String] = []
    ) {
        self.id = id
        self.documentID = documentID
        self.title = title
        self.headingLevel = headingLevel
        self.parentSectionID = parentSectionID
        self.anchor = anchor
        self.plainText = plainText
        self.searchTerms = searchTerms
    }
}