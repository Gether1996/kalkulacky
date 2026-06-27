import { RenderMode, ServerRoute } from '@angular/ssr';

// Every client route needs a server render mode. SEO-relevant pages are
// server-rendered (full HTML for crawlers); app/auth pages are client-rendered;
// embeds are client-only. The final '**' is a safety net for any new route.
export const serverRoutes: ServerRoute[] = [
  {
    // Server-rendered on demand (full HTML for SEO) rather than prerendered at
    // build — avoids a build-time prerender step and keeps deploys simple.
    path: '',
    renderMode: RenderMode.Server
  },
  {
    // Calculator pages are server-rendered so Google indexes full HTML
    // (titles, meta, intro copy, JSON-LD) instead of an empty CSR shell.
    // Components guard API calls behind isPlatformBrowser, so SSR is safe.
    path: 'calculator/**',
    renderMode: RenderMode.Server
  },
  {
    // Embeddable widgets are client-rendered (loaded inside third-party iframes).
    path: 'embed/**',
    renderMode: RenderMode.Client
  },
  // Blog — server-rendered for SEO.
  { path: 'blog', renderMode: RenderMode.Server },
  { path: 'blog/**', renderMode: RenderMode.Server },
  // App / auth pages — no SEO value, client-rendered.
  { path: 'login', renderMode: RenderMode.Client },
  { path: 'register', renderMode: RenderMode.Client },
  { path: 'dashboard', renderMode: RenderMode.Client },
  { path: 'profile', renderMode: RenderMode.Client },
  // Fallback for any other route.
  { path: '**', renderMode: RenderMode.Server }
];
