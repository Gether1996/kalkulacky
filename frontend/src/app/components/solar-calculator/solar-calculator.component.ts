import { Component, PLATFORM_ID, inject, ChangeDetectorRef, OnInit, effect } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CalculatorService } from '../../services/calculator.service';
import { SolarSubsidyCalculationResponse } from '../../models/calculator.models';
import { LeadFormComponent } from '../shared/lead-form/lead-form.component';
import { AffiliateCtaComponent } from '../shared/affiliate-cta/affiliate-cta.component';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';
import { EmbedSnippetComponent } from '../shared/embed-snippet/embed-snippet.component';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { getCountryParams } from '../../i18n/country-params';

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
  private calculatorService = inject(CalculatorService);
  private locale = inject(LocaleService);

  // Inputs
  annualConsumption = 4000;
  electricityRate = 0.22;
  includeBattery = false;

  constructor() {
    // Switch country with the language: NZÚ vs Zelená domácnostiam + currency.
    let firstRun = true;
    effect(() => {
      const c = this.country;
      if (!firstRun) {
        this.electricityRate = c === 'CZ' ? 5.0 : 0.22;
      }
      firstRun = false;
      if (isPlatformBrowser(this.platformId)) this.calculate();
    });
  }

  /** Engine country — SK + CZ implemented; other locales fall back to SK. */
  get country(): 'SK' | 'CZ' {
    return getCountryParams(this.locale.locale()).countryCode === 'CZ' ? 'CZ' : 'SK';
  }
  get isSK(): boolean { return this.country === 'SK'; }
  get currency(): string { return this.isSK ? 'EUR' : 'CZK'; }
  get currencySymbol(): string { return this.isSK ? '€' : 'Kč'; }
  get countryName(): string { return this.isSK ? 'Slovensko' : 'Česko'; }
  get programName(): string { return getCountryParams(this.locale.locale()).energyProgram.name; }
  get programUrl(): string { return getCountryParams(this.locale.locale()).energyProgram.url; }
  private get numberLocale(): string { return this.isSK ? 'sk-SK' : 'cs-CZ'; }

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
    // Initial calculation driven by the locale effect (constructor).
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
        country: this.country,
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
    if (value === undefined || value === null || isNaN(value)) return '0 ' + this.currencySymbol;
    return value.toLocaleString(this.numberLocale, { maximumFractionDigits: 0 }) + ' ' + this.currencySymbol;
  }

  formatNumber(value: number | null | undefined, digits = 0): string {
    if (value === undefined || value === null || isNaN(value)) return '0';
    return value.toLocaleString(this.numberLocale, { maximumFractionDigits: digits });
  }
}
