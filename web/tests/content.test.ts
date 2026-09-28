import { readFileSync } from 'node:fs';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { REPO_ROOT, loadManifest, readSource, sectionise } from '../src/content-pipeline';
import { slugify, tokenize } from '../src/content-pipeline/text';

const IOS_INDEX = path.join(REPO_ROOT, 'ios/GoogleInterviewPrep/GoogleInterviewPrep/Resources/SearchIndex.json');
const iosEntries: { documentID: string; sectionID: string; anchor: string; tokens: string[] }[] =
  JSON.parse(readFileSync(IOS_INDEX, 'utf8')).entries;

const manifest = loadManifest();
const sectioned = manifest.documents.map((doc) => ({ doc, ...sectionise(doc, readSource(doc).text) }));

describe('content integrity', () => {
  it('has all 18 canonical documents', () => {
    expect(manifest.documents).toHaveLength(18);
  });

  it.each(manifest.documents.map((d) => [d.sourceFilename, d] as const))('%s matches its manifest sha256', (_, doc) => {
    expect(readSource(doc).sha256).toBe(doc.sha256);
  });
});

describe('iOS parity', () => {
  it('produces exactly the same section anchors and ids as the iOS content builder', () => {
    const web = sectioned.flatMap((d) => d.sections.map((s) => `${s.id} ${s.anchor}`));
    const ios = iosEntries.map((e) => `${e.sectionID} ${e.anchor}`);
    expect(web).toEqual(ios);
  });

  it('produces the same token sets as iOS', () => {
    const web = sectioned.flatMap((d) => d.sections.map((s) => [...s.tokens].sort()));
    const ios = iosEntries.map((e) => [...e.tokens].sort());
    expect(web).toEqual(ios);
  });

  it('has globally unique anchors', () => {
    const anchors = sectioned.flatMap((d) => d.sections.map((s) => s.anchor));
    expect(new Set(anchors).size).toBe(anchors.length);
  });
});

describe('slugify / tokenize', () => {
  it('slugifies like Swift', () => {
    expect(slugify('1. Singleton')).toBe('1-singleton');
    expect(slugify('  Java 8 → 17: What changed?  ')).toBe('java-8-17-what-changed');
    expect(slugify('***')).toBe('section');
  });

  it('keeps code identifiers intact', () => {
    const tokens = tokenize('Use select_for_update() and @Transactional with 0-1 BFS.');
    expect(tokens).toEqual(expect.arrayContaining(['select_for_update', '@transactional', '@Transactional', '0-1']));
  });
});
