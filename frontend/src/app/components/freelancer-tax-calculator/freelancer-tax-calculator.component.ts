import { Component, ChangeDetectorRef, inject, OnInit, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CalculatorService } from '../../services/calculator.service';
import { 
  FreelancerTaxCalculationRequest, 
  FreelancerTaxCalculationResponse 
} from '../../models/calculator.models';

@Component({
  selector: 'app-freelancer-tax-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './freelancer-tax-calculator.component.html',
  styleUrl: './freelancer-tax-calculator.component.css'
})
export class FreelancerTaxCalculatorComponent implements OnInit {
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);
  private platformId = inject(PLATFORM_ID);

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

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  calculate() {
    this.loading = true;
    this.error = null;

    const request: FreelancerTaxCalculationRequest = {
      annual_revenue: this.annualRevenue,
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
