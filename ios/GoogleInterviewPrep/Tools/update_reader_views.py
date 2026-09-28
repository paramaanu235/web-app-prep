import os

reader_dir = "ios/GoogleInterviewPrep/GoogleInterviewPrep/Features/Reader"

# 1. JavaSourceReaderView.swift
java_code = r"""import SwiftUI
import UIKit

public struct JavaSourceReaderView: View {
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
                .background(Color(uiColor: .tertiarySystemGroupedBackground))
                .cornerRadius(8)

                Button(action: { wrapLines.toggle() }) {
                    Image(systemName: wrapLines ? "text.wrap" : "text.alignleft")
                        .font(.subheadline)
                        .padding(8)
                        .background(wrapLines ? Color.accentColor.opacity(0.15) : Color(uiColor: .tertiarySystemGroupedBackground))
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
                        .background(Color(uiColor: .tertiarySystemGroupedBackground))
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
            .background(Color(uiColor: .secondarySystemGroupedBackground))
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
        .background(Color(uiColor: .systemBackground))
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
"""

with open(f"{reader_dir}/JavaSourceReaderView.swift", "w", encoding="utf-8") as f:
    f.write(java_code.strip())
print("Updated JavaSourceReaderView.swift with line navigation, syntax highlighting, and symbol bookmarking")

# 2. MarkdownWebView.swift
md_web_code = r"""import SwiftUI
import WebKit

public struct MarkdownWebView: UIViewRepresentable {
    public let markdown: String
    public let documentID: String
    public let isHistorical: Bool
    public let theme: String
    public let bodyFontSize: Double
    public let codeFontSize: Double
    public let scrollAnchor: String?
    public let onCopyCode: ((String) -> Void)?
    public let onOpenExternalURL: ((URL) -> Void)?

    public init(
        markdown: String,
        documentID: String,
        isHistorical: Bool,
        theme: String,
        bodyFontSize: Double = 16.0,
        codeFontSize: Double = 13.5,
        scrollAnchor: String? = nil,
        onCopyCode: ((String) -> Void)? = nil,
        onOpenExternalURL: ((URL) -> Void)? = nil
    ) {
        self.markdown = markdown
        self.documentID = documentID
        self.isHistorical = isHistorical
        self.theme = theme
        self.bodyFontSize = bodyFontSize
        self.codeFontSize = codeFontSize
        self.scrollAnchor = scrollAnchor
        self.onCopyCode = onCopyCode
        self.onOpenExternalURL = onOpenExternalURL
    }

    public func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }

    public func makeUIView(context: Context) -> WKWebView {
        let contentController = WKUserContentController()
        contentController.add(context.coordinator, name: "copyCode")
        contentController.add(context.coordinator, name: "openExternalUrl")

        let config = WKWebViewConfiguration()
        config.userContentController = contentController

        let webView = WKWebView(frame: .zero, configuration: config)
        webView.navigationDelegate = context.coordinator
        webView.isOpaque = false
        webView.backgroundColor = .clear
        webView.scrollView.backgroundColor = .clear

        context.coordinator.webView = webView
        loadLocalHTML(into: webView)
        return webView
    }

    public func updateUIView(_ uiView: WKWebView, context: Context) {
        context.coordinator.parent = self
        if context.coordinator.isPageLoaded {
            if context.coordinator.lastRenderedMarkdown != markdown {
                context.coordinator.renderContent()
            }
            context.coordinator.applyThemeAndPreferences()
            if let anchor = scrollAnchor, !anchor.isEmpty {
                context.coordinator.scrollToAnchor(anchor)
            }
        }
    }

    private func loadLocalHTML(into webView: WKWebView) {
        if let htmlURL = Bundle.main.url(forResource: "reader", withExtension: "html") ??
                         Bundle.main.url(forResource: "reader", withExtension: "html", subdirectory: "Web") {
            let webDir = htmlURL.deletingLastPathComponent()
            webView.loadFileURL(htmlURL, allowingReadAccessTo: webDir)
        }
    }

    public class Coordinator: NSObject, WKNavigationDelegate, WKScriptMessageHandler {
        var parent: MarkdownWebView
        weak var webView: WKWebView?
        var isPageLoaded: Bool = false
        var lastRenderedMarkdown: String = ""

        init(_ parent: MarkdownWebView) {
            self.parent = parent
        }

        public func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
            isPageLoaded = true
            renderContent()
            applyThemeAndPreferences()
            if let anchor = parent.scrollAnchor, !anchor.isEmpty {
                scrollToAnchor(anchor)
            }
        }

        func renderContent() {
            guard let wv = webView, !parent.markdown.isEmpty else { return }
            lastRenderedMarkdown = parent.markdown
            let encoder = JSONEncoder()
            guard let mdData = try? encoder.encode(parent.markdown),
                  let jsonMD = String(data: mdData, encoding: .utf8) else { return }

            let js = "renderDocument(\(jsonMD), '\(parent.documentID)', \(parent.isHistorical));"
            wv.evaluateJavaScript(js, completionHandler: nil)
        }

        func applyThemeAndPreferences() {
            guard let wv = webView else { return }
            let js = "applyPreferences('\(parent.theme)', \(parent.bodyFontSize), \(parent.codeFontSize));"
            wv.evaluateJavaScript(js, completionHandler: nil)
        }

        func scrollToAnchor(_ anchor: String) {
            guard let wv = webView else { return }
            let js = "scrollToAnchor('\(anchor)');"
            wv.evaluateJavaScript(js, completionHandler: nil)
        }

        public func userContentController(_ userContentController: WKUserContentController, didReceive message: WKScriptMessage) {
            if message.name == "copyCode", let text = message.body as? String {
                UIPasteboard.general.string = text
                parent.onCopyCode?(text)
            } else if message.name == "openExternalUrl", let urlString = message.body as? String, let url = URL(string: urlString) {
                parent.onOpenExternalURL?(url)
            }
        }

        public func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
            if navigationAction.navigationType == .linkActivated {
                if let url = navigationAction.request.url {
                    parent.onOpenExternalURL?(url)
                }
                decisionHandler(.cancel)
                return
            }
            decisionHandler(.allow)
        }
    }
}
"""

with open(f"{reader_dir}/MarkdownWebView.swift", "w", encoding="utf-8") as f:
    f.write(md_web_code.strip())
print("Updated MarkdownWebView.swift with dynamic re-render on markdown update")

# 3. DocumentReaderView.swift
doc_reader_code = r"""import SwiftUI

public struct DocumentReaderView: View {
    public let document: ContentDocument
    public let initialAnchor: String?

    @EnvironmentObject private var env: AppEnvironment
    @EnvironmentObject private var stateStore: StudyStateStore

    @State private var scrollAnchor: String?
    @State private var showingTOC: Bool = false
    @State private var showingAddBookmark: Bool = false
    @State private var bookmarkTitle: String = ""
    @State private var bookmarkNote: String = ""
    @State private var showingExternalLinkAlert: Bool = false
    @State private var pendingExternalURL: URL? = nil
    @State private var contentString: String

    public init(document: ContentDocument, initialAnchor: String? = nil, repository: ContentRepository = ContentRepository()) {
        self.document = document
        self.initialAnchor = initialAnchor
        let preloaded = repository.content(for: document) ?? ""
        _contentString = State(initialValue: preloaded)
    }

    private var documentSections: [SearchIndexEntry] {
        env.repository.searchIndex.entries.filter { $0.documentID == document.id }
    }

    private var isCompleted: Bool {
        stateStore.readingState(for: document.id).explicitlyCompleted
    }

    public var body: some View {
        VStack(spacing: 0) {
            // Historical Badge Banner if applicable
            if document.isHistorical {
                HStack {
                    Image(systemName: "exclamationmark.triangle.fill")
                        .foregroundColor(.orange)
                    Text("Historical Review / Archival — do not treat as current truth")
                        .font(.caption.bold())
                        .foregroundColor(.orange)
                    Spacer()
                }
                .padding(.horizontal)
                .padding(.vertical, 6)
                .background(Color.orange.opacity(0.12))
            }

            // Reader Body
            if document.format == .java {
                JavaSourceReaderView(
                    code: contentString,
                    documentTitle: document.title,
                    initialAnchor: scrollAnchor,
                    onBookmarkSymbol: { symTitle, lineNum in
                        stateStore.addBookmark(
                            documentID: document.id,
                            sectionID: "\(document.id)-line-\(lineNum)",
                            title: symTitle,
                            note: "Bookmarked from Java symbol list (Line \(lineNum))"
                        )
                    }
                )
            } else {
                MarkdownWebView(
                    markdown: contentString,
                    documentID: document.id,
                    isHistorical: document.isHistorical,
                    theme: stateStore.state.themePreference,
                    bodyFontSize: stateStore.state.bodyFontSize,
                    codeFontSize: stateStore.state.codeFontSize,
                    scrollAnchor: scrollAnchor,
                    onOpenExternalURL: { url in
                        pendingExternalURL = url
                        showingExternalLinkAlert = true
                    }
                )
            }
        }
        .navigationTitle(document.title)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItemGroup(placement: .navigationBarTrailing) {
                Button(action: { showingTOC = true }) {
                    Image(systemName: "list.bullet")
                }

                Button(action: {
                    bookmarkTitle = document.title
                    bookmarkNote = ""
                    showingAddBookmark = true
                }) {
                    Image(systemName: "bookmark")
                }

                Button(action: {
                    stateStore.toggleExplicitCompletion(documentID: document.id)
                }) {
                    Image(systemName: isCompleted ? "checkmark.circle.fill" : "circle")
                        .foregroundColor(isCompleted ? .green : .secondary)
                }
            }
        }
        .sheet(isPresented: $showingTOC) {
            TableOfContentsDrawer(sections: documentSections) { sec in
                self.scrollAnchor = sec.anchor
                stateStore.updateReadingPosition(
                    documentID: document.id,
                    sectionID: sec.sectionID,
                    anchor: sec.anchor,
                    estimatedProgress: 0.5
                )
            }
        }
        .sheet(isPresented: $showingAddBookmark) {
            NavigationStack {
                Form {
                    Section("Bookmark Details") {
                        TextField("Title", text: $bookmarkTitle)
                        TextField("Notes / Takeaways", text: $bookmarkNote, axis: .vertical)
                            .lineLimit(3...6)
                    }
                }
                .navigationTitle("Add Bookmark")
                .navigationBarTitleDisplayMode(.inline)
                .toolbar {
                    ToolbarItem(placement: .cancellationAction) {
                        Button("Cancel") { showingAddBookmark = false }
                    }
                    ToolbarItem(placement: .confirmationAction) {
                        Button("Save") {
                            stateStore.addBookmark(
                                documentID: document.id,
                                sectionID: scrollAnchor,
                                title: bookmarkTitle.isEmpty ? document.title : bookmarkTitle,
                                note: bookmarkNote
                            )
                            showingAddBookmark = false
                        }
                    }
                }
            }
        }
        .alert("Open External Link?", isPresented: $showingExternalLinkAlert) {
            Button("Cancel", role: .cancel) {}
            Button("Open in Safari") {
                if let url = pendingExternalURL {
                    UIApplication.shared.open(url)
                }
            }
        } message: {
            if let url = pendingExternalURL {
                Text("This link opens in Safari:\n\(url.absoluteString)")
            }
        }
        .onAppear {
            if contentString.isEmpty, let loaded = env.repository.content(for: document) {
                self.contentString = loaded
            }
            if let initAnchor = initialAnchor {
                self.scrollAnchor = initAnchor
            } else {
                let saved = stateStore.readingState(for: document.id)
                self.scrollAnchor = saved.scrollAnchor
            }
            stateStore.updateReadingPosition(
                documentID: document.id,
                sectionID: scrollAnchor,
                anchor: scrollAnchor,
                estimatedProgress: 0.1
            )
        }
        .onDisappear {
            stateStore.updateReadingPosition(
                documentID: document.id,
                sectionID: scrollAnchor,
                anchor: scrollAnchor,
                estimatedProgress: 0.3
            )
        }
    }
}
"""

with open(f"{reader_dir}/DocumentReaderView.swift", "w", encoding="utf-8") as f:
    f.write(doc_reader_code.strip())
print("Updated DocumentReaderView.swift with synchronous content preloading and anchor propagation to Java reader")
