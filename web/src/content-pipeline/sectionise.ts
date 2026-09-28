// Port of the markdown/java sectioning loop in build_content.swift. The output
// anchors (`{docId}-{slug}`, `{docId}-line-{n}`, `{docId}-top`) must match iOS.
import { charCount, prefixChars, slugify, tokenize, trimWhitespace } from './text';
import type { CodeBlockInfo, ManifestDocument, Section, SectionedDocument } from './types';

function preview(text: string): string {
  return prefixChars(text, 200).replaceAll('\n', ' ');
}

function headingFor(trimmed: string): { level: number; title: string } | null {
  for (let level = 1; level <= 4; level++) {
    const prefix = '#'.repeat(level) + ' ';
    if (trimmed.startsWith(prefix)) return { level, title: trimmed.slice(prefix.length) };
  }
  // Bold-line pseudo headings used by the plan documents.
  if (
    trimmed.startsWith('**') &&
    (trimmed.endsWith('**') || trimmed.endsWith('**:')) &&
    charCount(trimmed) <= 75 &&
    !trimmed.includes('→')
  ) {
    const stripped = trimmed.replaceAll('**', '').replace(/^[: ]+|[: ]+$/g, '');
    if (/^[0-9]\.\s+/.test(stripped)) return { level: 2, title: stripped };
    if (stripped.startsWith('Phase-two gate') || stripped.startsWith('Final readiness gate')) {
      return { level: 3, title: stripped };
    }
  }
  return null;
}

export function sectioniseMarkdown(doc: ManifestDocument, content: string): SectionedDocument {
  const lines = content.split('\n');
  const sections: Section[] = [];
  const codeBlocks: CodeBlockInfo[] = [];
  const sectionsByLine = new Map<number, Section>();
  const slugCounts = new Map<string, number>();

  let current = { title: doc.title, level: 1, anchor: `${doc.id}-top`, id: `${doc.id}.overview`, line: 0 };
  let text = '';
  let inCode = false;
  let fenceChar = '';
  let fenceLength = 0;
  let codeLines: string[] = [];
  let codeStart = 0;
  let codeLang = '';

  const finish = () => {
    const section: Section = {
      id: current.id,
      documentID: doc.id,
      title: current.title,
      headingLevel: current.level,
      anchor: current.anchor,
      line: current.line,
      plainText: text,
      tokens: tokenize(text + ' ' + current.title),
      preview: preview(text),
    };
    sections.push(section);
    if (section.line > 0) sectionsByLine.set(section.line, section);
    text = '';
  };

  lines.forEach((line, idx) => {
    const trimmed = trimWhitespace(line);
    const isBacktick = trimmed.startsWith('```');
    const isTilde = trimmed.startsWith('~~~');

    if (isBacktick || isTilde) {
      const ch = isBacktick ? '`' : '~';
      let count = 0;
      while (trimmed[count] === ch) count++;
      if (inCode) {
        if (ch === fenceChar && count >= fenceLength) {
          codeBlocks.push({
            id: `${doc.id}-code-${codeBlocks.length + 1}`,
            sectionID: current.id,
            language: codeLang,
            startLine: codeStart,
          });
          text += '\n' + codeLines.join('\n');
          inCode = false;
          codeLines = [];
        } else {
          codeLines.push(line);
        }
      } else {
        inCode = true;
        fenceChar = ch;
        fenceLength = count;
        codeLang = trimWhitespace(trimmed.slice(count)).split(/\s/)[0] ?? '';
        codeStart = idx + 1;
        codeLines = [];
      }
      return;
    }

    if (inCode) {
      codeLines.push(line);
      return;
    }

    const heading = headingFor(trimmed);
    if (heading) {
      finish();
      const base = slugify(heading.title);
      const n = (slugCounts.get(base) ?? 0) + 1;
      slugCounts.set(base, n);
      const slug = n === 1 ? base : `${base}-${n}`;
      current = {
        title: heading.title,
        level: heading.level,
        anchor: `${doc.id}-${slug}`,
        id: `${doc.id}.${slug}`,
        line: idx + 1,
      };
    } else {
      text += '\n' + line;
    }
  });

  if (inCode) throw new Error(`Unclosed code block in ${doc.sourceFilename} starting at line ${codeStart}`);
  finish();
  return { sections, codeBlocks, sectionsByLine };
}

function javaSymbol(trimmed: string): string | null {
  const beforeBrace = () => trimmed.split('{')[0]!.trim();
  if (trimmed.includes('class ') || trimmed.includes('interface ') || trimmed.includes('record ')) {
    return beforeBrace();
  }
  if (
    (trimmed.startsWith('public ') ||
      trimmed.startsWith('static ') ||
      trimmed.startsWith('private ') ||
      trimmed.startsWith('protected ')) &&
    trimmed.includes('(') &&
    trimmed.includes(')')
  ) {
    return beforeBrace();
  }
  if (trimmed.includes('@Test') || trimmed.startsWith('void test')) return trimmed;
  return null;
}

export function sectioniseJava(doc: ManifestDocument, content: string): SectionedDocument {
  const lines = content.split('\n');
  const overview: Section = {
    id: `${doc.id}.overview`,
    documentID: doc.id,
    title: doc.title,
    headingLevel: 1,
    anchor: `${doc.id}-top`,
    line: 0,
    plainText: content,
    tokens: tokenize(content),
    preview: preview(content),
  };

  const detected: { title: string; line: number }[] = [];
  lines.forEach((line, idx) => {
    const symbol = javaSymbol(trimWhitespace(line));
    if (symbol !== null && charCount(symbol) < 100) detected.push({ title: symbol, line: idx + 1 });
  });

  const sections: Section[] = [overview];
  const sectionsByLine = new Map<number, Section>();
  detected.forEach((d, i) => {
    const next = i + 1 < detected.length ? detected[i + 1]!.line - 1 : lines.length;
    const block = lines.slice(d.line - 1, next).join('\n');
    const section: Section = {
      id: `${doc.id}.${slugify(d.title)}-${d.line}`,
      documentID: doc.id,
      title: d.title,
      headingLevel: 2,
      anchor: `${doc.id}-line-${d.line}`,
      line: d.line,
      plainText: block,
      tokens: tokenize(d.title + ' ' + block),
      preview: lines[d.line - 1]!,
    };
    sections.push(section);
    sectionsByLine.set(d.line, section);
  });
  return { sections, codeBlocks: [], sectionsByLine };
}
