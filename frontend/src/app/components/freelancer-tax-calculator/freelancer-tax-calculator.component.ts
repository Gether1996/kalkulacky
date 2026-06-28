import { Component, ChangeDetectorRef, inject, OnInit, PLATFORM_ID, effect } from '@angular/core';
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

@Component({
  selector: 'app-freelancer-tax-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, LeadFormComponent, AffiliateCtaComponent, AdSlotComponent, SaveCalculationComponent, TranslatePipe],
  templateUrl: './freelancer-tax-calculator.component.html',
  styleUrl: './freelancer-tax-calculator.component.css'
})
export class FreelancerTaxCalculatorComponent implements OnInit {
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
    this.seo.apply({
      title: 'Kalkulačka daní a odvodov SZČO 2026 (živnostník)',
      description: 'Vypočítajte daň z príjmu, zdravotné a sociálne odvody pre SZČO/živnostníka v roku 2026. Paušálne vs. skutočné výdavky a čistý príjem.',
      path: '/calculator/freelancer-tax',
      keywords: 'odvody SZČO 2026 kalkulačka, daň živnostník, paušálne výdavky, čistý príjem živnostník',
      isCalculator: true,
      faq: [
        {
          question: 'Aké sú minimálne odvody SZČO v roku 2026?',
          answer: 'Živnostník platí minimálne zdravotné aj sociálne odvody odvodené od minimálneho vymeriavacieho základu. Kalkulačka zohľadní aktuálne sadzby pre rok 2026.',
        },
        {
          question: 'Kedy sa oplatia paušálne výdavky 60 %?',
          answer: 'Paušálne výdavky (60 % z príjmu, do zákonného limitu) sa oplatia, ak sú vaše skutočné náklady nižšie. Pri vysokých reálnych nákladoch je výhodnejšie účtovať skutočné výdavky.',
        },
      ],
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

  calculate() {
    this.loading = true;
    this.error = null;

    const request: FreelancerTaxCalculationRequest = {
      annual_revenue: this.annualRevenue,
      country: this.country,
      annual_expenses: this.annualExpenses,
      use_flat_expenses: this.useFlatExpenses,
      include_sickness: this.includeSickness,
      months_active: this.monthsActive
    };

    this.calculatorService.calculateFreelancerTax(request).subscribe({
      next: (response) => {
        this.result = response;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = 'Chyba pri výpočte. Skontrolujte zadané údaje.';
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
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
