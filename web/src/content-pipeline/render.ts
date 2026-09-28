import { createHighlighter, type Highlighter } from 'shiki';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkRehype from 'remark-rehype';
import rehypeRaw from 'rehype-raw';
import rehypeStringify from 'rehype-stringify';
import { visit, SKIP } from 'unist-util-visit';
import type { Root as MdRoot, Link } from 'mdast';
import type { Element, ElementContent, Properties, Root as HastRoot, Text } from 'hast';
import { slugify } from './text';
import type { ManifestDocument, SectionedDocument } from './types';

const THEMES = { light: 'github-light', dark: 'github-dark-dimmed' } as const;
// Token colours that fall below WCAG AA (4.5:1) on our code backgrounds, swapped
// for darker/lighter variants of the same hue (checked against light and sepia).
const COLOR_REPLACEMENTS = {
  'github-light': { '#d73a49': '#b31d28', '#6a737d': '#57606a', '#e36209': '#a04600', '#22863a': '#1a6b2e' },
  'github-dark-dimmed': { '#768390': '#8b98a5' },
};
const LANGS = ['java', 'python', 'bash', 'swift', 'xml', 'yaml'];
const LANG_ALIASES: Record<string, string> = { sh: 'bash', shell: 'bash', zsh: 'bash', py: 'python' };

let highlighterPromise: Promise<Highlighter> | undefined;
export function getHighlighter(): Promise<Highlighter> {
  highlighterPromise ??= createHighlighter({ themes: Object.values(THEMES), langs: LANGS });
  return highlighterPromise;
}

export interface LinkContext {
  base: string;
  docsByFilename: Map<string, ManifestDocument>;
  anchors: Set<string>;
  /** Returns the anchor closest to (at or before) a 1-based source line. */
  anchorForLine: (docId: string, line: number) => string;
}

function hastText(node: ElementContent | HastRoot): string {
  if (node.type === 'text') return node.value;
  if ('children' in node) return node.children.map((c) => hastText(c as ElementContent)).join('');
  return '';
}

const el = (tagName: string, properties: Element['properties'], children: ElementContent[] = []): Element => ({
  type: 'element',
  tagName,
  properties,
  children,
});
const txt = (value: string): Text => ({ type: 'text', value });

const BOOKMARK_ICON = el('svg', { viewBox: '0 0 24 24', width: 16, height: 16, ariaHidden: 'true' }, [
  el('path', { d: 'M6 3h12v18l-6-4-6 4z', fill: 'none', stroke: 'currentColor', strokeWidth: '1.75', strokeLinejoin: 'round' }),
]);

export function resolveHref(url: string, doc: ManifestDocument, ctx: LinkContext): { href: string; external: boolean } {
  if (/^(https?:|mailto:)/i.test(url)) return { href: url, external: true };
  if (url.startsWith('#')) {
    // GitHub-style fragments (`#26-dao--repository`) -> iOS anchors (`{docId}-26-dao-repository`).
    const frag = decodeURIComponent(url.slice(1));
    const scoped = [`${doc.id}-${frag}`, `${doc.id}-${slugify(frag)}`].find((a) => ctx.anchors.has(a));
    return { href: scoped ? `#${scoped}` : url, external: false };
  }
  // Links to other study files, e.g. `/abs/path/grok_python_snippets.md:884` or `quick_reference.md#x`.
  const [pathPart = '', frag] = url.split('#');
  const lineMatch = pathPart.match(/:(\d+)$/);
  const filename = pathPart.replace(/:(\d+)$/, '').split('/').pop() ?? '';
  const target = ctx.docsByFilename.get(filename);
  if (!target) return { href: url, external: false };
  let anchor = '';
  if (lineMatch) anchor = ctx.anchorForLine(target.id, Number(lineMatch[1]));
  else if (frag && ctx.anchors.has(`${target.id}-${frag}`)) anchor = `${target.id}-${frag}`;
  return { href: `${ctx.base}docs/${target.id}/${anchor ? `#${anchor}` : ''}`, external: false };
}

/** remark: attach iOS-compatible ids to headings/pseudo-headings/code, rewrite links. */
function remarkStudyAnchors(doc: ManifestDocument, sectioned: SectionedDocument, ctx: LinkContext) {
  const codeByLine = new Map(sectioned.codeBlocks.map((c) => [c.startLine, c.id]));
  return () => (tree: MdRoot) => {
    const assigned = new Set<number>();
    visit(tree, (node) => {
      if (node.type === 'root') return;
      const line = node.position?.start.line;
      if (node.type === 'link') {
        const link = node as Link;
        const { href, external } = resolveHref(link.url, doc, ctx);
        link.url = href;
        if (external) {
          link.data = { ...link.data, hProperties: { target: '_blank', rel: ['noopener', 'noreferrer'] } };
        }
        return;
      }
      if (line === undefined) return;
      if (node.type === 'code' && codeByLine.has(line)) {
        node.data = { ...node.data, hProperties: { dataBlockId: codeByLine.get(line) } };
        return;
      }
      const section = sectioned.sectionsByLine.get(line);
      if (section && !assigned.has(line)) {
        assigned.add(line);
        const props: Properties = {
          id: section.anchor,
          dataSectionId: section.id,
          dataSectionTitle: section.title,
        };
        if (node.type !== 'heading') props.className = ['pseudo-heading', `pseudo-h${section.headingLevel}`];
        node.data = { ...node.data, hProperties: props };
      } else if (node.type === 'heading') {
        node.data = { ...node.data, hProperties: { id: `${doc.id}-l${line}` } };
      }
    });
  };
}

/** rehype: shiki highlighting + code chrome, scrollable tables, heading affordances. */
function rehypeStudyChrome(highlighter: Highlighter) {
  return () => (tree: HastRoot) => {
    visit(tree, 'element', (node, index, parent) => {
      if (!parent || index === undefined) return;

      if (node.tagName === 'pre') {
        const code = node.children.find((c): c is Element => c.type === 'element' && c.tagName === 'code');
        if (!code) return;
        const classes = (code.properties.className as string[] | undefined) ?? [];
        const rawLang = classes.find((c) => c.startsWith('language-'))?.slice('language-'.length) ?? '';
        const lang = LANG_ALIASES[rawLang] ?? rawLang;
        const source = hastText(code).replace(/\n$/, '');
        const highlighted = highlighter.codeToHast(source, {
          lang: LANGS.includes(lang) ? lang : 'text',
          themes: THEMES,
          defaultColor: false,
          colorReplacements: COLOR_REPLACEMENTS,
        });
        const pre = highlighted.children[0] as Element;
        pre.properties.tabIndex = 0;
        const figure = el(
          'figure',
          { className: ['code'], id: code.properties.dataBlockId as string | undefined, dataLang: rawLang || 'text' },
          [
            el('div', { className: ['code-bar'] }, [
              el('span', { className: ['code-lang'] }, [txt(rawLang || 'text')]),
              el('span', { className: ['code-actions'] }, [
                el('button', { type: 'button', className: ['code-btn'], dataAction: 'wrap', ariaPressed: 'false' }, [txt('Wrap')]),
                el('button', { type: 'button', className: ['code-btn'], dataAction: 'copy' }, [txt('Copy')]),
              ]),
            ]),
            pre,
          ],
        );
        parent.children[index] = figure;
        return SKIP;
      }

      if (node.tagName === 'table') {
        parent.children[index] = el('div', { className: ['table-wrap'], tabIndex: 0 }, [node]);
        return SKIP;
      }

      if (node.properties.dataSectionId) {
        const anchor = node.properties.id as string;
        node.children.push(
          el('span', { className: ['h-tools'] }, [
            el('a', { className: ['h-link'], href: `#${anchor}`, ariaLabel: 'Link to this section' }, [txt('#')]),
            el('button', { type: 'button', className: ['bm-btn'], dataBookmark: '', ariaLabel: 'Bookmark this section', ariaPressed: 'false' }, [
              BOOKMARK_ICON,
            ]),
          ]),
        );
      }
    });
  };
}

export async function renderMarkdown(
  doc: ManifestDocument,
  content: string,
  sectioned: SectionedDocument,
  ctx: LinkContext,
): Promise<string> {
  const highlighter = await getHighlighter();
  const file = await unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkStudyAnchors(doc, sectioned, ctx))
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeRaw)
    .use(rehypeStudyChrome(highlighter))
    .use(rehypeStringify)
    .process(content);
  return String(file);
}

export async function renderJava(doc: ManifestDocument, content: string): Promise<string> {
  const highlighter = await getHighlighter();
  return highlighter.codeToHtml(content.replace(/\n$/, ''), {
    lang: 'java',
    themes: THEMES,
    defaultColor: false,
    colorReplacements: COLOR_REPLACEMENTS,
    transformers: [
      {
        pre(node) {
          node.properties.class = `${node.properties.class ?? ''} java-source`;
          node.properties.tabindex = 0;
        },
        line(node, line) {
          node.properties.id = `${doc.id}-line-${line}`;
          node.properties['data-line'] = line;
        },
      },
    ],
  });
}
