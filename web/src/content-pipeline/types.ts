export type ContentFormat = 'markdown' | 'java';

export interface ManifestDocument {
  id: string;
  title: string;
  sourceFilename: string;
  format: ContentFormat;
  primaryCategory: string;
  categoryIDs: string[];
  order: number;
  isHistorical: boolean;
  sha256: string;
  byteCount: number;
  lineCountAtManifestBuild: number;
  summary?: string | null;
}

export interface Manifest {
  version: number;
  builtAt: string;
  documents: ManifestDocument[];
}

export interface Section {
  id: string;
  documentID: string;
  title: string;
  headingLevel: number;
  anchor: string;
  /** 1-based source line of the heading (0 for the synthetic overview section). */
  line: number;
  plainText: string;
  tokens: string[];
  preview: string;
}

export interface CodeBlockInfo {
  id: string;
  sectionID: string;
  language: string;
  /** 1-based line of the opening fence. */
  startLine: number;
}

export interface SectionedDocument {
  sections: Section[];
  codeBlocks: CodeBlockInfo[];
  /** 1-based heading line -> section, for markdown anchor injection. */
  sectionsByLine: Map<number, Section>;
}

/** Compact search entry shipped to the browser (see src/pages/search-index.json.ts). */
export interface WebSearchEntry {
  d: string; // documentID
  s: string; // sectionID
  t: string; // section title
  a: string; // anchor
  c: string[]; // categoryIDs
  f: ContentFormat;
  h: boolean; // isHistorical
  k: string[]; // tokens
  p: string; // preview
  x: string; // plainText
}
