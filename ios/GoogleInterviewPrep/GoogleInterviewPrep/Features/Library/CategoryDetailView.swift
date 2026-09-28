import SwiftUI

public struct CategoryDetailView: View {
    public let title: String
    public let documents: [ContentDocument]
    @EnvironmentObject private var stateStore: StudyStateStore

    public init(title: String, documents: [ContentDocument]) {
        self.title = title
        self.documents = documents
    }

    public var body: some View {
        ScrollView {
            LazyVStack(spacing: 12) {
                ForEach(documents) { doc in
                    DocumentCard(
                        document: doc,
                        readingState: stateStore.readingState(for: doc.id)
                    )
                }
            }
            .padding()
        }
        .themedSurface()
        .navigationTitle(title)
        .navigationDestination(for: ContentDocument.self) { doc in
            DocumentReaderView(document: doc)
        }
    }
}
