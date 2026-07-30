import { Component, OnInit, OnDestroy, ChangeDetectorRef, PLATFORM_ID, inject, effect } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { PensionCalculationRequest, PensionCalculationResponse } from '../../models/calculator.models';
import { SeoService } from '../../services/seo.service';
import { AffiliateCtaComponent } from '../shared/affiliate-cta/affiliate-cta.component';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';
import { SaveCalculationComponent } from '../shared/save-calculation/save-calculation.component';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { getCountryParams } from '../../i18n/country-params';
import { getSeoContent } from '../../i18n/seo';
import { DebouncedCalc } from '../../utils/debounced-calc';

@Component({
  selector: 'app-pension-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, AffiliateCtaComponent, AdSlotComponent, SaveCalculationComponent, TranslatePipe],
  templateUrl: './pension-calculator.component.html',
  styleUrls: ['./pension-calculator.component.css']
})
export class PensionCalculatorComponent implements OnInit, OnDestroy {
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);
  private platformId = inject(PLATFORM_ID);
  private seo = inject(SeoService);

  // Input fields
  currentAge: number = 35;
  grossSalary: number = 1500;
  yearsWorked: number = 12;
  gender: 'male' | 'female' = 'male';
  includeSecondPillar: boolean = true;
  secondPillarRate: number = 6.0;
  
  // Results
  result: PensionCalculationResponse | null = null;
  loading: boolean = false;
  error: string = '';

  private locale = inject(LocaleService);

  constructor() {
    let firstRun = true;
    effect(() => {
      const c = this.country;
      if (!firstRun) {
        this.grossSalary = c === 'CZ' ? 45000 : 1500;
      }
      firstRun = false;
      if (isPlatformBrowser(this.platformId)) {
        this.calculate();
      }
    });
  }

  /** Engine country — SK + CZ implemented; other locales fall back to SK. */
  get country(): string {
    return getCountryParams(this.locale.locale()).countryCode;
  }
  get isSK(): boolean { return this.country === 'SK'; }
  get currency(): string { return getCountryParams(this.locale.locale()).currency; }
  get countryName(): string { return getCountryParams(this.locale.locale()).countryName; }
  private get numberLocale(): string { return getCountryParams(this.locale.locale()).numberLocale; }

  // Country-appropriate quick salary presets.
  get salaryBenchmarks() {
    return this.isSK
      ? [
          { label: 'Minimálna mzda', value: 816 },
          { label: 'Priemerná mzda', value: 1500 },
          { label: 'Nadpriemerná', value: 2200 },
          { label: 'Vysoká mzda', value: 3500 },
        ]
      : [
          { label: 'Minimální mzda', value: 20800 },
          { label: 'Průměrná mzda', value: 46000 },
          { label: 'Nadprůměrná', value: 65000 },
          { label: 'Vysoká mzda', value: 100000 },
        ];
  }

  ngOnInit() {
    const s = getSeoContent('pension', this.locale.locale());
    this.seo.apply({
      title: s.title,
      description: s.description,
      keywords: s.keywords,
      faq: s.faq,
      path: '/calculator/pension',
      isCalculator: true,
    });
    // Initial calculation driven by the locale effect (constructor).
  }

  setBenchmark(value: number) {
    this.grossSalary = value;
    this.calculate();
  }

  get saveParams(): Record<string, any> {
    return {
      current_age: this.currentAge,
      gross_salary: this.grossSalary,
      years_worked: this.yearsWorked,
      gender: this.gender,
      country: this.country,
    };
  }
  get saveName(): string { return `${this.locale.t('pension.title')} · ${this.grossSalary} ${this.currency === 'CZK' ? 'Kč' : '€'}`; }

  calculate() {
    // Validate inputs
    if (this.currentAge < 18 || this.currentAge > 70) {
      this.error = this.locale.t('err.ageRange');
      return;
    }
    
    if (this.grossSalary <= 0) {
      this.error = this.locale.t('err.grossPositive');
      return;
    }
    
    if (this.yearsWorked < 0 || this.yearsWorked > this.currentAge - 18) {
      this.error = this.locale.t('err.yearsWorked');
      return;
    }

    this.error = '';
    this.loading = true;
    this.result = null;
    this.calc.trigger();
  }

  // Debounced + cancellable calc pipeline (fixes per-keystroke API storm + race).
  private calc = new DebouncedCalc<PensionCalculationResponse>(
    () => this.calculatorService.calculatePension({
      current_age: this.currentAge,
      gross_salary: this.grossSalary,
      years_worked: this.yearsWorked,
      gender: this.gender,
      include_second_pillar: this.isSK && this.includeSecondPillar,
      second_pillar_rate: this.secondPillarRate,
      country: this.country
    } as PensionCalculationRequest),
    (response) => {
      this.result = response;
      this.loading = false;
      this.cdr.detectChanges();
    },
    (err: any) => {
      this.error = err.error?.error || this.locale.t('err.calc');
      this.loading = false;
      this.cdr.detectChanges();
    },
  );

  ngOnDestroy() {
    this.calc.destroy();
  }

  // Helper methods
  formatCurrency(value: number): string {
    const noDecimals = this.currency === 'CZK';
    return new Intl.NumberFormat(this.numberLocale, {
      style: 'currency',
      currency: this.currency,
      minimumFractionDigits: noDecimals ? 0 : 2,
      maximumFractionDigits: noDecimals ? 0 : 2
    }).format(value);
  }

  formatNumber(value: number): string {
    return new Intl.NumberFormat(this.numberLocale, {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  }

  formatPercent(value: number): string {
    return `${value.toFixed(1)}%`;
  }

  getReplacementRateColor(rate: number): string {
    if (rate >= 70) return 'green';
    if (rate >= 50) return 'orange';
    return 'red';
  }

  getReplacementRateLabel(rate: number): string {
    if (rate >= 70) return 'Výborná';
    if (rate >= 50) return 'Priemerná';
    return 'Nízka';
  }
}
