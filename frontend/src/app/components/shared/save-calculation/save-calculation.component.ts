import { Component, Input, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../services/auth.service';
import { DashboardService } from '../../../services/dashboard.service';
import { TranslatePipe } from '../../../i18n/translate.pipe';
import { LocaleService } from '../../../i18n/locale.service';

/**
 * Reusable "save & track" block for a calculator. Lets a logged-in user store a
 * calculation under their account and optionally receive email reminders
 * (mortgage payments, vacation expiry, pregnancy milestones, …) via the
 * ScheduledNotification system. Anonymous users are sent to log in first.
 *
 * Usage:
 *   <app-save-calculation
 *     calculatorType="mortgage"
 *     [params]="{ amount, rate, years }"
 *     [result]="result"
 *     [defaultName]="'Hypotéka ' + amount + ' €'">
 *   </app-save-calculation>
 */
@Component({
  selector: 'app-save-calculation',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslatePipe],
  template: `
    <div class="save-box">
      <ng-container *ngIf="!saved; else doneTpl">
        <button *ngIf="!open" type="button" class="save-trigger" (click)="onOpen()">
          💾 {{ 'save.cta' | t }}
        </button>

        <div class="save-form" *ngIf="open">
          <label class="save-label">{{ 'save.nameLabel' | t }}</label>
          <input class="save-input" type="text" [(ngModel)]="name" [placeholder]="'save.namePlaceholder' | t" />

          <textarea class="save-input" rows="2" [(ngModel)]="note"
                    [placeholder]="'save.notePlaceholder' | t"></textarea>

          <label class="save-track">
            <input type="checkbox" [(ngModel)]="track" />
            <span>{{ 'save.trackLabel' | t }}</span>
          </label>

          <div class="save-actions">
            <button type="button" class="save-btn" (click)="save()" [disabled]="loading">
              {{ loading ? ('save.saving' | t) : ('save.confirm' | t) }}
            </button>
            <button type="button" class="save-cancel" (click)="open = false">{{ 'save.cancel' | t }}</button>
          </div>
          <p class="save-error" *ngIf="error">{{ error }}</p>
        </div>
      </ng-container>

      <ng-template #doneTpl>
        <div class="save-done">✅ {{ 'save.done' | t }}</div>
      </ng-template>
    </div>
  `,
  styles: [`
    .save-box { margin: 16px 0; }
    .save-trigger {
      border: 1px dashed #cbd5e1; background: #f8fafc; color: #334155;
      border-radius: 12px; padding: 11px 16px; font-size: 14px; font-weight: 600; cursor: pointer;
    }
    .save-trigger:hover { background: #eef2f7; }
    .save-form {
      border: 1px solid #e2e8f0; border-radius: 14px; padding: 16px; background: #fff;
      display: flex; flex-direction: column; gap: 10px; max-width: 460px;
    }
    .save-label { font-size: 13px; font-weight: 600; color: #334155; }
    .save-input {
      border: 1px solid #cbd5e1; border-radius: 10px; padding: 10px 12px; font-size: 15px;
    }
    .save-input:focus { outline: none; border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.15); }
    .save-track { display: flex; gap: 8px; align-items: center; font-size: 14px; color: #475569; }
    .save-actions { display: flex; gap: 8px; }
    .save-btn {
      background: #4f46e5; color: #fff; border: none; border-radius: 10px;
      padding: 10px 16px; font-weight: 700; cursor: pointer;
    }
    .save-btn:disabled { opacity: .6; cursor: not-allowed; }
    .save-cancel { background: none; border: none; color: #64748b; cursor: pointer; font-size: 14px; }
    .save-error { color: #dc2626; font-size: 13px; margin: 0; }
    .save-done { color: #166534; font-weight: 600; }
  `],
})
export class SaveCalculationComponent {
  @Input() calculatorType = '';
  @Input() params: Record<string, any> = {};
  @Input() result: Record<string, any> | null = null;
  @Input() defaultName = '';

  private auth = inject(AuthService);
  private dashboard = inject(DashboardService);
  private router = inject(Router);
  private locale = inject(LocaleService);

  open = false;
  saved = false;
  loading = false;
  error: string | null = null;
  name = '';
  note = '';
  track = true;

  onOpen(): void {
    if (!this.auth.isAuthenticated()) {
      this.router.navigate(['/login'], { queryParams: { redirect: this.router.url } });
      return;
    }
    this.name = this.defaultName;
    this.open = true;
  }

  save(): void {
    if (!this.name.trim()) {
      this.error = this.locale.t('save.nameRequired');
      return;
    }
    this.loading = true;
    this.error = null;
    this.dashboard.saveCalculation({
      // Backend SavedCalculation types use underscores (e.g. freelancer_tax).
      calculator_type: this.calculatorType.replace(/-/g, '_'),
      name: this.name.trim(),
      params: this.params,
      result: this.result,
      note: this.note || '',
      is_tracking: this.track,
      notification_enabled: this.track,
    }).subscribe({
      next: () => { this.loading = false; this.saved = true; },
      error: () => { this.loading = false; this.error = this.locale.t('save.error'); },
    });
  }
}
