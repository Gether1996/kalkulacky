import { Component, ChangeDetectorRef, inject, OnInit, OnDestroy, PLATFORM_ID, effect } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import {
  FreelancerTaxCalculationRequest,
  FreelancerTaxCalculationResponse
} from '../../models/calculator.models';
import { SeoService } from '../../services/seo.service';
import { LeadFormComponent } from '../shared/lead-form/lead-form.component';
import { AffiliateCtaComponent } from '../shared/affiliate-cta/affiliate-cta.component';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';
import { SaveCalculationComponent } from '../shared/save-calculation/save-calculation.component';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { getCountryParams } from '../../i18n/country-params';
import { getSeoContent } from '../../i18n/seo';
import { DebouncedCalc } from '../../utils/debounced-calc';

@Component({
  selector: 'app-freelancer-tax-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, LeadFormComponent, AffiliateCtaComponent, AdSlotComponent, SaveCalculationComponent, TranslatePipe],
  templateUrl: './freelancer-tax-calculator.component.html',
  styleUrl: './freelancer-tax-calculator.component.css'
})
export class FreelancerTaxCalculatorComponent implements OnInit, OnDestroy {
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);
  private platformId = inject(PLATFORM_ID);
  private seo = inject(SeoService);
  private locale = inject(LocaleService);

  // Input values
  annualRevenue: number = 30000;
  annualExpenses: number = 0;
  useFlatExpenses: boolean = true;
  includeSickness: boolean = true;
  monthsActive: number = 12;

  // Result
  result: FreelancerTaxCalculationResponse | null = null;
  loading: boolean = false;
  error: string | null = null;

  constructor() {
    // Switching language switches the country. Freelancer rules exist for SK + CZ
    // only; other locales fall back to SK (the "Slovak rules" banner then shows).
    let firstRun = true;
    effect(() => {
      const c = this.country;
      if (!firstRun) {
        this.annualRevenue = c === 'CZ' ? 600000 : 30000;
      }
      firstRun = false;
      if (isPlatformBrowser(this.platformId)) {
        this.calculate();
      }
    });
  }

  /** Engine country — only SK and CZ are implemented; everything else → SK. */
  get country(): string {
    return getCountryParams(this.locale.locale()).countryCode === 'CZ' ? 'CZ' : 'SK';
  }
  get isSK(): boolean { return this.country === 'SK'; }
  get currencySymbol(): string { return this.isSK ? '€' : 'Kč'; }
  get currency(): string { return this.isSK ? 'EUR' : 'CZK'; }
  get countryName(): string { return this.isSK ? 'Slovensko' : 'Česko'; }
  private get numberLocale(): string { return this.isSK ? 'sk-SK' : 'cs-CZ'; }

  ngOnInit() {
    const s = getSeoContent('freelancer', this.locale.locale());
    this.seo.apply({
      title: s.title,
      description: s.description,
      keywords: s.keywords,
      faq: s.faq,
      path: '/calculator/freelancer-tax',
      isCalculator: true,
    });
    // Initial calculation is driven by the locale effect (constructor).
  }

  get saveParams(): Record<string, any> {
    return {
      annual_revenue: this.annualRevenue,
      country: this.country,
      use_flat_expenses: this.useFlatExpenses,
      annual_expenses: this.annualExpenses,
    };
  }
  get saveName(): string { return `SZČO / OSVČ · ${this.annualRevenue} ${this.currencySymbol}`; }

  /** Calculation snapshot attached to an accounting lead. */
  get leadContext(): Record<string, any> {
    return {
      annual_revenue: this.annualRevenue,
      use_flat_expenses: this.useFlatExpenses,
      net_income: this.result?.summary?.net_income ?? null,
    };
  }

  // Debounced + cancellable calc pipeline (fixes per-keystroke API storm + race).
  private calc = new DebouncedCalc<FreelancerTaxCalculationResponse>(
    () => this.calculatorService.calculateFreelancerTax({
      annual_revenue: this.annualRevenue,
      country: this.country,
      annual_expenses: this.annualExpenses,
      use_flat_expenses: this.useFlatExpenses,
      include_sickness: this.includeSickness,
      months_active: this.monthsActive
    } as FreelancerTaxCalculationRequest),
    (response) => {
      this.result = response;
      this.loading = false;
      this.cdr.detectChanges();
    },
    (err) => {
      this.error = this.locale.t('err.calcCheck');
      this.loading = false;
      this.cdr.detectChanges();
    },
  );

  calculate() {
    this.loading = true;
    this.error = null;
    this.calc.trigger();
  }

  ngOnDestroy() {
    this.calc.destroy();
  }

  formatNumber(value: number | string, decimals: number = 2): string {
    const num = typeof value === 'string' ? parseFloat(value) : value;
    return num.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  }

  formatCurrency(value: number | string): string {
    const num = typeof value === 'string' ? parseFloat(value) : value;
    const noDecimals = this.currency === 'CZK';
    return new Intl.NumberFormat(this.numberLocale, {
      style: 'currency',
      currency: this.currency,
      minimumFractionDigits: noDecimals ? 0 : 2,
      maximumFractionDigits: noDecimals ? 0 : 2
    }).format(num);
  }

  formatPercent(value: number | string): string {
    const num = typeof value === 'string' ? parseFloat(value) : value;
    return num.toFixed(2) + '%';
  }

  getEffectiveRateColor(rate: number): string {
    if (rate < 30) return '#27ae60'; // Green
    if (rate < 40) return '#f39c12'; // Orange
    return '#e74c3c'; // Red
  }

  onExpensesMethodChange() {
    if (this.useFlatExpenses) {
      this.annualExpenses = 0;
    }
  }
}
