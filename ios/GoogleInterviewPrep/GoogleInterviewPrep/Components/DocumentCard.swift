import SwiftUI

public struct DocumentCard: View {
    @Environment(\.appTheme) private var theme
    public let document: ContentDocument
    public let readingState: ReadingState?
    public var action: (() -> Void)?

    public init(document: ContentDocument, readingState: ReadingState? = nil, action: (() -> Void)? = nil) {
        self.document = document
        self.readingState = readingState
        self.action = action
    }

    public var body: some View {
        if let action = action {
            Button(action: action) {
                cardBody
            }
            .buttonStyle(.plain)
        } else {
            NavigationLink(value: document) {
                cardBody
            }
            .buttonStyle(.plain)
        }
    }

    private var cardBody: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack(alignment: .top) {
                VStack(alignment: .leading, spacing: 4) {
                    Text(document.title)
                        .font(.headline)
                        .foregroundColor(.primary)
                        .multilineTextAlignment(.leading)

                    Text(document.sourceFilename)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }

                Spacer()

                if document.isHistorical {
                    HistoricalBadge()
                } else if document.format == .java {
                    StatusBadge("Java Source", systemImage: "chevron.left.forwardslash.chevron.right", color: .purple)
                } else {
                    StatusBadge("Doc", systemImage: "doc.text", color: .blue)
                }
            }

            if let summary = document.summary {
                Text(summary)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .lineLimit(2)
                    .multilineTextAlignment(.leading)
            }

            HStack {
                Label("\(document.lineCountAtManifestBuild) lines", systemImage: "text.alignleft")
                    .font(.caption2)
                    .foregroundColor(.secondary)

                Spacer()

                if let state = readingState, state.estimatedProgress > 0 {
                    HStack(spacing: 4) {
                        ProgressView(value: state.estimatedProgress)
                            .frame(width: 50)
                        Text("\(Int(state.estimatedProgress * 100))%")
                            .font(.caption2.bold())
                            .foregroundColor(.secondary)
                    }
                }

                if let state = readingState, state.explicitlyCompleted {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundColor(.green)
                        .font(.caption)
                }
            }
        }
        .padding(14)
        .background(theme.secondaryBackground)
        .cornerRadius(12)
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(theme.separator.opacity(0.3), lineWidth: 1)
        )
    }
}
