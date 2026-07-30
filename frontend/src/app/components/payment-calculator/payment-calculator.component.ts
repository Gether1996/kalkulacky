import { Component, inject, ChangeDetectorRef, OnInit, OnDestroy, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CalculatorService } from '../../services/calculator.service';
import { PaymentCalculationResponse } from '../../models/calculator.models';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { DebouncedCalc } from '../../utils/debounced-calc';

@Component({
  selector: 'app-payment-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslatePipe],
  templateUrl: './payment-calculator.component.html',
  styleUrl: './payment-calculator.component.css'
})
export class PaymentCalculatorComponent implements OnInit, OnDestroy {
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);
  private platformId = inject(PLATFORM_ID);

  private calc = new DebouncedCalc<PaymentCalculationResponse | null>(
    () =>
      this.calculatorService.calculatePayment({
        loan_amount: this.loanAmount,
        annual_interest_rate: this.annualInterestRate,
        loan_term_years: this.loanTermYears,
        payment_frequency: this.paymentFrequency,
        include_schedule: this.includeSchedule,
      }),
    (data) => {
      this.result = data;
      this.isLoading = false;
      this.cdr.detectChanges();
    },
    (err) => {
      this.error = 'Chyba pri výpočte splátky. Skontrolujte zadané údaje.';
      this.isLoading = false;
      this.cdr.detectChanges();
      console.error('Payment calculation error:', err);
    },
  );

  // Input values
  loanAmount: number = 50000;
  annualInterestRate: number = 5.5;
  loanTermYears: number = 10;
  paymentFrequency: 'monthly' | 'quarterly' | 'yearly' = 'monthly';
  includeSchedule: boolean = false;

  // Result
  result: PaymentCalculationResponse | null = null;
  isLoading: boolean = false;
  error: string | null = null;

  // Payment frequency options
  frequencies = [
    { value: 'monthly', label: 'Mesačne', icon: '📆' },
    { value: 'quarterly', label: 'Štvrťročne', icon: '📅' },
    { value: 'yearly', label: 'Ročne', icon: '🗓️' }
  ];

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  calculate(): void {
    this.isLoading = true;
    this.error = null;
    this.result = null;
    this.calc.trigger();
  }

  ngOnDestroy(): void {
    this.calc.destroy();
  }

  formatNumber(value: number | null | undefined, decimals: number = 2): string {
    if (value === null || value === undefined) return '-';
    return value.toFixed(decimals);
  }

  formatCurrency(value: number | null | undefined): string {
    if (value === null || value === undefined) return '-';
    return new Intl.NumberFormat('sk-SK', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 2
    }).format(value);
  }

  getPercentageColor(percentage: number): string {
    if (percentage > 50) return '#e74c3c';
    if (percentage > 30) return '#f39c12';
    return '#27ae60';
  }
}
