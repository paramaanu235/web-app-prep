import Foundation

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
        func makeInvalid(version: Int = 0, message: String) -> (UserStudyState?, ImportValidationSummary) {
            let summary = ImportValidationSummary(
                bookmarkCount: 0,
                trackedWeeksCount: 0,
                checklistCount: 0,
                version: version,
                isValid: false,
                errorMessage: message
            )
            return (nil, summary)
        }

        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        let state: UserStudyState
        do {
            state = try decoder.decode(UserStudyState.self, from: data)
        } catch {
            return makeInvalid(message: "JSON decoding failed: \(error.localizedDescription)")
        }

        // Schema version check
        guard state.version == 1 else {
            return makeInvalid(version: state.version, message: "Unsupported schema version \(state.version). Expected version 1.")
        }

        // Appearance preferences validation
        guard state.bodyFontSize >= 10.0 && state.bodyFontSize <= 36.0 else {
            return makeInvalid(version: state.version, message: "Invalid body font size: \(state.bodyFontSize). Must be between 10 and 36.")
        }
        guard state.codeFontSize >= 8.0 && state.codeFontSize <= 30.0 else {
            return makeInvalid(version: state.version, message: "Invalid code font size: \(state.codeFontSize). Must be between 8 and 30.")
        }
        guard ["system", "light", "dark", "sepia"].contains(state.themePreference) else {
            return makeInvalid(version: state.version, message: "Invalid theme preference: \(state.themePreference).")
        }

        // Reading states validation
        for (docID, rs) in state.readingStates {
            guard rs.estimatedProgress >= 0.0 && rs.estimatedProgress <= 1.0 else {
                return makeInvalid(version: state.version, message: "Invalid reading progress for \(docID): \(rs.estimatedProgress). Must be between 0.0 and 1.0.")
            }
        }

        // Weekly progress validation
        for (weekKey, wp) in state.weeklyProgress {
            guard (1...12).contains(weekKey) && wp.week == weekKey else {
                return makeInvalid(version: state.version, message: "Invalid week number: \(weekKey). Must be between 1 and 12.")
            }
            guard wp.plannedHours >= 0.0 && wp.plannedHours <= 168.0 else {
                return makeInvalid(version: state.version, message: "Invalid planned hours for week \(weekKey): \(wp.plannedHours). Must be non-negative.")
            }
            guard wp.completedHours >= 0.0 && wp.completedHours <= 168.0 else {
                return makeInvalid(version: state.version, message: "Invalid completed hours for week \(weekKey): \(wp.completedHours). Must be non-negative.")
            }
            guard wp.attempted >= 0 && wp.independentlySolved >= 0 else {
                return makeInvalid(version: state.version, message: "Problem counts for week \(weekKey) must be non-negative.")
            }
            guard wp.independentlySolved <= wp.attempted else {
                return makeInvalid(version: state.version, message: "Independently solved problems (\(wp.independentlySolved)) cannot exceed attempted problems (\(wp.attempted)) for week \(weekKey).")
            }
            guard wp.confidence >= 1 && wp.confidence <= 5 else {
                return makeInvalid(version: state.version, message: "Confidence score for week \(weekKey) must be between 1 and 5 (got \(wp.confidence)).")
            }
            guard wp.systemDesignSessions >= 0 && wp.behavioralStoriesPracticed >= 0 else {
                return makeInvalid(version: state.version, message: "Session counts for week \(weekKey) must be non-negative.")
            }
            for mock in wp.mocks {
                guard mock.score >= 1 && mock.score <= 4 else {
                    return makeInvalid(version: state.version, message: "Mock interview score must be between 1 and 4 (got \(mock.score)).")
                }
            }
        }

        let summary = ImportValidationSummary(
            bookmarkCount: state.bookmarks.count,
            trackedWeeksCount: state.weeklyProgress.filter { $0.value.completedHours > 0 || $0.value.status != .notStarted }.count,
            checklistCount: state.dailyChecklist.count,
            version: state.version,
            isValid: true,
            errorMessage: nil
        )
        return (state, summary)
    }
}
