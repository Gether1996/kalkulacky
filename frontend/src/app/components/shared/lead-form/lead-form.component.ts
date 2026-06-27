import { Component, Input, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MonetizationService } from '../../../services/monetization.service';
import { LeadOffer, LeadFieldKey } from '../../../models/monetization.models';
import { TranslatePipe } from '../../../i18n/translate.pipe';
import { LocaleService } from '../../../i18n/locale.service';

/**
 * Qualified lead-capture block for a calculator. Lead-gen is the highest-value
 * monetization model in these markets (€3–40 per qualified lead).
 *
 * Usage — pass the calculator id and (optionally) the current calculation
 * snapshot so the lead carries qualifying context:
 *
 *   <app-lead-form
 *     calculatorType="mortgage"
 *     [context]="{ loan_amount: loanAmount, rate: rate, years: years }">
 *   </app-lead-form>
 */
@Component({
  selector: 'app-lead-form',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslatePipe],
  template: `
    <div class="lead-box" *ngIf="offer">
      <ng-container *ngIf="!submitted; else doneTpl">
        <h3 class="lead-title">{{ offer.headline }}</h3>
        <p class="lead-sub">{{ offer.subtext }}</p>

        <form class="lead-form" (ngSubmit)="submit()">
          <input
            *ngIf="hasField('name')"
            class="lead-input" type="text" name="name"
            [placeholder]="'lead.field.name' | t" [(ngModel)]="name" autocomplete="name" />

          <input
            *ngIf="hasField('email')"
            class="lead-input" type="email" name="email"
            [placeholder]="'lead.field.email' | t" [(ngModel)]="email" autocomplete="email" />

          <input
            *ngIf="hasField('phone')"
            class="lead-input" type="tel" name="phone"
            [placeholder]="'lead.field.phone' | t" [(ngModel)]="phone" autocomplete="tel" />

          <input
            *ngIf="hasField('region')"
            class="lead-input" type="text" name="region"
            [placeholder]="'lead.field.region' | t" [(ngModel)]="region" />

          <textarea
            *ngIf="hasField('message')"
            class="lead-input" name="message" rows="2"
            [placeholder]="'lead.field.message' | t" [(ngModel)]="message"></textarea>

          <label class="lead-consent">
            <input type="checkbox" name="consent" [(ngModel)]="consent" />
            <span>{{ 'lead.consent' | t }}</span>
          </label>

          <button class="lead-btn" type="submit" [disabled]="loading">
            {{ loading ? ('lead.sending' | t) : offer.ctaLabel }}
          </button>

          <p class="lead-error" *ngIf="error">{{ error }}</p>
        </form>
      </ng-container>

      <ng-template #doneTpl>
        <div class="lead-done">
          <div class="lead-done-icon">✅</div>
          <p>{{ successMessage }}</p>
        </div>
      </ng-template>
    </div>
  `,
  styles: [`
    .lead-box {
      border: 1px solid #bfdbfe; background: linear-gradient(180deg,#eff6ff,#fff);
      border-radius: 16px; padding: 20px; margin: 20px 0;
    }
    .lead-title { margin: 0 0 4px; font-size: 19px; font-weight: 700; color: #1e3a8a; }
    .lead-sub { margin: 0 0 14px; font-size: 14px; color: #475569; }
    .lead-form { display: flex; flex-direction: column; gap: 10px; }
    .lead-input {
      width: 100%; box-sizing: border-box; border: 1px solid #cbd5e1;
      border-radius: 10px; padding: 11px 13px; font-size: 15px; background:#fff;
    }
    .lead-input:focus { outline: none; border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,.15); }
    .lead-consent { display: flex; gap: 8px; align-items: flex-start; font-size: 12.5px; color: #64748b; }
    .lead-consent input { margin-top: 2px; }
    .lead-btn {
      background: #16a34a; color: #fff; border: none; border-radius: 10px;
      padding: 12px 18px; font-size: 15px; font-weight: 700; cursor: pointer;
      transition: background .15s;
    }
    .lead-btn:hover:not(:disabled) { background: #15803d; }
    .lead-btn:disabled { opacity: .6; cursor: not-allowed; }
    .lead-error { color: #dc2626; font-size: 13px; margin: 4px 0 0; }
    .lead-done { text-align: center; padding: 14px 0; }
    .lead-done-icon { font-size: 38px; }
    .lead-done p { color: #166534; font-weight: 600; margin: 8px 0 0; }
  `],
})
export class LeadFormComponent implements OnInit {
  @Input() calculatorType = '';
  @Input() context: Record<string, any> | null = null;

  private monetization = inject(MonetizationService);
  private locale = inject(LocaleService);

  offer: LeadOffer | null = null;
  name = '';
  email = '';
  phone = '';
  region = '';
  message = '';
  consent = false;

  loading = false;
  submitted = false;
  error: string | null = null;
  successMessage = '';

  ngOnInit(): void {
    this.offer = this.monetization.getConfig(this.calculatorType)?.leadOffer ?? null;
    this.successMessage = this.locale.t('lead.success');
  }

  hasField(field: LeadFieldKey): boolean {
    return this.offer?.fields?.includes(field) ?? false;
  }

  submit(): void {
    if (!this.offer) return;
    this.error = null;

    if (!this.email && !this.phone) {
      this.error = this.locale.t('lead.error.contact');
      return;
    }
    if (!this.consent) {
      this.error = this.locale.t('lead.error.consent');
      return;
    }

    this.loading = true;
    this.monetization
      .submitLead({
        vertical: this.offer.vertical,
        calculator_type: this.calculatorType,
        name: this.name || undefined,
        email: this.email || undefined,
        phone: this.phone || undefined,
        region: this.region || undefined,
        message: this.message || undefined,
        context: this.context ?? undefined,
        consent: this.consent,
      })
      .subscribe((res) => {
        this.loading = false;
        if (res.success) {
          this.submitted = true;
          if (res.message) this.successMessage = res.message;
        } else {
          this.error = this.locale.t('lead.error.submit');
        }
      });
  }
}
