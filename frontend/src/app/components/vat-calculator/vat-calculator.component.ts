import { Component, OnInit, PLATFORM_ID, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { VATCalculationRequest, VATCalculationResponse } from '../../models/calculator.models';

@Component({
  selector: 'app-vat-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './vat-calculator.component.html',
  styleUrl: './vat-calculator.component.css'
})
export class VatCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  // Inputs
  amount: number = 1000;
  vatRate: number = 23;  // Updated for 2026: 23% standard rate
  calculation_type: 'add_vat' | 'remove_vat' = 'add_vat';
  
  // Results
  result: VATCalculationResponse | null = null;
  isLoading = false;
  error: string | null = null;

  // Quick scenarios
  scenarios = [
    { label: 'Nákup spotrebiteľa', icon: '🛒', amount: 500 },
    { label: 'Firemný nákup', icon: '🏢', amount: 5000 },
    { label: 'Veľkoobchod', icon: '📦', amount: 20000 },
    { label: 'Služba/freelance', icon: '💼', amount: 1500 }
  ];

  constructor(private calculatorService: CalculatorService) {}

  ngOnInit() {
    // No auto-calculate - user inputs have (ngModelChange)="calculate()"
    // so calculation happens automatically when user changes values
  }

  calculate() {
    if (this.amount <= 0) {
      this.error = 'Čiastka musí byť väčšia ako 0';
      return;
    }

    this.isLoading = true;
    this.error = null;

    const request: VATCalculationRequest = {
      amount: this.amount,
      vat_rate: this.vatRate,
      calculation_type: this.calculation_type
    };

    this.calculatorService.calculateVAT(request).subscribe({
      next: (response) => {
        this.result = response;
        this.isLoading = false;
        this.cdr.detectChanges(); // Force change detection
      },
      error: (err) => {
        console.error('VAT Calculation error:', err);
        this.error = 'Chyba pri výpočte. Skúste to znova.';
        this.isLoading = false;
        this.cdr.detectChanges(); // Force change detection
      }
    });
  }

  applyScenario(amount: number) {
    this.amount = amount;
    this.calculate();
  }

  formatCurrency(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.00';
    }
    return new Intl.NumberFormat('sk-SK', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(value);
  }
}
