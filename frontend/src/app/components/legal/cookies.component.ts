import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { SeoService } from '../../services/seo.service';
import { ConsentService } from '../../services/consent.service';

/**
 * Cookie policy + a control to change the consent decision at any time.
 * ⚠️ Template — review before launch.
 */
@Component({
  selector: 'app-cookies',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="legal-page">
      <h1>Zásady používania cookies</h1>
      <p class="legal-updated">Účinné od: 1. 1. 2026</p>

      <p>Web používa cookies a lokálne úložisko prehliadača. Časť je nevyhnutná na fungovanie,
        ostatné používame iba s vaším súhlasom.</p>

      <h2>Nevyhnutné</h2>
      <ul>
        <li><strong>Prihlásenie:</strong> prihlasovacie tokeny pre váš účet.</li>
        <li><strong>Predvoľby:</strong> jazyk, svetlý/tmavý režim a vaša voľba súhlasu s cookies.</li>
      </ul>

      <h2>Analytické (voliteľné)</h2>
      <p>Pomáhajú nám pochopiť, ako sa web používa. Načítajú sa iba s vaším súhlasom.</p>

      <h2>Reklamné (voliteľné)</h2>
      <p>Ak ich povolíte, môžeme zobrazovať reklamy (napr. Google AdSense), ktoré používajú cookies.
        Bez súhlasu sa reklamné skripty nenačítajú.</p>

      <h2>Správa súhlasu</h2>
      <p>Aktuálny stav – analytika: <strong>{{ consent.analytics() ? 'povolené' : 'zakázané' }}</strong>,
        reklama: <strong>{{ consent.ads() ? 'povolené' : 'zakázané' }}</strong>.</p>
      <div class="cookie-controls">
        <button type="button" class="ck-btn ck-primary" (click)="consent.acceptAll()">Povoliť všetko</button>
        <button type="button" class="ck-btn" (click)="consent.rejectNonEssential()">Len nevyhnutné</button>
      </div>

      <p style="margin-top:24px">Súbory cookies viete spravovať aj v nastaveniach prehliadača.
        Viac o spracúvaní údajov nájdete v <a routerLink="/privacy">Zásadách ochrany osobných údajov</a>.</p>
    </div>
  `,
  styles: [`
    .cookie-controls { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }
    .ck-btn { border: 1px solid #cbd5e1; background: #fff; border-radius: 10px; padding: 9px 16px;
      font-size: 14px; font-weight: 600; cursor: pointer; }
    .ck-primary { background: #4f46e5; color: #fff; border-color: #4f46e5; }
    html[data-theme="dark"] .ck-btn { background: #1e293b; color: #e2e8f0; border-color: #334155; }
    html[data-theme="dark"] .ck-primary { background: #4f46e5; }
  `],
})
export class CookiesComponent implements OnInit {
  private seo = inject(SeoService);
  consent = inject(ConsentService);
  ngOnInit(): void {
    this.seo.apply({
      title: 'Zásady používania cookies',
      description: 'Aké cookies Kalkulačky.sk používa a ako spravovať svoj súhlas.',
      path: '/cookies',
    });
  }
}
