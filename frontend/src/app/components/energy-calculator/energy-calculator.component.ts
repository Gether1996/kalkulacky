import { Component, inject, ChangeDetectorRef, OnInit, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CalculatorService } from '../../services/calculator.service';
import { EnergyCalculationResponse } from '../../models/calculator.models';
import { SeoService } from '../../services/seo.service';
import { LeadFormComponent } from '../shared/lead-form/lead-form.component';
import { AffiliateCtaComponent } from '../shared/affiliate-cta/affiliate-cta.component';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';
import { SaveCalculationComponent } from '../shared/save-calculation/save-calculation.component';
import { TranslatePipe } from '../../i18n/translate.pipe';

@Component({
  selector: 'app-energy-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, LeadFormComponent, AffiliateCtaComponent, AdSlotComponent, SaveCalculationComponent, TranslatePipe],
  templateUrl: './energy-calculator.component.html',
  styleUrl: './energy-calculator.component.css'
})
export class EnergyCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private calculatorService = inject(CalculatorService);
  private cdr = inject(ChangeDetectorRef);
  private seo = inject(SeoService);

  // Input values
  electricityConsumption: number = 300;
  gasConsumption: number = 0;
  electricityRate: number = 0.20;
  gasRate: number = 0.06;
  hasDualTariff: boolean = false;
  highTariffPercentage: number = 40;
  householdSize: number = 2;

  // Result
  result: EnergyCalculationResponse | null = null;
  isLoading: boolean = false;
  error: string | null = null;

  get saveParams(): Record<string, any> {
    return {
      electricity_consumption: this.electricityConsumption,
      gas_consumption: this.gasConsumption,
      electricity_rate: this.electricityRate,
      gas_rate: this.gasRate,
      household_size: this.householdSize,
    };
  }
  get saveName(): string { return 'Náklady na energie'; }

  ngOnInit(): void {
    this.seo.apply({
      title: 'Kalkulačka nákladov na energie 2026 (elektrina a plyn)',
      description: 'Vypočítajte mesačné a ročné náklady na elektrinu a plyn, porovnajte spotrebu s priemerom a zistite, či sa vám oplatí fotovoltika.',
      path: '/calculator/energy',
      keywords: 'kalkulačka energie, náklady na elektrinu, cena plynu, fotovoltika návratnosť, dotácia zelená domácnostiam',
      isCalculator: true,
      faq: [
        {
          question: 'Oplatí sa mi fotovoltika?',
          answer: 'Návratnosť fotovoltiky závisí od spotreby, ceny elektriny a výšky dotácie (Zelená domácnostiam). Pri vyššej spotrebe a samospotrebe je návratnosť rýchlejšia. Pre presný odhad získajte nezáväznú ponuku od montážnej firmy.',
        },
        {
          question: 'Aká je priemerná spotreba elektriny domácnosti?',
          answer: 'Priemerná domácnosť spotrebuje rádovo 2 000–4 000 kWh ročne podľa počtu osôb a vykurovania. Kalkulačka porovná vašu spotrebu s priemerom.',
        },
      ],
    });
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  /** Calculation snapshot attached to a solar/installer lead. */
  get leadContext(): Record<string, any> {
    return {
      electricity_consumption: this.electricityConsumption,
      household_size: this.householdSize,
      annual_cost: this.result?.total?.annual_cost ?? null,
    };
  }

  calculate(): void {
    this.isLoading = true;
    this.error = null;
    this.result = null;

    const requestData = {
      electricity_consumption: this.electricityConsumption,
      gas_consumption: this.gasConsumption || 0,
      electricity_rate: this.electricityRate,
      gas_rate: this.gasRate,
      has_dual_tariff: this.hasDualTariff,
      high_tariff_percentage: this.highTariffPercentage,
      household_size: this.householdSize
    };

    this.calculatorService.calculateEnergy(requestData).subscribe({
      next: (data) => {
        this.result = data;
        this.isLoading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = 'Chyba pri výpočte nákladov na energiu. Skontrolujte zadané údaje.';
        this.isLoading = false;
        this.cdr.detectChanges();
        console.error('Energy calculation error:', err);
      }
    });
  }

  formatNumber(value: number | null | undefined, decimals: number = 2): string {
    if (value === null || value === undefined) return '-';
    return value.toFixed(decimals);
  }

  getEfficiencyColor(category: string): string {
    const colors: {[key: string]: string} = {
      'Veľmi úsporná': 'green',
      'Úsporná': 'lightgreen',
      'Priemerná': 'orange',
      'Vysoká spotreba': 'red'
    };
    return colors[category] || 'gray';
  }

  getComparisonClass(percentage: number): string {
    if (percentage < -10) return 'much-below';
    if (percentage < 0) return 'below';
    if (percentage > 10) return 'much-above';
    if (percentage > 0) return 'above';
    return 'average';
  }

  getComparisonText(percentage: number): string {
    if (percentage < -10) return 'Výrazne pod priemerom';
    if (percentage < 0) return 'Pod priemerom';
    if (percentage > 10) return 'Výrazne nad priemerom';
    if (percentage > 0) return 'Nad priemerom';
    return 'Priemer';
  }

  getComparisonIcon(percentage: number): string {
    if (percentage < 0) return '↓';
    if (percentage > 0) return '↑';
    return '=';
  }
}
