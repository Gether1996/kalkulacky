import { Component, ChangeDetectorRef, inject, OnInit, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CalculatorService } from '../../services/calculator.service';
import { 
  HoursWorkedCalculationRequest, 
  HoursWorkedCalculationResponse 
} from '../../models/calculator.models';

@Component({
  selector: 'app-hours-worked-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './hours-worked-calculator.component.html',
  styleUrl: './hours-worked-calculator.component.css'
})
export class HoursWorkedCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);

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
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  calculate() {
    this.loading = true;
    this.error = null;

    const request: HoursWorkedCalculationRequest = {
      hours_worked: this.hoursWorked,
      hourly_rate: this.hourlyRate,
      period_type: this.periodType,
      weekend_hours: this.weekendHours,
      holiday_hours: this.holidayHours
    };

    this.calculatorService.calculateHoursWorked(request).subscribe({
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
