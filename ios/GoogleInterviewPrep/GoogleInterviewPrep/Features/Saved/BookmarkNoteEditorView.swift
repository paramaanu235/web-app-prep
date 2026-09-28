import SwiftUI

public struct BookmarkNoteEditorView: View {
    public let bookmark: Bookmark
    @EnvironmentObject private var stateStore: StudyStateStore
    @Environment(\.dismiss) private var dismiss
    @Environment(\.appTheme) private var theme

    @State private var noteText: String = ""

    public init(bookmark: Bookmark) {
        self.bookmark = bookmark
    }

    public var body: some View {
        NavigationStack {
            Form {
                Group {
                Section("Bookmark") {
                    Text(bookmark.title)
                        .font(.headline)
                }

                Section("Study Note") {
                    TextEditor(text: $noteText)
                        .frame(minHeight: 120)
                }
                }
                .listRowBackground(theme.secondaryBackground)
            }
            .themedSurface()
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
