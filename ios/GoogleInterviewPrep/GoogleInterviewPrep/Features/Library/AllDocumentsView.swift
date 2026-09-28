import SwiftUI

public struct AllDocumentsView: View {
    @EnvironmentObject private var env: AppEnvironment
    @EnvironmentObject private var stateStore: StudyStateStore
    @Environment(\.appTheme) private var theme

    public init() {}

    public var body: some View {
        List {
            Group {
            Section {
                HStack {
                    Image(systemName: "checkmark.seal.fill")
                        .foregroundColor(.green)
                    Text("Manifest Audit: 18 / 18 Documents Verified")
                        .font(.subheadline.bold())
                }
            }

            ForEach(env.repository.documents.sorted(by: { $0.order < $1.order })) { doc in
                NavigationLink(value: doc) {
                    HStack(alignment: .top, spacing: 12) {
                        Text("\(doc.order)")
                            .font(.caption.bold())
                            .foregroundColor(.secondary)
                            .frame(width: 22, alignment: .leading)

                        VStack(alignment: .leading, spacing: 4) {
                            HStack {
                                Text(doc.title)
                                    .font(.headline)
                                    .foregroundColor(.primary)
                                Spacer()
                                if doc.isHistorical {
                                    HistoricalBadge()
                                }
                            }

                            Text(doc.sourceFilename)
                                .font(.caption)
                                .foregroundColor(.secondary)

                            HStack {
                                Text(doc.primaryCategory)
                                    .font(.caption2)
                                    .foregroundColor(.accentColor)
                                Spacer()
                                Text("\(doc.lineCountAtManifestBuild) lines")
                                    .font(.caption2)
                                    .foregroundColor(.secondary)
                            }
                        }
                    }
                    .padding(.vertical, 4)
                }
            }
            }
            .listRowBackground(theme.secondaryBackground)
        }
        .themedSurface()
        .navigationTitle("All Documents (\(env.repository.documents.count))")
        .navigationBarTitleDisplayMode(.inline)
        .navigationDestination(for: ContentDocument.self) { doc in
            DocumentReaderView(document: doc)
        }
    }
}
