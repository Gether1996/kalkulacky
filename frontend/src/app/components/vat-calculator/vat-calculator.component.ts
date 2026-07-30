import { Component, OnInit, OnDestroy, PLATFORM_ID, inject, ChangeDetectorRef, effect } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { VATCalculationRequest, VATCalculationResponse } from '../../models/calculator.models';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { getCountryParams } from '../../i18n/country-params';
import { DebouncedCalc } from '../../utils/debounced-calc';
import { SeoService } from '../../services/seo.service';
import { getSeoContent } from '../../i18n/seo';

@Component({
  selector: 'app-vat-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, TranslatePipe],
  templateUrl: './vat-calculator.component.html',
  styleUrl: './vat-calculator.component.css'
})
export class VatCalculatorComponent implements OnInit, OnDestroy {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  private locale = inject(LocaleService);
  private seo = inject(SeoService);
  // Inputs — VAT rate defaults to the current country's standard rate.
  amount: number = 1000;
  vatRate: number = getCountryParams(this.locale.locale()).vat.standard;
  calculation_type: 'add_vat' | 'remove_vat' = 'add_vat';
  
  // Results
  result: VATCalculationResponse | null = null;
  isLoading = false;
  error: string | null = null;

  // Quick scenarios
  scenarios = [
    { label: 'Nákup spotrebiteľa', icon: '🛒', amount: 500 },
    { label: 'Firemný nákup', icon: '🏢', amount: 5000 },
    { label: 'Veľkoobchod', icon: '📦', amount: 20000 },
    { label: 'Služba/freelance', icon: '💼', amount: 1500 }
  ];

  constructor(private calculatorService: CalculatorService) {
    // When the user switches language/country, snap the VAT rate to that
    // country's standard rate and recompute. VAT is just a rate, so this is
    // genuinely correct per country (unlike the SK-only tax calculators).
    effect(() => {
      const params = getCountryParams(this.locale.locale());
      this.vatRate = params.vat.standard;
      if (isPlatformBrowser(this.platformId)) {
        this.calculate();
      }
    });
  }

  /** Current country's VAT parameters, driven by the selected language. */
  get countryParams() {
    return getCountryParams(this.locale.locale());
  }

  /** Standard + reduced VAT rates offered as quick presets for this country. */
  get vatRatePresets(): number[] {
    const p = this.countryParams.vat;
    return [p.standard, ...p.reduced];
  }

  setVatRate(rate: number) {
    this.vatRate = rate;
    this.calculate();
  }

  ngOnInit() {
    const s = getSeoContent('vat', this.locale.locale());
    this.seo.apply({ title: s.title, description: s.description, keywords: s.keywords, faq: s.faq, path: '/calculator/vat', isCalculator: true });
    // Auto-calculate on component init (browser only)
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  // Debounced + cancellable calc pipeline (fixes per-keystroke API storm + race).
  private calc = new DebouncedCalc<VATCalculationResponse>(
    () => this.calculatorService.calculateVAT({
      amount: this.amount,
      vat_rate: this.vatRate,
      calculation_type: this.calculation_type,
    } as VATCalculationRequest),
    (response) => {
      this.result = response;
      this.isLoading = false;
      this.cdr.detectChanges();
    },
    (err) => {
      console.error('VAT Calculation error:', err);
      this.error = this.locale.t('err.calc');
      this.isLoading = false;
      this.cdr.detectChanges();
    },
  );

  calculate() {
    if (this.amount <= 0) {
      this.error = this.locale.t('err.amountPositive');
      return;
    }
    this.isLoading = true;
    this.error = null;
    this.calc.trigger();
  }

  ngOnDestroy() {
    this.calc.destroy();
  }

  applyScenario(amount: number) {
    this.amount = amount;
    this.calculate();
  }

  formatCurrency(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.00';
    }
    return new Intl.NumberFormat(this.countryParams.numberLocale, {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(value);
  }
}
