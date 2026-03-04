import { RenderMode, ServerRoute } from '@angular/ssr';

export const serverRoutes: ServerRoute[] = [
  {
    path: '',
    renderMode: RenderMode.Prerender
  },
  {
    path: 'calculator/**',
    renderMode: RenderMode.Client  // Calculator pages use Client-Side Rendering only
  }
];
