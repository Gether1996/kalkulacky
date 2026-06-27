import {
  Component,
  OnInit,
  Type,
  inject,
  signal,
  PLATFORM_ID,
} from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { LocaleService } from '../../i18n/locale.service';
import { isLocale } from '../../i18n/locales';
import { TranslatePipe } from '../../i18n/translate.pipe';

/**
 * Embeddable widget host: renders a single calculator in a minimal, branded
 * shell suitable for an <iframe> on third-party sites. The "powered by" backlink
 * is the point — embedded calculators are the strongest passive-link engine in
 * these markets (V4 report, Part 5).
 *
 * Route: /embed/:type  (optional ?lang=sk|cs|en|pl|hu)
 *
 * Content/SEO sections and the site's own monetization blocks are hidden in
 * embed mode via the global `.embed-host` styles in styles (see embed.component.css).
 */
const EMBEDDABLE: Record<string, () => Promise<Type<any>>> = {
  salary: () =>
    import('../salary-calculator/salary-calculator.component').then(
      (m) => m.SalaryCalculatorComponent
    ),
  mortgage: () =>
    import('../mortgage-calculator/mortgage-calculator.component').then(
      (m) => m.MortgageCalculatorComponent
    ),
  solar: () =>
    import('../solar-calculator/solar-calculator.component').then(
      (m) => m.SolarCalculatorComponent
    ),
  'freelancer-tax': () =>
    import('../freelancer-tax-calculator/freelancer-tax-calculator.component').then(
      (m) => m.FreelancerTaxCalculatorComponent
    ),
  energy: () =>
    import('../energy-calculator/energy-calculator.component').then(
      (m) => m.EnergyCalculatorComponent
    ),
  vat: () =>
    import('../vat-calculator/vat-calculator.component').then(
      (m) => m.VatCalculatorComponent
    ),
  loan: () =>
    import('../loan-calculator/loan-calculator.component').then(
      (m) => m.LoanCalculatorComponent
    ),
};

@Component({
  selector: 'app-embed',
  standalone: true,
  imports: [CommonModule, TranslatePipe],
  template: `
    <div class="embed-host">
      <div class="embed-body" *ngIf="component(); else loadingTpl">
        <ng-container *ngComponentOutlet="component()!"></ng-container>
      </div>
      <ng-template #loadingTpl>
        <div class="embed-loading" *ngIf="!notFound()">…</div>
        <div class="embed-loading" *ngIf="notFound()">
          Kalkulačka nie je dostupná na vloženie.
        </div>
      </ng-template>

      <a class="embed-credit" [href]="fullUrl" target="_blank" rel="noopener">
        🧮 {{ 'embed.poweredBy' | t }} <strong>Kalkulačky.sk</strong>
      </a>
    </div>
  `,
  styleUrls: ['./embed.component.css'],
})
export class EmbedComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private platformId = inject(PLATFORM_ID);
  private locale = inject(LocaleService);

  component = signal<Type<any> | null>(null);
  notFound = signal(false);
  type = '';

  get fullUrl(): string {
    return `https://kalkulacky.sk/calculator/${this.type}`;
  }

  ngOnInit(): void {
    this.type = this.route.snapshot.paramMap.get('type') ?? '';

    const langParam = this.route.snapshot.queryParamMap.get('lang');
    if (isLocale(langParam)) this.locale.setLocale(langParam);

    const loader = EMBEDDABLE[this.type];
    if (!loader) {
      this.notFound.set(true);
      return;
    }
    if (isPlatformBrowser(this.platformId)) {
      loader()
        .then((cmp) => this.component.set(cmp))
        .catch(() => this.notFound.set(true));
    }
  }
}
