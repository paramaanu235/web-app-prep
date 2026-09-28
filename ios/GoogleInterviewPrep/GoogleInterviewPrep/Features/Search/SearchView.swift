import SwiftUI

public struct SearchView: View {
    @Environment(\.appTheme) private var theme
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
                                .background(isSelected ? Color.accentColor : theme.secondaryBackground)
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
                        .background(searchService.selectedFormat == "java" ? Color.purple : theme.secondaryBackground)
                        .foregroundColor(searchService.selectedFormat == "java" ? .white : .primary)
                        .clipShape(Capsule())
                    }
                }
                .padding(.horizontal)
                .padding(.vertical, 8)
            }
            .background(theme.groupedBackground)

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
        .themedSurface()
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
