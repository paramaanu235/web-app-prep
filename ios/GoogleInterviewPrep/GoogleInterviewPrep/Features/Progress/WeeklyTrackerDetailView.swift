import SwiftUI

public struct WeeklyTrackerDetailView: View {
    public let weekNumber: Int
    @EnvironmentObject private var stateStore: StudyStateStore
    @Environment(\.dismiss) private var dismiss
    @Environment(\.appTheme) private var theme

    @State private var weekProgress: WeekProgress
    @State private var showingAddMock: Bool = false

    public init(weekNumber: Int) {
        self.weekNumber = weekNumber
        _weekProgress = State(initialValue: WeekProgress(week: weekNumber))
    }

    public var body: some View {
        Form {
            Group {
            Section("Week Status") {
                Picker("Status", selection: $weekProgress.status) {
                    ForEach(WeekStatus.allCases, id: \.self) { st in
                        Text(st.rawValue).tag(st)
                    }
                }
                .pickerStyle(.segmented)
            }

            Section("Hours Invested") {
                HStack {
                    Text("Planned Hours")
                    Spacer()
                    Text(String(format: "%.1f h", weekProgress.plannedHours))
                        .foregroundColor(.secondary)
                }

                Stepper(value: $weekProgress.completedHours, in: 0...60, step: 0.5) {
                    HStack {
                        Text("Completed Hours")
                        Spacer()
                        Text(String(format: "%.1f h", weekProgress.completedHours))
                            .bold()
                            .foregroundColor(.accentColor)
                    }
                }
            }

            Section("Problem Metrics") {
                Stepper("Attempted: \(weekProgress.attempted)", value: $weekProgress.attempted, in: 0...100)
                Stepper("Solved Independently: \(weekProgress.independentlySolved)", value: $weekProgress.independentlySolved, in: 0...weekProgress.attempted)
            }

            Section("Practice Blocks") {
                Stepper("System Design Sessions: \(weekProgress.systemDesignSessions)", value: $weekProgress.systemDesignSessions, in: 0...30)
                Stepper("Behavioral Stories Practiced: \(weekProgress.behavioralStoriesPracticed)", value: $weekProgress.behavioralStoriesPracticed, in: 0...30)
            }

            Section("Confidence (1-5)") {
                Picker("Confidence", selection: $weekProgress.confidence) {
                    Text("1 - High Uncertainty").tag(1)
                    Text("2 - Need Scaffolding").tag(2)
                    Text("3 - Steady Foundation").tag(3)
                    Text("4 - Fluent & Robust").tag(4)
                    Text("5 - Senior Interview Ready").tag(5)
                }
            }

            Section("Mocks & Simulations (\(weekProgress.mocks.count))") {
                ForEach(weekProgress.mocks) { mock in
                    VStack(alignment: .leading, spacing: 4) {
                        HStack {
                            Text(mock.type)
                                .font(.headline)
                            Spacer()
                            Text("Score: \(mock.score)/4")
                                .font(.caption.bold())
                                .foregroundColor(mock.score >= 3 ? .green : .orange)
                        }
                        if !mock.strengths.isEmpty {
                            Text("Strengths: \(mock.strengths)")
                                .font(.caption)
                                .foregroundColor(.secondary)
                        }
                        if !mock.nextDrill.isEmpty {
                            Text("Next Drill: \(mock.nextDrill)")
                                .font(.caption.bold())
                                .foregroundColor(.accentColor)
                        }
                    }
                    .padding(.vertical, 2)
                }

                Button(action: { showingAddMock = true }) {
                    Label("Log Mock Interview", systemImage: "plus.circle")
                }
            }

            Section("Week Notes & Retrospective") {
                TextEditor(text: $weekProgress.notes)
                    .frame(minHeight: 80)
            }
            }
            .listRowBackground(theme.secondaryBackground)
        }
        .themedSurface()
        .navigationTitle("Week \(weekNumber) Tracker")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .confirmationAction) {
                Button("Save") {
                    stateStore.updateWeekProgress(weekProgress)
                    dismiss()
                }
            }
        }
        .onAppear {
            self.weekProgress = stateStore.progress(for: weekNumber)
        }
        .sheet(isPresented: $showingAddMock) {
            MockInterviewLogView { mock in
                weekProgress.mocks.append(mock)
            }
        }
    }
}
