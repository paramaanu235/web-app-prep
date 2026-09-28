import SwiftUI

public struct SettingsView: View {
    @EnvironmentObject private var env: AppEnvironment
    @EnvironmentObject private var stateStore: StudyStateStore
    @Environment(\.dismiss) private var dismiss
    @Environment(\.appTheme) private var theme

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
            Group {
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

            contentIntegritySection

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
            .listRowBackground(theme.secondaryBackground)
        }
        .themedSurface()
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

    @ViewBuilder
    private var contentIntegritySection: some View {
        let live = env.repository.verifyLiveBundleIntegrity()
        let report = env.repository.loadIntegrityReport()
        let versionStr = "Version \(env.repository.manifest.version)"
        let totalLinesStr = report.map { "\($0.totalLines.formatted()) Lines" } ?? "10,833 Lines"
        let corpusSizeStr = report.map { ByteCountFormatter.string(fromByteCount: Int64($0.totalBytes), countStyle: .file) } ?? "473 KB"
        let buildAuditStr = (report?.allHashesMatch == true) ? "\(env.repository.documents.count) / \(env.repository.documents.count) Verified" : "Mismatched"
        let liveStr = live.allMatch ? "\(live.matched) / \(live.total) Live Verified" : "\(live.matched) / \(live.total) Mismatched"

        Section("Content Integrity Audit") {
            HStack {
                Text("Manifest Version")
                Spacer()
                Text(versionStr)
                    .foregroundColor(.secondary)
            }
            if !env.repository.manifest.builtAt.isEmpty {
                HStack {
                    Text("Manifest Build Date")
                    Spacer()
                    Text(env.repository.manifest.builtAt)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            HStack {
                Text("Live Runtime Integrity")
                Spacer()
                Text(liveStr)
                    .bold()
                    .foregroundColor(live.allMatch ? .green : .red)
            }
            HStack {
                Text("Build-Time Audit")
                Spacer()
                Text(buildAuditStr)
                    .foregroundColor((report?.allHashesMatch == true) ? .green : .orange)
            }
            HStack {
                Text("Total Baseline Lines")
                Spacer()
                Text(totalLinesStr)
                    .foregroundColor(.secondary)
            }
            HStack {
                Text("Corpus Size")
                Spacer()
                Text(corpusSizeStr)
                    .foregroundColor(.secondary)
            }
            HStack {
                Text("Offline Status")
                Spacer()
                Text("100% Bundled")
                    .foregroundColor(.green)
            }
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
