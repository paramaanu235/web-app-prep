import SwiftUI

public struct StatusBadge: View {
    public let text: String
    public let systemImage: String?
    public let color: Color

    public init(_ text: String, systemImage: String? = nil, color: Color = .blue) {
        self.text = text
        self.systemImage = systemImage
        self.color = color
    }

    public var body: some View {
        HStack(spacing: 4) {
            if let img = systemImage {
                Image(systemName: img)
                    .font(.caption2.bold())
            }
            Text(text)
                .font(.caption2.bold())
        }
        .padding(.horizontal, 8)
        .padding(.vertical, 3)
        .background(color.opacity(0.15))
        .foregroundColor(color)
        .clipShape(Capsule())
    }
}

public struct HistoricalBadge: View {
    public init() {}

    public var body: some View {
        StatusBadge("Historical Archive", systemImage: "clock.arrow.circlepath", color: .orange)
    }
}