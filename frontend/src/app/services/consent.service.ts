import { Injectable, signal, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

export interface ConsentState {
  necessary: true;       // always on (auth/session/preferences) — not gateable
  analytics: boolean;
  ads: boolean;
}

const STORAGE_KEY = 'kalk_consent';

/**
 * GDPR / ePrivacy consent. "Necessary" storage (auth tokens, locale, theme,
 * consent itself) is always allowed; analytics + ads require explicit opt-in.
 * Non-essential scripts (AdSense, analytics) must check `ads()` / `analytics()`
 * before loading. SSR-safe (no decision rendered on the server).
 */
@Injectable({ providedIn: 'root' })
export class ConsentService {
  private platformId = inject(PLATFORM_ID);

  /** Whether the user has made a choice yet (controls banner visibility). */
  readonly decided = signal<boolean>(false);
  readonly analytics = signal<boolean>(false);
  readonly ads = signal<boolean>(false);

  constructor() {
    if (!isPlatformBrowser(this.platformId)) return;
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const s = JSON.parse(raw) as ConsentState;
        this.analytics.set(!!s.analytics);
        this.ads.set(!!s.ads);
        this.decided.set(true);
      }
    } catch { /* ignore */ }
  }

  acceptAll(): void { this.persist(true, true); }
  rejectNonEssential(): void { this.persist(false, false); }
  save(analytics: boolean, ads: boolean): void { this.persist(analytics, ads); }

  private persist(analytics: boolean, ads: boolean): void {
    this.analytics.set(analytics);
    this.ads.set(ads);
    this.decided.set(true);
    if (!isPlatformBrowser(this.platformId)) return;
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(
        { necessary: true, analytics, ads } as ConsentState));
    } catch { /* ignore */ }
  }
}
