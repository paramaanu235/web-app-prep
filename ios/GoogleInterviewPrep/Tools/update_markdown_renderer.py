import os

web_dir = "ios/GoogleInterviewPrep/GoogleInterviewPrep/Resources/Web"

md_js = r"""window.MarkdownRenderer = (function() {
  function render(markdown, docID) {
    const lines = markdown.split('\n');
    let html = [];
    let inCode = false;
    let codeLines = [];
    let codeLang = '';
    let codeBlockIdx = 0;
    let inTable = false;
    let tableLines = [];
    let listStack = []; // Stack of { type: 'ul'|'ol', indent: number }

    function slugify(text) {
      return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '') || 'section';
    }

    function flushList(targetIndent = -1) {
      while (listStack.length > 0 && (targetIndent === -1 || listStack[listStack.length - 1].indent > targetIndent)) {
        const top = listStack.pop();
        html.push(`</${top.type}>`);
      }
    }

    function splitTableCells(row) {
      let trimmed = row.trim();
      if (trimmed.startsWith('|')) trimmed = trimmed.substring(1);
      if (trimmed.endsWith('|')) trimmed = trimmed.substring(0, trimmed.length - 1);

      const cells = [];
      let current = '';
      let inBacktick = false;
      let escaped = false;

      for (let i = 0; i < trimmed.length; i++) {
        const c = trimmed[i];
        if (escaped) {
          current += c;
          escaped = false;
          continue;
        }
        if (c === '\\') {
          escaped = true;
          continue;
        }
        if (c === '`') {
          inBacktick = !inBacktick;
          current += c;
          continue;
        }
        if (c === '|' && !inBacktick) {
          cells.push(current.trim());
          current = '';
          continue;
        }
        current += c;
      }
      cells.push(current.trim());
      return cells;
    }

    function flushTable() {
      if (!inTable) return;
      inTable = false;
      if (tableLines.length === 0) return;
      let tHtml = ['<div class="table-container"><table>'];
      let headerProcessed = false;
      for (let i = 0; i < tableLines.length; i++) {
        let cells = splitTableCells(tableLines[i]);
        if (i === 1 && cells.every(c => /^:?-+:?$/.test(c))) {
          headerProcessed = true;
          continue;
        }
        if (!headerProcessed && i === 0) {
          tHtml.push('<thead><tr>');
          cells.forEach(c => tHtml.push(`<th>${parseInline(c)}</th>`));
          tHtml.push('</tr></thead><tbody>');
        } else {
          tHtml.push('<tr>');
          cells.forEach(c => tHtml.push(`<td>${parseInline(c)}</td>`));
          tHtml.push('</tr>');
        }
      }
      tHtml.push('</tbody></table></div>');
      html.push(tHtml.join(''));
      tableLines = [];
    }

    function renderCodeBlock() {
      codeBlockIdx++;
      const rawCode = codeLines.join('\n');
      const highlighted = SyntaxHighlighter.highlight(rawCode, codeLang);
      const blockId = `${docID}-code-${codeBlockIdx}`;
      const safeRaw = encodeURIComponent(rawCode);
      html.push(`
        <div class="code-card" id="${blockId}">
          <div class="code-header">
            <span>${codeLang || 'CODE'}</span>
            <div class="code-actions">
              <button class="code-btn" onclick="toggleWrap('${blockId}')">Wrap</button>
              <button class="code-btn" onclick="copyCode('${safeRaw}', this)">Copy</button>
            </div>
          </div>
          <div class="code-scroll-container">
            <pre><code>${highlighted}</code></pre>
          </div>
        </div>
      `);
      codeLines = [];
      codeLang = '';
    }

    function parseInline(text) {
      if (!text) return '';
      let s = SyntaxHighlighter.escapeHtml(text);
      s = s.replace(/\[([^\]]+)\]\(([^\)]+)\)/g, function(m, label, url) {
        if (url.startsWith('http://') || url.startsWith('https://')) {
          return `<a href="${url}" class="external-link" target="_blank">${label}</a>`;
        }
        return `<span class="internal-link">${label}</span>`;
      });
      s = s.replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>');
      s = s.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      s = s.replace(/\*(.*?)\*/g, '<em>$1</em>');
      s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
      return s;
    }

    let headingCounts = {};

    for (let i = 0; i < lines.length; i++) {
      let line = lines[i];
      let trimmed = line.trim();

      // Fenced Code
      if (trimmed.startsWith('```') || trimmed.startsWith('~~~')) {
        flushTable();
        flushList();
        if (inCode) {
          inCode = false;
          renderCodeBlock();
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

      // Tables
      if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
        flushList();
        inTable = true;
        tableLines.push(trimmed);
        continue;
      } else if (inTable) {
        flushTable();
      }

      // Horizontal rules
      if (/^(---|---|\*\*\*|___)$/.test(trimmed)) {
        flushList();
        html.push('<hr />');
        continue;
      }

      // Headings
      let headingMatch = trimmed.match(/^(#{1,4})\s+(.*)$/);
      let boldHeadingMatch = (!headingMatch && /^\*\*[0-9]\.\s+(.*?)\*\*:?$/.test(trimmed)) ? trimmed.match(/^\*\*([0-9]\.\s+.*?)\*\*:?$/) : null;
      let gateHeadingMatch = (!headingMatch && !boldHeadingMatch && /^\*\*(Phase-two gate|Final readiness gate).*?\*\*:?$/.test(trimmed)) ? trimmed.match(/^\*\*(.*?)\*\*:?$/) : null;

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
        let slug = count === 1 ? baseSlug : `${baseSlug}-${count}`;
        let anchor = `${docID}-${slug}`;
        html.push(`<h${level} id="${anchor}">${parseInline(title)}</h${level}>`);
        continue;
      }

      // Lists (Nested list handling)
      let ulMatch = line.match(/^(\s*)([-*+])\s+(.*)$/);
      let olMatch = line.match(/^(\s*)(\d+)\.\s+(.*)$/);
      if (ulMatch || olMatch) {
        const indentStr = ulMatch ? ulMatch[1] : olMatch[1];
        const indent = indentStr.replace(/\t/g, '    ').length;
        const currentType = ulMatch ? 'ul' : 'ol';
        const content = ulMatch ? ulMatch[3] : olMatch[3];

        if (listStack.length === 0) {
          listStack.push({ type: currentType, indent: indent });
          html.push(`<${currentType}>`);
        } else {
          const currentTop = listStack[listStack.length - 1];
          if (indent > currentTop.indent) {
            listStack.push({ type: currentType, indent: indent });
            html.push(`<${currentType}>`);
          } else if (indent < currentTop.indent) {
            flushList(indent);
            if (listStack.length === 0 || listStack[listStack.length - 1].indent < indent) {
              listStack.push({ type: currentType, indent: indent });
              html.push(`<${currentType}>`);
            }
          } else if (currentTop.type !== currentType) {
            html.push(`</${currentTop.type}><${currentType}>`);
            currentTop.type = currentType;
          }
        }

        if (content.startsWith('[ ] ') || content.startsWith('[x] ')) {
          let checked = content.startsWith('[x] ');
          html.push(`<li class="task-list-item"><input type="checkbox" disabled ${checked ? 'checked' : ''} /> ${parseInline(content.substring(4))}</li>`);
        } else {
          html.push(`<li>${parseInline(content)}</li>`);
        }
        continue;
      } else {
        flushList();
      }

      // Blockquotes
      if (trimmed.startsWith('>')) {
        let bqContent = trimmed.substring(1).trim();
        html.push(`<blockquote><p>${parseInline(bqContent)}</p></blockquote>`);
        continue;
      }

      // Regular paragraph
      if (trimmed.length > 0) {
        html.push(`<p>${parseInline(trimmed)}</p>`);
      }
    }

    flushTable();
    flushList();

    // Auto-close code block if open at EOF
    if (inCode) {
      inCode = false;
      renderCodeBlock();
    }

    return html.join('\n');
  }

  return { render: render };
})();
"""

with open(f"{web_dir}/markdown-renderer.min.js", "w", encoding="utf-8") as f:
    f.write(md_js.strip())
print("Updated markdown-renderer.min.js with nested lists, pipe escaping, and EOF recovery")
