import SwiftUI

public struct LibraryView: View {
    @Environment(\.appTheme) private var theme
    @EnvironmentObject private var env: AppEnvironment
    @EnvironmentObject private var stateStore: StudyStateStore
    @State private var selectedFilter: String = "All"
    @State private var showingAllDocuments: Bool = false
    @State private var targetNavigation: (doc: ContentDocument, anchor: String?)? = nil

    private let categories = [
        "All", "Plans", "DSA", "Python", "Java", "Backend", "System Design", "Behavioral", "Archive"
    ]

    public init() {}

    public var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 18) {
                // Category Filter Pills
                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(categories, id: \.self) { cat in
                            Button(action: { selectedFilter = cat }) {
                                Text(cat)
                                    .font(.subheadline.bold())
                                    .padding(.horizontal, 14)
                                    .padding(.vertical, 7)
                                    .background(selectedFilter == cat ? Color.accentColor : theme.secondaryBackground)
                                    .foregroundColor(selectedFilter == cat ? .white : .primary)
                                    .clipShape(Capsule())
                            }
                        }
                    }
                    .padding(.horizontal)
                }

                // All Documents link proving 18 unique documents
                Button(action: { showingAllDocuments = true }) {
                    HStack {
                        Label("View All 18 Documents", systemImage: "list.bullet.rectangle.fill")
                            .font(.subheadline.bold())
                            .foregroundColor(.accentColor)
                        Spacer()
                        Text("18 Total")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        Image(systemName: "chevron.right")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    .padding(14)
                    .background(Color.accentColor.opacity(0.1))
                    .cornerRadius(10)
                }
                .buttonStyle(.plain)
                .accessibilityIdentifier("viewAllDocumentsButton")
                .padding(.horizontal)

                if selectedFilter == "All" || selectedFilter == "Plans" {
                    categoryGroup(title: "12-Week Preparation", docs: env.repository.prep12WeekDocuments)
                }
                if selectedFilter == "All" || selectedFilter == "DSA" {
                    categoryGroup(title: "DSA Practice", docs: env.repository.dsaDocuments)
                }
                if selectedFilter == "All" || selectedFilter == "Python" {
                    categoryGroup(title: "Python Interview Material", docs: env.repository.pythonDocuments)
                }
                if selectedFilter == "All" || selectedFilter == "Java" {
                    categoryGroup(title: "Java & Design", docs: env.repository.javaDocuments)
                }
                if selectedFilter == "All" || selectedFilter == "Backend" {
                    categoryGroup(title: "Backend Frameworks", docs: env.repository.backendDocuments)
                }
                if selectedFilter == "All" || selectedFilter == "System Design" {
                    systemDesignGroup
                }
                if selectedFilter == "All" || selectedFilter == "Behavioral" {
                    categoryGroup(title: "Behavioral", docs: env.repository.behavioralDocuments)
                }
                if selectedFilter == "All" || selectedFilter == "Archive" {
                    categoryGroup(title: "Archive & Reviews", docs: env.repository.archiveDocuments)
                }
            }
            .padding(.vertical)
        }
        .themedSurface()
        .navigationTitle("Library")
        .navigationDestination(for: ContentDocument.self) { doc in
            DocumentReaderView(document: doc)
        }
        .navigationDestination(isPresented: $showingAllDocuments) {
            AllDocumentsView()
        }
        .navigationDestination(isPresented: Binding(
            get: { targetNavigation != nil },
            set: { if !$0 { targetNavigation = nil } }
        )) {
            if let nav = targetNavigation {
                DocumentReaderView(document: nav.doc, initialAnchor: nav.anchor)
            }
        }
    }

    private func categoryGroup(title: String, docs: [ContentDocument]) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            Text(title)
                .font(.headline)
                .padding(.horizontal)

            VStack(spacing: 10) {
                ForEach(docs) { doc in
                    DocumentCard(
                        document: doc,
                        readingState: stateStore.readingState(for: doc.id)
                    )
                }
            }
            .padding(.horizontal)
        }
    }

    private var systemDesignGroup: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("System Design (Plan Deep Links)")
                .font(.headline)
                .padding(.horizontal)

            VStack(spacing: 8) {
                ForEach(env.repository.systemDesignSections) { sec in
                    if let doc = env.repository.document(withID: sec.documentID) {
                        Button(action: {
                            targetNavigation = (doc: doc, anchor: sec.anchor)
                        }) {
                            HStack {
                                VStack(alignment: .leading, spacing: 3) {
                                    Text(sec.title)
                                        .font(.subheadline.bold())
                                        .foregroundColor(.primary)
                                        .multilineTextAlignment(.leading)
                                    Text("Deep link in \(doc.title)")
                                        .font(.caption2)
                                        .foregroundColor(.accentColor)
                                }
                                Spacer()
                                Image(systemName: "arrow.up.right.square")
                                    .foregroundColor(.secondary)
                            }
                            .padding(12)
                            .background(theme.secondaryBackground)
                            .cornerRadius(10)
                        }
                        .buttonStyle(.plain)
                    }
                }
            }
            .padding(.horizontal)
        }
    }
}
