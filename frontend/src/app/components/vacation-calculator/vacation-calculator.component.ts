import { Component, OnInit, OnDestroy, ChangeDetectorRef, PLATFORM_ID, inject, effect } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { VacationCalculationRequest, VacationCalculationResponse } from '../../models/calculator.models';
import { DatePickerComponent } from '../date-picker/date-picker.component';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { getCountryParams } from '../../i18n/country-params';
import { DebouncedCalc } from '../../utils/debounced-calc';
import { SeoService } from '../../services/seo.service';
import { getSeoContent } from '../../i18n/seo';

@Component({
  selector: 'app-vacation-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, DatePickerComponent, TranslatePipe],
  templateUrl: './vacation-calculator.component.html',
  styleUrls: ['./vacation-calculator.component.css']
})
export class VacationCalculatorComponent implements OnInit, OnDestroy {
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);
  private platformId = inject(PLATFORM_ID);
  private seo = inject(SeoService);

  currentYear: number = new Date().getFullYear();

  // Input fields
  age: number = 35;
  employmentStartDate: Date | null = null;
  currentDate: Date = new Date();
  vacationDaysUsed: number = 0;
  daysCarriedOver: number = 0;
  plannedVacationDays: number = 5;
  
  // Results
  result: VacationCalculationResponse | null = null;
  loading: boolean = false;
  error: string = '';

  // UI helpers
  today: Date = new Date();

  private locale = inject(LocaleService);

  /** Engine country — SK + CZ implemented; other locales fall back to SK. */
  get country(): string {
    return getCountryParams(this.locale.locale()).countryCode;
  }
  get isSK(): boolean { return this.country === 'SK'; }
  get countryName(): string { return getCountryParams(this.locale.locale()).countryName; }

  constructor() {
    effect(() => {
      this.country; // re-run when language/country changes
      if (this.employmentStartDate && isPlatformBrowser(this.platformId)) {
        this.calculate();
      }
    });
  }

  ngOnInit() {
    const s = getSeoContent('vacation', this.locale.locale());
    this.seo.apply({ title: s.title, description: s.description, keywords: s.keywords, faq: s.faq, path: '/calculator/vacation', isCalculator: true });
    // Set today's date
    this.today = new Date();
    this.currentDate = new Date();

    // Set default employment start date (3 years ago)
    this.employmentStartDate = new Date();
    this.employmentStartDate.setFullYear(this.employmentStartDate.getFullYear() - 3);

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

  calculate() {
    // Validate inputs
    if (this.age < 15 || this.age > 100) {
      this.error = this.locale.t('vacation.errAge');
      return;
    }

    if (!this.employmentStartDate) {
      this.error = this.locale.t('vacation.errStartDate');
      return;
    }

    this.error = '';
    this.loading = true;
    this.result = null;
    this.calc.trigger();
  }

  // Debounced + cancellable calc pipeline (fixes per-keystroke API storm + race).
  private calc = new DebouncedCalc<VacationCalculationResponse>(
    () => this.calculatorService.calculateVacation({
      age: this.age,
      employment_start_date: this.formatDateForInput(this.employmentStartDate || this.today),
      current_date: this.formatDateForInput(this.currentDate),
      vacation_days_used: this.vacationDaysUsed,
      days_carried_over: this.daysCarriedOver,
      planned_vacation_days: this.plannedVacationDays,
      country: this.country
    } as VacationCalculationRequest),
    (response) => {
      this.result = response;
      this.loading = false;
      this.cdr.detectChanges();
    },
    (err: any) => {
      this.error = err.error?.error || this.locale.t('common.error');
      this.loading = false;
      this.cdr.detectChanges();
    },
  );

  ngOnDestroy() {
    this.calc.destroy();
  }

  // Helper methods
  formatNumber(value: number): string {
    return new Intl.NumberFormat('sk-SK', {
      minimumFractionDigits: 0,
      maximumFractionDigits: 1
    }).format(value);
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('sk-SK', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  }

  getUsageStatusColor(percentage: number): string {
    if (percentage > 100) return 'red';
    if (percentage > 75) return 'orange';
    if (percentage > 50) return 'yellow';
    return 'green';
  }

  getUsageStatusLabel(percentage: number): string {
    if (percentage > 100) return this.locale.t('vacation.statusOver');
    if (percentage > 75) return this.locale.t('vacation.statusHigh');
    if (percentage > 50) return this.locale.t('vacation.statusMedium');
    return this.locale.t('vacation.statusLow');
  }
}
