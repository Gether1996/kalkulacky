import { Component, OnInit, ChangeDetectorRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { PensionCalculationRequest, PensionCalculationResponse } from '../../models/calculator.models';

@Component({
  selector: 'app-pension-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './pension-calculator.component.html',
  styleUrls: ['./pension-calculator.component.css']
})
export class PensionCalculatorComponent implements OnInit {
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);

  // Input fields
  currentAge: number = 35;
  grossSalary: number = 1500;
  yearsWorked: number = 12;
  gender: 'male' | 'female' = 'male';
  includeSecondPillar: boolean = true;
  secondPillarRate: number = 6.0;
  
  // Results
  result: PensionCalculationResponse | null = null;
  loading: boolean = false;
  error: string = '';

  // Benchmarks for quick input
  salaryBenchmarks = [
    { label: 'Minimálna mzda', value: 750 },
    { label: 'Priemerná mzda', value: 1400 },
    { label: 'Nadpriemerná', value: 2000 },
    { label: 'Vysoká mzda', value: 3000 }
  ];

  ngOnInit() {
    this.calculate();
  }

  setBenchmark(value: number) {
    this.grossSalary = value;
    this.calculate();
  }

  calculate() {
    // Validate inputs
    if (this.currentAge < 18 || this.currentAge > 70) {
      this.error = 'Vek musí byť medzi 18 a 70 rokmi';
      return;
    }
    
    if (this.grossSalary <= 0) {
      this.error = 'Hrubá mzda musí byť väčšia ako 0';
      return;
    }
    
    if (this.yearsWorked < 0 || this.yearsWorked > this.currentAge - 18) {
      this.error = 'Neplatný počet odpracovaných rokov';
      return;
    }

    this.error = '';
    this.loading = true;
    this.result = null;

    const request: PensionCalculationRequest = {
      current_age: this.currentAge,
      gross_salary: this.grossSalary,
      years_worked: this.yearsWorked,
      gender: this.gender,
      include_second_pillar: this.includeSecondPillar,
      second_pillar_rate: this.secondPillarRate
    };

    this.calculatorService.calculatePension(request).subscribe({
      next: (response) => {
        this.result = response;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = err.error?.error || 'Chyba pri výpočte';
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }

  // Helper methods
  formatCurrency(value: number): string {
    return new Intl.NumberFormat('sk-SK', { 
      style: 'currency', 
      currency: 'EUR',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(value);
  }

  formatNumber(value: number): string {
    return new Intl.NumberFormat('sk-SK', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(value);
  }

  formatPercent(value: number): string {
    return `${value.toFixed(1)}%`;
  }

  getReplacementRateColor(rate: number): string {
    if (rate >= 70) return 'green';
    if (rate >= 50) return 'orange';
    return 'red';
  }

  getReplacementRateLabel(rate: number): string {
    if (rate >= 70) return 'Výborná';
    if (rate >= 50) return 'Priemerná';
    return 'Nízka';
  }
}
