import { Component, OnInit, PLATFORM_ID, inject, effect } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { SickLeaveCalculationResponse } from '../../models/calculator.models';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { getCountryParams } from '../../i18n/country-params';

@Component({
  selector: 'app-sick-leave-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, TranslatePipe],
  templateUrl: './sick-leave-calculator.component.html',
  styleUrls: ['./sick-leave-calculator.component.css']
})
export class SickLeaveCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);

  // Form fields
  gross_salary: number = 1500;
  days_sick: number = 7;
  leave_type: 'illness' | 'care' = 'illness';

  // Result
  result: SickLeaveCalculationResponse | null = null;
  isLoading: boolean = false;
  error: string = '';

  private locale = inject(LocaleService);

  constructor(private calculatorService: CalculatorService) {
    let firstRun = true;
    effect(() => {
      const c = this.country;
      if (!firstRun) {
        this.gross_salary = c === 'CZ' ? 45000 : 1500;
      }
      firstRun = false;
      if (isPlatformBrowser(this.platformId)) {
        this.calculate();
      }
    });
  }

  /** Engine country — SK + CZ implemented; other locales fall back to SK. */
  get country(): string {
    return getCountryParams(this.locale.locale()).countryCode === 'CZ' ? 'CZ' : 'SK';
  }
  get isSK(): boolean { return this.country === 'SK'; }
  get currency(): string { return this.isSK ? 'EUR' : 'CZK'; }
  get countryName(): string { return this.isSK ? 'Slovensko' : 'Česko'; }
  private get numberLocale(): string { return this.isSK ? 'sk-SK' : 'cs-CZ'; }

  ngOnInit() {
    // Initial calculation driven by the locale effect (constructor).
  }

  calculate() {
    if (!this.gross_salary || this.gross_salary <= 0) {
      this.error = 'Zadajte hrubú mzdu';
      return;
    }

    if (!this.days_sick || this.days_sick < 1) {
      this.error = 'Zadajte počet dní pracovnej neschopnosti';
      return;
    }

    this.isLoading = true;
    this.error = '';

    this.calculatorService.calculateSickLeave({
      gross_salary: this.gross_salary,
      days_sick: this.days_sick,
      leave_type: this.leave_type,
      country: this.country
    }).subscribe({
      next: (response) => {
        this.result = response;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Calculation error:', err);
        this.error = err.error?.error || 'Nastala chyba pri výpočte. Skúste to znova.';
        this.isLoading = false;
        this.result = null;
      }
    });
  }

  // Preset scenarios for quick testing
  usePreset(preset: string) {
    switch (preset) {
      case 'short':
        this.gross_salary = 1200;
        this.days_sick = 3;
        this.leave_type = 'illness';
        break;
      case 'medium':
        this.gross_salary = 1500;
        this.days_sick = 10;
        this.leave_type = 'illness';
        break;
      case 'long':
        this.gross_salary = 2000;
        this.days_sick = 20;
        this.leave_type = 'illness';
        break;
      case 'care':
        this.gross_salary = 1800;
        this.days_sick = 5;
        this.leave_type = 'care';
        break;
    }
    this.calculate();
  }

  // Helper to get payer badge color (SK "Zamestnávateľ" / CZ "Zaměstnavatel")
  getPayerBadgeClass(payer: string): string {
    return (payer || '').toLowerCase().startsWith('zam') ? 'payer-employer' : 'payer-insurance';
  }

  // Format currency in the active country's currency
  formatCurrency(value: number): string {
    const noDecimals = this.currency === 'CZK';
    return new Intl.NumberFormat(this.numberLocale, {
      style: 'currency',
      currency: this.currency,
      minimumFractionDigits: noDecimals ? 0 : 2,
      maximumFractionDigits: noDecimals ? 0 : 2
    }).format(value);
  }

  // Show first N days in breakdown
  showBreakdownDays: number = 10;

  toggleFullBreakdown() {
    if (this.result) {
      this.showBreakdownDays = this.showBreakdownDays === 10 
        ? this.result.breakdown.length 
        : 10;
    }
  }
}
