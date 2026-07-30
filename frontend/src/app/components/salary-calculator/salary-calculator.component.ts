import { Component, PLATFORM_ID, inject, ChangeDetectorRef, OnInit, OnDestroy, effect } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subject, of } from 'rxjs';
import { debounceTime, switchMap, catchError, takeUntil } from 'rxjs/operators';
import { CalculatorService } from '../../services/calculator.service';
import { SalaryCalculationResponse } from '../../models/calculator.models';
import { SeoService } from '../../services/seo.service';
import { AffiliateCtaComponent } from '../shared/affiliate-cta/affiliate-cta.component';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';
import { EmbedSnippetComponent } from '../shared/embed-snippet/embed-snippet.component';
import { SaveCalculationComponent } from '../shared/save-calculation/save-calculation.component';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { getCountryParams } from '../../i18n/country-params';

@Component({
  selector: 'app-salary-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, AffiliateCtaComponent, AdSlotComponent, EmbedSnippetComponent, SaveCalculationComponent, TranslatePipe],
  templateUrl: './salary-calculator.component.html',
  styleUrls: ['./salary-calculator.component.css']
})
export class SalaryCalculatorComponent implements OnInit, OnDestroy {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  private seo = inject(SeoService);
  private locale = inject(LocaleService);
  // Debounced, cancellable calculation pipeline. Every input/slider change calls
  // calculate(), which only pushes to this Subject — the actual HTTP call is
  // debounced (coalesces keystrokes) and switchMapped (a newer request cancels
  // the in-flight one, so a slow earlier response can't overwrite a newer result).
  private calcTrigger$ = new Subject<void>();
  private destroy$ = new Subject<void>();
  grossSalary: number = 1500;
  childrenUnder15: number = 0;
  children15To18: number = 0;
  applyNontaxableAmount: boolean = true;
  hasDisability: boolean = false;
  result: SalaryCalculationResponse | null = null;
  loading: boolean = false;
  error: string | null = null;

  constructor(private calculatorService: CalculatorService) {
    // Switching language switches the country: load that country's payroll
    // rules + currency and reset the gross to a sensible local amount.
    let firstRun = true;
    effect(() => {
      const params = getCountryParams(this.locale.locale());
      if (!firstRun) {
        this.grossSalary = params.salaryPresets[1] ?? this.grossSalary;
      }
      firstRun = false;
      if (isPlatformBrowser(this.platformId)) {
        this.calculate();
      }
    });
  }

  /** ISO country code whose payroll rules apply, from the active language. */
  get country(): string { return getCountryParams(this.locale.locale()).countryCode; }
  get isSK(): boolean { return this.country === 'SK'; }
  get countryName(): string { return getCountryParams(this.locale.locale()).countryName; }
  get currency(): string { return getCountryParams(this.locale.locale()).currency; }
  get currencySymbol(): string { return getCountryParams(this.locale.locale()).currencySymbol; }
  private get numberLocale(): string { return getCountryParams(this.locale.locale()).numberLocale; }

  /** Snapshot persisted when a logged-in user saves this calculation. */
  get saveParams(): Record<string, any> {
    return {
      gross_salary: this.grossSalary,
      country: this.country,
      children_under_15: this.childrenUnder15,
      children_15_to_18: this.children15To18,
    };
  }
  get saveName(): string { return `${this.locale.t('salary.net')} · ${this.grossSalary} ${this.currencySymbol}`; }

  /** Country-appropriate quick-select gross amounts [minimum, average]. */
  get benchmarks(): { labelKey: string; value: number }[] {
    const p = getCountryParams(this.locale.locale()).salaryPresets;
    return [
      { labelKey: 'salary.benchmarkMin', value: p[0] },
      { labelKey: 'salary.benchmarkAvg', value: p[1] },
    ];
  }

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

    // Debounced + cancellable calculation stream. Built here (before the
    // constructor's locale effect flushes on first change detection) so the
    // initial calculate() has a live subscriber.
    this.calcTrigger$
      .pipe(
        debounceTime(300),
        switchMap(() =>
          this.calculatorService
            .calculateSalary({
              gross_salary: this.grossSalary,
              country: this.country,
              children_under_15: this.childrenUnder15,
              children_15_to_18: this.children15To18,
              apply_nontaxable_amount: this.applyNontaxableAmount,
              has_disability: this.hasDisability,
            })
            .pipe(
              catchError((err) => {
                console.error('❌ Salary calculation error:', err);
                this.error = this.locale.t('err.calc');
                this.loading = false;
                this.cdr.detectChanges();
                return of(null);
              })
            )
        ),
        takeUntil(this.destroy$)
      )
      .subscribe((data) => {
        if (data) {
          this.result = data;
          this.error = null;
        }
        this.loading = false;
        this.cdr.detectChanges();
      });

    // Initial calculation is driven by the locale effect (constructor), which
    // runs on init and whenever the country/language changes.
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  calculate(): void {
    if (!this.grossSalary || this.grossSalary <= 0) {
      this.error = this.locale.t('err.grossValid');
      this.result = null;
      return;
    }

    this.loading = true;
    this.error = null;
    // Actual HTTP call is debounced + switchMapped in the ngOnInit pipeline.
    this.calcTrigger$.next();
  }

  setBenchmark(value: number): void {
    this.grossSalary = value;
    this.calculate();
  }

  formatCurrency(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.00 ' + this.currencySymbol;
    }
    // HUF/CZK are typically shown without decimals; EUR/PLN with two.
    const noDecimals = this.country === 'HU';
    const formatted = new Intl.NumberFormat(this.numberLocale, {
      minimumFractionDigits: noDecimals ? 0 : 2,
      maximumFractionDigits: noDecimals ? 0 : 2,
    }).format(value);
    return formatted + ' ' + this.currencySymbol;
  }

  formatPercentage(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.0%';
    }
    return value.toFixed(1) + '%';
  }
}
