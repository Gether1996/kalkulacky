import { Component, OnInit, OnDestroy, ChangeDetectorRef, PLATFORM_ID, inject } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { PregnancyCalculationRequest, PregnancyCalculationResponse } from '../../models/calculator.models';
import { DatePickerComponent } from '../date-picker/date-picker.component';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { DebouncedCalc } from '../../utils/debounced-calc';

@Component({
  selector: 'app-pregnancy-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, DatePickerComponent, TranslatePipe],
  templateUrl: './pregnancy-calculator.component.html',
  styleUrls: ['./pregnancy-calculator.component.css']
})
export class PregnancyCalculatorComponent implements OnInit, OnDestroy {
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);
  private platformId = inject(PLATFORM_ID);
  private locale = inject(LocaleService);

  // Input fields
  calculationMethod: 'lmp' | 'conception' = 'lmp';
  lmpDate: Date | null = null;
  conceptionDate: Date | null = null;
  currentDate: Date = new Date();
  
  // Results
  result: PregnancyCalculationResponse | null = null;
  loading: boolean = false;
  error: string = '';

  // UI helpers
  today: Date = new Date();
  maxDate: Date = new Date();

  ngOnInit() {
    // Set today's date
    this.today = new Date();
    this.currentDate = new Date();
    
    // Max date is 9 months ago (earliest possible LMP)
    this.maxDate = new Date();
    this.maxDate.setMonth(this.maxDate.getMonth() - 9);
    
    // Set default LMP date to 8 weeks ago for demo
    this.lmpDate = new Date();
    this.lmpDate.setDate(this.lmpDate.getDate() - 56); // 8 weeks

    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
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
      this.error = this.locale.t('err.lmpDate');
      return;
    }
    
    if (this.calculationMethod === 'conception' && !this.conceptionDate) {
      this.error = this.locale.t('err.conceptionDate');
      return;
    }

    this.error = '';
    this.loading = true;
    this.result = null;
    this.calc.trigger();
  }

  // Debounced + cancellable calc pipeline (fixes per-keystroke API storm + race).
  private calc = new DebouncedCalc<PregnancyCalculationResponse>(
    () => {
      const request: PregnancyCalculationRequest = {
        calculation_method: this.calculationMethod,
        current_date: this.formatDateForInput(this.currentDate)
      };

      if (this.calculationMethod === 'lmp' && this.lmpDate) {
        request.lmp_date = this.formatDateForInput(this.lmpDate);
      } else if (this.conceptionDate) {
        request.conception_date = this.formatDateForInput(this.conceptionDate);
      }

      return this.calculatorService.calculatePregnancy(request);
    },
    (response) => {
      this.result = response;
      this.loading = false;
      this.cdr.detectChanges();
    },
    (err: any) => {
      this.error = err.error?.error || this.locale.t('err.calc');
      this.loading = false;
      this.cdr.detectChanges();
    },
  );

  ngOnDestroy() {
    this.calc.destroy();
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
