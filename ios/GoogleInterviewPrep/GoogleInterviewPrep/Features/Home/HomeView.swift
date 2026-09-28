import SwiftUI

public struct HomeView: View {
    @Environment(\.appTheme) private var theme
    @EnvironmentObject private var env: AppEnvironment
    @EnvironmentObject private var stateStore: StudyStateStore
    @State private var showingSettings: Bool = false

    public init() {}

    private var currentWeek: Int {
        guard let start = stateStore.state.startDate else { return 1 }
        let diff = Calendar.current.dateComponents([.day], from: start, to: Date()).day ?? 0
        let week = max(1, min(12, (diff / 7) + 1))
        return week
    }

    private var daysUntilInterview: Int? {
        guard let target = stateStore.state.interviewDate else { return nil }
        let diff = Calendar.current.dateComponents([.day], from: Date(), to: target).day
        return diff
    }

    private var lastOpenedDoc: ContentDocument? {
        let sorted = stateStore.state.readingStates.values.sorted { $0.lastOpenedAt > $1.lastOpenedAt }
        guard let recent = sorted.first else { return nil }
        return env.repository.document(withID: recent.documentID)
    }

    public var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Header Banner
                HStack {
                    VStack(alignment: .leading, spacing: 4) {
                        Text("Preparation Dashboard")
                            .font(.caption.bold())
                            .foregroundColor(.accentColor)
                            .textCase(.uppercase)

                        Text("Week \(currentWeek) of 12")
                            .font(.title.bold())

                        if let days = daysUntilInterview {
                            Text("\(max(0, days)) days until interview")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        } else {
                            Text("Interview date not set")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                    }
                    Spacer()
                    Button(action: { showingSettings = true }) {
                        Image(systemName: "gearshape.fill")
                            .font(.title2)
                            .foregroundColor(.secondary)
                    }
                }
                .padding(.horizontal)
                .padding(.top, 8)

                // Offline status badge
                HStack {
                    Label("18 documents available offline", systemImage: "arrow.down.circle.fill")
                        .font(.caption.bold())
                        .foregroundColor(.green)
                    Spacer()
                    Text("Zero Network Required")
                        .font(.caption2)
                        .foregroundColor(.secondary)
                }
                .padding(.horizontal, 14)
                .padding(.vertical, 8)
                .background(Color.green.opacity(0.1))
                .cornerRadius(8)
                .padding(.horizontal)

                // Quick Reference Card
                if let qrDoc = env.repository.document(withID: "quick.reference") {
                    NavigationLink(value: qrDoc) {
                        HStack {
                            VStack(alignment: .leading, spacing: 4) {
                                HStack {
                                    Image(systemName: "bolt.fill")
                                        .foregroundColor(.orange)
                                    Text("Quick Reference")
                                        .font(.headline)
                                        .foregroundColor(.primary)
                                }
                                Text("Key interview mechanics, timeline & scoring rubric")
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                            }
                            Spacer()
                            Image(systemName: "chevron.right")
                                .foregroundColor(.secondary)
                        }
                        .padding(16)
                        .background(theme.secondaryBackground)
                        .cornerRadius(12)
                    }
                    .buttonStyle(.plain)
                    .padding(.horizontal)
                }

                // Continue Reading Card
                if let doc = lastOpenedDoc {
                    VStack(alignment: .leading, spacing: 10) {
                        Text("Continue Reading")
                            .font(.headline)
                            .padding(.horizontal)

                        DocumentCard(
                            document: doc,
                            readingState: stateStore.readingState(for: doc.id)
                        )
                        .padding(.horizontal)
                    }
                }

                // Today's Preparation Checklist
                VStack(alignment: .leading, spacing: 10) {
                    HStack {
                        Text("Today's Drill Checklist")
                            .font(.headline)
                        Spacer()
                    }
                    .padding(.horizontal)

                    VStack(spacing: 8) {
                        ForEach(stateStore.state.dailyChecklist.prefix(4)) { item in
                            HStack {
                                Button(action: { stateStore.toggleChecklist(id: item.id) }) {
                                    Image(systemName: item.isDone ? "checkmark.circle.fill" : "circle")
                                        .foregroundColor(item.isDone ? .green : .secondary)
                                        .font(.title3)
                                }
                                Text(item.title)
                                    .font(.subheadline)
                                    .strikethrough(item.isDone)
                                    .foregroundColor(item.isDone ? .secondary : .primary)
                                Spacer()
                                Text(item.category)
                                    .font(.caption2)
                                    .padding(.horizontal, 6)
                                    .padding(.vertical, 2)
                                    .background(theme.tertiaryBackground)
                                    .cornerRadius(4)
                            }
                            .padding(.vertical, 4)
                        }
                    }
                    .padding(14)
                    .background(theme.secondaryBackground)
                    .cornerRadius(12)
                    .padding(.horizontal)
                }

                // Recent Bookmarks
                if !stateStore.state.bookmarks.isEmpty {
                    VStack(alignment: .leading, spacing: 10) {
                        Text("Recent Bookmarks")
                            .font(.headline)
                            .padding(.horizontal)

                        VStack(spacing: 8) {
                            ForEach(stateStore.state.bookmarks.prefix(3)) { bm in
                                if let doc = env.repository.document(withID: bm.documentID) {
                                    NavigationLink(value: doc) {
                                        HStack {
                                            VStack(alignment: .leading, spacing: 2) {
                                                Text(bm.title.isEmpty ? doc.title : bm.title)
                                                    .font(.subheadline.bold())
                                                    .foregroundColor(.primary)
                                                if !bm.note.isEmpty {
                                                    Text(bm.note)
                                                        .font(.caption)
                                                        .foregroundColor(.secondary)
                                                }
                                            }
                                            Spacer()
                                            Image(systemName: "chevron.right")
                                                .font(.caption)
                                                .foregroundColor(.secondary)
                                        }
                                        .padding(.vertical, 4)
                                    }
                                    .buttonStyle(.plain)
                                }
                            }
                        }
                        .padding(14)
                        .background(theme.secondaryBackground)
                        .cornerRadius(12)
                        .padding(.horizontal)
                    }
                }
            }
            .padding(.bottom, 24)
        }
        .themedSurface()
        .navigationTitle("Home")
        .sheet(isPresented: $showingSettings) {
            NavigationStack {
                SettingsView()
            }
        }
        .navigationDestination(for: ContentDocument.self) { doc in
            DocumentReaderView(document: doc)
        }
    }
}
