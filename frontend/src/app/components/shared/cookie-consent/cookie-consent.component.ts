import { Component, inject, signal, PLATFORM_ID, OnInit } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ConsentService } from '../../../services/consent.service';
import { TranslatePipe } from '../../../i18n/translate.pipe';

/**
 * GDPR / ePrivacy cookie-consent banner. Shows until the user chooses. Only
 * renders in the browser (avoids SSR flash). "Necessary only" and "Accept all"
 * are one click; granular settings are explained on the cookie-policy page.
 */
@Component({
  selector: 'app-cookie-consent',
  standalone: true,
  imports: [CommonModule, RouterLink, TranslatePipe],
  template: `
    <div class="cc-banner" *ngIf="show()">
      <div class="cc-text">
        <strong>🍪 {{ 'consent.title' | t }}</strong>
        <span>{{ 'consent.text' | t }}
          <a routerLink="/cookies">{{ 'consent.more' | t }}</a>
        </span>
      </div>
      <div class="cc-actions">
        <button type="button" class="cc-btn cc-ghost" (click)="reject()">{{ 'consent.necessary' | t }}</button>
        <button type="button" class="cc-btn cc-primary" (click)="accept()">{{ 'consent.acceptAll' | t }}</button>
      </div>
    </div>
  `,
  styles: [`
    .cc-banner {
      position: fixed; left: 0; right: 0; bottom: 0; z-index: 1000;
      display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between;
      gap: 14px; padding: 16px 20px; background: #1e293b; color: #e2e8f0;
      box-shadow: 0 -4px 20px rgba(0,0,0,.25);
    }
    .cc-text { display: flex; flex-direction: column; gap: 2px; max-width: 760px; font-size: 13.5px; }
    .cc-text strong { font-size: 14.5px; }
    .cc-text a { color: #93c5fd; }
    .cc-actions { display: flex; gap: 10px; flex-shrink: 0; }
    .cc-btn { border: none; border-radius: 10px; padding: 10px 18px; font-size: 14px; font-weight: 700; cursor: pointer; }
    .cc-ghost { background: transparent; color: #e2e8f0; border: 1px solid #475569; }
    .cc-primary { background: #4f46e5; color: #fff; }
    .cc-primary:hover { background: #4338ca; }
    @media (max-width: 640px) {
      .cc-banner { flex-direction: column; align-items: stretch; }
      .cc-actions { justify-content: stretch; }
      .cc-btn { flex: 1; }
    }
  `],
})
export class CookieConsentComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private consent = inject(ConsentService);

  // Only show in the browser, and only until a choice is made.
  private browser = signal(false);
  show = () => this.browser() && !this.consent.decided();

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) this.browser.set(true);
  }

  accept(): void { this.consent.acceptAll(); }
  reject(): void { this.consent.rejectNonEssential(); }
}
