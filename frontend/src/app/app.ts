import { Component, inject, signal, computed } from '@angular/core';
import { RouterOutlet, Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { NavbarComponent } from './components/navbar/navbar.component';
import { FooterComponent } from './components/footer/footer.component';
import { DataReportComponent } from './components/shared/data-report/data-report.component';
import { CalculatorRatingComponent } from './components/shared/calculator-rating/calculator-rating.component';
import { CookieConsentComponent } from './components/shared/cookie-consent/cookie-consent.component';
import { TranslatePipe } from './i18n/translate.pipe';
import { LocaleService } from './i18n/locale.service';
import { AnalyticsService } from './services/analytics.service';
import { RecentCalculatorsService } from './services/recent-calculators.service';
import { calcIdFromPath } from './config/calculator-registry';
import { SeoService } from './services/seo.service';
import { buildCalcSeo, buildHomeSeo, defaultSeoFor } from './config/seo-routes';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, NavbarComponent, FooterComponent, DataReportComponent, CalculatorRatingComponent, CookieConsentComponent, TranslatePipe],
  template: `
    @if (showChrome()) {
      <app-navbar />
    }
    @if (showI18nNote()) {
      <div class="i18n-note">{{ 'i18n.skRulesNote' | t }}</div>
    }
    <router-outlet />
    @if (isCalcRoute()) {
      <app-calculator-rating />
    }
    @if (showDataReport()) {
      <app-data-report />
    }
    @if (showChrome()) {
      <app-footer />
      <app-cookie-consent />
    }
  `,
  styles: [],
})
export class App {
  private router = inject(Router);
  private locale = inject(LocaleService);
  private analytics = inject(AnalyticsService);
  private recent = inject(RecentCalculatorsService);
  private seo = inject(SeoService);

  // Hide site chrome on embeddable widget routes.
  showChrome = signal(true);
  isCalcRoute = signal(false);

  // "Report wrong data" — on calculators and tool/landing pages that show
  // real-world figures (not on the home page, auth, blog or embeds).
  showDataReport = signal(false);

  // Calculators that already have a real per-country engine — no "Slovak rules"
  // banner there (the figures are correct for the selected country).
  private hasOwnCountryLogic = signal(false);

  // Localized "uses Slovak rules" note — only on calculator pages that DON'T yet
  // have a per-country engine, and only for locales where the Slovak SEO content
  // is hidden (everything except sk/cs).
  showI18nNote = computed(() => {
    const loc = this.locale.locale();
    return this.isCalcRoute() && !this.hasOwnCountryLogic() && loc !== 'sk' && loc !== 'cs';
  });

  constructor() {
    // Start consent-gated, first-party page-view tracking.
    this.analytics.init();

    // Routes whose calculations are already localized per country.
    const perCountry = ['/calculator/salary', '/calculator/vat'];
    const update = (url: string) => {
      const path = url.split('?')[0];
      this.showChrome.set(!path.startsWith('/embed'));
      this.isCalcRoute.set(path.startsWith('/calculator'));
      this.hasOwnCountryLogic.set(perCountry.includes(path));
      this.showDataReport.set(
        path.startsWith('/calculator') ||
        path.startsWith('/energia') ||
        path.startsWith('/cista-mzda')
      );
      // Track recently-used calculators (client-side only).
      const calcId = calcIdFromPath(path);
      if (calcId) this.recent.record(calcId);

      // Localized SEO, applied centrally so every language is covered. Runs on
      // NavigationEnd (after a route component's own ngOnInit), so it provides
      // the correct per-locale title/description/canonical for all calculators
      // and the home page — built from the i18n `calc.<id>.name/.desc` keys.
      if (calcId) {
        const seo = buildCalcSeo(calcId, this.locale.locale(), (k) => this.locale.t(k));
        if (seo) this.seo.apply(seo);
      } else if (path === '/') {
        this.seo.apply(buildHomeSeo(this.locale.locale()));
      } else {
        // Account/auth routes with no SEO owner get a generic default so stale
        // tags from the previous page don't linger in <head>.
        const def = defaultSeoFor(path, this.locale.locale());
        if (def) this.seo.apply(def);
      }
    };
    update(this.router.url);
    this.router.events
      .pipe(filter((e): e is NavigationEnd => e instanceof NavigationEnd))
      .subscribe((e) => update(e.urlAfterRedirects));
  }
}
