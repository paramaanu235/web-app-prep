import SwiftUI

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