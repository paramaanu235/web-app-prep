import SwiftUI
import UIKit

public struct JavaSourceReaderView: View {
    @Environment(\.appTheme) private var theme
    public let code: String
    public let documentTitle: String
    public let initialAnchor: String?
    public var onBookmarkSymbol: ((String, Int) -> Void)?

    @State private var searchQuery: String = ""
    @State private var wrapLines: Bool = false
    @State private var showingSymbolPicker: Bool = false
    @State private var symbols: [(title: String, line: Int)] = []
    @State private var selectedLine: Int? = nil
    @State private var copied: Bool = false

    public init(
        code: String,
        documentTitle: String,
        initialAnchor: String? = nil,
        onBookmarkSymbol: ((String, Int) -> Void)? = nil
    ) {
        self.code = code
        self.documentTitle = documentTitle
        self.initialAnchor = initialAnchor
        self.onBookmarkSymbol = onBookmarkSymbol
    }

    private var lines: [String] {
        code.components(separatedBy: "\n")
    }

    public var body: some View {
        VStack(spacing: 0) {
            // Controls Bar
            HStack(spacing: 12) {
                HStack {
                    Image(systemName: "magnifyingglass")
                        .foregroundColor(.secondary)
                    TextField("Find in Java source...", text: $searchQuery)
                        .font(.subheadline)
                        .autocorrectionDisabled()
                        .textInputAutocapitalization(.never)
                }
                .padding(8)
                .background(theme.tertiaryBackground)
                .cornerRadius(8)

                Button(action: { wrapLines.toggle() }) {
                    Image(systemName: wrapLines ? "text.wrap" : "text.alignleft")
                        .font(.subheadline)
                        .padding(8)
                        .background(wrapLines ? Color.accentColor.opacity(0.15) : theme.tertiaryBackground)
                        .foregroundColor(wrapLines ? .accentColor : .secondary)
                        .cornerRadius(8)
                }

                Button(action: {
                    extractSymbols()
                    showingSymbolPicker = true
                }) {
                    Image(systemName: "list.bullet.indent")
                        .font(.subheadline)
                        .padding(8)
                        .background(theme.tertiaryBackground)
                        .foregroundColor(.accentColor)
                        .cornerRadius(8)
                }

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
                    .font(.caption.bold())
                    .padding(.horizontal, 10)
                    .padding(.vertical, 8)
                    .background(Color.accentColor)
                    .foregroundColor(.white)
                    .cornerRadius(8)
                }
            }
            .padding(.horizontal)
            .padding(.vertical, 8)
            .background(theme.secondaryBackground)
            .overlay(Divider(), alignment: .bottom)

            // Source View with Line Numbers and Syntax Highlighting
            ScrollViewReader { proxy in
                ScrollView([.vertical, .horizontal], showsIndicators: true) {
                    LazyVStack(alignment: .leading, spacing: 1) {
                        ForEach(0..<lines.count, id: \.self) { idx in
                            let line = lines[idx]
                            let lineNum = idx + 1
                            let matchesSearch = !searchQuery.isEmpty && line.localizedCaseInsensitiveContains(searchQuery)
                            let isTargetLine = (selectedLine == lineNum)

                            HStack(alignment: .top, spacing: 10) {
                                Text("\(lineNum)")
                                    .font(.system(size: 11, weight: .regular, design: .monospaced))
                                    .foregroundColor(isTargetLine ? .accentColor : (matchesSearch ? .red : .secondary.opacity(0.6)))
                                    .frame(width: 38, alignment: .trailing)

                                Text(highlightedLine(line))
                                    .font(.system(size: 12.5, design: .monospaced))
                                    .fixedSize(horizontal: !wrapLines, vertical: false)
                            }
                            .id(lineNum)
                            .padding(.vertical, 1)
                            .padding(.horizontal, 4)
                            .background(
                                isTargetLine ? Color.accentColor.opacity(0.18) :
                                (matchesSearch ? Color.yellow.opacity(0.25) : Color.clear)
                            )
                            .cornerRadius(isTargetLine ? 4 : 0)
                        }
                    }
                    .padding(8)
                }
                .onAppear {
                    extractSymbols()
                    scrollToAnchorIfNeeded(proxy: proxy)
                }
                .onChange(of: initialAnchor) { _ in
                    scrollToAnchorIfNeeded(proxy: proxy)
                }
                .sheet(isPresented: $showingSymbolPicker) {
                    NavigationStack {
                        List(symbols, id: \.line) { sym in
                            HStack {
                                Button(action: {
                                    showingSymbolPicker = false
                                    selectedLine = sym.line
                                    withAnimation {
                                        proxy.scrollTo(sym.line, anchor: .center)
                                    }
                                }) {
                                    VStack(alignment: .leading, spacing: 2) {
                                        Text(sym.title)
                                            .font(.subheadline.bold())
                                            .foregroundColor(.primary)
                                        Text("Line \(sym.line)")
                                            .font(.caption2)
                                            .foregroundColor(.secondary)
                                    }
                                }
                                Spacer()
                                Button(action: {
                                    onBookmarkSymbol?(sym.title, sym.line)
                                    showingSymbolPicker = false
                                }) {
                                    Image(systemName: "bookmark")
                                        .foregroundColor(.accentColor)
                                }
                                .buttonStyle(.borderless)
                            }
                        }
                        .themedSurface()
                        .navigationTitle("Symbols & Methods")
                        .navigationBarTitleDisplayMode(.inline)
                        .toolbar {
                            ToolbarItem(placement: .cancellationAction) {
                                Button("Done") { showingSymbolPicker = false }
                            }
                        }
                    }
                }
            }
        }
        .background(theme.background)
    }

    private func scrollToAnchorIfNeeded(proxy: ScrollViewProxy) {
        guard let anchor = initialAnchor, !anchor.isEmpty else { return }
        
        var targetLineNum: Int? = nil
        if let range = anchor.range(of: #"-line-(\d+)$"#, options: .regularExpression) {
            let numStr = String(anchor[range]).replacingOccurrences(of: "-line-", with: "")
            targetLineNum = Int(numStr)
        } else {
            // Check if matches any extracted symbol slug
            for sym in symbols {
                let slug = sym.title.lowercased().replacingOccurrences(of: " ", with: "-")
                if anchor.contains(slug) {
                    targetLineNum = sym.line
                    break
                }
            }
        }

        if let line = targetLineNum, line > 0 && line <= lines.count {
            self.selectedLine = line
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
                withAnimation {
                    proxy.scrollTo(line, anchor: .center)
                }
            }
        }
    }

    private func extractSymbols() {
        var found: [(title: String, line: Int)] = []
        for (i, line) in lines.enumerated() {
            let t = line.trimmingCharacters(in: .whitespaces)
            if t.contains("class ") || t.contains("interface ") || t.contains("record ") {
                let name = t.components(separatedBy: "{").first?.trimmingCharacters(in: .whitespaces) ?? t
                found.append((title: name, line: i + 1))
            } else if t.hasPrefix("public ") && t.contains("(") && t.contains(")") {
                let name = t.components(separatedBy: "{").first?.trimmingCharacters(in: .whitespaces) ?? t
                found.append((title: name, line: i + 1))
            } else if t.contains("@Test") {
                found.append((title: t, line: i + 1))
            }
        }
        self.symbols = found
    }

    // Native AttributedString syntax highlighting for Java
    private func highlightedLine(_ line: String) -> AttributedString {
        var attr = AttributedString(line)
        let keywords: Set<String> = [
            "abstract","assert","boolean","break","byte","case","catch","char","class","const","continue",
            "default","do","double","else","enum","extends","final","finally","float","for","goto","if",
            "implements","import","instanceof","int","interface","long","native","new","package","private",
            "protected","public","return","short","static","strictfp","super","switch","synchronized","this",
            "throw","throws","transient","try","void","volatile","while","record","sealed","permits","var","yield"
        ]

        let trimmed = line.trimmingCharacters(in: .whitespaces)
        // Full-line or trailing comments
        if let range = line.range(of: "//") {
            let commentStart = line.distance(from: line.startIndex, to: range.lowerBound)
            if let attrRange = Range(NSRange(location: commentStart, length: line.count - commentStart), in: attr) {
                attr[attrRange].foregroundColor = .gray
                attr[attrRange].font = .system(size: 12.5, weight: .regular, design: .monospaced).italic()
            }
        }

        // Annotations
        if trimmed.hasPrefix("@") {
            attr.foregroundColor = .orange
            return attr
        }

        // Word tokens
        let words = line.components(separatedBy: CharacterSet.alphanumerics.inverted)
        for word in words where !word.isEmpty {
            if keywords.contains(word) {
                if let r = attr.range(of: word) {
                    attr[r].foregroundColor = .purple
                    attr[r].font = .system(size: 12.5, weight: .bold, design: .monospaced)
                }
            } else if word.first?.isUppercase == true && word.count > 1 {
                if let r = attr.range(of: word) {
                    attr[r].foregroundColor = .teal
                }
            }
        }

        return attr
    }
}
