import { Component, PLATFORM_ID, inject, ChangeDetectorRef, OnInit, OnDestroy } from '@angular/core';
import { LocaleService } from '../../i18n/locale.service';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { LoanCalculationResponse } from '../../models/calculator.models';
import { SeoService } from '../../services/seo.service';
import { AffiliateCtaComponent } from '../shared/affiliate-cta/affiliate-cta.component';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';
import { SaveCalculationComponent } from '../shared/save-calculation/save-calculation.component';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { getSeoContent } from '../../i18n/seo';
import { DebouncedCalc } from '../../utils/debounced-calc';

@Component({
  selector: 'app-loan-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, AffiliateCtaComponent, AdSlotComponent, SaveCalculationComponent, TranslatePipe],
  templateUrl: './loan-calculator.component.html',
  styleUrls: ['./loan-calculator.component.css']
})
export class LoanCalculatorComponent implements OnInit, OnDestroy {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  private locale = inject(LocaleService);
  
  loanAmount: number = 50000;
  interestRate: number = 5.5;
  loanYears: number = 10;
  includeSchedule: boolean = false;
  
  result: LoanCalculationResponse | null = null;
  loading: boolean = false;
  error: string | null = null;

  // Common loan amounts for quick selection
  loanBenchmarks = [
    { label: '10 000 €', value: 10000 },
    { label: '25 000 €', value: 25000 },
    { label: '50 000 €', value: 50000 },
    { label: '100 000 €', value: 100000 }
  ];

  private seo = inject(SeoService);

  constructor(private calculatorService: CalculatorService) {}

  ngOnInit(): void {
    const s = getSeoContent('loan', this.locale.locale());
    this.seo.apply({
      title: s.title,
      description: s.description,
      keywords: s.keywords,
      faq: s.faq,
      path: '/calculator/loan',
      isCalculator: true,
    });
    // Auto-calculate on component init (browser only) for immediate results
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  private calc = new DebouncedCalc<LoanCalculationResponse>(
    () => this.calculatorService.calculateLoan({
      loan_amount: this.loanAmount,
      interest_rate: this.interestRate,
      loan_years: this.loanYears,
      include_schedule: this.includeSchedule
    }),
    (response) => {
      this.result = response;
      this.loading = false;
      this.cdr.detectChanges();
    },
    (err: any) => {
      console.error('Loan calculation error:', err);
      this.error = err.error?.error || this.locale.t('err.calc');
      this.loading = false;
      this.cdr.detectChanges();
    },
  );

  calculate(): void {
    this.loading = true;
    this.error = null;

    this.calc.trigger();
  }

  ngOnDestroy(): void {
    this.calc.destroy();
  }

  selectBenchmark(value: number): void {
    this.loanAmount = value;
    this.calculate();
  }

  get saveParams(): Record<string, any> {
    return { loan_amount: this.loanAmount, interest_rate: this.interestRate, loan_years: this.loanYears };
  }
  get saveName(): string { return `Úver · ${this.loanAmount} € · ${this.loanYears} r`; }

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('sk-SK', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount);
  }

  formatNumber(num: number): string {
    return new Intl.NumberFormat('sk-SK', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(num);
  }

  getMonthLabel(month: number): string {
    const years = Math.floor((month - 1) / 12) + 1;
    const monthInYear = ((month - 1) % 12) + 1;
    return `Rok ${years}, Mesiac ${monthInYear}`;
  }

  // Show only first 12 months, last 12 months, and some middle months
  getSchedulePreview(): any[] {
    if (!this.result?.amortization_schedule) return [];
    
    const schedule = this.result.amortization_schedule;
    if (schedule.length <= 36) return schedule;
    
    // Show first 12, middle 12, and last 12 months
    return [
      ...schedule.slice(0, 12),
      { month: -1, payment: 0, principal_payment: 0, interest_payment: 0, remaining_balance: 0 }, // Separator
      ...schedule.slice(Math.floor(schedule.length / 2) - 6, Math.floor(schedule.length / 2) + 6),
      { month: -1, payment: 0, principal_payment: 0, interest_payment: 0, remaining_balance: 0 }, // Separator
      ...schedule.slice(-12)
    ];
  }
}
