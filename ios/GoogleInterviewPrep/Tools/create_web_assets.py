import os

web_dir = "ios/GoogleInterviewPrep/GoogleInterviewPrep/Resources/Web"
os.makedirs(web_dir, exist_ok=True)

css_content = """
:root {
  --bg-color: #ffffff;
  --text-color: #1c1c1e;
  --secondary-text: #6e6e73;
  --border-color: #e5e5ea;
  --code-bg: #f2f2f7;
  --code-text: #1c1c1e;
  --inline-code-bg: #e5e5ea;
  --accent-color: #007aff;
  --table-stripe: #f9f9fb;
  --table-header: #f2f2f7;
  --blockquote-border: #007aff;
  --blockquote-bg: #f2f2f7;
  --body-font-size: 16px;
  --code-font-size: 13.5px;
  --line-height: 1.6;
}

[data-theme="dark"] {
  --bg-color: #000000;
  --text-color: #f2f2f7;
  --secondary-text: #8e8e93;
  --border-color: #38383a;
  --code-bg: #1c1c1e;
  --code-text: #f2f2f7;
  --inline-code-bg: #2c2c2e;
  --accent-color: #0a84ff;
  --table-stripe: #1c1c1e;
  --table-header: #2c2c2e;
  --blockquote-border: #0a84ff;
  --blockquote-bg: #1c1c1e;
}

@media (prefers-color-scheme: dark) {
  [data-theme="system"] {
    --bg-color: #000000;
    --text-color: #f2f2f7;
    --secondary-text: #8e8e93;
    --border-color: #38383a;
    --code-bg: #1c1c1e;
    --code-text: #f2f2f7;
    --inline-code-bg: #2c2c2e;
    --accent-color: #0a84ff;
    --table-stripe: #1c1c1e;
    --table-header: #2c2c2e;
    --blockquote-border: #0a84ff;
    --blockquote-bg: #1c1c1e;
  }
}

[data-theme="sepia"] {
  --bg-color: #f3ead2;
  --text-color: #3f3024;
  --secondary-text: #75604b;
  --border-color: #c9b48f;
  --code-bg: #e5d5b5;
  --code-text: #33261c;
  --inline-code-bg: #dfcba7;
  --accent-color: #7a4a21;
  --table-stripe: #eee0c4;
  --table-header: #e5d5b5;
  --blockquote-border: #9a6330;
  --blockquote-bg: #eadbbc;
}

* {
  box-sizing: border-box;
  -webkit-tap-highlight-color: transparent;
}

body {
  margin: 0;
  padding: 16px 16px 60px 16px;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
  font-size: var(--body-font-size);
  line-height: var(--line-height);
  color: var(--text-color);
  background-color: var(--bg-color);
  word-wrap: break-word;
}

h1, h2, h3, h4 {
  color: var(--text-color);
  font-weight: 700;
  line-height: 1.3;
  scroll-margin-top: 20px;
}

h1 { font-size: 1.65em; margin: 1.4em 0 0.6em 0; border-bottom: 1px solid var(--border-color); padding-bottom: 8px; }
h2 { font-size: 1.35em; margin: 1.3em 0 0.5em 0; border-bottom: 1px solid var(--border-color); padding-bottom: 6px; }
h3 { font-size: 1.15em; margin: 1.2em 0 0.4em 0; }
h4 { font-size: 1.0em; margin: 1.1em 0 0.3em 0; }

p {
  margin: 0.8em 0;
}

a {
  color: var(--accent-color);
  text-decoration: none;
}

a:hover, a:active {
  text-decoration: underline;
}

.table-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  margin: 1.2em 0;
  border: 1px solid var(--border-color);
  border-radius: 8px;
}

table {
  border-collapse: collapse;
  width: 100%;
  font-size: 0.9em;
  min-width: 320px;
}

th, td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
  vertical-align: top;
}

th {
  background-color: var(--table-header);
  font-weight: 600;
}

tr:nth-child(even) td {
  background-color: var(--table-stripe);
}

code {
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.9em;
  background-color: var(--inline-code-bg);
  padding: 2px 5px;
  border-radius: 4px;
}

.code-card {
  margin: 1.2em 0;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background-color: var(--code-bg);
  overflow: hidden;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 12px;
  background: rgba(128, 128, 128, 0.08);
  font-size: 12px;
  font-weight: 600;
  color: var(--secondary-text);
  border-bottom: 1px solid var(--border-color);
}

.code-actions {
  display: flex;
  gap: 8px;
}

.code-btn {
  background: none;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  color: var(--accent-color);
  font-size: 11px;
  padding: 3px 8px;
  cursor: pointer;
}

.code-btn:active {
  opacity: 0.7;
}

.code-scroll-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  padding: 12px;
  margin: 0;
}

.code-scroll-container pre {
  margin: 0;
  padding: 0;
  font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  font-size: var(--code-font-size);
  line-height: 1.45;
  color: var(--code-text);
}

.code-scroll-container.wrap pre {
  white-space: pre-wrap;
  word-break: break-word;
}

blockquote {
  margin: 1.2em 0;
  padding: 8px 16px;
  border-left: 4px solid var(--blockquote-border);
  background-color: var(--blockquote-bg);
  border-radius: 0 8px 8px 0;
  color: var(--secondary-text);
}

blockquote p {
  margin: 0.4em 0;
}

ul, ol {
  padding-left: 24px;
  margin: 0.8em 0;
}

li {
  margin: 0.4em 0;
}

hr {
  border: none;
  border-top: 1px solid var(--border-color);
  margin: 2em 0;
}

.task-list-item {
  list-style-type: none;
  margin-left: -20px;
}

.historical-badge {
  display: inline-block;
  background-color: #ff9500;
  color: #ffffff;
  font-size: 11px;
  font-weight: bold;
  padding: 4px 10px;
  border-radius: 12px;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Syntax Highlighting */
.hl-keyword { color: #d73a49; font-weight: 600; }
.hl-type { color: #6f42c1; }
.hl-string { color: #032f62; }
.hl-comment { color: #6a737d; font-style: italic; }
.hl-number { color: #005cc5; }
.hl-annotation { color: #e36209; font-weight: 500; }
.hl-builtin { color: #005cc5; }

[data-theme="dark"] .hl-keyword { color: #ff7b72; font-weight: 600; }
[data-theme="dark"] .hl-type { color: #d2a8ff; }
[data-theme="dark"] .hl-string { color: #a5d6ff; }
[data-theme="dark"] .hl-comment { color: #8b949e; font-style: italic; }
[data-theme="dark"] .hl-number { color: #79c0ff; }
[data-theme="dark"] .hl-annotation { color: #ffa657; font-weight: 500; }
[data-theme="dark"] .hl-builtin { color: #79c0ff; }

[data-theme="sepia"] .hl-keyword { color: #8f2d2d; font-weight: 600; }
[data-theme="sepia"] .hl-type { color: #68458f; }
[data-theme="sepia"] .hl-string { color: #315d4a; }
[data-theme="sepia"] .hl-comment { color: #766854; font-style: italic; }
[data-theme="sepia"] .hl-number { color: #1f5b78; }
[data-theme="sepia"] .hl-annotation { color: #934f18; font-weight: 500; }
[data-theme="sepia"] .hl-builtin { color: #1f5b78; }
"""

with open(f"{web_dir}/reader.css", "w", encoding="utf-8") as f:
    f.write(css_content.strip())
print("Wrote reader.css")

hl_js = """
window.SyntaxHighlighter = (function() {
  const javaKeywords = new Set([
    'abstract','assert','boolean','break','byte','case','catch','char','class','const','continue',
    'default','do','double','else','enum','extends','final','finally','float','for','goto','if',
    'implements','import','instanceof','int','interface','long','native','new','package','private',
    'protected','public','return','short','static','strictfp','super','switch','synchronized','this',
    'throw','throws','transient','try','void','volatile','while','record','sealed','permits','non-sealed','var','yield'
  ]);

  const pythonKeywords = new Set([
    'and','as','assert','async','await','break','class','continue','def','del','elif','else','except',
    'finally','for','from','global','if','import','in','is','lambda','nonlocal','not','or','pass',
    'raise','return','try','while','with','yield','True','False','None','match','case'
  ]);

  function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function highlight(code, lang) {
    const language = (lang || "").toLowerCase();
    const lines = code.split('\\n');
    const highlightedLines = lines.map(line => {
      let l = escapeHtml(line);
      if (language === 'python' && l.includes('#')) {
        const parts = l.split('#');
        const codePart = highlightTokens(parts[0], pythonKeywords, true);
        return codePart + '<span class="hl-comment">#' + parts.slice(1).join('#') + '</span>';
      }
      if ((language === 'java' || language === 'cpp' || language === 'javascript') && l.includes('//')) {
        const idx = l.indexOf('//');
        const codePart = highlightTokens(l.substring(0, idx), javaKeywords, false);
        return codePart + '<span class="hl-comment">' + l.substring(idx) + '</span>';
      }
      if (l.trim().startsWith('@')) {
        return '<span class="hl-annotation">' + l + '</span>';
      }
      const keywords = language === 'python' ? pythonKeywords : javaKeywords;
      return highlightTokens(l, keywords, language === 'python');
    });
    return highlightedLines.join('\\n');
  }

  function highlightTokens(str, keywords, isPython) {
    str = str.replace(/(&quot;.*?&quot;|&#39;.*?&#39;|".*?"|\'[^\']*\')/g, '<span class="hl-string">$1</span>');
    str = str.replace(/\\b(\\d+(\\.\\d+)?)\\b/g, '<span class="hl-number">$1</span>');
    str = str.replace(/\\b([a-zA-Z_][a-zA-Z0-9_]*)\\b/g, function(match, token) {
      if (keywords.has(token)) {
        return '<span class="hl-keyword">' + token + '</span>';
      }
      if (/^[A-Z][a-zA-Z0-9_]*$/.test(token)) {
        return '<span class="hl-type">' + token + '</span>';
      }
      return token;
    });
    return str;
  }

  return { highlight: highlight, escapeHtml: escapeHtml };
})();
"""

with open(f"{web_dir}/syntax-highlighter.min.js", "w", encoding="utf-8") as f:
    f.write(hl_js.strip())
print("Wrote syntax-highlighter.min.js")

md_js = """
window.MarkdownRenderer = (function() {
  function render(markdown, docID) {
    const lines = markdown.split('\\n');
    let html = [];
    let inCode = false;
    let codeLines = [];
    let codeLang = '';
    let codeBlockIdx = 0;
    let inTable = false;
    let tableLines = [];
    let inList = false;
    let listType = 'ul';

    function slugify(text) {
      return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'section';
    }

    function flushList() {
      if (inList) {
        html.push('</' + listType + '>');
        inList = false;
      }
    }

    function flushTable() {
      if (!inTable) return;
      inTable = false;
      if (tableLines.length === 0) return;
      let tHtml = ['<div class="table-container"><table>'];
      let headerProcessed = false;
      for (let i = 0; i < tableLines.length; i++) {
        let row = tableLines[i].trim();
        if (row.startsWith('|')) row = row.substring(1);
        if (row.endsWith('|')) row = row.substring(0, row.length - 1);
        let cells = row.split('|').map(c => c.trim());
        if (i === 1 && cells.every(c => /^:?-+:?$/.test(c))) {
          headerProcessed = true;
          continue;
        }
        if (!headerProcessed && i === 0) {
          tHtml.push('<thead><tr>');
          cells.forEach(c => tHtml.push('<th>' + parseInline(c) + '</th>'));
          tHtml.push('</tr></thead><tbody>');
        } else {
          tHtml.push('<tr>');
          cells.forEach(c => tHtml.push('<td>' + parseInline(c) + '</td>'));
          tHtml.push('</tr>');
        }
      }
      tHtml.push('</tbody></table></div>');
      html.push(tHtml.join(''));
      tableLines = [];
    }

    function parseInline(text) {
      if (!text) return '';
      let s = SyntaxHighlighter.escapeHtml(text);
      s = s.replace(/\\[([^\\]]+)\\]\\(([^\\)]+)\\)/g, function(m, label, url) {
        if (url.startsWith('http://') || url.startsWith('https://')) {
          return '<a href="' + url + '" class="external-link" target="_blank">' + label + '</a>';
        }
        return '<span class="internal-link">' + label + '</span>';
      });
      s = s.replace(/\\*\\*\\*(.*?)\\*\\*\\*/g, '<strong><em>$1</em></strong>');
      s = s.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
      s = s.replace(/\\*(.*?)\\*/g, '<em>$1</em>');
      s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
      return s;
    }

    let headingCounts = {};

    for (let i = 0; i < lines.length; i++) {
      let line = lines[i];
      let trimmed = line.trim();

      if (trimmed.startsWith('```') || trimmed.startsWith('~~~')) {
        flushTable();
        flushList();
        if (inCode) {
          inCode = false;
          codeBlockIdx++;
          const rawCode = codeLines.join('\\n');
          const highlighted = SyntaxHighlighter.highlight(rawCode, codeLang);
          const blockId = docID + '-code-' + codeBlockIdx;
          const safeRaw = encodeURIComponent(rawCode);
          html.push('<div class="code-card" id="' + blockId + '">');
          html.push('  <div class="code-header">');
          html.push('    <span>' + (codeLang || 'CODE') + '</span>');
          html.push('    <div class="code-actions">');
          html.push('      <button class="code-btn" onclick="toggleWrap(\\'' + blockId + '\\')">Wrap</button>');
          html.push('      <button class="code-btn" onclick="copyCode(\\'' + safeRaw + '\\', this)">Copy</button>');
          html.push('    </div>');
          html.push('  </div>');
          html.push('  <div class="code-scroll-container">');
          html.push('    <pre><code>' + highlighted + '</code></pre>');
          html.push('  </div>');
          html.push('</div>');
          codeLines = [];
          codeLang = '';
        } else {
          inCode = true;
          codeLang = trimmed.substring(3).trim();
          codeLines = [];
        }
        continue;
      }

      if (inCode) {
        codeLines.push(line);
        continue;
      }

      if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
        flushList();
        inTable = true;
        tableLines.push(trimmed);
        continue;
      } else if (inTable) {
        flushTable();
      }

      if (/^(---|\\*\\*\\*|___)$/.test(trimmed)) {
        flushList();
        html.push('<hr />');
        continue;
      }

      let headingMatch = trimmed.match(/^(#{1,4})\\s+(.*)$/);
      let boldHeadingMatch = (!headingMatch && /^\\*\\*[0-9]\\.\\s+(.*?)\\*\\*:?$/.test(trimmed)) ? trimmed.match(/^\\*\\*([0-9]\\.\\s+.*?)\\*\\*:?$/) : null;
      let gateHeadingMatch = (!headingMatch && !boldHeadingMatch && /^\\*\\*(Phase-two gate|Final readiness gate).*?\\*\\*:?$/.test(trimmed)) ? trimmed.match(/^\\*\\*(.*?)\\*\\*:?$/) : null;

      if (headingMatch || boldHeadingMatch || gateHeadingMatch) {
        flushList();
        let level = 2;
        let title = '';
        if (headingMatch) {
          level = headingMatch[1].length;
          title = headingMatch[2];
        } else if (boldHeadingMatch) {
          level = 2;
          title = boldHeadingMatch[1];
        } else if (gateHeadingMatch) {
          level = 3;
          title = gateHeadingMatch[1];
        }
        let baseSlug = slugify(title);
        let count = (headingCounts[baseSlug] || 0) + 1;
        headingCounts[baseSlug] = count;
        let slug = count === 1 ? baseSlug : baseSlug + '-' + count;
        let anchor = docID + '-' + slug;
        html.push('<h' + level + ' id="' + anchor + '">' + parseInline(title) + '</h' + level + '>');
        continue;
      }

      let ulMatch = trimmed.match(/^[-*+]\\s+(.*)$/);
      let olMatch = trimmed.match(/^(\\d+)\\.\\s+(.*)$/);
      if (ulMatch || olMatch) {
        let currentType = ulMatch ? 'ul' : 'ol';
        let content = ulMatch ? ulMatch[1] : olMatch[2];
        if (!inList || listType !== currentType) {
          flushList();
          inList = true;
          listType = currentType;
          html.push('<' + listType + '>');
        }
        if (content.startsWith('[ ] ') || content.startsWith('[x] ')) {
          let checked = content.startsWith('[x] ');
          html.push('<li class="task-list-item"><input type="checkbox" disabled ' + (checked ? 'checked' : '') + ' /> ' + parseInline(content.substring(4)) + '</li>');
        } else {
          html.push('<li>' + parseInline(content) + '</li>');
        }
        continue;
      } else {
        flushList();
      }

      if (trimmed.startsWith('>')) {
        let bqContent = trimmed.substring(1).trim();
        html.push('<blockquote><p>' + parseInline(bqContent) + '</p></blockquote>');
        continue;
      }

      if (trimmed.length > 0) {
        html.push('<p>' + parseInline(trimmed) + '</p>');
      }
    }

    flushTable();
    flushList();
    return html.join('\\n');
  }

  return { render: render };
})();
"""

with open(f"{web_dir}/markdown-renderer.min.js", "w", encoding="utf-8") as f:
    f.write(md_js.strip())
print("Wrote markdown-renderer.min.js")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self' 'unsafe-inline' blob:; img-src 'self' data: blob:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';">
  <title>Reader</title>
  <link rel="stylesheet" href="reader.css">
  <script src="syntax-highlighter.min.js"></script>
  <script src="markdown-renderer.min.js"></script>
</head>
<body data-theme="system">
  <div id="content-container"></div>

  <script>
    function toggleWrap(cardId) {
      const card = document.getElementById(cardId);
      if (!card) return;
      const scroll = card.querySelector('.code-scroll-container');
      if (scroll) {
        scroll.classList.toggle('wrap');
      }
    }

    function copyCode(encodedCode, btn) {
      const text = decodeURIComponent(encodedCode);
      if (navigator.clipboard) {
        navigator.clipboard.writeText(text);
      }
      if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.copyCode) {
        window.webkit.messageHandlers.copyCode.postMessage(text);
      }
      const original = btn.innerText;
      btn.innerText = "Copied!";
      setTimeout(() => { btn.innerText = original; }, 1500);
    }

    function renderDocument(markdownContent, docId, isHistorical) {
      const container = document.getElementById('content-container');
      let badge = isHistorical ? '<div class="historical-badge">Historical Review / Archival</div>' : '';
      container.innerHTML = badge + MarkdownRenderer.render(markdownContent, docId);

      document.querySelectorAll('a.external-link').forEach(link => {
        link.addEventListener('click', function(e) {
          e.preventDefault();
          if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.openExternalUrl) {
            window.webkit.messageHandlers.openExternalUrl.postMessage(this.href);
          }
        });
      });
    }

    function scrollToAnchor(anchorId) {
      const el = document.getElementById(anchorId);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }

    function applyPreferences(theme, bodyFontSize, codeFontSize) {
      const resolvedTheme = theme === 'system'
        ? (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
        : theme;
      document.body.setAttribute('data-theme', resolvedTheme);
      if (bodyFontSize) {
        document.documentElement.style.setProperty('--body-font-size', bodyFontSize + 'px');
      }
      if (codeFontSize) {
        document.documentElement.style.setProperty('--code-font-size', codeFontSize + 'px');
      }
    }
  </script>
</body>
</html>
"""

with open(f"{web_dir}/reader.html", "w", encoding="utf-8") as f:
    f.write(html_content.strip())
print("Wrote reader.html")
