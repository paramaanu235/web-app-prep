import os

web_dir = "ios/GoogleInterviewPrep/GoogleInterviewPrep/Resources/Web"

hl_js = r"""window.SyntaxHighlighter = (function() {
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
    const lines = code.split('\n');
    const keywords = language === 'python' ? pythonKeywords : javaKeywords;

    const highlightedLines = lines.map(line => {
      let l = escapeHtml(line);
      let commentPart = null;

      // Handle comments first
      if (language === 'python' && l.includes('#')) {
        const idx = l.indexOf('#');
        commentPart = l.substring(idx);
        l = l.substring(0, idx);
      } else if ((language === 'java' || language === 'cpp' || language === 'javascript') && l.includes('//')) {
        const idx = l.indexOf('//');
        commentPart = l.substring(idx);
        l = l.substring(0, idx);
      }

      // Tokenize code part with protected placeholders
      const strings = [];
      l = l.replace(/(&quot;.*?&quot;|&#39;.*?&#39;|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')/g, function(match) {
        strings.push(match);
        return `\u0000STR_${strings.length - 1}\u0000`;
      });

      const annotations = [];
      l = l.replace(/(@[a-zA-Z_][a-zA-Z0-9_]*)/g, function(match) {
        annotations.push(match);
        return `\u0000ANN_${annotations.length - 1}\u0000`;
      });

      const numbers = [];
      l = l.replace(/\b(\d+(\.\d+)?)\b/g, function(match) {
        numbers.push(match);
        return `\u0000NUM_${numbers.length - 1}\u0000`;
      });

      // Highlight keywords and types
      l = l.replace(/\b([a-zA-Z_][a-zA-Z0-9_]*)\b/g, function(match, token) {
        if (keywords.has(token)) {
          return `<span class="hl-keyword">${token}</span>`;
        }
        if (/^[A-Z][a-zA-Z0-9_]*$/.test(token)) {
          return `<span class="hl-type">${token}</span>`;
        }
        return token;
      });

      // Restore protected placeholders
      l = l.replace(/\u0000NUM_(\d+)\u0000/g, (m, idx) => `<span class="hl-number">${numbers[parseInt(idx, 10)]}</span>`);
      l = l.replace(/\u0000ANN_(\d+)\u0000/g, (m, idx) => `<span class="hl-annotation">${annotations[parseInt(idx, 10)]}</span>`);
      l = l.replace(/\u0000STR_(\d+)\u0000/g, (m, idx) => `<span class="hl-string">${strings[parseInt(idx, 10)]}</span>`);

      if (commentPart !== null) {
        l += `<span class="hl-comment">${commentPart}</span>`;
      }
      return l;
    });

    return highlightedLines.join('\n');
  }

  return { highlight: highlight, escapeHtml: escapeHtml };
})();
"""

with open(f"{web_dir}/syntax-highlighter.min.js", "w", encoding="utf-8") as f:
    f.write(hl_js.strip())
print("Updated syntax-highlighter.min.js with placeholder protection")
