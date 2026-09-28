import SwiftUI

public struct TableOfContentsDrawer: View {
    public let sections: [SearchIndexEntry]
    public let onSelect: (SearchIndexEntry) -> Void
    @Environment(\.dismiss) private var dismiss

    public init(sections: [SearchIndexEntry], onSelect: @escaping (SearchIndexEntry) -> Void) {
        self.sections = sections
        self.onSelect = onSelect
    }

    public var body: some View {
        NavigationStack {
            List(sections) { sec in
                Button(action: {
                    onSelect(sec)
                    dismiss()
                }) {
                    HStack(spacing: 8) {
                        if sec.headingLevel > 1 {
                            Rectangle()
                                .fill(Color.clear)
                                .frame(width: CGFloat((sec.headingLevel - 1) * 16), height: 1)
                        }
                        Text(sec.title)
                            .font(sec.headingLevel == 1 ? .headline : .subheadline)
                            .foregroundColor(sec.headingLevel == 1 ? .primary : .secondary)
                            .multilineTextAlignment(.leading)
                        Spacer()
                    }
                    .padding(.vertical, 2)
                }
                .buttonStyle(.plain)
            }
            .themedSurface()
            .navigationTitle("Table of Contents")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }
}
