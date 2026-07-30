import { Component, OnInit, OnDestroy, ChangeDetectorRef, PLATFORM_ID, inject, effect } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { ParentalBenefitCalculationRequest, ParentalBenefitCalculationResponse } from '../../models/calculator.models';
import { DatePickerComponent } from '../date-picker/date-picker.component';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { getCountryParams } from '../../i18n/country-params';
import { DebouncedCalc } from '../../utils/debounced-calc';

@Component({
  selector: 'app-parental-benefit-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, DatePickerComponent, TranslatePipe],
  templateUrl: './parental-benefit-calculator.component.html',
  styleUrls: ['./parental-benefit-calculator.component.css']
})
export class ParentalBenefitCalculatorComponent implements OnInit, OnDestroy {
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);
  private platformId = inject(PLATFORM_ID);

  // Input fields
  birthDate: string = '';
  grossSalary: number | null = null;
  benefitType: 'basic' | 'alternative' = 'basic';
  twinsOrMore: boolean = false;
  planToWork: boolean = false;
  plannedMonthlyIncome: number = 0;
  secondChildBirthDate: string = '';
  currentDate: string = '';
  
  // Results
  result: ParentalBenefitCalculationResponse | null = null;
  loading: boolean = false;
  error: string = '';

  // UI helpers
  today: Date = new Date();
  maxDate: Date | null = null;

  private locale = inject(LocaleService);

  /** Engine country — SK + CZ implemented; other locales fall back to SK. */
  get country(): string {
    return getCountryParams(this.locale.locale()).countryCode === 'CZ' ? 'CZ' : 'SK';
  }
  get isSK(): boolean { return this.country === 'SK'; }
  get currency(): string { return this.isSK ? 'EUR' : 'CZK'; }
  get countryName(): string { return this.isSK ? 'Slovensko' : 'Česko'; }
  private get numberLocale(): string { return this.isSK ? 'sk-SK' : 'cs-CZ'; }

  constructor() {
    effect(() => {
      const c = this.country;
      if (this.birthDate) {
        if (this.grossSalary != null) this.grossSalary = c === 'CZ' ? 45000 : 1400;
        if (isPlatformBrowser(this.platformId)) this.calculate();
      }
    });
  }

  ngOnInit() {
    // Set today's date
    const now = new Date();
    this.today = now;
    this.currentDate = this.formatDateForInput(now);
    
    // Note: Not setting maxDate as we want to allow any date in the past for birth date
    
    // Set default birth date (6 months ago)
    const defaultBirth = new Date();
    defaultBirth.setMonth(defaultBirth.getMonth() - 6);
    this.birthDate = this.formatDateForInput(defaultBirth);
    
    // Default salary
    this.grossSalary = 1400;

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

  onBenefitTypeChange() {
    this.result = null;
    this.error = '';
  }

  calculate() {
    // Validate inputs
    if (!this.birthDate) {
      this.error = this.locale.t('err.birthDate');
      return;
    }

    this.error = '';
    this.loading = true;
    this.result = null;
    this.calc.trigger();
  }

  // Debounced + cancellable calc pipeline (fixes per-keystroke API storm + race).
  private calc = new DebouncedCalc<ParentalBenefitCalculationResponse>(
    () => this.calculatorService.calculateParentalBenefit({
      birth_date: this.birthDate,
      country: this.country,
      gross_salary: this.grossSalary || undefined,
      benefit_type: this.benefitType,
      twins_or_more: this.twinsOrMore,
      plan_to_work: this.planToWork,
      planned_monthly_income: this.plannedMonthlyIncome,
      second_child_birth_date: this.secondChildBirthDate || undefined,
      current_date: this.currentDate || this.formatDateForInput(this.today)
    } as ParentalBenefitCalculationRequest),
    (response) => {
      this.result = response;
      this.error = '';
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

  formatDate(dateString: string | null): string {
    if (!dateString) return '';
    const date = new Date(dateString);
    const options: Intl.DateTimeFormatOptions = { 
      day: 'numeric', 
      month: 'long', 
      year: 'numeric' 
    };
    return date.toLocaleDateString('sk-SK', options);
  }

  formatCurrency(amount: number): string {
    const noDecimals = this.currency === 'CZK';
    return new Intl.NumberFormat(this.numberLocale, {
      style: 'currency',
      currency: this.currency,
      minimumFractionDigits: noDecimals ? 0 : 2,
      maximumFractionDigits: noDecimals ? 0 : 2
    }).format(amount);
  }

  getBenefitTypeName(type: string): string {
    switch(type) {
      case 'basic': return 'Rodičovská osnova';
      case 'alternative': return 'Rodičovská alternatíva';
      default: return type;
    }
  }

  getChildAgeLabel(months: number, years: number): string {
    if (years > 0) {
      if (months % 12 === 0) {
        return `${years} ${years === 1 ? 'rok' : years < 5 ? 'roky' : 'rokov'}`;
      }
      const remainingMonths = months % 12;
      return `${years} ${years === 1 ? 'rok' : years < 5 ? 'roky' : 'rokov'} a ${remainingMonths} ${remainingMonths === 1 ? 'mesiac' : remainingMonths < 5 ? 'mesiace' : 'mesiacov'}`;
    }
    return `${months} ${months === 1 ? 'mesiac' : months < 5 ? 'mesiace' : 'mesiacov'}`;
  }

  getBenefitStatusClass(status: string): string {
    if (status.includes('poberáte')) return 'status-active';
    if (status.includes('materskej')) return 'status-maternity';
    if (status.includes('skončil')) return 'status-expired';
    return 'status-default';
  }

  getNotificationPriorityClass(priority: string): string {
    switch(priority) {
      case 'urgent': return 'notification-urgent';
      case 'high': return 'notification-high';
      case 'medium': return 'notification-medium';
      default: return 'notification-low';
    }
  }

  // Expose Math for template
  Math = Math;
}
