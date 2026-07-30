import { Component, ChangeDetectorRef, inject, OnInit, OnDestroy, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CalculatorService } from '../../services/calculator.service';
import {
  HoursWorkedCalculationRequest,
  HoursWorkedCalculationResponse
} from '../../models/calculator.models';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { SeoService } from '../../services/seo.service';
import { getSeoContent } from '../../i18n/seo';
import { DebouncedCalc } from '../../utils/debounced-calc';

@Component({
  selector: 'app-hours-worked-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslatePipe],
  templateUrl: './hours-worked-calculator.component.html',
  styleUrl: './hours-worked-calculator.component.css'
})
export class HoursWorkedCalculatorComponent implements OnInit, OnDestroy {
  private platformId = inject(PLATFORM_ID);
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);
  private locale = inject(LocaleService);
  private seo = inject(SeoService);

  private calc = new DebouncedCalc<HoursWorkedCalculationResponse | null>(
    () =>
      this.calculatorService.calculateHoursWorked({
        hours_worked: this.hoursWorked,
        hourly_rate: this.hourlyRate,
        period_type: this.periodType,
        weekend_hours: this.weekendHours,
        holiday_hours: this.holidayHours,
      } as HoursWorkedCalculationRequest),
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
  hoursWorked: number = 48;
  hourlyRate: number | null = 12.50;
  periodType: string = 'weekly';
  weekendHours: number = 0;
  holidayHours: number = 0;

  periodTypes = [
    { value: 'daily', label: 'Deň', icon: '📅' },
    { value: 'weekly', label: 'Týždeň', icon: '📆' },
    { value: 'monthly', label: 'Mesiac', icon: '🗓️' },
    { value: 'custom', label: 'Vlastné', icon: '⚙️' }
  ];

  // Result
  result: HoursWorkedCalculationResponse | null = null;
  loading: boolean = false;
  error: string | null = null;

  ngOnInit(): void {
    const s = getSeoContent('hours-worked', this.locale.locale());
    this.seo.apply({ title: s.title, description: s.description, keywords: s.keywords, faq: s.faq, path: '/calculator/hours-worked', isCalculator: true });
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

  getBalanceColor(category: string): string {
    switch (category) {
      case 'Výborný': return '#27ae60';
      case 'Dobrý': return '#2ecc71';
      case 'Upozornenie': return '#f39c12';
      case 'Kritický': return '#e74c3c';
      default: return '#95a5a6';
    }
  }
}
