import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { catchError, switchMap, throwError } from 'rxjs';

// Auth endpoints that must NOT carry a Bearer token (they mint or don't need one).
// Everything else under /auth/ (check/, profile/, logout/, change-password/,
// delete-account/) DOES need the token — the old blanket `/auth/` skip logged the
// user out on every page load because /auth/check/ was called token-less.
const PUBLIC_AUTH_PATHS = [
  '/auth/login/',
  '/auth/register/',
  '/auth/token/refresh/',
  '/auth/google/',
  '/auth/forgot-password/',
  '/auth/reset-password/',
];

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const accessToken = authService.getAccessToken();
  const isPublicAuth = PUBLIC_AUTH_PATHS.some((p) => req.url.includes(p));

  // Attach the Bearer token to every authenticated request.
  let authReq = req;
  if (accessToken && !isPublicAuth) {
    authReq = req.clone({
      setHeaders: { Authorization: `Bearer ${accessToken}` },
    });
  }

  return next(authReq).pipe(
    catchError((error: HttpErrorResponse) => {
      // On 401 for an authenticated request, refresh once and retry.
      // refreshToken() is single-flight, so concurrent 401s share one refresh
      // call and don't race the rotate/blacklist rotation into a false logout.
      if (error.status === 401 && accessToken && !isPublicAuth) {
        return authService.refreshToken().pipe(
          switchMap(() => {
            const newToken = authService.getAccessToken();
            const retryReq = req.clone({
              setHeaders: { Authorization: `Bearer ${newToken}` },
            });
            return next(retryReq);
          }),
          catchError((refreshError) => {
            // Refresh genuinely failed — clear state and send to login
            // (no HTTP call here; logout() would post with a dead token).
            authService.forceLogout();
            return throwError(() => refreshError);
          })
        );
      }
      return throwError(() => error);
    })
  );
};
