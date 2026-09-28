import Foundation
import Combine

@MainActor
public final class SearchService: ObservableObject {
    @Published public var query: String = ""
    @Published public var selectedCategory: String? = nil
    @Published public var selectedFormat: String? = nil
    @Published public var includeHistorical: Bool = false
    @Published public private(set) var results: [SearchResult] = []
    @Published public private(set) var isSearching: Bool = false

    private let repository: ContentRepository
    private var cancellables = Set<AnyCancellable>()

    public init(repository: ContentRepository) {
        self.repository = repository

        $query
            .combineLatest($selectedCategory, $selectedFormat, $includeHistorical)
            .debounce(for: .milliseconds(120), scheduler: RunLoop.main)
            .sink { [weak self] query, cat, fmt, hist in
                self?.performSearch(query: query, category: cat, format: fmt, includeHistorical: hist)
            }
            .store(in: &cancellables)
    }

    public func performSearch(query: String, category: String?, format: String?, includeHistorical: Bool) {
        let trimmed = query.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else {
            self.results = []
            self.isSearching = false
            return
        }

        self.isSearching = true
        let lowerQuery = trimmed.lowercased()
        let queryTokens = lowerQuery.components(separatedBy: CharacterSet.alphanumerics.inverted).filter { !$0.isEmpty }

        var matches: [SearchResult] = []

        for entry in repository.searchIndex.entries {
            if !includeHistorical && entry.isHistorical {
                continue
            }
            if let cat = category, !entry.categoryIDs.contains(cat) {
                continue
            }
            if let fmt = format, entry.format.lowercased() != fmt.lowercased() {
                continue
            }

            var score = 0
            let titleLower = entry.title.lowercased()
            let doc = repository.document(withID: entry.documentID)
            let docTitleLower = (doc?.title ?? "").lowercased()
            let plainTextLower = entry.plainText.lowercased()

            // 1. Exact phrase match in title
            if titleLower == lowerQuery || docTitleLower == lowerQuery {
                score += 150
            } else if titleLower.contains(lowerQuery) {
                score += 80
            } else if docTitleLower.contains(lowerQuery) {
                score += 40
            }

            // 2. Exact phrase match in body / plain text
            let hasExactPhraseInBody = plainTextLower.contains(lowerQuery)
            if hasExactPhraseInBody {
                score += 60
            }

            // 3. Multi-word conjunction: check if ALL query tokens are present
            if !queryTokens.isEmpty {
                let allTokensMatch = queryTokens.allSatisfy { qTok in
                    titleLower.contains(qTok) || plainTextLower.contains(qTok) || entry.tokens.contains(qTok)
                }
                if allTokensMatch {
                    score += 50
                }
            }

            // 4. Individual token matches (for code identifiers like @Transactional, select_for_update)
            for token in entry.tokens {
                if token == trimmed || token.lowercased() == lowerQuery {
                    score += 50
                } else if token.lowercased().contains(lowerQuery) {
                    score += 20
                }
            }

            // 5. Build contextual preview snippet
            var snippet = entry.preview
            if hasExactPhraseInBody, let range = plainTextLower.range(of: lowerQuery) {
                let matchPos = plainTextLower.distance(from: plainTextLower.startIndex, to: range.lowerBound)
                let start = max(0, matchPos - 50)
                let end = min(entry.plainText.count, matchPos + trimmed.count + 70)
                let startIdx = entry.plainText.index(entry.plainText.startIndex, offsetBy: start)
                let endIdx = entry.plainText.index(entry.plainText.startIndex, offsetBy: end)
                let rawSub = String(entry.plainText[startIdx..<endIdx]).replacingOccurrences(of: "\n", with: " ")
                snippet = (start > 0 ? "…" : "") + rawSub + (end < entry.plainText.count ? "…" : "")
            }

            if score > 0 {
                var resultAnchor = entry.anchor
                if entry.format.lowercased() == "java" {
                    var targetLineOffset = 0
                    if let range = plainTextLower.range(of: lowerQuery) {
                        targetLineOffset = entry.plainText[..<range.lowerBound].filter { $0 == "\n" }.count
                    } else if let firstMatch = queryTokens.first(where: { plainTextLower.contains($0) }),
                              let range = plainTextLower.range(of: firstMatch) {
                        targetLineOffset = entry.plainText[..<range.lowerBound].filter { $0 == "\n" }.count
                    }

                    var baseLine = 1
                    if let range = entry.anchor.range(of: #"-line-(\d+)$"#, options: .regularExpression) {
                        let numStr = String(entry.anchor[range]).replacingOccurrences(of: "-line-", with: "")
                        baseLine = Int(numStr) ?? 1
                    }
                    let actualLine = baseLine + targetLineOffset
                    resultAnchor = "\(entry.documentID)-line-\(actualLine)"
                }

                matches.append(SearchResult(
                    id: entry.sectionID,
                    documentID: entry.documentID,
                    documentTitle: doc?.title ?? entry.documentID,
                    sectionID: entry.sectionID,
                    sectionTitle: entry.title,
                    anchor: resultAnchor,
                    preview: snippet,
                    matchScore: score,
                    categoryIDs: entry.categoryIDs,
                    format: entry.format,
                    isHistorical: entry.isHistorical
                ))
            }
        }

        matches.sort { $0.matchScore > $1.matchScore }
        self.results = Array(matches.prefix(60))
        self.isSearching = false
    }
}