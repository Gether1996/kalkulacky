import { Component, PLATFORM_ID, inject, OnInit, effect } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { LeadFormComponent } from '../shared/lead-form/lead-form.component';
import { AffiliateCtaComponent } from '../shared/affiliate-cta/affiliate-cta.component';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { getCountryParams } from '../../i18n/country-params';

/**
 * Heat-pump sizing, cost & savings estimator (V4 report idea #8, score 7.28).
 * Part of the "home-energy hub" — qualifies a homeowner and routes them to an
 * installer (lead vertical `heat_pump`, already defined in the backend Lead model).
 *
 * The calculation is INDICATIVE and runs client-side (like the solar tool's
 * browser-side calculate()); the SEO shell (title/meta/JSON-LD/intro) is still
 * server-rendered. All constants are centralised here for easy yearly updates.
 */

// --- Tunable indicative constants per country (update per subsidy round) ------
const DHW_KWH_PER_YEAR = 1800;        // hot-water demand (indicative)
const SCOP = 3.5;                      // seasonal COP for a modern air-water HP
const CO2_KG_PER_KWH_GRID = 0.20;      // grid CO2 intensity

interface CountryHeatPumpConfig {
  electricityPrice: number;   // per kWh for the HP's electricity
  costBase: number;           // min turnkey cost
  costPerKw: number;          // turnkey cost per kW of output
  subsidyPerKw: number;       // subsidy per kW
  subsidyMax: number;         // subsidy cap
  fuel: Record<string, number>; // cost per kWh of delivered heat by fuel
}

const HP_CONFIG: Record<'SK' | 'CZ', CountryHeatPumpConfig> = {
  // SK — Zelená domácnostiam (INDICATIVE).
  SK: {
    electricityPrice: 0.18, costBase: 9000, costPerKw: 1400,
    subsidyPerKw: 380, subsidyMax: 3400,
    fuel: { gas: 0.10, electric: 0.18, coal: 0.08, oil: 0.13, wood: 0.06 },
  },
  // CZ — Nová zelená úsporám (INDICATIVE, CZK). Flat ~80 000 Kč air-water grant.
  CZ: {
    electricityPrice: 5.0, costBase: 220000, costPerKw: 30000,
    subsidyPerKw: 8000, subsidyMax: 80000,
    fuel: { gas: 2.0, electric: 5.0, coal: 1.5, oil: 3.0, wood: 1.2 },
  },
};
const SUBSIDY_RATE_OF_COST = 0.5;      // ≤ 50 % of eligible cost (both countries)

interface InsulationOption {
  key: string;
  labelKey: string;
  specificDemand: number; // kWh/m²/year for space heating
  loadFactor: number;     // kW of heat loss per m² (design load)
}

interface HeatingOption {
  key: string;
  labelKey: string;
  costPerKwh: number;     // € per kWh of delivered heat (efficiency folded in)
}

interface HeatPumpResult {
  annualHeatDemand: number;
  recommendedKw: number;
  hpType: string;
  totalCost: number;
  subsidy: number;
  netCost: number;
  currentAnnualCost: number;
  hpAnnualCost: number;
  annualSavings: number;
  paybackYears: number | null;
  savings15y: number;
  co2SavingsKg: number;
  subsidyLimitedBy: string;
}

@Component({
  selector: 'app-heat-pump-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, LeadFormComponent, AffiliateCtaComponent, AdSlotComponent, TranslatePipe],
  templateUrl: './heat-pump-calculator.component.html',
  styleUrls: ['./heat-pump-calculator.component.css'],
})
export class HeatPumpCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private locale = inject(LocaleService);

  // Inputs
  heatedArea = 120;
  insulation = 'partial';
  currentHeating = 'gas';

  constructor() {
    // Recompute when the language/country changes (currency + subsidy programme).
    effect(() => {
      this.country; // track
      if (isPlatformBrowser(this.platformId)) this.calculate();
    });
  }

  /** Engine country — SK + CZ implemented; other locales fall back to SK. */
  get country(): 'SK' | 'CZ' {
    return getCountryParams(this.locale.locale()).countryCode === 'CZ' ? 'CZ' : 'SK';
  }
  get isSK(): boolean { return this.country === 'SK'; }
  get cfg(): CountryHeatPumpConfig { return HP_CONFIG[this.country]; }
  get currency(): string { return this.isSK ? 'EUR' : 'CZK'; }
  get currencySymbol(): string { return this.isSK ? '€' : 'Kč'; }
  get countryName(): string { return this.isSK ? 'Slovensko' : 'Česko'; }
  get programName(): string { return getCountryParams(this.locale.locale()).energyProgram.name; }
  get programUrl(): string { return getCountryParams(this.locale.locale()).energyProgram.url; }
  private get numberLocale(): string { return this.isSK ? 'sk-SK' : 'cs-CZ'; }

  result: HeatPumpResult | null = null;
  error: string | null = null;

  insulationOptions: InsulationOption[] = [
    { key: 'old', labelKey: 'heatpump.insul.old', specificDemand: 150, loadFactor: 0.08 },
    { key: 'partial', labelKey: 'heatpump.insul.partial', specificDemand: 100, loadFactor: 0.06 },
    { key: 'new', labelKey: 'heatpump.insul.new', specificDemand: 60, loadFactor: 0.045 },
  ];

  heatingOptions: HeatingOption[] = [
    { key: 'gas', labelKey: 'heatpump.fuel.gas', costPerKwh: 0.10 },
    { key: 'electric', labelKey: 'heatpump.fuel.electric', costPerKwh: 0.18 },
    { key: 'coal', labelKey: 'heatpump.fuel.coal', costPerKwh: 0.08 },
    { key: 'oil', labelKey: 'heatpump.fuel.oil', costPerKwh: 0.13 },
    { key: 'wood', labelKey: 'heatpump.fuel.wood', costPerKwh: 0.06 },
  ];

  ngOnInit(): void {
    // Initial calculation driven by the locale effect (constructor).
  }

  setArea(area: number): void {
    this.heatedArea = area;
    this.calculate();
  }

  calculate(): void {
    if (!this.heatedArea || this.heatedArea <= 0) {
      this.error = 'Zadajte vykurovanú plochu domu';
      this.result = null;
      return;
    }
    this.error = null;

    const cfg = this.cfg;
    const insul = this.insulationOptions.find(o => o.key === this.insulation) ?? this.insulationOptions[1];
    const fuelCost = cfg.fuel[this.currentHeating] ?? cfg.fuel['gas'];

    const spaceHeating = this.heatedArea * insul.specificDemand;
    const annualHeatDemand = spaceHeating + DHW_KWH_PER_YEAR;

    // Sizing — design heat load, rounded to 0.5 kW, sensible bounds.
    let recommendedKw = Math.round((this.heatedArea * insul.loadFactor) * 2) / 2;
    recommendedKw = Math.max(4, Math.min(recommendedKw, 20));

    // Indicative turnkey cost (country pricing).
    const totalCost = Math.round(Math.max(cfg.costBase, recommendedKw * cfg.costPerKw));

    // Subsidy — per-kW capped, and ≤ 50 % of cost.
    const subsidyByPower = Math.min(recommendedKw * cfg.subsidyPerKw, cfg.subsidyMax);
    const subsidyByCost = SUBSIDY_RATE_OF_COST * totalCost;
    const subsidy = Math.round(Math.min(subsidyByPower, subsidyByCost));
    let subsidyLimitedBy: string;
    if (subsidy >= subsidyByCost) subsidyLimitedBy = '50 % nákladov';
    else if (recommendedKw * cfg.subsidyPerKw >= cfg.subsidyMax) subsidyLimitedBy = 'max. dotácia';
    else subsidyLimitedBy = 'výkon';

    const netCost = Math.max(totalCost - subsidy, 0);

    const currentAnnualCost = Math.round(annualHeatDemand * fuelCost);
    const hpAnnualCost = Math.round((annualHeatDemand / SCOP) * cfg.electricityPrice);
    const annualSavings = currentAnnualCost - hpAnnualCost;
    const paybackYears = annualSavings > 0 ? Math.round((netCost / annualSavings) * 10) / 10 : null;
    const savings15y = Math.round(annualSavings * 15 - netCost);
    const co2SavingsKg = Math.round(
      annualHeatDemand * CO2_KG_PER_KWH_GRID * (1 - 1 / SCOP)
    );

    this.result = {
      annualHeatDemand: Math.round(annualHeatDemand),
      recommendedKw,
      hpType: 'vzduch–voda',
      totalCost,
      subsidy,
      netCost,
      currentAnnualCost,
      hpAnnualCost,
      annualSavings,
      paybackYears,
      savings15y,
      co2SavingsKg,
      subsidyLimitedBy,
    };
  }

  /** Snapshot attached to the installer lead. */
  get leadContext(): Record<string, any> {
    return {
      heated_area_m2: this.heatedArea,
      insulation: this.insulation,
      current_heating: this.currentHeating,
      recommended_kw: this.result?.recommendedKw ?? null,
      net_cost: this.result?.netCost ?? null,
      annual_savings: this.result?.annualSavings ?? null,
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
