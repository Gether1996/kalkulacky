import { Injectable, PLATFORM_ID, inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface SavedCalculation {
  id: number;
  calculator_type: string;
  calculator_type_display?: string;
  name: string;
  params: Record<string, any>;
  result?: Record<string, any> | null;
  is_tracking: boolean;
  is_favorite: boolean;
  notification_enabled: boolean;
  note?: string;
  email?: string | null;
  created_at?: string;
  last_accessed?: string;
}

export interface UserReminder {
  id: number;
  title: string;
  note?: string;
  category?: string;
  remind_date: string;          // YYYY-MM-DD
  remind_time?: string;
  related_calculator?: string;
  email_enabled?: boolean;
  sent?: boolean;
  created_at?: string;
}

export interface UpcomingNotification {
  id: number;
  calculation_id: number;
  notification_type: string;
  priority: string;
  scheduled_date: string;
  scheduled_time: string;
  title: string;
  message: string;
  action_url?: string | null;
}

export interface DashboardStats {
  totalCalculations: number;
  trackedCalculations: number;
  favoritesCount: number;
  upcomingNotifications: number;
}

export interface DashboardData {
  success: boolean;
  stats: DashboardStats;
  calculations: SavedCalculation[];
  upcomingNotifications: UpcomingNotification[];
  reminders: UserReminder[];
}

export interface SaveCalculationRequest {
  calculator_type: string;
  name: string;
  params: Record<string, any>;
  result?: Record<string, any> | null;
  is_tracking?: boolean;
  notification_enabled?: boolean;
  note?: string;
  email?: string | null;
}

/**
 * Data layer for the logged-in user's dashboard: saved calculations + tracked
 * reminders. The auth interceptor attaches the JWT, so /my/dashboard/ resolves
 * to the current user. Saving/tracking feeds the email-notification system
 * (ScheduledNotification + the send_notifications management command).
 */
@Injectable({ providedIn: 'root' })
export class DashboardService {
  private platformId = inject(PLATFORM_ID);
  private apiUrl: string;

  constructor(private http: HttpClient) {
    this.apiUrl = isPlatformBrowser(this.platformId)
      ? environment.apiUrl
      : 'http://backend:8000/api';
  }

  getDashboard(): Observable<DashboardData> {
    return this.http.get<DashboardData>(`${this.apiUrl}/calculators/my/dashboard/`);
  }

  saveCalculation(data: SaveCalculationRequest): Observable<{ success: boolean; data: SavedCalculation }> {
    return this.http.post<{ success: boolean; data: SavedCalculation }>(
      `${this.apiUrl}/calculators/saved-calculations/`, data
    );
  }

  updateCalculation(id: number, patch: Partial<SaveCalculationRequest & { is_favorite: boolean }>):
    Observable<{ success: boolean; data: SavedCalculation }> {
    return this.http.put<{ success: boolean; data: SavedCalculation }>(
      `${this.apiUrl}/calculators/saved-calculations/${id}/`, patch
    );
  }

  deleteCalculation(id: number): Observable<{ success: boolean }> {
    return this.http.delete<{ success: boolean }>(
      `${this.apiUrl}/calculators/saved-calculations/${id}/`
    );
  }

  // ---- Custom reminders ----
  createReminder(data: Partial<UserReminder>): Observable<{ success: boolean; data: UserReminder }> {
    return this.http.post<{ success: boolean; data: UserReminder }>(
      `${this.apiUrl}/calculators/my/reminders/`, data
    );
  }

  updateReminder(id: number, patch: Partial<UserReminder>): Observable<{ success: boolean; data: UserReminder }> {
    return this.http.patch<{ success: boolean; data: UserReminder }>(
      `${this.apiUrl}/calculators/my/reminders/${id}/`, patch
    );
  }

  deleteReminder(id: number): Observable<{ success: boolean }> {
    return this.http.delete<{ success: boolean }>(
      `${this.apiUrl}/calculators/my/reminders/${id}/`
    );
  }
}
