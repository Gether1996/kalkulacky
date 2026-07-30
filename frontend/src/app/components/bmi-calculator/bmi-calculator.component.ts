import { Component, PLATFORM_ID, inject, ChangeDetectorRef, OnInit, OnDestroy } from '@angular/core';
import { LocaleService } from '../../i18n/locale.service';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { BMICalculationResponse } from '../../models/calculator.models';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { SeoService } from '../../services/seo.service';
import { getSeoContent } from '../../i18n/seo';
import { DebouncedCalc } from '../../utils/debounced-calc';

@Component({
  selector: 'app-bmi-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, TranslatePipe],
  templateUrl: './bmi-calculator.component.html',
  styleUrls: ['./bmi-calculator.component.css']
})
export class BmiCalculatorComponent implements OnInit, OnDestroy {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  private locale = inject(LocaleService);
  private seo = inject(SeoService);

  weight: number = 75;
  height: number = 175;
  
  result: BMICalculationResponse | null = null;
  loading: boolean = false;
  error: string | null = null;

  constructor(private calculatorService: CalculatorService) {}

  ngOnInit(): void {
    const s = getSeoContent('bmi', this.locale.locale());
    this.seo.apply({ title: s.title, description: s.description, keywords: s.keywords, faq: s.faq, path: '/calculator/bmi', isCalculator: true });
    // Auto-calculate on component init for immediate results
    this.calculate();
  }

  private calc = new DebouncedCalc<BMICalculationResponse>(
    () => this.calculatorService.calculateBMI({
      weight: this.weight,
      height: this.height
    }),
    (response) => {
      this.result = response;
      this.loading = false;
      this.cdr.detectChanges();
    },
    (err: any) => {
      console.error('BMI calculation error:', err);
      this.error = err.error?.error || this.locale.t('err.calc');
      this.loading = false;
      this.cdr.detectChanges();
    },
  );

  calculate(): void {
    this.loading = true;
    this.error = null;

    this.calc.trigger();
  }

  ngOnDestroy(): void {
    this.calc.destroy();
  }

  formatNumber(num: number): string {
    return new Intl.NumberFormat('sk-SK', {
      minimumFractionDigits: 1,
      maximumFractionDigits: 1
    }).format(num);
  }

  getBMIColor(bmi: number): string {
    if (bmi < 18.5) return '#3498db'; // Blue for underweight
    if (bmi < 25) return '#27ae60'; // Green for normal
    if (bmi < 30) return '#f39c12'; // Orange for overweight
    return '#e74c3c'; // Red for obese
  }

  getBMIBarWidth(bmi: number): number {
    // Scale BMI 15-40 to 0-100%
    const min = 15;
    const max = 40;
    const percentage = ((bmi - min) / (max - min)) * 100;
    return Math.max(0, Math.min(100, percentage));
  }
}
