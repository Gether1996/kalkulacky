import {
  AngularNodeAppEngine,
  createNodeRequestHandler,
  isMainModule,
  writeResponseToNodeResponse,
} from '@angular/ssr/node';
import express from 'express';
import { join } from 'node:path';
import { CALCULATOR_REGISTRY } from './app/config/calculator-registry';
import { ssrApiBase } from './app/services/ssr-api-base';

const browserDistFolder = join(import.meta.dirname, '../browser');

const app = express();
const angularApp = new AngularNodeAppEngine();

/**
 * Dynamic sitemap — generated from the calculator registry + live blog posts so
 * it never goes stale (new calculators/articles appear automatically). Served
 * before the static middleware so it wins over any bundled sitemap.xml. Blog
 * fetch is best-effort: if the API is down we still emit calculators + pages.
 */
const SITEMAP_ORIGIN = 'https://kalkulacky.sk';
const SITEMAP_STATIC_ROUTES: { path: string; priority: string; changefreq: string }[] = [
  { path: '/', priority: '1.0', changefreq: 'weekly' },
  { path: '/energia', priority: '0.8', changefreq: 'monthly' },
  { path: '/blog', priority: '0.6', changefreq: 'weekly' },
  { path: '/privacy', priority: '0.3', changefreq: 'yearly' },
  { path: '/terms', priority: '0.3', changefreq: 'yearly' },
  { path: '/cookies', priority: '0.3', changefreq: 'yearly' },
];

app.get('/sitemap.xml', async (_req, res) => {
  const rows: string[] = [];
  const add = (
    path: string,
    opts: { priority?: string; changefreq?: string; lastmod?: string } = {},
  ) => {
    const parts = [`<loc>${SITEMAP_ORIGIN}${path}</loc>`];
    if (opts.changefreq) parts.push(`<changefreq>${opts.changefreq}</changefreq>`);
    if (opts.priority) parts.push(`<priority>${opts.priority}</priority>`);
    if (opts.lastmod) parts.push(`<lastmod>${opts.lastmod}</lastmod>`);
    rows.push(`  <url>${parts.join('')}</url>`);
  };

  for (const r of SITEMAP_STATIC_ROUTES) {
    add(r.path, { priority: r.priority, changefreq: r.changefreq });
  }
  for (const c of CALCULATOR_REGISTRY) {
    add(c.route, { priority: '0.7', changefreq: 'monthly' });
  }

  try {
    const resp = await fetch(`${ssrApiBase()}/calculators/blog/posts/`, {
      signal: AbortSignal.timeout(4000),
    });
    if (resp.ok) {
      const body = await resp.json();
      const posts = Array.isArray(body) ? body : (body?.data ?? body?.results ?? []);
      for (const p of posts) {
        if (p?.slug) {
          add(`/blog/${p.slug}`, {
            priority: '0.6',
            changefreq: 'monthly',
            lastmod: (p.published_at || p.updated_at || '').slice(0, 10) || undefined,
          });
        }
      }
    }
  } catch {
    // API unavailable — serve calculators + static pages only.
  }

  const xml =
    `<?xml version="1.0" encoding="UTF-8"?>\n` +
    `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n` +
    `${rows.join('\n')}\n` +
    `</urlset>\n`;
  res.set('Content-Type', 'application/xml').send(xml);
});

/**
 * Example Express Rest API endpoints can be defined here.
 * Uncomment and define endpoints as necessary.
 *
 * Example:
 * ```ts
 * app.get('/api/{*splat}', (req, res) => {
 *   // Handle API request
 * });
 * ```
 */

/**
 * Serve static files from /browser
 */
app.use(
  express.static(browserDistFolder, {
    maxAge: '1y',
    index: false,
    redirect: false,
  }),
);

/**
 * Handle all other requests by rendering the Angular application.
 */
app.use((req, res, next) => {
  angularApp
    .handle(req)
    .then((response) =>
      response ? writeResponseToNodeResponse(response, res) : next(),
    )
    .catch(next);
});

/**
 * Start the server if this module is the main entry point, or it is ran via PM2.
 * The server listens on the port defined by the `PORT` environment variable, or defaults to 4000.
 */
if (isMainModule(import.meta.url) || process.env['pm_id']) {
  const port = process.env['PORT'] || 4000;
  app.listen(port, (error) => {
    if (error) {
      throw error;
    }

    console.log(`Node Express server listening on http://localhost:${port}`);
  });
}

/**
 * Request handler used by the Angular CLI (for dev-server and during build) or Firebase Cloud Functions.
 */
export const reqHandler = createNodeRequestHandler(app);
