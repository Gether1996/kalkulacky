import { Component, PLATFORM_ID, inject, ChangeDetectorRef, OnInit } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { MortgageCalculationResponse } from '../../models/calculator.models';
import { SeoService } from '../../services/seo.service';
import { LeadFormComponent } from '../shared/lead-form/lead-form.component';
import { AffiliateCtaComponent } from '../shared/affiliate-cta/affiliate-cta.component';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';
import { EmbedSnippetComponent } from '../shared/embed-snippet/embed-snippet.component';
import { TranslatePipe } from '../../i18n/translate.pipe';

@Component({
  selector: 'app-mortgage-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, LeadFormComponent, AffiliateCtaComponent, AdSlotComponent, EmbedSnippetComponent, TranslatePipe],
  templateUrl: './mortgage-calculator.component.html',
  styleUrls: ['./mortgage-calculator.component.css']
})
export class MortgageCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  private seo = inject(SeoService);
  loanAmount: number = 150000;
  interestRate: number = 3.5;
  loanTerm: number = 25;
  
  result: MortgageCalculationResponse | null = null;
  loading: boolean = false;
  error: string | null = null;
  showAmortization: boolean = false;

  // Common mortgage scenarios
  scenarios = [
    { label: 'Prvé bývanie', amount: 100000, rate: 3.2, years: 25 },
    { label: 'Byt v BA', amount: 150000, rate: 3.5, years: 25 },
    { label: 'Rodinný dom', amount: 200000, rate: 3.8, years: 30 },
    { label: 'Investícia', amount: 100000, rate: 4.2, years: 20 }
  ];

  constructor(private calculatorService: CalculatorService) {}

  ngOnInit(): void {
    this.seo.apply({
      title: 'Hypotekárna kalkulačka 2026 – výpočet splátky hypotéky',
      description: 'Vypočítajte si mesačnú splátku hypotéky, celkové úroky a amortizačnú tabuľku. Porovnajte scenáre a získajte nezáväznú ponuku od hypotekárneho špecialistu.',
      path: '/calculator/mortgage',
      keywords: 'hypotéka kalkulačka, výpočet splátky hypotéky, refinancovanie hypotéky, hypotekárna kalkulačka 2026',
      isCalculator: true,
      faq: [
        {
          question: 'Ako sa počíta mesačná splátka hypotéky?',
          answer: 'Mesačná splátka sa počíta anuitne z výšky úveru, ročnej úrokovej sadzby a doby splácania. Kalkulačka zohľadňuje istinu aj úroky a zobrazí celkové preplatenie.',
        },
        {
          question: 'Oplatí sa refinancovať hypotéku?',
          answer: 'Refinancovanie sa zvyčajne oplatí, ak je nová sadzba výrazne nižšia alebo končí fixácia. Porovnajte súčasnú splátku s ponukou a zohľadnite poplatky za predčasné splatenie.',
        },
      ],
    });

    // Auto-calculate on component init (browser only)
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  /** Calculation snapshot attached to a lead so it is fully qualified. */
  get leadContext(): Record<string, any> {
    return {
      loan_amount: this.loanAmount,
      interest_rate: this.interestRate,
      loan_term_years: this.loanTerm,
      monthly_payment: this.result?.monthly_payment ?? null,
    };
  }

  calculate(): void {
    if (!this.loanAmount || this.loanAmount <= 0) {
      this.error = 'Zadajte platnú výšku úveru';
      return;
    }

    if (!this.interestRate || this.interestRate < 0) {
      this.error = 'Zadajte platnú úrokovú sadzbu';
      return;
    }

    if (!this.loanTerm || this.loanTerm <= 0) {
      this.error = 'Zadajte platnú dĺžku úveru';
      return;
    }

    this.loading = true;
    this.error = null;

    this.calculatorService.calculateMortgage({
      loan_amount: this.loanAmount,
      annual_interest_rate: this.interestRate,
      loan_term_years: this.loanTerm
    }).subscribe({
      next: (data) => {
        this.result = data;
        this.loading = false;
        this.cdr.detectChanges(); // Force change detection
      },
      error: (err) => {
        this.error = 'Chyba pri výpočte. Skúste znova.';
        this.loading = false;
        this.cdr.detectChanges(); // Force change detection
        console.error(err);
      }
    });
  }

  setScenario(scenario: any): void {
    this.loanAmount = scenario.amount;
    this.interestRate = scenario.rate;
    this.loanTerm = scenario.years;
    this.calculate();
  }

  toggleAmortization(): void {
    this.showAmortization = !this.showAmortization;
  }

  formatCurrency(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.00 €';
    }
    return value.toLocaleString('sk-SK', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' €';
  }

  formatPercent(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.00%';
    }
    return value.toFixed(2) + '%';
  }

  getInterestPercentage(): number {
    if (!this.result) return 0;
    return (this.result.total_interest / this.result.loan_amount) * 100;
  }
}
