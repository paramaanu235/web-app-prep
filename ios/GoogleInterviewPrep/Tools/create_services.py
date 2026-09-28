import os

services_dir = "ios/GoogleInterviewPrep/GoogleInterviewPrep/Services"
os.makedirs(services_dir, exist_ok=True)

# 1. ContentRepository.swift
repo_code = """import Foundation
import Combine

public final class ContentRepository: @unchecked Sendable {
    public let manifest: ManifestData
    public let searchIndex: SearchIndexData
    public let documents: [ContentDocument]
    public let documentsByID: [String: ContentDocument]
    public let bundle: Bundle

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

        // Load SearchIndex
        if let url = bundle.url(forResource: "SearchIndex", withExtension: "json"),
           let data = try? Data(contentsOf: url),
           let decoded = try? JSONDecoder().decode(SearchIndexData.self, from: data) {
            self.searchIndex = decoded
        } else {
            self.searchIndex = SearchIndexData(generatedAt: "", totalEntries: 0, entries: [])
        }
    }

    public func document(withID id: String) -> ContentDocument? {
        return documentsByID[id]
    }

    public func content(for document: ContentDocument) -> String? {
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
}
"""

with open(f"{services_dir}/ContentRepository.swift", "w", encoding="utf-8") as f:
    f.write(repo_code.strip())
print("Wrote ContentRepository.swift")

# 2. StudyStateStore.swift
store_code = """import Foundation
import Combine

@MainActor
public final class StudyStateStore: ObservableObject {
    @Published public private(set) var state: UserStudyState

    private let fileManager = FileManager.default
    private let stateURL: URL
    private let backupURL: URL

    public init(customDirectory: URL? = nil) {
        let baseDir: URL
        if let custom = customDirectory {
            baseDir = custom
        } else {
            let appSupport = FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask).first!
            baseDir = appSupport.appendingPathComponent("GoogleInterviewPrep", isDirectory: true)
        }
        try? FileManager.default.createDirectory(at: baseDir, withIntermediateDirectories: true)
        self.stateURL = baseDir.appendingPathComponent("UserStudyState.json")
        self.backupURL = baseDir.appendingPathComponent("UserStudyState.backup.json")

        if let loaded = Self.load(from: stateURL) {
            self.state = loaded
        } else if let backup = Self.load(from: backupURL) {
            self.state = backup
        } else {
            self.state = UserStudyState.makeDefault()
        }
    }

    private static func load(from url: URL) -> UserStudyState? {
        guard let data = try? Data(contentsOf: url) else { return nil }
        return try? JSONDecoder().decode(UserStudyState.self, from: data)
    }

    public func save() {
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted]
        guard let data = try? encoder.encode(state) else { return }

        let tempURL = stateURL.deletingLastPathComponent().appendingPathComponent("UserStudyState.tmp")
        do {
            try data.write(to: tempURL, options: .atomic)
            // Validate temp file before replacing
            if let _ = try? JSONDecoder().decode(UserStudyState.self, from: Data(contentsOf: tempURL)) {
                if fileManager.fileExists(atPath: stateURL.path) {
                    try? fileManager.removeItem(at: backupURL)
                    try? fileManager.copyItem(at: stateURL, to: backupURL)
                    try? fileManager.removeItem(at: stateURL)
                }
                try fileManager.moveItem(at: tempURL, to: stateURL)
            }
        } catch {
            print("Failed to atomically save UserStudyState: \(error)")
        }
    }

    // MARK: - Reading State
    public func readingState(for documentID: String) -> ReadingState {
        return state.readingStates[documentID] ?? ReadingState(documentID: documentID)
    }

    public func updateReadingPosition(documentID: String, sectionID: String?, anchor: String?, estimatedProgress: Double) {
        var current = readingState(for: documentID)
        current.lastSectionID = sectionID
        current.scrollAnchor = anchor
        current.estimatedProgress = max(current.estimatedProgress, min(1.0, estimatedProgress))
        current.lastOpenedAt = Date()
        state.readingStates[documentID] = current
        save()
    }

    public func toggleExplicitCompletion(documentID: String) {
        var current = readingState(for: documentID)
        current.explicitlyCompleted.toggle()
        state.readingStates[documentID] = current
        save()
    }

    // MARK: - Bookmarks
    public func addBookmark(documentID: String, sectionID: String? = nil, codeBlockID: String? = nil, title: String, note: String = "") {
        let bookmark = Bookmark(
            documentID: documentID,
            sectionID: sectionID,
            codeBlockID: codeBlockID,
            title: title,
            note: note
        )
        state.bookmarks.insert(bookmark, at: 0)
        save()
    }

    public func removeBookmark(id: UUID) {
        state.bookmarks.removeAll { $0.id == id }
        save()
    }

    public func updateBookmarkNote(id: UUID, note: String) {
        if let idx = state.bookmarks.firstIndex(where: { $0.id == id }) {
            state.bookmarks[idx].note = note
            state.bookmarks[idx].updatedAt = Date()
            save()
        }
    }

    // MARK: - Weekly Tracker
    public func progress(for week: Int) -> WeekProgress {
        return state.weeklyProgress[week] ?? WeekProgress(week: week)
    }

    public func updateWeekProgress(_ progress: WeekProgress) {
        state.weeklyProgress[progress.week] = progress
        save()
    }

    public func addMockResult(to week: Int, mock: MockResult) {
        var wp = progress(for: week)
        wp.mocks.append(mock)
        state.weeklyProgress[week] = wp
        save()
    }

    // MARK: - Checklist
    public func toggleChecklist(id: UUID) {
        if let idx = state.dailyChecklist.firstIndex(where: { $0.id == id }) {
            state.dailyChecklist[idx].isDone.toggle()
            save()
        }
    }

    public func addChecklistItem(title: String, category: String) {
        state.dailyChecklist.append(ChecklistItem(title: title, category: category))
        save()
    }

    // MARK: - Settings & Dates
    public func updateDates(startDate: Date?, interviewDate: Date?) {
        state.startDate = startDate
        state.interviewDate = interviewDate
        save()
    }

    public func updatePreferences(theme: String? = nil, bodySize: Double? = nil, codeSize: Double? = nil, keepAwake: Bool? = nil) {
        if let theme = theme { state.themePreference = theme }
        if let b = bodySize { state.bodyFontSize = b }
        if let c = codeSize { state.codeFontSize = c }
        if let k = keepAwake { state.keepScreenAwake = k }
        save()
    }

    // MARK: - Destructive Resets
    public func resetReadingPositions() {
        state.readingStates.removeAll()
        save()
    }

    public func resetTrackerData() {
        let def = UserStudyState.makeDefault()
        state.weeklyProgress = def.weeklyProgress
        state.dailyChecklist = def.dailyChecklist
        save()
    }

    public func resetAllState() {
        state = UserStudyState.makeDefault()
        save()
    }

    public func replaceState(with newState: UserStudyState) {
        state = newState
        save()
    }
}
"""

with open(f"{services_dir}/StudyStateStore.swift", "w", encoding="utf-8") as f:
    f.write(store_code.strip())
print("Wrote StudyStateStore.swift")

# 3. SearchService.swift
search_code = """import Foundation
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

            // Exact match in section or doc title
            if titleLower == lowerQuery || docTitleLower == lowerQuery {
                score += 100
            } else if titleLower.contains(lowerQuery) {
                score += 50
            } else if docTitleLower.contains(lowerQuery) {
                score += 30
            }

            // Token matching: exact symbol preservation
            for token in entry.tokens {
                if token == trimmed || token.lowercased() == lowerQuery {
                    score += 40
                } else if token.lowercased().contains(lowerQuery) {
                    score += 15
                }
            }

            // Preview matching
            if entry.preview.lowercased().contains(lowerQuery) {
                score += 10
            }

            if score > 0 {
                matches.append(SearchResult(
                    id: entry.sectionID,
                    documentID: entry.documentID,
                    documentTitle: doc?.title ?? entry.documentID,
                    sectionID: entry.sectionID,
                    sectionTitle: entry.title,
                    anchor: entry.anchor,
                    preview: entry.preview,
                    matchScore: score,
                    categoryIDs: entry.categoryIDs,
                    format: entry.format,
                    isHistorical: entry.isHistorical
                ))
            }
        }

        // Rank by highest matchScore, then heading level (top-level first)
        matches.sort { $0.matchScore > $1.matchScore }
        self.results = Array(matches.prefix(60))
        self.isSearching = false
    }
}
"""

with open(f"{services_dir}/SearchService.swift", "w", encoding="utf-8") as f:
    f.write(search_code.strip())
print("Wrote SearchService.swift")

# 4. ExportImportService.swift
export_code = """import Foundation

public struct ImportValidationSummary {
    public let bookmarkCount: Int
    public let trackedWeeksCount: Int
    public let checklistCount: Int
    public let version: Int
    public let isValid: Bool
    public let errorMessage: String?
}

public final class ExportImportService {
    public static func exportState(state: UserStudyState) -> URL? {
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
        encoder.dateEncodingStrategy = .iso8601
        guard let data = try? encoder.encode(state) else { return nil }

        let tempURL = FileManager.default.temporaryDirectory.appendingPathComponent("GoogleInterviewPrep_Backup.json")
        try? data.write(to: tempURL, options: .atomic)
        return tempURL
    }

    public static func validateImportData(_ data: Data) -> (UserStudyState?, ImportValidationSummary) {
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        do {
            let state = try decoder.decode(UserStudyState.self, from: data)
            let summary = ImportValidationSummary(
                bookmarkCount: state.bookmarks.count,
                trackedWeeksCount: state.weeklyProgress.filter { $0.value.completedHours > 0 || $0.value.status != .notStarted }.count,
                checklistCount: state.dailyChecklist.count,
                version: state.version,
                isValid: true,
                errorMessage: nil
            )
            return (state, summary)
        } catch {
            let summary = ImportValidationSummary(
                bookmarkCount: 0,
                trackedWeeksCount: 0,
                checklistCount: 0,
                version: 0,
                isValid: false,
                errorMessage: error.localizedDescription
            )
            return (nil, summary)
        }
    }
}
"""

with open(f"{services_dir}/ExportImportService.swift", "w", encoding="utf-8") as f:
    f.write(export_code.strip())
print("Wrote ExportImportService.swift")
