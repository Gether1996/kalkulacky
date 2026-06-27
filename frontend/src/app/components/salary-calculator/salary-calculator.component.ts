import { Component, PLATFORM_ID, inject, ChangeDetectorRef, OnInit } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CalculatorService } from '../../services/calculator.service';
import { SalaryCalculationResponse } from '../../models/calculator.models';
import { SeoService } from '../../services/seo.service';
import { AffiliateCtaComponent } from '../shared/affiliate-cta/affiliate-cta.component';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';
import { EmbedSnippetComponent } from '../shared/embed-snippet/embed-snippet.component';
import { TranslatePipe } from '../../i18n/translate.pipe';

@Component({
  selector: 'app-salary-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, AffiliateCtaComponent, AdSlotComponent, EmbedSnippetComponent, TranslatePipe],
  templateUrl: './salary-calculator.component.html',
  styleUrls: ['./salary-calculator.component.css']
})
export class SalaryCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  private seo = inject(SeoService);
  grossSalary: number = 1500;
  childrenUnder15: number = 0;
  children15To18: number = 0;
  applyNontaxableAmount: boolean = true;
  hasDisability: boolean = false;
  result: SalaryCalculationResponse | null = null;
  loading: boolean = false;
  error: string | null = null;

  // Common salary benchmarks for quick selection
  benchmarks = [
    { label: 'Min. mzda', value: 915 },
    { label: 'Priemer SK', value: 1400 }
  ];

  constructor(private calculatorService: CalculatorService) {}

  ngOnInit(): void {
    this.seo.apply({
      title: 'Čistá mzda 2026 – kalkulačka výplaty (hrubá → čistá)',
      description: 'Vypočítajte si čistú mzdu z hrubej mzdy pre rok 2026. Kalkulačka zohľadňuje odvody, daň, nezdaniteľnú časť a daňový bonus na deti.',
      path: '/calculator/salary',
      keywords: 'čistá mzda kalkulačka, výpočet čistej mzdy 2026, hrubá mzda na čistú, výplata kalkulačka',
      isCalculator: true,
      faq: [
        {
          question: 'Ako sa počíta čistá mzda z hrubej?',
          answer: 'Od hrubej mzdy sa odpočítajú odvody do Sociálnej a zdravotnej poisťovne (9,4 % + 5 %), uplatní sa nezdaniteľná časť základu dane a vypočíta sa daň z príjmu. Výsledok znížený o daň je čistá mzda, ku ktorej sa pripočíta daňový bonus na deti.',
        },
        {
          question: 'Aký je daňový bonus na dieťa v roku 2026?',
          answer: 'Daňový bonus závisí od veku dieťaťa a výšky príjmu. Kalkulačka ho automaticky zohľadní podľa počtu detí do 15 rokov a od 15 do 18 rokov.',
        },
      ],
    });

    // Calculate on init only if running in browser
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  calculate(): void {
    if (!this.grossSalary || this.grossSalary <= 0) {
      this.error = 'Zadajte platnú hrubú mzdu';
      return;
    }

    console.log('📊 Calculating salary for:', this.grossSalary, 'children under 15:', this.childrenUnder15, '15-18:', this.children15To18, 'NČZD:', this.applyNontaxableAmount, 'ZŤP:', this.hasDisability);
    this.loading = true;
    this.error = null;

    this.calculatorService.calculateSalary({ 
      gross_salary: this.grossSalary,
      children_under_15: this.childrenUnder15,
      children_15_to_18: this.children15To18,
      apply_nontaxable_amount: this.applyNontaxableAmount,
      has_disability: this.hasDisability
    })
      .subscribe({
        next: (data) => {
          console.log('✅ Salary calculated:', data);
          this.result = data;
          this.loading = false;
          this.cdr.detectChanges(); // Force change detection
        },
        error: (err) => {
          console.error('❌ Salary calculation error:', err);
          this.error = 'Chyba pri výpočte. Skúste znova.';
          this.loading = false;
          this.cdr.detectChanges(); // Force change detection
        }
      });
  }

  setBenchmark(value: number): void {
    this.grossSalary = value;
    this.calculate();
  }

  formatCurrency(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.00 €';
    }
    return value.toFixed(2) + ' €';
  }

  formatPercentage(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.0%';
    }
    return value.toFixed(1) + '%';
  }
}
