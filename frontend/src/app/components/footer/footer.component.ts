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
        <nav class="footer-links" aria-label="Footer">
          <a routerLink="/">{{ 'nav.home' | t }}</a>
          <a routerLink="/privacy">{{ 'footer.privacy' | t }}</a>
          <a routerLink="/terms">{{ 'footer.terms' | t }}</a>
          <a routerLink="/cookies">{{ 'footer.cookies' | t }}</a>
          <a routerLink="/blog">{{ 'nav.blog' | t }}</a>
        </nav>
      </div>
      <div class="footer-bottom">© {{ year }} Kalkulačky.sk · {{ 'footer.rights' | t }}</div>
    </footer>
  `,
  styles: [`
    .site-footer { background: #0f172a; color: #cbd5e1; margin-top: 40px; }
    .footer-inner {
      max-width: 1100px; margin: 0 auto; padding: 32px 20px 16px;
      display: flex; flex-wrap: wrap; gap: 24px; justify-content: space-between;
    }
    .footer-logo { font-size: 18px; font-weight: 800; color: #fff; }
    .footer-logo .accent { color: #818cf8; }
    .footer-disclaimer { max-width: 520px; font-size: 12.5px; color: #94a3b8; margin: 8px 0 0; }
    .footer-links { display: flex; flex-wrap: wrap; gap: 16px; align-items: flex-start; }
    .footer-links a { color: #cbd5e1; text-decoration: none; font-size: 14px; }
    .footer-links a:hover { color: #fff; text-decoration: underline; }
    .footer-bottom {
      max-width: 1100px; margin: 0 auto; padding: 12px 20px 24px;
      border-top: 1px solid #1e293b; font-size: 12px; color: #64748b;
    }
    @media (max-width: 640px) { .footer-inner { flex-direction: column; gap: 16px; } }
  `],
})
export class FooterComponent {
  year = 2026;
}
