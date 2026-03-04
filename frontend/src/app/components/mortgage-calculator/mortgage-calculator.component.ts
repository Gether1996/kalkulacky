import { Component, PLATFORM_ID, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { MortgageCalculationResponse } from '../../models/calculator.models';

@Component({
  selector: 'app-mortgage-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './mortgage-calculator.component.html',
  styleUrls: ['./mortgage-calculator.component.css']
})
export class MortgageCalculatorComponent {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  loanAmount: number = 150000;
  interestRate: number = 3.5;
  loanTerm: number = 25;
  
  result: MortgageCalculationResponse | null = null;
  loading: boolean = false;
  error: string | null = null;
  showAmortization: boolean = false;

  // Common mortgage scenarios
  scenarios = [
    { label: 'Prvé bývanie', amount: 100000, rate: 3.2, years: 25 },
    { label: 'Byt v BA', amount: 150000, rate: 3.5, years: 25 },
    { label: 'Rodinný dom', amount: 200000, rate: 3.8, years: 30 },
    { label: 'Investícia', amount: 100000, rate: 4.2, years: 20 }
  ];

  constructor(private calculatorService: CalculatorService) {
    // No auto-calculate - user inputs have (ngModelChange)="calculate()"
    // so calculation happens automatically when user changes values
  }

  calculate(): void {
    if (!this.loanAmount || this.loanAmount <= 0) {
      this.error = 'Zadajte platnú výšku úveru';
      return;
    }

    if (!this.interestRate || this.interestRate < 0) {
      this.error = 'Zadajte platnú úrokovú sadzbu';
      return;
    }

    if (!this.loanTerm || this.loanTerm <= 0) {
      this.error = 'Zadajte platnú dĺžku úveru';
      return;
    }

    this.loading = true;
    this.error = null;

    this.calculatorService.calculateMortgage({
      loan_amount: this.loanAmount,
      annual_interest_rate: this.interestRate,
      loan_term_years: this.loanTerm
    }).subscribe({
      next: (data) => {
        this.result = data;
        this.loading = false;
        this.cdr.detectChanges(); // Force change detection
      },
      error: (err) => {
        this.error = 'Chyba pri výpočte. Skúste znova.';
        this.loading = false;
        this.cdr.detectChanges(); // Force change detection
        console.error(err);
      }
    });
  }

  setScenario(scenario: any): void {
    this.loanAmount = scenario.amount;
    this.interestRate = scenario.rate;
    this.loanTerm = scenario.years;
    this.calculate();
  }

  toggleAmortization(): void {
    this.showAmortization = !this.showAmortization;
  }

  formatCurrency(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.00 €';
    }
    return value.toLocaleString('sk-SK', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' €';
  }

  formatPercent(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.00%';
    }
    return value.toFixed(2) + '%';
  }

  getInterestPercentage(): number {
    if (!this.result) return 0;
    return (this.result.total_interest / this.result.loan_amount) * 100;
  }
}
