import { Component, OnInit, ChangeDetectorRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { VacationCalculationRequest, VacationCalculationResponse } from '../../models/calculator.models';

@Component({
  selector: 'app-vacation-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './vacation-calculator.component.html',
  styleUrls: ['./vacation-calculator.component.css']
})
export class VacationCalculatorComponent implements OnInit {
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);

  currentYear: number = new Date().getFullYear();

  // Input fields
  age: number = 35;
  employmentStartDate: string = '';
  currentDate: string = '';
  vacationDaysUsed: number = 0;
  daysCarriedOver: number = 0;
  plannedVacationDays: number = 5;
  
  // Results
  result: VacationCalculationResponse | null = null;
  loading: boolean = false;
  error: string = '';

  // UI helpers
  today: string = '';

  ngOnInit() {
    // Set today's date
    const now = new Date();
    this.today = this.formatDateForInput(now);
    this.currentDate = this.today;
    
    // Set default employment start date (3 years ago)
    const defaultStart = new Date();
    defaultStart.setFullYear(defaultStart.getFullYear() - 3);
    this.employmentStartDate = this.formatDateForInput(defaultStart);
    
    this.calculate();
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
      this.error = 'Vek musí byť medzi 15 a 100 rokmi';
      return;
    }
    
    if (!this.employmentStartDate) {
      this.error = 'Prosím zadajte dátum nástupu do zamestnania';
      return;
    }

    this.error = '';
    this.loading = true;
    this.result = null;

    const request: VacationCalculationRequest = {
      age: this.age,
      employment_start_date: this.employmentStartDate,
      current_date: this.currentDate || this.today,
      vacation_days_used: this.vacationDaysUsed,
      days_carried_over: this.daysCarriedOver,
      planned_vacation_days: this.plannedVacationDays
    };

    this.calculatorService.calculateVacation(request).subscribe({
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
    if (percentage > 100) return 'Prekročený limit';
    if (percentage > 75) return 'Vysoké využitie';
    if (percentage > 50) return 'Stredné využitie';
    return 'Nízke využitie';
  }
}
