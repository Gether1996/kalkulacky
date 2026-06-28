import { Injectable, PLATFORM_ID, inject, signal } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

const STORAGE_KEY = 'kalk_recent';
const MAX = 6;

/**
 * Recently-used calculators, kept client-side in localStorage (no account
 * needed, no tracking sent to the server). Complements favourites: favourites
 * are explicit pins, "recent" is automatic. SSR-safe.
 */
@Injectable({ providedIn: 'root' })
export class RecentCalculatorsService {
  private platformId = inject(PLATFORM_ID);
  readonly recent = signal<string[]>(this.read());

  private read(): string[] {
    if (!isPlatformBrowser(this.platformId)) return [];
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      const arr = raw ? JSON.parse(raw) : [];
      return Array.isArray(arr) ? arr.filter(x => typeof x === 'string').slice(0, MAX) : [];
    } catch { return []; }
  }

  /** Record a visit to a calculator id (most-recent first, de-duplicated). */
  record(calculatorId: string): void {
    if (!isPlatformBrowser(this.platformId) || !calculatorId) return;
    const next = [calculatorId, ...this.recent().filter(id => id !== calculatorId)].slice(0, MAX);
    this.recent.set(next);
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(next)); } catch { /* ignore */ }
  }

  clear(): void {
    this.recent.set([]);
    if (isPlatformBrowser(this.platformId)) {
      try { localStorage.removeItem(STORAGE_KEY); } catch { /* ignore */ }
    }
  }
}
