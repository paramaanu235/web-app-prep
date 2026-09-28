import SwiftUI

public struct ProgressDashboardView: View {
    @Environment(\.appTheme) private var theme
    @EnvironmentObject private var env: AppEnvironment
    @EnvironmentObject private var stateStore: StudyStateStore
    @State private var selectedWeek: Int? = nil
    @State private var showingExportSheet: Bool = false
    @State private var exportURL: URL? = nil

    public init() {}

    private var totalCompletedHours: Double {
        stateStore.state.weeklyProgress.values.reduce(0) { $0 + $1.completedHours }
    }

    private var totalSolvedProblems: Int {
        stateStore.state.weeklyProgress.values.reduce(0) { $0 + $1.independentlySolved }
    }

    private var totalMocks: Int {
        stateStore.state.weeklyProgress.values.reduce(0) { $0 + $1.mocks.count }
    }

    public var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Top Metrics Row
                HStack(spacing: 12) {
                    MetricCard(title: "Completed Hours", value: String(format: "%.1f", totalCompletedHours), unit: "/ 208 h", icon: "clock.fill", color: .blue)
                    MetricCard(title: "Independent Solves", value: "\(totalSolvedProblems)", unit: "problems", icon: "checkmark.seal.fill", color: .green)
                    MetricCard(title: "Mocks Logged", value: "\(totalMocks)", unit: "simulations", icon: "person.2.fill", color: .purple)
                }
                .padding(.horizontal)

                // Quick Link to Tracker Document
                if let trackerDoc = env.repository.document(withID: "weekly.tracker") {
                    NavigationLink(destination: DocumentReaderView(document: trackerDoc)) {
                        HStack {
                            Image(systemName: "doc.text.fill")
                                .foregroundColor(.accentColor)
                            Text("Open Full 12-Week Tracker Document")
                                .font(.subheadline.bold())
                                .foregroundColor(.primary)
                            Spacer()
                            Image(systemName: "chevron.right")
                                .foregroundColor(.secondary)
                        }
                        .padding(14)
                        .background(theme.secondaryBackground)
                        .cornerRadius(10)
                    }
                    .padding(.horizontal)
                }

                // 12-Week Interactive Schedule
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        Text("12-Week Schedule")
                            .font(.headline)
                        Spacer()
                    }
                    .padding(.horizontal)

                    LazyVStack(spacing: 8) {
                        ForEach(1...12, id: \.self) { w in
                            let prog = stateStore.progress(for: w)
                            NavigationLink(destination: WeeklyTrackerDetailView(weekNumber: w)) {
                                HStack {
                                    VStack(alignment: .leading, spacing: 4) {
                                        HStack {
                                            Text("Week \(w)")
                                                .font(.headline)
                                                .foregroundColor(.primary)
                                            StatusBadge(prog.status.rawValue, color: statusColor(prog.status))
                                        }

                                        Text("\(String(format: "%.1f", prog.completedHours)) / \(String(format: "%.1f", prog.plannedHours)) h · \(prog.independentlySolved) solves · \(prog.mocks.count) mocks")
                                            .font(.caption)
                                            .foregroundColor(.secondary)
                                    }
                                    Spacer()
                                    Image(systemName: "chevron.right")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                }
                                .padding(12)
                                .background(theme.secondaryBackground)
                                .cornerRadius(10)
                            }
                            .buttonStyle(.plain)
                        }
                    }
                    .padding(.horizontal)
                }

                // Slow Patterns to Drill
                VStack(alignment: .leading, spacing: 10) {
                    Text("Slow Patterns (High Review Priority)")
                        .font(.headline)
                        .padding(.horizontal)

                    VStack(alignment: .leading, spacing: 6) {
                        ForEach(stateStore.state.slowPatterns, id: \.self) { pattern in
                            HStack {
                                Image(systemName: "exclamationmark.circle.fill")
                                    .foregroundColor(.orange)
                                Text(pattern)
                                    .font(.subheadline)
                                Spacer()
                            }
                            .padding(.vertical, 2)
                        }
                    }
                    .padding(14)
                    .background(theme.secondaryBackground)
                    .cornerRadius(10)
                    .padding(.horizontal)
                }
            }
            .padding(.vertical)
        }
        .themedSurface()
        .navigationTitle("12-Week Tracker")
        .toolbar {
            ToolbarItem(placement: .navigationBarTrailing) {
                NavigationLink(destination: ChecklistView()) {
                    Image(systemName: "checklist")
                }
            }
        }
    }

    private func statusColor(_ status: WeekStatus) -> Color {
        switch status {
        case .completed: return .green
        case .inProgress: return .blue
        case .notStarted: return .secondary
        }
    }
}

public struct MetricCard: View {
    @Environment(\.appTheme) private var theme
    public let title: String
    public let value: String
    public let unit: String
    public let icon: String
    public let color: Color

    public var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack {
                Image(systemName: icon)
                    .foregroundColor(color)
                    .font(.caption)
                Spacer()
            }
            Text(value)
                .font(.title3.bold())
                .foregroundColor(.primary)
            Text(unit)
                .font(.caption2)
                .foregroundColor(.secondary)
        }
        .padding(10)
        .frame(maxWidth: .infinity)
        .background(theme.secondaryBackground)
        .cornerRadius(10)
    }
}
