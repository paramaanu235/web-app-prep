// Build-time content loader. Reads the 18 canonical files from the repo root and
// the iOS ContentManifest.json, verifies hashes, sections and renders them.
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { renderJava, renderMarkdown, type LinkContext } from './render';
import { sectioniseJava, sectioniseMarkdown } from './sectionise';
import type { Manifest, ManifestDocument, Section, SectionedDocument, WebSearchEntry } from './types';

export const REPO_ROOT = process.env.CONTENT_ROOT ?? path.resolve(process.cwd(), '..');
export const MANIFEST_PATH = path.join(REPO_ROOT, 'ios/GoogleInterviewPrep/GoogleInterviewPrep/Resources/ContentManifest.json');

export interface TocItem {
  sectionId: string;
  anchor: string;
  title: string;
  depth: number;
}

export interface StudyDocument {
  meta: ManifestDocument;
  html: string;
  sections: Section[];
  toc: TocItem[];
  lineCount: number;
  codeBlockCount: number;
  sha256: string;
  /** Markdown that opens with its own `# Title` renders it; otherwise the page shows the manifest title. */
  hasOwnTitle: boolean;
  wordCount: number;
}

export interface Category {
  id: string;
  name: string;
  docs: ManifestDocument[];
}

export interface StudyContent {
  manifest: Manifest;
  docs: StudyDocument[];
  docsById: Map<string, StudyDocument>;
  categories: Category[];
  searchEntries: WebSearchEntry[];
}

export function loadManifest(): Manifest {
  const manifest = JSON.parse(readFileSync(MANIFEST_PATH, 'utf8')) as Manifest;
  manifest.documents.sort((a, b) => a.order - b.order);
  return manifest;
}

export function readSource(doc: ManifestDocument): { bytes: Buffer; text: string; sha256: string } {
  const bytes = readFileSync(path.join(REPO_ROOT, doc.sourceFilename));
  const sha256 = createHash('sha256').update(bytes).digest('hex');
  return { bytes, text: bytes.toString('utf8'), sha256 };
}

export function sectionise(doc: ManifestDocument, text: string): SectionedDocument {
  return doc.format === 'java' ? sectioniseJava(doc, text) : sectioniseMarkdown(doc, text);
}

function buildToc(doc: ManifestDocument, sections: Section[]): TocItem[] {
  const entries = sections.filter((s) => s.line > 0 && (doc.format === 'java' || s.headingLevel <= 3));
  const minLevel = Math.min(...entries.map((s) => s.headingLevel), 99);
  return entries.map((s) => ({ sectionId: s.id, anchor: s.anchor, title: s.title, depth: s.headingLevel - minLevel }));
}

async function build(base: string): Promise<StudyContent> {
  const manifest = loadManifest();
  const sources = manifest.documents.map((meta) => {
    const source = readSource(meta);
    if (source.sha256 !== meta.sha256) {
      throw new Error(
        `Content integrity failure for ${meta.sourceFilename}: manifest ${meta.sha256}, file ${source.sha256}. ` +
          'Run ios/GoogleInterviewPrep/Tools/build_content.swift after editing content (see CONTENT_UPDATE.md).',
      );
    }
    return { meta, source, sectioned: sectionise(meta, source.text) };
  });

  const anchors = new Set<string>();
  const sectionsByDoc = new Map<string, Section[]>();
  for (const { meta, sectioned } of sources) {
    sectioned.sections.forEach((s) => anchors.add(s.anchor));
    sectionsByDoc.set(meta.id, sectioned.sections);
  }
  const ctx: LinkContext = {
    base,
    anchors,
    docsByFilename: new Map(manifest.documents.map((d) => [d.sourceFilename, d])),
    anchorForLine(docId, line) {
      const doc = manifest.documents.find((d) => d.id === docId)!;
      if (doc.format === 'java') return `${docId}-line-${line}`;
      const sections = sectionsByDoc.get(docId) ?? [];
      let best = `${docId}-top`;
      for (const s of sections) if (s.line > 0 && s.line <= line) best = s.anchor;
      return best;
    },
  };

  const docs: StudyDocument[] = [];
  for (const { meta, source, sectioned } of sources) {
    const html = meta.format === 'java' ? await renderJava(meta, source.text) : await renderMarkdown(meta, source.text, sectioned, ctx);
    docs.push({
      meta,
      html,
      sections: sectioned.sections,
      toc: buildToc(meta, sectioned.sections),
      lineCount: source.bytes.filter((b) => b === 0x0a).length,
      codeBlockCount: sectioned.codeBlocks.length,
      sha256: source.sha256,
      hasOwnTitle: meta.format === 'markdown' && source.text.trimStart().startsWith('# '),
      wordCount: source.text.split(/\s+/).filter(Boolean).length,
    });
  }

  const categories: Category[] = [];
  for (const meta of manifest.documents) {
    const id = meta.categoryIDs[0] ?? 'other';
    let cat = categories.find((c) => c.id === id);
    if (!cat) categories.push((cat = { id, name: meta.primaryCategory, docs: [] }));
    cat.docs.push(meta);
  }

  const searchEntries: WebSearchEntry[] = docs.flatMap((doc) =>
    doc.sections.map((s) => ({
      d: doc.meta.id,
      s: s.id,
      t: s.title,
      a: s.anchor,
      c: doc.meta.categoryIDs,
      f: doc.meta.format,
      h: doc.meta.isHistorical,
      k: s.tokens,
      p: s.preview,
      x: s.plainText,
    })),
  );

  return { manifest, docs, docsById: new Map(docs.map((d) => [d.meta.id, d])), categories, searchEntries };
}

let cache: Promise<StudyContent> | undefined;
export function loadContent(): Promise<StudyContent> {
  cache ??= build(import.meta.env?.BASE_URL ?? '/');
  return cache;
}
