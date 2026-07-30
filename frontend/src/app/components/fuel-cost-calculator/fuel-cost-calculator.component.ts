import { Component, PLATFORM_ID, inject, ChangeDetectorRef, OnInit, OnDestroy } from '@angular/core';
import { LocaleService } from '../../i18n/locale.service';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { FuelCostCalculationResponse } from '../../models/calculator.models';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { SeoService } from '../../services/seo.service';
import { getSeoContent } from '../../i18n/seo';
import { DebouncedCalc } from '../../utils/debounced-calc';

@Component({
  selector: 'app-fuel-cost-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, TranslatePipe],
  templateUrl: './fuel-cost-calculator.component.html',
  styleUrls: ['./fuel-cost-calculator.component.css']
})
export class FuelCostCalculatorComponent implements OnInit, OnDestroy {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  private locale = inject(LocaleService);
  private seo = inject(SeoService);

  distance: number = 350;
  consumption: number = 6.5;
  fuelPrice: number = 1.65;
  
  result: FuelCostCalculationResponse | null = null;
  loading: boolean = false;
  error: string | null = null;

  // Common routes and consumption benchmarks
  routeBenchmarks = [
    { label: 'Bratislava - Košice', distance: 450 },
    { label: 'Bratislava - Žilina', distance: 200 },
    { label: 'Bratislava - Trnava', distance: 50 }
  ];

  consumptionBenchmarks = [
    { label: 'Malé auto', consumption: 5.5 },
    { label: 'Stredné auto', consumption: 7.0 },
    { label: 'Veľké auto / SUV', consumption: 9.0 }
  ];

  constructor(private calculatorService: CalculatorService) {}

  ngOnInit(): void {
    const s = getSeoContent('fuel-cost', this.locale.locale());
    this.seo.apply({ title: s.title, description: s.description, keywords: s.keywords, faq: s.faq, path: '/calculator/fuel-cost', isCalculator: true });
    // Auto-calculate on component init for immediate results
    this.calculate();
  }

  private calc = new DebouncedCalc<FuelCostCalculationResponse>(
    () => this.calculatorService.calculateFuelCost({
      distance: this.distance,
      consumption: this.consumption,
      fuel_price: this.fuelPrice
    }),
    (response) => {
      this.result = response;
      this.loading = false;
      this.cdr.detectChanges();
    },
    (err: any) => {
      console.error('Fuel cost calculation error:', err);
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

  selectRoute(distance: number): void {
    this.distance = distance;
    this.calculate();
  }

  selectConsumption(consumption: number): void {
    this.consumption = consumption;
    this.calculate();
  }

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('sk-SK', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount);
  }

  formatNumber(num: number): string {
    return new Intl.NumberFormat('sk-SK', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(num);
  }
}
