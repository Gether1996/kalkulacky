import { Component, ChangeDetectorRef, inject, OnInit, OnDestroy, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import {
  ROICalculationRequest,
  ROICalculationResponse
} from '../../models/calculator.models';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { DebouncedCalc } from '../../utils/debounced-calc';

@Component({
  selector: 'app-roi-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, TranslatePipe],
  templateUrl: './roi-calculator.component.html',
  styleUrl: './roi-calculator.component.css'
})
export class RoiCalculatorComponent implements OnInit, OnDestroy {
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);
  private platformId = inject(PLATFORM_ID);
  private locale = inject(LocaleService);

  private calc = new DebouncedCalc<ROICalculationResponse | null>(
    () =>
      this.calculatorService.calculateROI({
        initial_investment: this.initialInvestment,
        final_value: this.finalValue,
        additional_costs: this.additionalCosts,
        investment_period_months: this.investmentPeriodMonths,
      } as ROICalculationRequest),
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

  // Input values
  initialInvestment: number = 10000;
  finalValue: number = 15000;
  additionalCosts: number = 0;
  investmentPeriodMonths: number | null = 24;

  // Result
  result: ROICalculationResponse | null = null;
  loading: boolean = false;
  error: string | null = null;

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  calculate() {
    this.loading = true;
    this.error = null;
    this.calc.trigger();
  }

  ngOnDestroy() {
    this.calc.destroy();
  }

  formatNumber(value: number | string | null, decimals: number = 2): string {
    if (value === null) return 'N/A';
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

  getROIColor(roi: number): string {
    if (roi >= 50) return '#27ae60'; // Green
    if (roi >= 20) return '#2ecc71'; // Light green
    if (roi >= 10) return '#f39c12'; // Orange
    if (roi >= 0) return '#e67e22'; // Dark orange
    return '#e74c3c'; // Red
  }
}
