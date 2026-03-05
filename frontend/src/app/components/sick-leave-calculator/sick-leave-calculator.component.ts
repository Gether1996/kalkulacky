import { Component, OnInit, PLATFORM_ID, inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CalculatorService } from '../../services/calculator.service';
import { SickLeaveCalculationResponse } from '../../models/calculator.models';

@Component({
  selector: 'app-sick-leave-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule],
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

  constructor(private calculatorService: CalculatorService) {}

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
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
      leave_type: this.leave_type
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

  // Helper to get payer badge color
  getPayerBadgeClass(payer: string): string {
    return payer === 'Zamestnávateľ' ? 'payer-employer' : 'payer-insurance';
  }

  // Format currency
  formatCurrency(value: number): string {
    return new Intl.NumberFormat('sk-SK', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
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
