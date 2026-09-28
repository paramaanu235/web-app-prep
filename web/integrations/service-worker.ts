import { createHash } from 'node:crypto';
import { readdirSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import type { AstroIntegration } from 'astro';

function listFiles(dir: string): string[] {
  return readdirSync(dir).flatMap((name) => {
    const full = path.join(dir, name);
    return statSync(full).isDirectory() ? listFiles(full) : [full];
  });
}

/**
 * Writes dist/sw.js after the build, precaching every page and asset so the whole
 * library works offline after the first visit (like the iOS app's bundle). The
 * cache name is a hash of the output, so a deploy with changes replaces the cache.
 */
export default function serviceWorker(): AstroIntegration {
  let base = '/';
  return {
    name: 'prep-service-worker',
    hooks: {
      'astro:config:done': ({ config }) => {
        base = config.base.endsWith('/') ? config.base : `${config.base}/`;
      },
      'astro:build:done': ({ dir, logger }) => {
        const root = fileURLToPath(dir);
        const hash = createHash('sha256');
        const urls: string[] = [];
        for (const file of listFiles(root).sort()) {
          const rel = path.relative(root, file).split(path.sep).join('/');
          if (rel === 'sw.js' || rel === '404.html' || rel.startsWith('.')) continue;
          hash.update(rel).update(readFileSync(file));
          urls.push(base + rel.replace(/(^|\/)index\.html$/, '$1'));
        }
        const version = `prep-${hash.digest('hex').slice(0, 12)}`;
        const template = readFileSync(new URL('./sw-template.js', import.meta.url), 'utf8');
        const script = template
          .replace('__CACHE__', JSON.stringify(version))
          .replace('__PRECACHE__', JSON.stringify(urls))
          .replace('__BASE__', JSON.stringify(base));
        writeFileSync(path.join(root, 'sw.js'), script);
        logger.info(`sw.js: precaching ${urls.length} files as ${version}`);
      },
    },
  };
}
