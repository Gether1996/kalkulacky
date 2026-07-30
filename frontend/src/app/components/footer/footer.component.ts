import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { TranslatePipe } from '../../i18n/translate.pipe';

/**
 * Site footer — legal links (privacy/terms/cookies), an indicative-results
 * disclaimer, and copyright. Rendered on all non-embed pages.
 */
@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [CommonModule, RouterLink, TranslatePipe],
  template: `
    <footer class="site-footer">
      <div class="footer-inner">
        <div class="footer-brand">
          <span class="footer-logo">🧮 Kalkulačky<span class="accent">.sk</span></span>
          <p class="footer-disclaimer">{{ 'footer.disclaimer' | t }}</p>
        </div>

        <nav class="footer-col" aria-label="Populárne kalkulačky">
          <h4 class="footer-h">{{ 'nav.tools' | t }}</h4>
          <a *ngFor="let c of popular" [routerLink]="'/calculator/' + c">{{ ('calc.' + c + '.name') | t }}</a>
        </nav>

        <nav class="footer-col" aria-label="Footer">
          <h4 class="footer-h">Kalkulačky.sk</h4>
          <a routerLink="/">{{ 'nav.home' | t }}</a>
          <a routerLink="/blog">{{ 'nav.blog' | t }}</a>
          <a routerLink="/privacy">{{ 'footer.privacy' | t }}</a>
          <a routerLink="/terms">{{ 'footer.terms' | t }}</a>
          <a routerLink="/cookies">{{ 'footer.cookies' | t }}</a>
        </nav>
      </div>
      <div class="footer-bottom">© {{ year }} Kalkulačky.sk · {{ 'footer.rights' | t }}</div>
    </footer>
  `,
  styles: [`
    .site-footer { background: #0f172a; color: #cbd5e1; margin-top: 40px; }
    .footer-inner {
      max-width: 1100px; margin: 0 auto; padding: 40px 20px 20px;
      display: grid; grid-template-columns: 1.6fr 1fr 1fr; gap: 32px;
    }
    .footer-logo { font-size: 18px; font-weight: 800; color: #fff; }
    .footer-logo .accent { color: #818cf8; }
    .footer-disclaimer { max-width: 480px; font-size: 12.5px; color: #94a3b8; margin: 10px 0 0; line-height: 1.6; }
    .footer-h {
      font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.06em;
      color: #cbd5e1; margin: 0 0 12px;
    }
    .footer-col { display: flex; flex-direction: column; gap: 9px; }
    .footer-col a { color: #94a3b8; text-decoration: none; font-size: 14px; transition: color 0.15s; }
    .footer-col a:hover { color: #fff; }
    .footer-bottom {
      max-width: 1100px; margin: 0 auto; padding: 16px 20px 28px;
      border-top: 1px solid #1e293b; font-size: 12px; color: #64748b;
    }
    @media (max-width: 720px) {
      .footer-inner { grid-template-columns: 1fr 1fr; }
      .footer-brand { grid-column: 1 / -1; }
    }
    @media (max-width: 440px) { .footer-inner { grid-template-columns: 1fr; } }
  `],
})
export class FooterComponent {
  year = 2026;
  /** Popular calculators surfaced in the footer for internal linking + SEO. */
  popular = ['salary', 'mortgage', 'vat', 'loan', 'pension', 'freelancer-tax', 'bmi', 'solar'];
}
