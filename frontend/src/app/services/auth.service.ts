import { Injectable, signal, PLATFORM_ID, inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject, tap, catchError, throwError, finalize, shareReplay } from 'rxjs';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';
import {
  User,
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RegisterResponse,
  ChangePasswordRequest,
  GoogleAuthRequest,
  GoogleAuthResponse,
  CheckAuthResponse
} from '../models/auth.models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly API_URL = `${environment.apiUrl}/auth`;
  private readonly ACCESS_TOKEN_KEY = 'access_token';
  private readonly REFRESH_TOKEN_KEY = 'refresh_token';
  private platformId = inject(PLATFORM_ID);
  private get isBrowser(): boolean { return isPlatformBrowser(this.platformId); }

  // User state
  private currentUserSubject = new BehaviorSubject<User | null>(this.getUserFromStorage());
  public currentUser$ = this.currentUserSubject.asObservable();
  
  // Authentication state signal
  public isAuthenticated = signal<boolean>(this.hasValidToken());

  // Single-flight token refresh: concurrent 401s share one refresh call so the
  // rotate-refresh + blacklist-after-rotation backend config can't blacklist a
  // token mid-flight and force a spurious logout.
  private refreshInProgress$: Observable<any> | null = null;

  constructor(
    private http: HttpClient,
    private router: Router
  ) {
    // Check auth status on initialization
    this.checkAuthStatus();
  }

  /**
   * Register a new user
   */
  register(data: RegisterRequest): Observable<RegisterResponse> {
    return this.http.post<RegisterResponse>(`${this.API_URL}/register/`, data).pipe(
      tap(response => {
        this.handleAuthResponse(response);
      }),
      catchError(this.handleError)
    );
  }

  /**
   * Login user with email and password
   */
  login(data: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.API_URL}/login/`, data).pipe(
      tap(response => {
        this.handleAuthResponse(response);
      }),
      catchError(this.handleError)
    );
  }

  /**
   * Logout current user
   */
  logout(): Observable<any> {
    const refreshToken = this.getRefreshToken();
    const body = { refresh: refreshToken };

    return this.http.post(`${this.API_URL}/logout/`, body).pipe(
      tap(() => {
        this.clearAuthData();
        this.router.navigate(['/']);
      }),
      catchError(error => {
        // Clear auth data even if logout fails
        this.clearAuthData();
        this.router.navigate(['/']);
        return throwError(() => error);
      })
    );
  }

  /**
   * Google OAuth authentication
   */
  googleAuth(token: string): Observable<GoogleAuthResponse> {
    const data: GoogleAuthRequest = { token };
    return this.http.post<GoogleAuthResponse>(`${this.API_URL}/google/`, data).pipe(
      tap(response => {
        this.handleAuthResponse(response);
      }),
      catchError(this.handleError)
    );
  }

  /**
   * Get current user profile
   */
  getProfile(): Observable<User> {
    return this.http.get<User>(`${this.API_URL}/profile/`).pipe(
      tap(user => {
        this.currentUserSubject.next(user);
        this.saveUserToStorage(user);
      }),
      catchError(this.handleError)
    );
  }

  /**
   * Update user profile
   */
  updateProfile(data: Partial<User>): Observable<User> {
    return this.http.patch<User>(`${this.API_URL}/profile/`, data).pipe(
      tap(user => {
        this.currentUserSubject.next(user);
        this.saveUserToStorage(user);
      }),
      catchError(this.handleError)
    );
  }

  /**
   * Change password
   */
  changePassword(data: ChangePasswordRequest): Observable<any> {
    return this.http.post(`${this.API_URL}/change-password/`, data).pipe(
      catchError(this.handleError)
    );
  }

  /**
   * Request a password-reset email (forgot password).
   */
  forgotPassword(email: string): Observable<any> {
    return this.http.post(`${this.API_URL}/forgot-password/`, { email }).pipe(
      catchError(this.handleError)
    );
  }

  /**
   * Set a new password using the emailed uid + token.
   */
  resetPassword(data: { uid: string; token: string; new_password: string; new_password_confirm: string }): Observable<any> {
    return this.http.post(`${this.API_URL}/reset-password/`, data).pipe(
      catchError(this.handleError)
    );
  }

  /**
   * Permanently delete the account (GDPR erasure) and sign out.
   */
  deleteAccount(): Observable<any> {
    return this.http.delete(`${this.API_URL}/delete-account/`).pipe(
      tap(() => {
        this.clearAuthData();
        this.router.navigate(['/']);
      }),
      catchError(this.handleError)
    );
  }

  /**
   * Refresh the access token. Single-flight: while one refresh is in progress,
   * every caller gets the same observable so we issue exactly one refresh call.
   */
  refreshToken(): Observable<any> {
    if (this.refreshInProgress$) {
      return this.refreshInProgress$;
    }

    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      this.clearAuthData();
      return throwError(() => new Error('No refresh token available'));
    }

    this.refreshInProgress$ = this.http
      .post(`${this.API_URL}/token/refresh/`, { refresh: refreshToken })
      .pipe(
        tap((response: any) => {
          this.setAccessToken(response.access);
          if (response.refresh) {
            this.setRefreshToken(response.refresh);
          }
          this.isAuthenticated.set(true);
        }),
        catchError((error) => {
          this.clearAuthData();
          return throwError(() => error);
        }),
        finalize(() => {
          this.refreshInProgress$ = null;
        }),
        shareReplay(1)
      );

    return this.refreshInProgress$;
  }

  /**
   * Clear auth state and navigate to login without any network call.
   * Used when a token refresh has definitively failed.
   */
  forceLogout(): void {
    this.clearAuthData();
    if (this.isBrowser) {
      this.router.navigate(['/login']);
    }
  }

  /**
   * Check authentication status from backend. The interceptor now attaches the
   * Bearer token to /auth/check/, so `authenticated: false` genuinely means the
   * token is invalid. Only runs in the browser (SSR has no stored token) and
   * only when we actually hold a token.
   */
  checkAuthStatus(): void {
    if (!this.isBrowser || !this.getAccessToken()) {
      return;
    }
    this.http.get<CheckAuthResponse>(`${this.API_URL}/check/`).subscribe({
      next: (response) => {
        if (response.authenticated && response.user) {
          this.currentUserSubject.next(response.user);
          this.saveUserToStorage(response.user);
          this.isAuthenticated.set(true);
        } else {
          this.clearAuthData();
        }
      },
      // On a network/5xx error keep the locally-stored session as-is; a genuine
      // 401 is handled by the interceptor's refresh flow, not here.
      error: () => {},
    });
  }

  /**
   * Get access token
   */
  getAccessToken(): string | null {
    if (!this.isBrowser) return null;
    return localStorage.getItem(this.ACCESS_TOKEN_KEY);
  }

  /**
   * Get refresh token
   */
  getRefreshToken(): string | null {
    if (!this.isBrowser) return null;
    return localStorage.getItem(this.REFRESH_TOKEN_KEY);
  }

  /**
   * Get current user value
   */
  getCurrentUser(): User | null {
    return this.currentUserSubject.value;
  }

  /**
   * Check if user has valid token
   */
  private hasValidToken(): boolean {
    return !!this.getAccessToken();
  }

  /**
   * Handle authentication response
   */
  private handleAuthResponse(response: LoginResponse | RegisterResponse | GoogleAuthResponse): void {
    this.setAccessToken(response.access);
    this.setRefreshToken(response.refresh);
    this.currentUserSubject.next(response.user);
    this.saveUserToStorage(response.user);
    this.isAuthenticated.set(true);
  }

  /**
   * Set access token
   */
  private setAccessToken(token: string): void {
    if (!this.isBrowser) return;
    localStorage.setItem(this.ACCESS_TOKEN_KEY, token);
  }

  /**
   * Set refresh token
   */
  private setRefreshToken(token: string): void {
    if (!this.isBrowser) return;
    localStorage.setItem(this.REFRESH_TOKEN_KEY, token);
  }

  /**
   * Save user to localStorage
   */
  private saveUserToStorage(user: User): void {
    if (!this.isBrowser) return;
    localStorage.setItem('current_user', JSON.stringify(user));
  }

  /**
   * Get user from localStorage
   */
  private getUserFromStorage(): User | null {
    if (!this.isBrowser) return null;
    const userStr = localStorage.getItem('current_user');
    return userStr ? JSON.parse(userStr) : null;
  }

  /**
   * Clear all authentication data
   */
  private clearAuthData(): void {
    this.currentUserSubject.next(null);
    this.isAuthenticated.set(false);
    if (!this.isBrowser) return;
    localStorage.removeItem(this.ACCESS_TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    localStorage.removeItem('current_user');
  }

  /**
   * Handle HTTP errors
   */
  private handleError(error: any): Observable<never> {
    console.error('Auth error:', error);
    return throwError(() => error);
  }
}
