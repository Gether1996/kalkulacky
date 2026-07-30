import { Component, PLATFORM_ID, inject, ChangeDetectorRef, OnInit, OnDestroy } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CalculatorService } from '../../services/calculator.service';
import { CarLeasingCalculationResponse, CarLeasingOption } from '../../models/calculator.models';
import { DebouncedCalc } from '../../utils/debounced-calc';
import { SeoService } from '../../services/seo.service';
import { AffiliateCtaComponent } from '../shared/affiliate-cta/affiliate-cta.component';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';

@Component({
  selector: 'app-car-leasing-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, AffiliateCtaComponent, AdSlotComponent, TranslatePipe],
  templateUrl: './car-leasing-calculator.component.html',
  styleUrls: ['./car-leasing-calculator.component.css']
})
export class CarLeasingCalculatorComponent implements OnInit, OnDestroy {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  private seo = inject(SeoService);
  private locale = inject(LocaleService);

  // Input parameters
  carPrice: number = 25000;
  downPayment: number = 5000;
  termMonths: number = 60;
  leasingRate: number = 5.5;
  loanRate: number = 6.0;
  residualValuePercent: number = 30;
  includeVat: boolean = true;

  result: CarLeasingCalculationResponse | null = null;
  loading: boolean = false;
  error: string | null = null;
  selectedOption: string = 'all';

  // Car price presets for quick selection
  carPresets = [
    { label: 'Malé auto', value: 15000 },
    { label: 'Kompakt', value: 25000 },
    { label: 'SUV', value: 35000 },
    { label: 'Luxus', value: 50000 }
  ];

  // Term presets
  termPresets = [
    { label: '36 mes.', value: 36 },
    { label: '48 mes.', value: 48 },
    { label: '60 mes.', value: 60 },
    { label: '72 mes.', value: 72 }
  ];

  constructor(private calculatorService: CalculatorService) {}

  ngOnInit(): void {
    this.seo.apply({
      title: 'Kalkulačka lízingu auta 2026 – lízing vs úver vs hotovosť',
      description: 'Porovnajte finančný lízing, operatívny lízing, úver a kúpu auta na hotovosť. Zistite najvýhodnejší spôsob financovania auta.',
      path: '/calculator/car-leasing',
      keywords: 'lízing auta kalkulačka, operatívny lízing, financovanie auta, lízing vs úver',
      isCalculator: true,
    });
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  calculate(): void {
    if (!this.carPrice || this.carPrice <= 0) {
      this.error = this.locale.t('err.carPrice');
      return;
    }

    if (this.downPayment < 0 || this.downPayment >= this.carPrice) {
      this.error = this.locale.t('err.downPayment');
      return;
    }

    if (this.termMonths < 12 || this.termMonths > 120) {
      this.error = this.locale.t('err.termMonths');
      return;
    }

    this.loading = true;
    this.error = null;
    this.calc.trigger();
  }

  private calc = new DebouncedCalc<CarLeasingCalculationResponse>(
    () =>
      this.calculatorService.calculateCarLeasing({
        car_price: this.carPrice,
        down_payment: this.downPayment,
        term_months: this.termMonths,
        leasing_rate: this.leasingRate,
        loan_rate: this.loanRate,
        residual_value_percent: this.residualValuePercent,
        include_vat: this.includeVat
      }),
    (data) => {
      this.result = data;
      this.loading = false;
      this.cdr.detectChanges();
    },
    (err) => {
      console.error('❌ Car leasing calculation error:', err);
      this.error = this.locale.t('err.calc');
      this.loading = false;
      this.cdr.detectChanges();
    },
  );

  ngOnDestroy(): void {
    this.calc.destroy();
  }

  setCarPreset(value: number): void {
    this.carPrice = value;
    this.downPayment = Math.floor(value * 0.2); // 20% down payment
    this.calculate();
  }

  setTermPreset(value: number): void {
    this.termMonths = value;
    this.calculate();
  }

  formatCurrency(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.00 €';
    }
    return value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' €';
  }

  formatPercentage(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.0%';
    }
    return value.toFixed(1) + '%';
  }

  getOptionClass(option: CarLeasingOption): string {
    if (!this.result) return '';
    
    const cheapestTotal = Math.min(
      this.result.options.financial_leasing.total_cost,
      this.result.options.operational_leasing.total_cost,
      this.result.options.loan.total_cost,
      this.result.options.cash.total_cost
    );

    const cheapestMonthly = Math.min(
      this.result.options.financial_leasing.monthly_payment || Infinity,
      this.result.options.operational_leasing.monthly_payment || Infinity,
      this.result.options.loan.monthly_payment || Infinity
    );

    if (option.total_cost === cheapestTotal) {
      return 'best-total';
    }
    if (option.monthly_payment && option.monthly_payment === cheapestMonthly) {
      return 'best-monthly';
    }
    return '';
  }

  getOptionBadge(option: CarLeasingOption): string {
    if (!this.result) return '';
    
    const cheapestTotal = Math.min(
      this.result.options.financial_leasing.total_cost,
      this.result.options.operational_leasing.total_cost,
      this.result.options.loan.total_cost,
      this.result.options.cash.total_cost
    );

    const cheapestMonthly = Math.min(
      this.result.options.financial_leasing.monthly_payment || Infinity,
      this.result.options.operational_leasing.monthly_payment || Infinity,
      this.result.options.loan.monthly_payment || Infinity
    );

    if (option.total_cost === cheapestTotal) {
      return 'Najlacnejšie celkovo';
    }
    if (option.monthly_payment && option.monthly_payment === cheapestMonthly) {
      return 'Najnižšia splátka';
    }
    return '';
  }

  scrollToResults(): void {
    if (isPlatformBrowser(this.platformId)) {
      const element = document.getElementById('results');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  }
}
