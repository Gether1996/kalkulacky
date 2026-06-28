import { Component, OnInit, inject, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { RouterLink } from '@angular/router';
import { SeoService } from '../../services/seo.service';
import { TranslatePipe } from '../../i18n/translate.pipe';

/**
 * 404 page for unknown routes (replaces the previous silent redirect to home,
 * which produced soft-404s). Tells the user clearly and offers a way back.
 */
@Component({
  selector: 'app-not-found',
  standalone: true,
  imports: [CommonModule, RouterLink, TranslatePipe],
  template: `
    <div class="nf">
      <div class="nf-code">404</div>
      <h1 class="nf-title">{{ 'notfound.title' | t }}</h1>
      <p class="nf-text">{{ 'notfound.text' | t }}</p>
      <a routerLink="/" class="nf-btn">← {{ 'notfound.home' | t }}</a>
    </div>
  `,
  styles: [`
    .nf { max-width: 560px; margin: 0 auto; padding: 80px 20px; text-align: center; }
    .nf-code { font-size: 86px; font-weight: 800; color: var(--calc-accent, #667eea); line-height: 1; }
    .nf-title { font-size: 24px; margin: 8px 0 6px; color: #1e293b; }
    .nf-text { color: #64748b; margin: 0 0 24px; }
    .nf-btn { display: inline-block; background: var(--calc-accent, #4f46e5); color: #fff;
      border-radius: 10px; padding: 12px 22px; font-weight: 700; text-decoration: none; }
  `],
})
export class NotFoundComponent implements OnInit {
  private seo = inject(SeoService);
  private platformId = inject(PLATFORM_ID);

  ngOnInit(): void {
    this.seo.apply({
      title: '404 – Stránka nenájdená',
      description: 'Požadovaná stránka neexistuje.',
      path: '',
    });
    // Best-effort noindex for the 404 (avoids indexing dead URLs).
    if (isPlatformBrowser(this.platformId)) {
      let m = document.querySelector('meta[name="robots"]') as HTMLMetaElement | null;
      if (!m) { m = document.createElement('meta'); m.name = 'robots'; document.head.appendChild(m); }
      m.content = 'noindex, follow';
    }
  }
}
