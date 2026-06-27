import { Component, PLATFORM_ID, inject, ChangeDetectorRef, OnInit } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CalculatorService } from '../../services/calculator.service';
import { SolarSubsidyCalculationResponse } from '../../models/calculator.models';
import { SeoService } from '../../services/seo.service';
import { LeadFormComponent } from '../shared/lead-form/lead-form.component';
import { AffiliateCtaComponent } from '../shared/affiliate-cta/affiliate-cta.component';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';
import { EmbedSnippetComponent } from '../shared/embed-snippet/embed-snippet.component';
import { TranslatePipe } from '../../i18n/translate.pipe';

@Component({
  selector: 'app-solar-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, LeadFormComponent, AffiliateCtaComponent, AdSlotComponent, EmbedSnippetComponent, TranslatePipe],
  templateUrl: './solar-calculator.component.html',
  styleUrls: ['./solar-calculator.component.css'],
})
export class SolarCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  private seo = inject(SeoService);
  private calculatorService = inject(CalculatorService);

  // Inputs
  annualConsumption = 4000;
  electricityRate = 0.22;
  includeBattery = false;

  result: SolarSubsidyCalculationResponse | null = null;
  loading = false;
  error: string | null = null;

  // Quick presets by household type
  presets = [
    { label: 'Byt / malá domácnosť', kwh: 2500 },
    { label: 'Rodinný dom', kwh: 4000 },
    { label: 'Dom s tepelným čerpadlom', kwh: 7000 },
    { label: 'Dom + elektromobil', kwh: 9000 },
  ];

  ngOnInit(): void {
    this.seo.apply({
      title: 'Kalkulačka fotovoltiky 2026 – dotácia a návratnosť',
      description: 'Vypočítajte odporúčaný výkon fotovoltiky, dotáciu Zelená domácnostiam, náklady, ročnú úsporu a návratnosť. Získajte nezáväznú ponuku od montážnej firmy.',
      path: '/calculator/solar',
      keywords: 'kalkulačka fotovoltiky, dotácia na fotovoltiku 2026, zelená domácnostiam, návratnosť fotovoltiky, cena fotovoltiky',
      isCalculator: true,
      faq: [
        {
          question: 'Akú dotáciu môžem získať na fotovoltiku?',
          answer: 'Cez program Zelená domácnostiam je príspevok 500 €/kW inštalovaného výkonu, oprávnené sú 3 kW (po preukázaní spotreby až 7 kW). Maximálna dotácia je 3 500 € (so zvýhodnením +15 % až 4 025 €) a zároveň najviac 50 % oprávnených nákladov. Výška a podmienky sa menia podľa aktuálneho kola SIEA.',
        },
        {
          question: 'Aká je návratnosť fotovoltiky na Slovensku?',
          answer: 'Návratnosť závisí od spotreby, ceny elektriny, samospotreby a dotácie. Pri bežnej domácnosti býva orientačne 7–11 rokov, pričom panely vydržia 25+ rokov.',
        },
        {
          question: 'Oplatí sa k fotovoltike batéria?',
          answer: 'Batéria zvyšuje podiel vlastnej spotreby (z ~40 % na ~75 %), čím rastie úspora, no predlžuje návratnosť kvôli vyššej cene. Vyplatí sa pri vyššej večernej spotrebe.',
        },
      ],
    });
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  setPreset(kwh: number): void {
    this.annualConsumption = kwh;
    this.calculate();
  }

  calculate(): void {
    if (!this.annualConsumption || this.annualConsumption <= 0) {
      this.error = 'Zadajte ročnú spotrebu elektriny';
      return;
    }
    this.loading = true;
    this.error = null;
    this.calculatorService
      .calculateSolarSubsidy({
        annual_consumption_kwh: this.annualConsumption,
        electricity_rate: this.electricityRate,
        include_battery: this.includeBattery,
      })
      .subscribe({
        next: (data) => {
          this.result = data;
          this.loading = false;
          this.cdr.detectChanges();
        },
        error: (err) => {
          this.error = 'Chyba pri výpočte. Skúste znova.';
          this.loading = false;
          this.cdr.detectChanges();
          console.error(err);
        },
      });
  }

  /** Snapshot attached to the installer lead. */
  get leadContext(): Record<string, any> {
    return {
      annual_consumption_kwh: this.annualConsumption,
      recommended_kwp: this.result?.system?.recommended_kwp ?? null,
      include_battery: this.includeBattery,
      net_cost: this.result?.subsidy?.net_cost ?? null,
    };
  }

  formatCurrency(value: number | null | undefined): string {
    if (value === undefined || value === null || isNaN(value)) return '0 €';
    return value.toLocaleString('sk-SK', { maximumFractionDigits: 0 }) + ' €';
  }

  formatNumber(value: number | null | undefined, digits = 0): string {
    if (value === undefined || value === null || isNaN(value)) return '0';
    return value.toLocaleString('sk-SK', { maximumFractionDigits: digits });
  }
}
