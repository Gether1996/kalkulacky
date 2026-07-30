import { Component, ChangeDetectorRef, inject, OnInit, OnDestroy, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CalculatorService } from '../../services/calculator.service';
import {
  InflationCalculationRequest,
  InflationCalculationResponse
} from '../../models/calculator.models';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { DebouncedCalc } from '../../utils/debounced-calc';
import { SeoService } from '../../services/seo.service';
import { getSeoContent } from '../../i18n/seo';

@Component({
  selector: 'app-inflation-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslatePipe],
  templateUrl: './inflation-calculator.component.html',
  styleUrl: './inflation-calculator.component.css'
})
export class InflationCalculatorComponent implements OnInit, OnDestroy {
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);
  private platformId = inject(PLATFORM_ID);
  private locale = inject(LocaleService);
  private seo = inject(SeoService);

  // Input values
  presentValue: number = 10000;
  years: number = 10;
  inflationRate: number = 3.0;
  calculateReverse: boolean = false;

  // Result
  result: InflationCalculationResponse | null = null;
  loading: boolean = false;
  error: string | null = null;

  ngOnInit() {
    const s = getSeoContent('inflation', this.locale.locale());
    this.seo.apply({ title: s.title, description: s.description, keywords: s.keywords, faq: s.faq, path: '/calculator/inflation', isCalculator: true });
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  private calc = new DebouncedCalc<InflationCalculationResponse>(
    () => this.calculatorService.calculateInflation({
      present_value: this.presentValue,
      years: this.years,
      inflation_rate: this.inflationRate,
      calculate_reverse: this.calculateReverse
    } as InflationCalculationRequest),
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

  ngOnDestroy(): void {
    this.calc.destroy();
  }

  formatNumber(value: number | string, decimals: number = 2): string {
    const num = typeof value === 'string' ? parseFloat(value) : value;
    return num.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
  }

  formatCurrency(value: number | string): string {
    const num = typeof value === 'string' ? parseFloat(value) : value;
    return new Intl.NumberFormat('sk-SK', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(num);
  }

  formatPercent(value: number | string): string {
    const num = typeof value === 'string' ? parseFloat(value) : value;
    return num.toFixed(2) + '%';
  }

  getPowerColor(power: number): string {
    if (power >= 90) return '#27ae60'; // Green
    if (power >= 70) return '#2ecc71'; // Light green
    if (power >= 50) return '#f39c12'; // Orange
    if (power >= 30) return '#e67e22'; // Dark orange
    return '#e74c3c'; // Red
  }

  getChangeColor(value: number): string {
    if (value < 0) return '#e74c3c'; // Red (loss)
    if (value > 0) return '#27ae60'; // Green (gain)
    return '#95a5a6'; // Gray (neutral)
  }
}
