import { Injectable, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { environment } from '../../environments/environment';
import { ConsentService } from './consent.service';
import { LocaleService } from '../i18n/locale.service';

/**
 * First-party page-view tracking. Sends a lightweight beacon to the backend on
 * each navigation, but ONLY with the user's analytics consent. No cookies; a
 * random visitor id (for unique-visitor counts) lives in localStorage and is
 * created only once consent is granted. Failures are swallowed silently.
 */
@Injectable({ providedIn: 'root' })
export class AnalyticsService {
  private platformId = inject(PLATFORM_ID);
  private http = inject(HttpClient);
  private consent = inject(ConsentService);
  private locale = inject(LocaleService);
  private router = inject(Router);

  private apiUrl = environment.apiUrl;
  private started = false;
  private firstHit = true;

  /** Begin tracking navigation (called once from the app shell). */
  init(): void {
    if (this.started || !isPlatformBrowser(this.platformId)) return;
    this.started = true;
    this.router.events
      .pipe(filter((e): e is NavigationEnd => e instanceof NavigationEnd))
      .subscribe((e) => this.track(e.urlAfterRedirects));
  }

  private track(url: string): void {
    if (!this.consent.analytics()) return;            // consent required
    const path = (url || '/').split('?')[0];
    if (path.startsWith('/embed')) return;             // don't track embeds

    const payload = {
      path,
      locale: this.locale.locale(),
      device: this.device(),
      referrer_host: this.firstHit ? this.referrerHost() : '',
      visitor_hash: this.visitorId(),
    };
    this.firstHit = false;

    this.http.post(`${this.apiUrl}/calculators/analytics/collect/`, payload)
      .subscribe({ next: () => {}, error: () => {} });  // fire-and-forget
  }

  private device(): string {
    const w = window.innerWidth;
    if (w < 768) return 'mobile';
    if (w < 1024) return 'tablet';
    return 'desktop';
  }

  private referrerHost(): string {
    try {
      const r = document.referrer;
      if (!r) return '';
      const h = new URL(r).hostname;
      return h && h !== window.location.hostname ? h.slice(0, 200) : '';
    } catch { return ''; }
  }

  private visitorId(): string {
    try {
      let id = localStorage.getItem('kalk_vid');
      if (!id) {
        id = (Date.now().toString(36) + Math.random().toString(36).slice(2, 10));
        localStorage.setItem('kalk_vid', id);
      }
      return id;
    } catch { return ''; }
  }
}
