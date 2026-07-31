import { Component, OnInit, PLATFORM_ID, inject } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { DashboardService, SavingsGoalProjection } from '../../services/dashboard.service';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { getCountryParams } from '../../i18n/country-params';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';

type Mode = 'time' | 'monthly';

/**
 * Savings Goal calculator + tracker entry point.
 *
 * Public calculator: "how long until I reach my target?" (mode='time') or
 * "how much must I save each month?" (mode='monthly'). Compound interest is
 * computed server-side (single source of truth, also exposed as an API).
 *
 * Logged-in users can turn the current inputs into a tracked goal (saved to
 * their account) and then log deposits + watch progress on the dashboard.
 * Currency follows the active language (EUR/CZK/PLN/HUF) — the maths is the same.
 */
@Component({
  selector: 'app-savings-goal-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslatePipe, AdSlotComponent],
  templateUrl: './savings-goal-calculator.component.html',
  styleUrls: ['./savings-goal-calculator.component.css'],
})
export class SavingsGoalCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private auth = inject(AuthService);
  private dashboard = inject(DashboardService);
  private router = inject(Router);
  locale = inject(LocaleService);

  mode: Mode = 'time';

  // Inputs (defaults sized for the home market; CZK/PLN/HUF still work — the
  // user edits the figures, the maths is currency-agnostic).
  targetAmount = 10000;
  initialAmount = 1000;
  monthlyContribution = 200;
  months = 36;
  annualRate = 2.5;

  result: SavingsGoalProjection | null = null;
  loading = false;
  error: string | null = null;

  // Track-as-goal panel
  trackOpen = false;
  trackSaving = false;
  trackSaved = false;
  trackError: string | null = null;
  goalName = '';

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  get currency(): string {
    return getCountryParams(this.locale.locale()).currency;
  }

  setMode(m: Mode): void {
    this.mode = m;
    this.calculate();
  }

  calculate(): void {
    if (!isPlatformBrowser(this.platformId)) return;
    this.loading = true;
    this.error = null;
    this.dashboard.calcSavingsGoal({
      mode: this.mode,
      target_amount: this.targetAmount,
      initial_amount: this.initialAmount,
      monthly_contribution: this.monthlyContribution,
      months: this.months,
      annual_rate: this.annualRate,
      currency: this.currency,
    }).subscribe({
      next: (res) => { this.result = res.result; this.loading = false; },
      error: () => { this.loading = false; this.error = this.locale.t('save.error'); },
    });
  }

  // ---- Track as a goal (logged-in) ----
  openTrack(): void {
    if (!this.auth.isAuthenticated()) {
      this.router.navigate(['/login'], { queryParams: { redirect: this.router.url } });
      return;
    }
    this.goalName = '';
    this.trackError = null;
    this.trackOpen = true;
  }

  saveGoal(): void {
    const name = this.goalName.trim();
    if (name.length < 2) {
      this.trackError = this.locale.t('dash.sg.name');
      return;
    }
    this.trackSaving = true;
    this.trackError = null;

    // In "monthly" mode the user has a deadline → store it so the tracker can
    // judge on-track / behind. In "time" mode there is no deadline.
    let targetDate: string | null = null;
    if (this.mode === 'monthly' && this.months > 0) {
      const d = new Date();
      d.setMonth(d.getMonth() + this.months);
      targetDate = d.toISOString().slice(0, 10);
    }
    const monthly = this.mode === 'monthly' && this.result?.required_monthly != null
      ? this.result.required_monthly
      : this.monthlyContribution;

    this.dashboard.createSavingsGoal({
      name,
      target_amount: this.targetAmount,
      initial_amount: this.initialAmount,
      monthly_contribution: monthly,
      annual_rate: this.annualRate,
      target_date: targetDate,
      currency: this.currency,
    }).subscribe({
      next: () => { this.trackSaving = false; this.trackSaved = true; this.trackOpen = false; },
      error: () => { this.trackSaving = false; this.trackError = this.locale.t('save.error'); },
    });
  }

  goToDashboard(): void {
    this.router.navigate(['/dashboard']);
  }

  formatCurrency(value: number | null | undefined): string {
    if (value == null) return '–';
    const p = getCountryParams(this.locale.locale());
    return new Intl.NumberFormat(p.numberLocale, {
      style: 'currency', currency: p.currency, maximumFractionDigits: 0,
    }).format(value);
  }
}
