import { Injectable, signal } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, BehaviorSubject, tap, catchError, throwError } from 'rxjs';
import { Router } from '@angular/router';
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
  private readonly API_URL = 'http://localhost:8000/api/auth';
  private readonly ACCESS_TOKEN_KEY = 'access_token';
  private readonly REFRESH_TOKEN_KEY = 'refresh_token';

  // User state
  private currentUserSubject = new BehaviorSubject<User | null>(this.getUserFromStorage());
  public currentUser$ = this.currentUserSubject.asObservable();
  
  // Authentication state signal
  public isAuthenticated = signal<boolean>(this.hasValidToken());

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
   * Refresh access token
   */
  refreshToken(): Observable<any> {
    const refreshToken = this.getRefreshToken();
    return this.http.post(`${this.API_URL}/token/refresh/`, { refresh: refreshToken }).pipe(
      tap((response: any) => {
        this.setAccessToken(response.access);
        if (response.refresh) {
          this.setRefreshToken(response.refresh);
        }
      }),
      catchError(error => {
        this.clearAuthData();
        return throwError(() => error);
      })
    );
  }

  /**
   * Check authentication status from backend
   */
  checkAuthStatus(): void {
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
      error: () => {
        this.clearAuthData();
      }
    });
  }

  /**
   * Get access token
   */
  getAccessToken(): string | null {
    return localStorage.getItem(this.ACCESS_TOKEN_KEY);
  }

  /**
   * Get refresh token
   */
  getRefreshToken(): string | null {
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
    localStorage.setItem(this.ACCESS_TOKEN_KEY, token);
  }

  /**
   * Set refresh token
   */
  private setRefreshToken(token: string): void {
    localStorage.setItem(this.REFRESH_TOKEN_KEY, token);
  }

  /**
   * Save user to localStorage
   */
  private saveUserToStorage(user: User): void {
    localStorage.setItem('current_user', JSON.stringify(user));
  }

  /**
   * Get user from localStorage
   */
  private getUserFromStorage(): User | null {
    const userStr = localStorage.getItem('current_user');
    return userStr ? JSON.parse(userStr) : null;
  }

  /**
   * Clear all authentication data
   */
  private clearAuthData(): void {
    localStorage.removeItem(this.ACCESS_TOKEN_KEY);
    localStorage.removeItem(this.REFRESH_TOKEN_KEY);
    localStorage.removeItem('current_user');
    this.currentUserSubject.next(null);
    this.isAuthenticated.set(false);
  }

  /**
   * Handle HTTP errors
   */
  private handleError(error: any): Observable<never> {
    console.error('Auth error:', error);
    return throwError(() => error);
  }
}
