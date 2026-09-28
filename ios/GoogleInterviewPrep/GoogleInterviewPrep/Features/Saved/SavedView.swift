import SwiftUI

public struct SavedView: View {
    @EnvironmentObject private var env: AppEnvironment
    @EnvironmentObject private var stateStore: StudyStateStore
    @Environment(\.appTheme) private var theme
    @State private var selectedBookmarkToEdit: Bookmark? = nil
    @State private var targetNavigation: (doc: ContentDocument, anchor: String?)? = nil

    public init() {}

    public var body: some View {
        Group {
            if stateStore.state.bookmarks.isEmpty {
                EmptyStateView(
                    icon: "bookmark",
                    title: "No Bookmarks Yet",
                    message: "Tap the bookmark icon while reading any document or code block to save it here for fast revision."
                )
            } else {
                List {
                    Group {
                    ForEach(stateStore.state.bookmarks) { bm in
                        VStack(alignment: .leading, spacing: 6) {
                            HStack {
                                Text(bm.title)
                                    .font(.headline)
                                    .foregroundColor(.primary)
                                Spacer()
                                if let doc = env.repository.document(withID: bm.documentID) {
                                    Button(action: {
                                        targetNavigation = (doc: doc, anchor: bm.sectionID)
                                    }) {
                                        Text("Open")
                                            .font(.caption.bold())
                                            .foregroundColor(.accentColor)
                                    }
                                    .buttonStyle(.borderless)
                                }
                            }

                            if !bm.note.isEmpty {
                                Text(bm.note)
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)
                            }

                            HStack {
                                Text(bm.createdAt.formatted(date: .abbreviated, time: .shortened))
                                    .font(.caption2)
                                    .foregroundColor(.secondary)

                                Spacer()

                                Button(action: { selectedBookmarkToEdit = bm }) {
                                    Label("Edit Note", systemImage: "pencil")
                                        .font(.caption2)
                                        .foregroundColor(.accentColor)
                                }
                                .buttonStyle(.borderless)
                            }
                        }
                        .padding(.vertical, 4)
                    }
                    .onDelete { indexSet in
                        for idx in indexSet {
                            let item = stateStore.state.bookmarks[idx]
                            stateStore.removeBookmark(id: item.id)
                        }
                    }
                    }
                    .listRowBackground(theme.secondaryBackground)
                }
                .listStyle(.insetGrouped)
            }
        }
        .themedSurface()
        .navigationTitle("Saved (\(stateStore.state.bookmarks.count))")
        .sheet(item: $selectedBookmarkToEdit) { bm in
            BookmarkNoteEditorView(bookmark: bm)
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
}
