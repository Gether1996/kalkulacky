import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { MonetizationService } from '../../../services/monetization.service';
import { LocaleService } from '../../../i18n/locale.service';
import { TranslatePipe } from '../../../i18n/translate.pipe';

/**
 * "Report wrong data" widget. Calculators rely on real-world values (tax rates,
 * subsidies, prices) that change over time; this lets any user flag an incorrect
 * figure. The report is stored and emailed to the operator immediately so it can
 * be fixed. Placed globally in the app shell on calculator/tool routes — it
 * derives which calculator from the current URL.
 */
@Component({
  selector: 'app-data-report',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslatePipe],
  template: `
    <div class="dr-wrap">
      <button *ngIf="!open() && !done()" type="button" class="dr-toggle" (click)="open.set(true)">
        ⚠️ {{ 'report.trigger' | t }}
      </button>

      <div class="dr-card" *ngIf="open() && !done()">
        <h3 class="dr-title">{{ 'report.title' | t }}</h3>
        <p class="dr-sub">{{ 'report.sub' | t }}</p>
        <textarea class="dr-input" rows="3" [(ngModel)]="message"
                  [placeholder]="'report.placeholder' | t"></textarea>
        <input class="dr-input" type="email" [(ngModel)]="email"
               [placeholder]="'report.emailPlaceholder' | t" autocomplete="email" />
        <div class="dr-actions">
          <button type="button" class="dr-send" (click)="submit()" [disabled]="loading()">
            {{ loading() ? ('report.sending' | t) : ('report.send' | t) }}
          </button>
          <button type="button" class="dr-cancel" (click)="open.set(false)">{{ 'report.cancel' | t }}</button>
        </div>
        <p class="dr-error" *ngIf="error()">{{ error() }}</p>
      </div>

      <div class="dr-done" *ngIf="done()">✅ {{ 'report.done' | t }}</div>
    </div>
  `,
  styles: [`
    .dr-wrap { max-width: 880px; margin: 8px auto 40px; padding: 0 16px; }
    .dr-toggle {
      background: none; border: none; color: #94a3b8; font-size: 13px;
      cursor: pointer; padding: 4px 0; text-decoration: underline;
    }
    .dr-toggle:hover { color: #64748b; }
    .dr-card {
      border: 1px solid #fde68a; background: #fffbeb; border-radius: 14px;
      padding: 16px; display: flex; flex-direction: column; gap: 10px;
    }
    .dr-title { margin: 0; font-size: 16px; font-weight: 700; color: #92400e; }
    .dr-sub { margin: 0; font-size: 13px; color: #78716c; }
    .dr-input {
      width: 100%; box-sizing: border-box; border: 1px solid #e7d8a8;
      border-radius: 10px; padding: 10px 12px; font-size: 14px; background: #fff;
      font-family: inherit;
    }
    .dr-input:focus { outline: none; border-color: #d97706; box-shadow: 0 0 0 3px rgba(217,119,6,.12); }
    .dr-actions { display: flex; gap: 8px; align-items: center; }
    .dr-send {
      background: #d97706; color: #fff; border: none; border-radius: 10px;
      padding: 9px 16px; font-weight: 700; cursor: pointer; font-size: 14px;
    }
    .dr-send:disabled { opacity: .6; cursor: not-allowed; }
    .dr-cancel { background: none; border: none; color: #78716c; cursor: pointer; font-size: 14px; }
    .dr-error { color: #dc2626; font-size: 13px; margin: 0; }
    .dr-done { color: #166534; font-weight: 600; font-size: 14px; padding: 6px 0; }
  `],
})
export class DataReportComponent {
  private monetization = inject(MonetizationService);
  private locale = inject(LocaleService);
  private router = inject(Router);

  open = signal(false);
  done = signal(false);
  loading = signal(false);
  error = signal<string | null>(null);

  message = '';
  email = '';

  /** Derive the calculator id from the current URL (e.g. /calculator/salary → salary). */
  private currentCalculatorType(): string {
    const url = (this.router.url || '').split('?')[0];
    if (url.startsWith('/calculator/')) return url.replace('/calculator/', '').replace(/\/.*/, '');
    if (url.startsWith('/cista-mzda')) return 'salary';
    if (url.startsWith('/energia')) return 'energia';
    return url.replace(/^\//, '') || 'unknown';
  }

  submit(): void {
    this.error.set(null);
    if (!this.message || this.message.trim().length < 5) {
      this.error.set(this.locale.t('report.errorEmpty'));
      return;
    }
    this.loading.set(true);
    this.monetization.submitDataReport({
      calculator_type: this.currentCalculatorType(),
      message: this.message.trim(),
      reporter_email: this.email || undefined,
      locale: this.locale.locale(),
    }).subscribe((res) => {
      this.loading.set(false);
      if (res.success) {
        this.done.set(true);
        this.open.set(false);
      } else {
        this.error.set(this.locale.t('report.errorSend'));
      }
    });
  }
}
