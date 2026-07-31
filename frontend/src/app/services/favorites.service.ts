import { Injectable, PLATFORM_ID, computed, inject, signal } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { ssrApiBase } from './ssr-api-base';
import { AuthService } from './auth.service';

export interface FavoriteCalculator {
  id: number;
  calculator_id: string;
  order: number;
  created_at?: string;
}

/**
 * Per-user favourite calculators ("My tools"). Signal-based so the navbar,
 * home grid and dashboard all react to changes. Loads automatically when the
 * user logs in; clears on logout. SSR-safe (no HTTP on the server).
 */
@Injectable({ providedIn: 'root' })
export class FavoritesService {
  private platformId = inject(PLATFORM_ID);
  private http = inject(HttpClient);
  private auth = inject(AuthService);
  private apiUrl: string;

  readonly favorites = signal<FavoriteCalculator[]>([]);
  /** Set of favourited calculator ids — cheap membership checks for star toggles. */
  readonly favoriteIds = computed(() => new Set(this.favorites().map(f => f.calculator_id)));

  constructor() {
    this.apiUrl = isPlatformBrowser(this.platformId)
      ? environment.apiUrl
      : ssrApiBase();

    if (isPlatformBrowser(this.platformId)) {
      // (Re)load on auth state changes.
      this.auth.currentUser$.subscribe(user => {
        if (user) this.load();
        else this.favorites.set([]);
      });
    }
  }

  private get base() { return `${this.apiUrl}/calculators/my/favorites`; }

  load(): void {
    if (!isPlatformBrowser(this.platformId) || !this.auth.isAuthenticated()) return;
    this.http.get<{ success: boolean; data: FavoriteCalculator[] }>(`${this.base}/`)
      .subscribe({
        next: (res) => this.favorites.set(res.data ?? []),
        error: () => { /* leave existing list */ },
      });
  }

  isFavorite(calculatorId: string): boolean {
    return this.favoriteIds().has(calculatorId);
  }

  add(calculatorId: string): void {
    this.http.post<{ success: boolean; data: FavoriteCalculator }>(`${this.base}/`,
      { calculator_id: calculatorId }).subscribe({
        next: (res) => {
          if (res.data && !this.favoriteIds().has(calculatorId)) {
            this.favorites.set([...this.favorites(), res.data]);
          }
        },
      });
  }

  remove(calculatorId: string): void {
    // Optimistic removal.
    const prev = this.favorites();
    this.favorites.set(prev.filter(f => f.calculator_id !== calculatorId));
    this.http.delete(`${this.base}/${calculatorId}/`).subscribe({
      error: () => this.favorites.set(prev),  // revert on failure
    });
  }

  toggle(calculatorId: string): void {
    if (this.isFavorite(calculatorId)) this.remove(calculatorId);
    else this.add(calculatorId);
  }

  /** Persist a new ordering (array of calculator ids, top-to-bottom). */
  reorder(orderedIds: string[]): void {
    // Optimistic reorder.
    const byId = new Map(this.favorites().map(f => [f.calculator_id, f]));
    const reordered = orderedIds.map((id, i) => {
      const f = byId.get(id)!;
      return { ...f, order: i };
    }).filter(Boolean) as FavoriteCalculator[];
    if (reordered.length) this.favorites.set(reordered);

    this.http.post<{ success: boolean; data: FavoriteCalculator[] }>(`${this.base}/reorder/`,
      { order: orderedIds }).subscribe({
        next: (res) => { if (res.data) this.favorites.set(res.data); },
        error: () => this.load(),
      });
  }
}
