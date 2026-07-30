import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import { provideRouter, withInMemoryScrolling } from '@angular/router';
import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';

import { routes } from './app.routes';
import { authInterceptor } from './interceptors/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    // Start each navigation at the top of the page (SSR/SPA otherwise keep the
    // previous scroll position) and support in-page #anchor links.
    provideRouter(routes, withInMemoryScrolling({
      scrollPositionRestoration: 'top',
      anchorScrolling: 'enabled',
    })),
    provideHttpClient(
      withFetch(),
      withInterceptors([authInterceptor])
    ),
    // SSR IS enabled (see app.config.server.ts + app.routes.server.ts). Hydrate
    // the server-rendered DOM instead of throwing it away and re-bootstrapping
    // (destructive re-render). withEventReplay() captures clicks fired before
    // hydration completes and replays them once the app is interactive.
    provideClientHydration(withEventReplay())
  ]
};
