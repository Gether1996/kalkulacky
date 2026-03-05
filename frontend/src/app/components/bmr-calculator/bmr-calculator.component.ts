import { Component, inject, ChangeDetectorRef, OnInit, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CalculatorService } from '../../services/calculator.service';
import { BMRCalculationResponse } from '../../models/calculator.models';

@Component({
  selector: 'app-bmr-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './bmr-calculator.component.html',
  styleUrl: './bmr-calculator.component.css'
})
export class BmrCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);

  // Input values
  weight: number = 75;
  height: number = 175;
  age: number = 30;
  gender: 'male' | 'female' = 'male';
  activityLevel: 'sedentary' | 'light' | 'moderate' | 'active' | 'very_active' = 'moderate';
  weightGoal: 'lose_fast' | 'lose_moderate' | 'lose_slow' | 'maintain' | 'gain_slow' | 'gain_moderate' | 'gain_fast' = 'maintain';

  // Result
  result: BMRCalculationResponse | null = null;
  isLoading: boolean = false;
  error: string | null = null;

  // Activity level labels
  activityLevels = [
    { value: 'sedentary', label: 'Sedavý (žiadne cvičenie)', icon: '🛋️' },
    { value: 'light', label: 'Mierna aktivita (1-3x týždenne)', icon: '🚶' },
    { value: 'moderate', label: 'Stredná aktivita (3-5x týždenne)', icon: '🏃' },
    { value: 'active', label: 'Aktívny (6-7x týždenne)', icon: '🏋️' },
    { value: 'very_active', label: 'Veľmi aktívny (intenzívne)', icon: '💪' }
  ];

  // Weight goal labels
  weightGoals = [
    { value: 'lose_fast', label: 'Rýchle chudnutie (~1kg/týždeň)', icon: '⚡', class: 'lose-fast' },
    { value: 'lose_moderate', label: 'Stredné chudnutie (~0.5kg/týždeň)', icon: '📉', class: 'lose-moderate' },
    { value: 'lose_slow', label: 'Pomalé chudnutie (~0.25kg/týždeň)', icon: '📊', class: 'lose-slow' },
    { value: 'maintain', label: 'Udržanie hmotnosti', icon: '⚖️', class: 'maintain' },
    { value: 'gain_slow', label: 'Pomalé pribieranie (~0.25kg/týždeň)', icon: '📈', class: 'gain-slow' },
    { value: 'gain_moderate', label: 'Stredné pribieranie (~0.5kg/týždeň)', icon: '💪', class: 'gain-moderate' },
    { value: 'gain_fast', label: 'Rýchle pribieranie (~1kg/týždeň)', icon: '🚀', class: 'gain-fast' }
  ];

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  calculate(): void {
    this.isLoading = true;
    this.error = null;
    this.result = null;

    const requestData = {
      weight: this.weight,
      height: this.height,
      age: this.age,
      gender: this.gender,
      activity_level: this.activityLevel,
      weight_goal: this.weightGoal
    };

    this.calculatorService.calculateBMR(requestData).subscribe({
      next: (data) => {
        this.result = data;
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = 'Chyba pri výpočte BMR. Skontrolujte zadané údaje.';
        this.isLoading = false;
        this.cdr.detectChanges();
        console.error('BMR calculation error:', err);
      }
    });
  }

  formatNumber(value: number | null | undefined, decimals: number = 0): string {
    if (value === null || value === undefined) return '-';
    return value.toFixed(decimals);
  }

  getBMICategory(bmi: number): string {
    if (bmi < 18.5) return 'Podvýživa';
    if (bmi < 25) return 'Normálna hmotnosť';
    if (bmi < 30) return 'Nadváha';
    return 'Obezita';
  }

  getBMIColor(bmi: number): string {
    if (bmi < 18.5) return '#3498db';
    if (bmi < 25) return '#27ae60';
    if (bmi < 30) return '#f39c12';
    return '#e74c3c';
  }

  getWeeklyChange(): string {
    if (!this.result || !this.result.recommendations.kg_per_week) return '';
    const kg = this.result.recommendations.kg_per_week;
    if (kg === 0) return 'Bez zmeny';
    return kg > 0 ? `+${this.formatNumber(kg, 2)} kg/týždeň` : `${this.formatNumber(kg, 2)} kg/týždeň`;
  }

  getMacroColor(macroType: string): string {
    const colors: {[key: string]: string} = {
      'protein': '#e74c3c',
      'carbs': '#3498db',
      'fats': '#f39c12'
    };
    return colors[macroType] || '#95a5a6';
  }
}
