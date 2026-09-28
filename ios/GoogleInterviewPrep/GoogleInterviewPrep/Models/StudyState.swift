import Foundation

public enum WeekStatus: String, Codable, CaseIterable, Sendable {
    case notStarted = "Not Started"
    case inProgress = "In Progress"
    case completed = "Completed"
}

public struct MockResult: Codable, Identifiable, Hashable, Sendable {
    public var id: UUID
    public var date: Date
    public var type: String // "Coding", "System Design", "Behavioral"
    public var score: Int   // 1 (Needs Practice) to 4 (Strong Hire)
    public var strengths: String
    public var misses: String
    public var nextDrill: String

    public init(
        id: UUID = UUID(),
        date: Date = Date(),
        type: String = "Coding",
        score: Int = 3,
        strengths: String = "",
        misses: String = "",
        nextDrill: String = ""
    ) {
        self.id = id
        self.date = date
        self.type = type
        self.score = score
        self.strengths = strengths
        self.misses = misses
        self.nextDrill = nextDrill
    }
}

public struct ChecklistItem: Codable, Identifiable, Hashable, Sendable {
    public var id: UUID
    public var title: String
    public var isDone: Bool
    public var category: String

    public init(id: UUID = UUID(), title: String, isDone: Bool = false, category: String = "General") {
        self.id = id
        self.title = title
        self.isDone = isDone
        self.category = category
    }
}

public struct ReadingState: Codable, Sendable {
    public let documentID: String
    public var lastSectionID: String?
    public var scrollAnchor: String?
    public var estimatedProgress: Double // 0.0 - 1.0
    public var explicitlyCompleted: Bool
    public var lastOpenedAt: Date

    public init(
        documentID: String,
        lastSectionID: String? = nil,
        scrollAnchor: String? = nil,
        estimatedProgress: Double = 0.0,
        explicitlyCompleted: Bool = false,
        lastOpenedAt: Date = Date()
    ) {
        self.documentID = documentID
        self.lastSectionID = lastSectionID
        self.scrollAnchor = scrollAnchor
        self.estimatedProgress = estimatedProgress
        self.explicitlyCompleted = explicitlyCompleted
        self.lastOpenedAt = lastOpenedAt
    }
}

public struct Bookmark: Codable, Identifiable, Hashable, Sendable {
    public let id: UUID
    public let documentID: String
    public let sectionID: String?
    public let codeBlockID: String?
    public let exactQuoteHash: String?
    public var title: String
    public var note: String
    public let createdAt: Date
    public var updatedAt: Date

    public init(
        id: UUID = UUID(),
        documentID: String,
        sectionID: String? = nil,
        codeBlockID: String? = nil,
        exactQuoteHash: String? = nil,
        title: String = "",
        note: String = "",
        createdAt: Date = Date(),
        updatedAt: Date = Date()
    ) {
        self.id = id
        self.documentID = documentID
        self.sectionID = sectionID
        self.codeBlockID = codeBlockID
        self.exactQuoteHash = exactQuoteHash
        self.title = title
        self.note = note
        self.createdAt = createdAt
        self.updatedAt = updatedAt
    }
}

public struct WeekProgress: Codable, Identifiable, Hashable, Sendable {
    public let week: Int
    public var status: WeekStatus
    public var plannedHours: Double
    public var completedHours: Double
    public var attempted: Int
    public var independentlySolved: Int
    public var mocks: [MockResult]
    public var systemDesignSessions: Int
    public var behavioralStoriesPracticed: Int
    public var confidence: Int // 1 to 5
    public var notes: String

    public var id: Int { week }

    public init(
        week: Int,
        status: WeekStatus = .notStarted,
        plannedHours: Double = 18.0,
        completedHours: Double = 0.0,
        attempted: Int = 0,
        independentlySolved: Int = 0,
        mocks: [MockResult] = [],
        systemDesignSessions: Int = 0,
        behavioralStoriesPracticed: Int = 0,
        confidence: Int = 3,
        notes: String = ""
    ) {
        self.week = week
        self.status = status
        self.plannedHours = plannedHours
        self.completedHours = completedHours
        self.attempted = attempted
        self.independentlySolved = independentlySolved
        self.mocks = mocks
        self.systemDesignSessions = systemDesignSessions
        self.behavioralStoriesPracticed = behavioralStoriesPracticed
        self.confidence = confidence
        self.notes = notes
    }
}

public struct UserStudyState: Codable, Sendable {
    public var version: Int
    public var startDate: Date?
    public var interviewDate: Date?
    public var readingStates: [String: ReadingState]
    public var bookmarks: [Bookmark]
    public var weeklyProgress: [Int: WeekProgress]
    public var dailyChecklist: [ChecklistItem]
    public var slowPatterns: [String]
    public var themePreference: String // "system", "light", "dark", "sepia"
    public var bodyFontSize: Double
    public var codeFontSize: Double
    public var keepScreenAwake: Bool

    public init(
        version: Int = 1,
        startDate: Date? = nil,
        interviewDate: Date? = nil,
        readingStates: [String: ReadingState] = [:],
        bookmarks: [Bookmark] = [],
        weeklyProgress: [Int: WeekProgress] = [:],
        dailyChecklist: [ChecklistItem] = [],
        slowPatterns: [String] = [],
        themePreference: String = "system",
        bodyFontSize: Double = 16.0,
        codeFontSize: Double = 13.5,
        keepScreenAwake: Bool = false
    ) {
        self.version = version
        self.startDate = startDate
        self.interviewDate = interviewDate
        self.readingStates = readingStates
        self.bookmarks = bookmarks
        self.weeklyProgress = weeklyProgress
        self.dailyChecklist = dailyChecklist
        self.slowPatterns = slowPatterns
        self.themePreference = themePreference
        self.bodyFontSize = bodyFontSize
        self.codeFontSize = codeFontSize
        self.keepScreenAwake = keepScreenAwake
    }

    public static func makeDefault() -> UserStudyState {
        var wp: [Int: WeekProgress] = [:]
        for w in 1...12 {
            let planned = (w == 12) ? 10.0 : 18.0
            wp[w] = WeekProgress(week: w, plannedHours: planned)
        }
        let defaultChecklist = [
            ChecklistItem(title: "Complete 1 timed Medium problem (40 min)", category: "Daily DSA"),
            ChecklistItem(title: "Review invariant and space complexity", category: "Daily DSA"),
            ChecklistItem(title: "Log tricky edge-cases / mistakes", category: "Error Log"),
            ChecklistItem(title: "Rehearse 1 system design architecture or 1 STAR story", category: "Design / Story")
        ]
        return UserStudyState(
            version: 1,
            weeklyProgress: wp,
            dailyChecklist: defaultChecklist,
            slowPatterns: ["Monotonic Queue", "Segment Tree", "0-1 BFS", "Topological Sort Cycle Detection"]
        )
    }
}
