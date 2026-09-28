// Exact TypeScript ports of `slugify` / `tokenize` from
// ios/GoogleInterviewPrep/Tools/build_content.swift. Anchors and bookmarks are
// shared with the iOS app, so any change here must be mirrored there.

const ALPHANUMERIC = /[\p{L}\p{M}\p{N}]/u;

export function slugify(text: string): string {
  let result = '';
  for (const ch of text) {
    if (ALPHANUMERIC.test(ch)) {
      result += ch.toLowerCase();
    } else if (ch === ' ' || ch === '-' || ch === '_') {
      if (!result.endsWith('-') && result.length > 0) result += '-';
    }
  }
  while (result.endsWith('-')) result = result.slice(0, -1);
  return result.length === 0 ? 'section' : result;
}

const TOKEN_PATTERN = /[a-zA-Z0-9_\-@./:]+/g;
const EDGE_TRIM = /^[-.:/]+|[-.:/]+$/g;

export function tokenize(text: string): string[] {
  const tokens = new Set<string>();
  for (const match of text.matchAll(TOKEN_PATTERN)) {
    const token = match[0].replace(EDGE_TRIM, '');
    if (token.length >= 2) {
      tokens.add(token.toLowerCase());
      if (token.includes('_') || token.includes('-') || token.startsWith('@')) tokens.add(token);
    }
  }
  return [...tokens];
}

/** Swift's `trimmingCharacters(in: .whitespaces)`: spaces and tabs, but not newlines/CR. */
export function trimWhitespace(line: string): string {
  return line.replace(/^[\p{Zs}\t]+|[\p{Zs}\t]+$/gu, '');
}

/** Swift `String.count` counts grapheme clusters; code points are close enough here. */
export function charCount(text: string): number {
  return Array.from(text).length;
}

export function prefixChars(text: string, n: number): string {
  return Array.from(text).slice(0, n).join('');
}
