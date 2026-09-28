import SwiftUI
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

    @MainActor
    public final class Coordinator: NSObject, WKNavigationDelegate, WKScriptMessageHandler {
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

        public func webView(
            _ webView: WKWebView,
            decidePolicyFor navigationAction: WKNavigationAction,
            decisionHandler: @escaping @MainActor @Sendable (WKNavigationActionPolicy) -> Void
        ) {
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