import { Component, OnInit, ChangeDetectorRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { ParentalBenefitCalculationRequest, ParentalBenefitCalculationResponse } from '../../models/calculator.models';
import { DatePickerComponent } from '../date-picker/date-picker.component';

@Component({
  selector: 'app-parental-benefit-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, DatePickerComponent],
  templateUrl: './parental-benefit-calculator.component.html',
  styleUrls: ['./parental-benefit-calculator.component.css']
})
export class ParentalBenefitCalculatorComponent implements OnInit {
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);

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
    
    this.calculate();
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
      this.error = 'Prosím zadajte dátum narodenia dieťaťa';
      return;
    }

    this.error = '';
    this.loading = true;
    this.result = null;

    const request: ParentalBenefitCalculationRequest = {
      birth_date: this.birthDate,
      gross_salary: this.grossSalary || undefined,
      benefit_type: this.benefitType,
      twins_or_more: this.twinsOrMore,
      plan_to_work: this.planToWork,
      planned_monthly_income: this.plannedMonthlyIncome,
      second_child_birth_date: this.secondChildBirthDate || undefined,
      current_date: this.currentDate || this.formatDateForInput(this.today)
    };

    this.calculatorService.calculateParentalBenefit(request).subscribe({
      next: (response) => {
        this.result = response;
        this.error = '';
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = err.error?.error || 'Chyba pri výpočte rodičovského príspevku';
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
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
    return new Intl.NumberFormat('sk-SK', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
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
