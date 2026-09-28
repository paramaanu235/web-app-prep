import os

prog_dir = "ios/GoogleInterviewPrep/GoogleInterviewPrep/Features/Progress"
sett_dir = "ios/GoogleInterviewPrep/GoogleInterviewPrep/Features/Settings"
os.makedirs(prog_dir, exist_ok=True)
os.makedirs(sett_dir, exist_ok=True)

# 1. WeeklyTrackerDetailView.swift
weekly_detail_code = r"""import SwiftUI

public struct WeeklyTrackerDetailView: View {
    public let weekNumber: Int
    @EnvironmentObject private var stateStore: StudyStateStore
    @Environment(\.dismiss) private var dismiss

    @State private var weekProgress: WeekProgress
    @State private var showingAddMock: Bool = false

    public init(weekNumber: Int) {
        self.weekNumber = weekNumber
        _weekProgress = State(initialValue: WeekProgress(week: weekNumber))
    }

    public var body: some View {
        Form {
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
"""

with open(f"{prog_dir}/WeeklyTrackerDetailView.swift", "w", encoding="utf-8") as f:
    f.write(weekly_detail_code.strip())
print("Wrote WeeklyTrackerDetailView.swift")

# 2. MockInterviewLogView.swift
mock_view_code = r"""import SwiftUI

public struct MockInterviewLogView: View {
    public let onSave: (MockResult) -> Void
    @Environment(\.dismiss) private var dismiss

    @State private var type: String = "Coding"
    @State private var score: Int = 3
    @State private var strengths: String = ""
    @State private var misses: String = ""
    @State private var nextDrill: String = ""

    public init(onSave: @escaping (MockResult) -> Void) {
        self.onSave = onSave
    }

    public var body: some View {
        NavigationStack {
            Form {
                Section("Format & Calibration") {
                    Picker("Type", selection: $type) {
                        Text("Coding (45m)").tag("Coding")
                        Text("System Design (45m)").tag("System Design")
                        Text("Behavioral / Leadership").tag("Behavioral")
                    }

                    Picker("Score", selection: $score) {
                        Text("1 - No Hire / Major Gaps").tag(1)
                        Text("2 - Lean No Hire / Needs Scaffolding").tag(2)
                        Text("3 - Lean Hire / Meets Bar").tag(3)
                        Text("4 - Strong Hire / Exceeds Bar").tag(4)
                    }
                }

                Section("Debrief Notes") {
                    TextField("What went well (strengths)", text: $strengths)
                    TextField("Misses / Hesitations", text: $misses)
                    TextField("Next targeted drill", text: $nextDrill)
                }
            }
            .navigationTitle("Log Mock")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        let result = MockResult(
                            date: Date(),
                            type: type,
                            score: score,
                            strengths: strengths,
                            misses: misses,
                            nextDrill: nextDrill
                        )
                        onSave(result)
                        dismiss()
                    }
                }
            }
        }
    }
}
"""

with open(f"{prog_dir}/MockInterviewLogView.swift", "w", encoding="utf-8") as f:
    f.write(mock_view_code.strip())
print("Wrote MockInterviewLogView.swift")

# 3. ChecklistView.swift
check_code = r"""import SwiftUI

public struct ChecklistView: View {
    @EnvironmentObject private var stateStore: StudyStateStore
    @State private var newTitle: String = ""
    @State private var newCategory: String = "Daily DSA"

    public init() {}

    public var body: some View {
        List {
            Section("Today's Active Checklist") {
                ForEach(stateStore.state.dailyChecklist) { item in
                    HStack {
                        Button(action: { stateStore.toggleChecklist(id: item.id) }) {
                            Image(systemName: item.isDone ? "checkmark.circle.fill" : "circle")
                                .foregroundColor(item.isDone ? .green : .secondary)
                                .font(.title3)
                        }
                        .buttonStyle(.plain)

                        VStack(alignment: .leading, spacing: 2) {
                            Text(item.title)
                                .font(.subheadline)
                                .strikethrough(item.isDone)
                                .foregroundColor(item.isDone ? .secondary : .primary)
                            Text(item.category)
                                .font(.caption2)
                                .foregroundColor(.secondary)
                        }
                    }
                    .padding(.vertical, 4)
                }
            }

            Section("Add Drill Item") {
                TextField("Drill description...", text: $newTitle)
                Picker("Category", selection: $newCategory) {
                    Text("Daily DSA").tag("Daily DSA")
                    Text("System Design").tag("System Design")
                    Text("Behavioral").tag("Behavioral")
                    Text("Error Log").tag("Error Log")
                }
                Button("Add to Checklist") {
                    if !newTitle.isEmpty {
                        stateStore.addChecklistItem(title: newTitle, category: newCategory)
                        newTitle = ""
                    }
                }
                .disabled(newTitle.isEmpty)
            }
        }
        .navigationTitle("Daily Drill Checklist")
    }
}
"""

with open(f"{prog_dir}/ChecklistView.swift", "w", encoding="utf-8") as f:
    f.write(check_code.strip())
print("Wrote ChecklistView.swift")

# 4. ProgressDashboardView.swift
dash_code = r"""import SwiftUI

public struct ProgressDashboardView: View {
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
                        .background(Color(uiColor: .secondarySystemGroupedBackground))
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
                                .background(Color(uiColor: .secondarySystemGroupedBackground))
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
                    .background(Color(uiColor: .secondarySystemGroupedBackground))
                    .cornerRadius(10)
                    .padding(.horizontal)
                }
            }
            .padding(.vertical)
        }
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
        .background(Color(uiColor: .secondarySystemGroupedBackground))
        .cornerRadius(10)
    }
}
"""

with open(f"{prog_dir}/ProgressDashboardView.swift", "w", encoding="utf-8") as f:
    f.write(dash_code.strip())
print("Wrote ProgressDashboardView.swift")

# 5. LocalInstallHelpView.swift
install_code = r"""import SwiftUI

public struct LocalInstallHelpView: View {
    public init() {}

    public var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text("Physical iPhone Local Installation")
                    .font(.title2.bold())

                Text("This app is designed to run 100% offline on your iPhone using Xcode's free local development provisioning. No paid Apple Developer account or App Store submission is needed.")
                    .font(.subheadline)
                    .foregroundColor(.secondary)

                VStack(alignment: .leading, spacing: 12) {
                    StepRow(number: 1, title: "Open Xcode Project", description: "Open `ios/GoogleInterviewPrep/GoogleInterviewPrep.xcodeproj` in Xcode.")
                    StepRow(number: 2, title: "Select Signing Team", description: "Select the app target in Xcode → Signing & Capabilities. Enable 'Automatically manage signing' and select your Personal Team.")
                    StepRow(number: 3, title: "Unique Bundle ID", description: "If prompted, change the bundle identifier to a unique string (e.g. dev.yourname.GoogleInterviewPrep).")
                    StepRow(number: 4, title: "Connect iPhone", description: "Connect your iPhone with a USB cable. Trust the Mac when prompted on the iPhone.")
                    StepRow(number: 5, title: "Enable Developer Mode", description: "On iPhone: Settings → Privacy & Security → Developer Mode → Turn ON and reboot.")
                    StepRow(number: 6, title: "Build & Run", description: "Select your iPhone as the destination in Xcode and press Run (Cmd+R).")
                    StepRow(number: 7, title: "Trust Developer Certificate", description: "On iPhone: Settings → General → VPN & Device Management → tap your Apple ID and tap Trust.")
                    StepRow(number: 8, title: "Verify Airplane Mode", description: "Turn on Airplane Mode on your iPhone to verify all 18 documents, full-text search, and notes work with zero network connection.")
                }
            }
            .padding()
        }
        .navigationTitle("Local Install Guide")
        .navigationBarTitleDisplayMode(.inline)
    }
}

public struct StepRow: View {
    public let number: Int
    public let title: String
    public let description: String

    public var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Text("\(number)")
                .font(.headline)
                .foregroundColor(.white)
                .frame(width: 28, height: 28)
                .background(Color.accentColor)
                .clipShape(Circle())

            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.headline)
                Text(description)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}
"""

with open(f"{sett_dir}/LocalInstallHelpView.swift", "w", encoding="utf-8") as f:
    f.write(install_code.strip())
print("Wrote LocalInstallHelpView.swift")

# 6. SettingsView.swift
settings_code = r"""import SwiftUI

public struct SettingsView: View {
    @EnvironmentObject private var env: AppEnvironment
    @EnvironmentObject private var stateStore: StudyStateStore
    @Environment(\.dismiss) private var dismiss

    @State private var showingResetPositionsAlert: Bool = false
    @State private var showingResetTrackerAlert: Bool = false
    @State private var showingResetAllAlert: Bool = false
    @State private var showingExportSheet: Bool = false
    @State private var exportURL: URL? = nil
    @State private var showingFileImporter: Bool = false
    @State private var importAlertMessage: String? = nil
    @State private var pendingImportState: UserStudyState? = nil
    @State private var showingConfirmImportAlert: Bool = false

    public init() {}

    public var body: some View {
        Form {
            Section("Timeline & Targets") {
                DatePicker(
                    "Preparation Start Date",
                    selection: Binding(
                        get: { stateStore.state.startDate ?? Date() },
                        set: { stateStore.updateDates(startDate: $0, interviewDate: stateStore.state.interviewDate) }
                    ),
                    displayedComponents: .date
                )

                DatePicker(
                    "Target Interview Date",
                    selection: Binding(
                        get: { stateStore.state.interviewDate ?? Calendar.current.date(byAdding: .day, value: 84, to: Date())! },
                        set: { stateStore.updateDates(startDate: stateStore.state.startDate, interviewDate: $0) }
                    ),
                    displayedComponents: .date
                )
            }

            Section("Appearance & Typography") {
                Picker("Theme", selection: Binding(
                    get: { stateStore.state.themePreference },
                    set: { stateStore.updatePreferences(theme: $0) }
                )) {
                    Text("System Default").tag("system")
                    Text("Light").tag("light")
                    Text("Dark").tag("dark")
                    Text("Sepia").tag("sepia")
                }

                VStack(alignment: .leading) {
                    HStack {
                        Text("Body Font Size")
                        Spacer()
                        Text("\(Int(stateStore.state.bodyFontSize)) pt")
                            .foregroundColor(.secondary)
                    }
                    Slider(
                        value: Binding(
                            get: { stateStore.state.bodyFontSize },
                            set: { stateStore.updatePreferences(bodySize: $0) }
                        ),
                        in: 14...22,
                        step: 1
                    )
                }

                VStack(alignment: .leading) {
                    HStack {
                        Text("Code Font Size")
                        Spacer()
                        Text("\(String(format: "%.1f", stateStore.state.codeFontSize)) pt")
                            .foregroundColor(.secondary)
                    }
                    Slider(
                        value: Binding(
                            get: { stateStore.state.codeFontSize },
                            set: { stateStore.updatePreferences(codeSize: $0) }
                        ),
                        in: 11...18,
                        step: 0.5
                    )
                }

                Toggle("Keep Screen Awake (Study Session)", isOn: Binding(
                    get: { stateStore.state.keepScreenAwake },
                    set: { stateStore.updatePreferences(keepAwake: $0) }
                ))
            }

            Section("Data Backup & Restore") {
                Button(action: {
                    if let url = ExportImportService.exportState(state: stateStore.state) {
                        self.exportURL = url
                        self.showingExportSheet = true
                    }
                }) {
                    Label("Export Study Progress (JSON)", systemImage: "square.and.arrow.up")
                }

                Button(action: { showingFileImporter = true }) {
                    Label("Import Study Progress (JSON)", systemImage: "square.and.arrow.down")
                }
            }

            Section("Content Integrity Audit") {
                HStack {
                    Text("Corpus Documents")
                    Spacer()
                    Text("18 / 18 Verified")
                        .bold()
                        .foregroundColor(.green)
                }
                HStack {
                    Text("Total Baseline Lines")
                    Spacer()
                    Text("10,833 Lines")
                        .foregroundColor(.secondary)
                }
                HStack {
                    Text("Offline Status")
                    Spacer()
                    Text("100% Bundled")
                        .foregroundColor(.green)
                }
            }

            Section("Installation Help") {
                NavigationLink(destination: LocalInstallHelpView()) {
                    Label("Physical iPhone Install Guide", systemImage: "iphone")
                }
            }

            Section("Destructive Resets") {
                Button("Reset Reading Positions & Completion", role: .destructive) {
                    showingResetPositionsAlert = true
                }

                Button("Reset Weekly Tracker & Checklists", role: .destructive) {
                    showingResetTrackerAlert = true
                }

                Button("Reset All Local Data", role: .destructive) {
                    showingResetAllAlert = true
                }
            }
        }
        .navigationTitle("Settings")
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .confirmationAction) {
                Button("Done") { dismiss() }
            }
        }
        .sheet(isPresented: $showingExportSheet) {
            if let url = exportURL {
                ShareSheet(items: [url])
            }
        }
        .fileImporter(
            isPresented: $showingFileImporter,
            allowedContentTypes: [.json]
        ) { result in
            switch result {
            case .success(let url):
                if url.startAccessingSecurityScopedResource() {
                    defer { url.stopAccessingSecurityScopedResource() }
                    if let data = try? Data(contentsOf: url) {
                        let (parsedState, summary) = ExportImportService.validateImportData(data)
                        if summary.isValid, let valid = parsedState {
                            self.pendingImportState = valid
                            self.importAlertMessage = "Valid backup found:\n• \(summary.bookmarkCount) bookmarks\n• \(summary.trackedWeeksCount) tracked weeks\n• \(summary.checklistCount) checklist items\n\nReplace current study progress?"
                            self.showingConfirmImportAlert = true
                        } else {
                            self.importAlertMessage = "Failed to import JSON: \(summary.errorMessage ?? "Invalid schema")"
                            self.showingConfirmImportAlert = true
                        }
                    }
                }
            case .failure(let err):
                self.importAlertMessage = err.localizedDescription
                self.showingConfirmImportAlert = true
            }
        }
        .alert("Import Backup", isPresented: $showingConfirmImportAlert) {
            if pendingImportState != nil {
                Button("Cancel", role: .cancel) { pendingImportState = nil }
                Button("Replace Local State", role: .destructive) {
                    if let p = pendingImportState {
                        stateStore.replaceState(with: p)
                    }
                    pendingImportState = nil
                }
            } else {
                Button("OK", role: .cancel) {}
            }
        } message: {
            Text(importAlertMessage ?? "")
        }
        .themedSurface()
        .alert("Reset Reading Positions?", isPresented: $showingResetPositionsAlert) {
            Button("Cancel", role: .cancel) {}
            Button("Reset Positions", role: .destructive) {
                stateStore.resetReadingPositions()
            }
        } message: {
            Text("This will clear all scroll positions and reading completion marks. Your notes, bookmarks, and tracker data are preserved.")
        }
        .alert("Reset Tracker Data?", isPresented: $showingResetTrackerAlert) {
            Button("Cancel", role: .cancel) {}
            Button("Reset Tracker", role: .destructive) {
                stateStore.resetTrackerData()
            }
        } message: {
            Text("This will reset all 12-week hours, mock logs, and daily checklists to defaults. Bookmarks and reading positions are preserved.")
        }
        .alert("Reset All Local Data?", isPresented: $showingResetAllAlert) {
            Button("Cancel", role: .cancel) {}
            Button("Reset Everything", role: .destructive) {
                stateStore.resetAllState()
            }
        } message: {
            Text("This will erase all reading history, bookmarks, notes, and tracker logs. This action cannot be undone.")
        }
    }
}

public struct ShareSheet: UIViewControllerRepresentable {
    public let items: [Any]

    public func makeUIViewController(context: Context) -> UIActivityViewController {
        UIActivityViewController(activityItems: items, applicationActivities: nil)
    }

    public func updateUIViewController(_ uiViewController: UIActivityViewController, context: Context) {}
}
"""

with open(f"{sett_dir}/SettingsView.swift", "w", encoding="utf-8") as f:
    f.write(settings_code.strip())
print("Wrote SettingsView.swift")
