import SwiftUI

public struct DocumentReaderView: View {
    public let document: ContentDocument
    public let initialAnchor: String?

    @EnvironmentObject private var env: AppEnvironment
    @EnvironmentObject private var stateStore: StudyStateStore
    @Environment(\.appTheme) private var theme

    @State private var scrollAnchor: String?
    @State private var showingTOC: Bool = false
    @State private var showingAddBookmark: Bool = false
    @State private var bookmarkTitle: String = ""
    @State private var bookmarkNote: String = ""
    @State private var showingExternalLinkAlert: Bool = false
    @State private var pendingExternalURL: URL? = nil
    @State private var contentString: String

    public init(document: ContentDocument, initialAnchor: String? = nil, repository: ContentRepository? = nil) {
        self.document = document
        self.initialAnchor = initialAnchor
        let preloaded = repository?.content(for: document) ?? ContentRepository.loadContent(for: document) ?? ""
        _contentString = State(initialValue: preloaded)
    }

    private var documentSections: [SearchIndexEntry] {
        env.repository.searchIndex.entries.filter { $0.documentID == document.id }
    }

    private var isCompleted: Bool {
        stateStore.readingState(for: document.id).explicitlyCompleted
    }

    public var body: some View {
        VStack(spacing: 0) {
            // Historical Badge Banner if applicable
            if document.isHistorical {
                HStack {
                    Image(systemName: "exclamationmark.triangle.fill")
                        .foregroundColor(.orange)
                    Text("Historical Review / Archival — do not treat as current truth")
                        .font(.caption.bold())
                        .foregroundColor(.orange)
                    Spacer()
                }
                .padding(.horizontal)
                .padding(.vertical, 6)
                .background(Color.orange.opacity(0.12))
            }

            // Reader Body
            if document.format == .java {
                JavaSourceReaderView(
                    code: contentString,
                    documentTitle: document.title,
                    initialAnchor: scrollAnchor,
                    onBookmarkSymbol: { symTitle, lineNum in
                        stateStore.addBookmark(
                            documentID: document.id,
                            sectionID: "\(document.id)-line-\(lineNum)",
                            title: symTitle,
                            note: "Bookmarked from Java symbol list (Line \(lineNum))"
                        )
                    }
                )
            } else {
                MarkdownWebView(
                    markdown: contentString,
                    documentID: document.id,
                    isHistorical: document.isHistorical,
                    theme: stateStore.state.themePreference,
                    bodyFontSize: stateStore.state.bodyFontSize,
                    codeFontSize: stateStore.state.codeFontSize,
                    scrollAnchor: scrollAnchor,
                    onOpenExternalURL: { url in
                        pendingExternalURL = url
                        showingExternalLinkAlert = true
                    }
                )
            }
        }
        .themedSurface()
        .navigationTitle(document.title)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItemGroup(placement: .navigationBarTrailing) {
                Button(action: { showingTOC = true }) {
                    Image(systemName: "list.bullet")
                }

                Button(action: {
                    bookmarkTitle = document.title
                    bookmarkNote = ""
                    showingAddBookmark = true
                }) {
                    Image(systemName: "bookmark")
                }

                Button(action: {
                    stateStore.toggleExplicitCompletion(documentID: document.id)
                }) {
                    Image(systemName: isCompleted ? "checkmark.circle.fill" : "circle")
                        .foregroundColor(isCompleted ? .green : .secondary)
                }
            }
        }
        .sheet(isPresented: $showingTOC) {
            TableOfContentsDrawer(sections: documentSections) { sec in
                self.scrollAnchor = sec.anchor
                stateStore.updateReadingPosition(
                    documentID: document.id,
                    sectionID: sec.sectionID,
                    anchor: sec.anchor,
                    estimatedProgress: 0.5
                )
            }
        }
        .sheet(isPresented: $showingAddBookmark) {
            NavigationStack {
                Form {
                    Section("Bookmark Details") {
                        TextField("Title", text: $bookmarkTitle)
                        TextField("Notes / Takeaways", text: $bookmarkNote, axis: .vertical)
                            .lineLimit(3...6)
                    }
                    .listRowBackground(theme.secondaryBackground)
                }
                .themedSurface()
                .navigationTitle("Add Bookmark")
                .navigationBarTitleDisplayMode(.inline)
                .toolbar {
                    ToolbarItem(placement: .cancellationAction) {
                        Button("Cancel") { showingAddBookmark = false }
                    }
                    ToolbarItem(placement: .confirmationAction) {
                        Button("Save") {
                            stateStore.addBookmark(
                                documentID: document.id,
                                sectionID: scrollAnchor,
                                title: bookmarkTitle.isEmpty ? document.title : bookmarkTitle,
                                note: bookmarkNote
                            )
                            showingAddBookmark = false
                        }
                    }
                }
            }
        }
        .alert("Open External Link?", isPresented: $showingExternalLinkAlert) {
            Button("Cancel", role: .cancel) {}
            Button("Open in Safari") {
                if let url = pendingExternalURL {
                    UIApplication.shared.open(url)
                }
            }
        } message: {
            if let url = pendingExternalURL {
                Text("This link opens in Safari:\n\(url.absoluteString)")
            }
        }
        .onAppear {
            if contentString.isEmpty, let loaded = env.repository.content(for: document) {
                self.contentString = loaded
            }
            if let initAnchor = initialAnchor {
                self.scrollAnchor = initAnchor
            } else {
                let saved = stateStore.readingState(for: document.id)
                self.scrollAnchor = saved.scrollAnchor
            }
            stateStore.updateReadingPosition(
                documentID: document.id,
                sectionID: scrollAnchor,
                anchor: scrollAnchor,
                estimatedProgress: 0.1
            )
        }
        .onDisappear {
            stateStore.updateReadingPosition(
                documentID: document.id,
                sectionID: scrollAnchor,
                anchor: scrollAnchor,
                estimatedProgress: 0.3
            )
        }
    }
}
