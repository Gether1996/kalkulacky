import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
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
    )
    // Note: Hydration disabled for development (no SSR)
  ]
};
