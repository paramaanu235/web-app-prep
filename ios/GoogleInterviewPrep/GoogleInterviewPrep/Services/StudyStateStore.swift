import Foundation
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
                    _ = try fileManager.replaceItemAt(stateURL, withItemAt: tempURL)
                } else {
                    try fileManager.moveItem(at: tempURL, to: stateURL)
                }
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