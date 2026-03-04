import { Component, PLATFORM_ID, inject, ChangeDetectorRef, OnInit } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { SalaryCalculationResponse } from '../../models/calculator.models';

@Component({
  selector: 'app-salary-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './salary-calculator.component.html',
  styleUrls: ['./salary-calculator.component.css']
})
export class SalaryCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  grossSalary: number = 1500;
  childrenUnder15: number = 0;
  children15To18: number = 0;
  applyNontaxableAmount: boolean = true;
  hasDisability: boolean = false;
  result: SalaryCalculationResponse | null = null;
  loading: boolean = false;
  error: string | null = null;

  // Common salary benchmarks for quick selection
  benchmarks = [
    { label: 'Min. mzda', value: 915 },
    { label: 'Priemer SK', value: 1400 }
  ];

  constructor(private calculatorService: CalculatorService) {}

  ngOnInit(): void {
    // Auto-calculate on component init for immediate results
    this.calculate();
  }

  calculate(): void {
    if (!this.grossSalary || this.grossSalary <= 0) {
      this.error = 'Zadajte platnú hrubú mzdu';
      return;
    }

    console.log('📊 Calculating salary for:', this.grossSalary, 'children under 15:', this.childrenUnder15, '15-18:', this.children15To18, 'NČZD:', this.applyNontaxableAmount, 'ZŤP:', this.hasDisability);
    this.loading = true;
    this.error = null;

    this.calculatorService.calculateSalary({ 
      gross_salary: this.grossSalary,
      children_under_15: this.childrenUnder15,
      children_15_to_18: this.children15To18,
      apply_nontaxable_amount: this.applyNontaxableAmount,
      has_disability: this.hasDisability
    })
      .subscribe({
        next: (data) => {
          console.log('✅ Salary calculated:', data);
          this.result = data;
          this.loading = false;
          this.cdr.detectChanges(); // Force change detection
        },
        error: (err) => {
          console.error('❌ Salary calculation error:', err);
          this.error = 'Chyba pri výpočte. Skúste znova.';
          this.loading = false;
          this.cdr.detectChanges(); // Force change detection
        }
      });
  }

  setBenchmark(value: number): void {
    this.grossSalary = value;
    this.calculate();
  }

  formatCurrency(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.00 €';
    }
    return value.toFixed(2) + ' €';
  }

  formatPercentage(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.0%';
    }
    return value.toFixed(1) + '%';
  }
}
