import os

search_dir = "ios/GoogleInterviewPrep/GoogleInterviewPrep/Features/Search"
saved_dir = "ios/GoogleInterviewPrep/GoogleInterviewPrep/Features/Saved"
os.makedirs(search_dir, exist_ok=True)
os.makedirs(saved_dir, exist_ok=True)

# 1. SearchResultRow.swift
row_code = r"""import SwiftUI

public struct SearchResultRow: View {
    public let result: SearchResult
    public let onSelect: () -> Void

    public init(result: SearchResult, onSelect: @escaping () -> Void) {
        self.result = result
        self.onSelect = onSelect
    }

    public var body: some View {
        Button(action: onSelect) {
            VStack(alignment: .leading, spacing: 6) {
                HStack {
                    Text(result.documentTitle)
                        .font(.caption.bold())
                        .foregroundColor(.accentColor)
                    Spacer()
                    if result.isHistorical {
                        StatusBadge("Historical", color: .orange)
                    } else {
                        StatusBadge(result.format.uppercased(), color: .secondary)
                    }
                }

                Text(result.sectionTitle)
                    .font(.headline)
                    .foregroundColor(.primary)

                if !result.preview.isEmpty {
                    Text(result.preview)
                        .font(.caption)
                        .foregroundColor(.secondary)
                        .lineLimit(2)
                }
            }
            .padding(.vertical, 6)
        }
        .buttonStyle(.plain)
    }
}
"""

with open(f"{search_dir}/SearchResultRow.swift", "w", encoding="utf-8") as f:
    f.write(row_code.strip())
print("Wrote SearchResultRow.swift")

# 2. SearchView.swift
search_view_code = r"""import SwiftUI

public struct SearchView: View {
    @EnvironmentObject private var env: AppEnvironment
    @EnvironmentObject private var searchService: SearchService
    @State private var targetNavigation: (doc: ContentDocument, anchor: String?)? = nil

    private let categories = [
        ("All", nil),
        ("Plans", "plans"),
        ("DSA", "dsa"),
        ("Java", "java"),
        ("Backend", "backend"),
        ("Behavioral", "behavioral")
    ]

    public init() {}

    public var body: some View {
        VStack(spacing: 0) {
            // Category Filter Pills
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 8) {
                    ForEach(categories, id: \.0) { cat in
                        let isSelected = searchService.selectedCategory == cat.1
                        Button(action: { searchService.selectedCategory = cat.1 }) {
                            Text(cat.0)
                                .font(.subheadline.bold())
                                .padding(.horizontal, 14)
                                .padding(.vertical, 6)
                                .background(isSelected ? Color.accentColor : Color(uiColor: .secondarySystemGroupedBackground))
                                .foregroundColor(isSelected ? .white : .primary)
                                .clipShape(Capsule())
                        }
                    }

                    // Format toggle: Java vs Markdown
                    Button(action: {
                        if searchService.selectedFormat == "java" {
                            searchService.selectedFormat = nil
                        } else {
                            searchService.selectedFormat = "java"
                        }
                    }) {
                        HStack(spacing: 4) {
                            Image(systemName: "curlybraces")
                            Text("Java Only")
                        }
                        .font(.subheadline.bold())
                        .padding(.horizontal, 14)
                        .padding(.vertical, 6)
                        .background(searchService.selectedFormat == "java" ? Color.purple : Color(uiColor: .secondarySystemGroupedBackground))
                        .foregroundColor(searchService.selectedFormat == "java" ? .white : .primary)
                        .clipShape(Capsule())
                    }
                }
                .padding(.horizontal)
                .padding(.vertical, 8)
            }
            .background(Color(uiColor: .systemGroupedBackground))

            // Results List
            if searchService.query.isEmpty {
                EmptyStateView(
                    icon: "magnifyingglass",
                    title: "Offline Corpus Search",
                    message: "Search across 10,833 lines of algorithms, Java patterns, Python snippets, and system design plans. Tokens like @Transactional, 0-1 BFS, select_for_update are fully indexed."
                )
            } else if searchService.results.isEmpty {
                EmptyStateView(
                    icon: "doc.text.magnifyingglass",
                    title: "No Matching Results",
                    message: "No document sections found matching '\(searchService.query)' with the current filters."
                )
            } else {
                List(searchService.results) { result in
                    SearchResultRow(result: result) {
                        if let doc = env.repository.document(withID: result.documentID) {
                            targetNavigation = (doc: doc, anchor: result.anchor)
                        }
                    }
                }
                .listStyle(.insetGrouped)
            }
        }
        .searchable(text: $searchService.query, prompt: "Search topics, code symbols, patterns...")
        .navigationTitle("Search")
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
"""

with open(f"{search_dir}/SearchView.swift", "w", encoding="utf-8") as f:
    f.write(search_view_code.strip())
print("Wrote SearchView.swift")

# 3. BookmarkNoteEditorView.swift
bm_editor_code = r"""import SwiftUI

public struct BookmarkNoteEditorView: View {
    public let bookmark: Bookmark
    @EnvironmentObject private var stateStore: StudyStateStore
    @Environment(\.dismiss) private var dismiss

    @State private var noteText: String = ""

    public init(bookmark: Bookmark) {
        self.bookmark = bookmark
    }

    public var body: some View {
        NavigationStack {
            Form {
                Section("Bookmark") {
                    Text(bookmark.title)
                        .font(.headline)
                }

                Section("Study Note") {
                    TextEditor(text: $noteText)
                        .frame(minHeight: 120)
                }
            }
            .navigationTitle("Edit Note")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") {
                        stateStore.updateBookmarkNote(id: bookmark.id, note: noteText)
                        dismiss()
                    }
                }
            }
            .onAppear {
                self.noteText = bookmark.note
            }
        }
    }
}
"""

with open(f"{saved_dir}/BookmarkNoteEditorView.swift", "w", encoding="utf-8") as f:
    f.write(bm_editor_code.strip())
print("Wrote BookmarkNoteEditorView.swift")

# 4. SavedView.swift
saved_view_code = r"""import SwiftUI

public struct SavedView: View {
    @EnvironmentObject private var env: AppEnvironment
    @EnvironmentObject private var stateStore: StudyStateStore
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
                .listStyle(.insetGrouped)
            }
        }
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
"""

with open(f"{saved_dir}/SavedView.swift", "w", encoding="utf-8") as f:
    f.write(saved_view_code.strip())
print("Wrote SavedView.swift")
