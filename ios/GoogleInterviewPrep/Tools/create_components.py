import os

comp_dir = "ios/GoogleInterviewPrep/GoogleInterviewPrep/Components"
os.makedirs(comp_dir, exist_ok=True)

# 1. StatusBadge.swift
badge_code = """import SwiftUI

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
"""

with open(f"{comp_dir}/StatusBadge.swift", "w", encoding="utf-8") as f:
    f.write(badge_code.strip())
print("Wrote StatusBadge.swift")

# 2. DocumentCard.swift
card_code = """import SwiftUI

public struct DocumentCard: View {
    public let document: ContentDocument
    public let readingState: ReadingState?
    public let action: () -> Void

    public init(document: ContentDocument, readingState: ReadingState? = nil, action: @escaping () -> Void) {
        self.document = document
        self.readingState = readingState
        self.action = action
    }

    public var body: some View {
        Button(action: action) {
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
            .background(Color(uiColor: .secondarySystemGroupedBackground))
            .cornerRadius(12)
            .overlay(
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color(uiColor: .separator).opacity(0.3), lineWidth: 1)
            )
        }
        .buttonStyle(.plain)
    }
}
"""

with open(f"{comp_dir}/DocumentCard.swift", "w", encoding="utf-8") as f:
    f.write(card_code.strip())
print("Wrote DocumentCard.swift")

# 3. EmptyStateView.swift
empty_code = """import SwiftUI

public struct EmptyStateView: View {
    public let icon: String
    public let title: String
    public let message: String
    public let actionTitle: String?
    public let action: (() -> Void)?

    public init(
        icon: String,
        title: String,
        message: String,
        actionTitle: String? = nil,
        action: (() -> Void)? = nil
    ) {
        self.icon = icon
        self.title = title
        self.message = message
        self.actionTitle = actionTitle
        self.action = action
    }

    public var body: some View {
        VStack(spacing: 12) {
            Image(systemName: icon)
                .font(.system(size: 44))
                .foregroundColor(.secondary)
            Text(title)
                .font(.headline)
            Text(message)
                .font(.subheadline)
                .foregroundColor(.secondary)
                .multilineTextAlignment(.center)
                .padding(.horizontal, 32)

            if let actionTitle = actionTitle, let action = action {
                Button(action: action) {
                    Text(actionTitle)
                        .font(.subheadline.bold())
                        .padding(.horizontal, 16)
                        .padding(.vertical, 8)
                        .background(Color.accentColor)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
                .padding(.top, 8)
            }
        }
        .padding(24)
        .frame(maxWidth: .infinity, maxHeight: .infinity)
    }
}
"""

with open(f"{comp_dir}/EmptyStateView.swift", "w", encoding="utf-8") as f:
    f.write(empty_code.strip())
print("Wrote EmptyStateView.swift")

# 4. CodeBlockView.swift
code_view = """import SwiftUI
import UIKit

public struct CodeBlockView: View {
    public let code: String
    public let language: String?
    @State private var copied: Bool = false

    public init(code: String, language: String? = nil) {
        self.code = code
        self.language = language
    }

    public var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            HStack {
                Text(language?.uppercased() ?? "CODE")
                    .font(.caption2.bold())
                    .foregroundColor(.secondary)
                Spacer()
                Button(action: {
                    UIPasteboard.general.string = code
                    copied = true
                    DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
                        copied = false
                    }
                }) {
                    HStack(spacing: 4) {
                        Image(systemName: copied ? "checkmark" : "doc.on.doc")
                        Text(copied ? "Copied" : "Copy")
                    }
                    .font(.caption2.bold())
                    .foregroundColor(.accentColor)
                }
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 6)
            .background(Color(uiColor: .tertiarySystemGroupedBackground))

            ScrollView(.horizontal, showsIndicators: true) {
                Text(code)
                    .font(.system(.caption, design: .monospaced))
                    .padding(12)
                    .foregroundColor(.primary)
            }
        }
        .background(Color(uiColor: .secondarySystemGroupedBackground))
        .cornerRadius(8)
        .overlay(
            RoundedRectangle(cornerRadius: 8)
                .stroke(Color(uiColor: .separator).opacity(0.4), lineWidth: 1)
        )
    }
}
"""

with open(f"{comp_dir}/CodeBlockView.swift", "w", encoding="utf-8") as f:
    f.write(code_view.strip())
print("Wrote CodeBlockView.swift")
