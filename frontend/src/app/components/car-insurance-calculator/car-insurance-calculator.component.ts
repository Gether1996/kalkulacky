import { Component, OnInit, PLATFORM_ID, inject } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SeoService } from '../../services/seo.service';
import { LeadFormComponent } from '../shared/lead-form/lead-form.component';
import { AffiliateCtaComponent } from '../shared/affiliate-cta/affiliate-cta.component';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { getSeoContent } from '../../i18n/seo';

/**
 * Car-insurance (PZP / povinné ručenie) niche lead page — V4 report idea #9.
 * The report advises attacking PZP via niches (young drivers, higher-power cars)
 * rather than head-on. Indicative premium estimate (client-side) → qualified
 * lead to a broker/insurer (vertical `insurance_car`).
 *
 * INDICATIVE only — real premiums depend on the insurer, bonus/malus, etc.
 */
@Component({
  selector: 'app-car-insurance-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, LeadFormComponent, AffiliateCtaComponent, AdSlotComponent, TranslatePipe],
  templateUrl: './car-insurance-calculator.component.html',
  styleUrls: ['./car-insurance-calculator.component.css'],
})
export class CarInsuranceCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private seo = inject(SeoService);
  private locale = inject(LocaleService);

  power = 85;       // engine power in kW
  driverAge = 35;
  region = 'city';

  estLow = 0;
  estHigh = 0;

  ngOnInit(): void {
    const s = getSeoContent('car-insurance', this.locale.locale());
    this.seo.apply({
      title: s.title,
      description: s.description,
      keywords: s.keywords,
      faq: s.faq,
      path: '/calculator/car-insurance',
      isCalculator: true,
    });
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  calculate(): void {
    const base = 120; // indicative annual base premium (€)
    const powerFactor = 1 + Math.max(0, (this.power - 55)) * 0.011;
    let ageFactor = 1;
    if (this.driverAge < 25) ageFactor = 1.6;
    else if (this.driverAge < 30) ageFactor = 1.25;
    else if (this.driverAge > 65) ageFactor = 1.15;
    const regionFactor = this.region === 'city' ? 1.15 : 1.0;

    const mid = base * powerFactor * ageFactor * regionFactor;
    this.estLow = Math.round(mid * 0.8);
    this.estHigh = Math.round(mid * 1.25);
  }

  get leadContext(): Record<string, any> {
    return {
      vehicle_power_kw: this.power,
      driver_age: this.driverAge,
      region_type: this.region,
      est_premium_low: this.estLow,
      est_premium_high: this.estHigh,
    };
  }

  formatCurrency(value: number): string {
    return value.toLocaleString('sk-SK', { maximumFractionDigits: 0 }) + ' €';
  }
}
