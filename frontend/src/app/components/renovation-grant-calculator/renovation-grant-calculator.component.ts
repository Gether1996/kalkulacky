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
 * Renovation-grant eligibility wizard + grant estimator (V4 report idea #5,
 * score 7.45) for the Slovak "Obnov dom" programme. Part of the home-energy hub.
 * Qualifies a homeowner and routes them to an energy auditor / contractor
 * (lead vertical `renovation`, already defined in the backend Lead model).
 *
 * INDICATIVE estimate, computed client-side. Verify current round parameters on
 * the official obnovdom.sk portal. Constants centralised for easy updates.
 */

// --- Tunable indicative constants per country (verify per current round) ------
interface RenoConfig {
  rate: number;            // share of eligible cost covered
  maxBasic: number;        // cap, ≥30 % savings tier
  maxComprehensive: number;// cap, ≥60 % savings tier
  defaultCost: number;     // default project-cost input
  requiresOldHouse: boolean; // SK Obnov dom requires a pre-2013 house
}
const RENO_CONFIG: Record<'SK' | 'CZ', RenoConfig> = {
  // SK — Obnov dom (Plán obnovy), INDICATIVE.
  SK: { rate: 0.60, maxBasic: 14000, maxComprehensive: 19000, defaultCost: 25000, requiresOldHouse: true },
  // CZ — Nová zelená úsporám, INDICATIVE (CZK). Broader eligibility, higher caps.
  CZ: { rate: 0.50, maxBasic: 150000, maxComprehensive: 500000, defaultCost: 600000, requiresOldHouse: false },
};

interface Measure {
  key: string;
  labelKey: string;
  points: number;   // contribution toward the savings tier
  checked: boolean;
}

interface RenovationResult {
  eligible: boolean;
  reasonKey: string | null;
  tierKey: string;
  tierPct: string;
  estimatedGrant: number;
  contribution: number;
  coveragePct: number;
}

@Component({
  selector: 'app-renovation-grant-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, LeadFormComponent, AffiliateCtaComponent, AdSlotComponent, TranslatePipe],
  templateUrl: './renovation-grant-calculator.component.html',
  styleUrls: ['./renovation-grant-calculator.component.css'],
})
export class RenovationGrantCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private locale = inject(LocaleService);

  // Eligibility
  isFamilyHouse = true;
  builtBefore2013 = true;

  // Project
  projectCost = 25000;

  constructor() {
    effect(() => {
      const c = this.country;
      this.projectCost = RENO_CONFIG[c].defaultCost;
      if (isPlatformBrowser(this.platformId)) this.calculate();
    });
  }

  /** Engine country — SK + CZ implemented; other locales fall back to SK. */
  get country(): 'SK' | 'CZ' {
    return getCountryParams(this.locale.locale()).countryCode === 'CZ' ? 'CZ' : 'SK';
  }
  get isSK(): boolean { return this.country === 'SK'; }
  get cfg(): RenoConfig { return RENO_CONFIG[this.country]; }
  get currency(): string { return this.isSK ? 'EUR' : 'CZK'; }
  get currencySymbol(): string { return this.isSK ? '€' : 'Kč'; }
  get countryName(): string { return this.isSK ? 'Slovensko' : 'Česko'; }
  get programName(): string { return getCountryParams(this.locale.locale()).energyProgram.name; }
  get programUrl(): string { return getCountryParams(this.locale.locale()).energyProgram.url; }
  private get numberLocale(): string { return this.isSK ? 'sk-SK' : 'cs-CZ'; }

  measures: Measure[] = [
    { key: 'insulation', labelKey: 'reno.m.insulation', points: 2, checked: true },
    { key: 'windows', labelKey: 'reno.m.windows', points: 1, checked: true },
    { key: 'roof', labelKey: 'reno.m.roof', points: 1, checked: false },
    { key: 'heatSource', labelKey: 'reno.m.heatSource', points: 2, checked: false },
    { key: 'pv', labelKey: 'reno.m.pv', points: 1, checked: false },
    { key: 'recuperation', labelKey: 'reno.m.recuperation', points: 1, checked: false },
    { key: 'shading', labelKey: 'reno.m.shading', points: 0.5, checked: false },
  ];

  result: RenovationResult | null = null;

  ngOnInit(): void {
    // Initial calculation driven by the locale effect (constructor).
  }

  calculate(): void {
    const cfg = this.cfg;
    const points = this.measures.filter(m => m.checked).reduce((s, m) => s + m.points, 0);

    let tierKey: string;
    let tierPct: string;
    let maxGrant: number;
    let tierPoints: number;
    if (points >= 4) { tierKey = 'reno.tier.comprehensive'; tierPct = '≥ 60 %'; maxGrant = cfg.maxComprehensive; tierPoints = 4; }
    else { tierKey = 'reno.tier.basic'; tierPct = '≥ 30 %'; maxGrant = cfg.maxBasic; tierPoints = 2; }

    // Eligibility checks
    let eligible = true;
    let reasonKey: string | null = null;
    if (!this.isFamilyHouse) { eligible = false; reasonKey = 'reno.reason.notFamily'; }
    else if (cfg.requiresOldHouse && !this.builtBefore2013) { eligible = false; reasonKey = 'reno.reason.tooNew'; }
    else if (points < tierPoints || points < 2) { eligible = false; reasonKey = 'reno.reason.notEnough'; }

    const cost = Math.max(this.projectCost || 0, 0);
    const estimatedGrant = eligible ? Math.round(Math.min(cfg.rate * cost, maxGrant)) : 0;
    const contribution = Math.max(cost - estimatedGrant, 0);
    const coveragePct = cost > 0 ? Math.round((estimatedGrant / cost) * 100) : 0;

    this.result = {
      eligible,
      reasonKey,
      tierKey,
      tierPct,
      estimatedGrant,
      contribution,
      coveragePct,
    };
  }

  /** Snapshot attached to the auditor/contractor lead. */
  get leadContext(): Record<string, any> {
    return {
      family_house: this.isFamilyHouse,
      built_before_2013: this.builtBefore2013,
      measures: this.measures.filter(m => m.checked).map(m => m.key),
      project_cost: this.projectCost,
      estimated_grant: this.result?.estimatedGrant ?? null,
      eligible: this.result?.eligible ?? null,
    };
  }

  formatCurrency(value: number | null | undefined): string {
    if (value === undefined || value === null || isNaN(value)) return '0 ' + this.currencySymbol;
    return value.toLocaleString(this.numberLocale, { maximumFractionDigits: 0 }) + ' ' + this.currencySymbol;
  }
}
