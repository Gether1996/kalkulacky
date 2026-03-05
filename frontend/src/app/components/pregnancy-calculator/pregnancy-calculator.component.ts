import { Component, OnInit, ChangeDetectorRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { PregnancyCalculationRequest, PregnancyCalculationResponse } from '../../models/calculator.models';

@Component({
  selector: 'app-pregnancy-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './pregnancy-calculator.component.html',
  styleUrls: ['./pregnancy-calculator.component.css']
})
export class PregnancyCalculatorComponent implements OnInit {
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);

  // Input fields
  calculationMethod: 'lmp' | 'conception' = 'lmp';
  lmpDate: string = '';
  conceptionDate: string = '';
  currentDate: string = '';
  
  // Results
  result: PregnancyCalculationResponse | null = null;
  loading: boolean = false;
  error: string = '';

  // UI helpers
  today: string = '';
  maxDate: string = '';

  ngOnInit() {
    // Set today's date in local timezone
    const now = new Date();
    this.today = this.formatDateForInput(now);
    this.currentDate = this.today;
    
    // Max date is 9 months ago (earliest possible LMP)
    const maxLmpDate = new Date();
    maxLmpDate.setMonth(maxLmpDate.getMonth() - 9);
    this.maxDate = this.formatDateForInput(maxLmpDate);
    
    // Set default LMP date to 8 weeks ago for demo
    const defaultLmp = new Date();
    defaultLmp.setDate(defaultLmp.getDate() - 56); // 8 weeks
    this.lmpDate = this.formatDateForInput(defaultLmp);
    
    this.calculate();
  }

  formatDateForInput(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  onMethodChange() {
    // Clear results when method changes
    this.result = null;
    this.error = '';
  }

  calculate() {
    // Validate inputs
    if (this.calculationMethod === 'lmp' && !this.lmpDate) {
      this.error = 'Prosím zadajte dátum poslednej menštruácie';
      return;
    }
    
    if (this.calculationMethod === 'conception' && !this.conceptionDate) {
      this.error = 'Prosím zadajte dátum počatia';
      return;
    }

    this.error = '';
    this.loading = true;
    this.result = null;

    const request: PregnancyCalculationRequest = {
      calculation_method: this.calculationMethod,
      current_date: this.currentDate || this.today
    };

    if (this.calculationMethod === 'lmp') {
      request.lmp_date = this.lmpDate;
    } else {
      request.conception_date = this.conceptionDate;
    }

    this.calculatorService.calculatePregnancy(request).subscribe({
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
  getTrimesterName(trimester: number): string {
    const names = ['', 'Prvý trimester', 'Druhý trimester', 'Tretí trimester'];
    return names[trimester] || '';
  }

  getTrimesterWeeks(trimester: number): string {
    const ranges = ['', '1-12 týždňov', '13-26 týždňov', '27-40 týždňov'];
    return ranges[trimester] || '';
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('sk-SK', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  }

  getWeeksAndDays(totalDays: number): string {
    const weeks = Math.floor(totalDays / 7);
    const days = totalDays % 7;
    return `${weeks} týždňov a ${days} dní`;
  }

  // Trimester milestones
  getTrimesterDescription(trimester: number): string {
    const descriptions = [
      '',
      'Embryo sa vyvíja, tvoria sa základné orgány',
      'Plod rastie, začína sa pohybovať',
      'Plod dospeje, pripravuje sa na pôrod'
    ];
    return descriptions[trimester] || '';
  }
}
