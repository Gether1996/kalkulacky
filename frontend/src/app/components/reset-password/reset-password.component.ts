import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, RouterLink, Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { PasswordInputComponent } from '../shared/password-input/password-input.component';

/**
 * "Reset password" page — reached from the emailed link with ?uid=&token=.
 * Sets a new password via the backend, then sends the user to log in.
 */
@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, TranslatePipe, PasswordInputComponent],
  template: `
    <div class="auth-card">
      <h1>{{ 'auth.reset.title' | t }}</h1>

      <div *ngIf="!validLink" class="auth-error">{{ 'auth.reset.badLink' | t }}</div>

      <form *ngIf="validLink && !done" (ngSubmit)="submit()">
        <label class="auth-label" for="rp-pw">{{ 'auth.reset.new' | t }}</label>
        <app-password-input inputId="rp-pw" name="pw" [(ngModel)]="newPassword"
               autocomplete="new-password" [showStrength]="true"></app-password-input>
        <label class="auth-label" for="rp-pw2">{{ 'auth.reset.confirm' | t }}</label>
        <app-password-input inputId="rp-pw2" name="pw2" [(ngModel)]="confirm"
               autocomplete="new-password"></app-password-input>
        <button class="auth-btn" type="submit" [disabled]="loading">
          {{ loading ? ('common.loading' | t) : ('auth.reset.cta' | t) }}
        </button>
        <p class="auth-error" *ngIf="error">{{ error }}</p>
      </form>

      <div *ngIf="done" class="auth-done">
        ✅ {{ 'auth.reset.done' | t }}
        <p class="auth-foot"><a routerLink="/login">{{ 'auth.backToLogin' | t }}</a></p>
      </div>
    </div>
  `,
  styles: [`
    .auth-card { max-width: 420px; margin: 48px auto; background:#fff; border:1px solid #e5e7eb;
      border-radius:16px; padding:28px; }
    h1 { font-size:24px; margin:0 0 14px; color:#1e293b; }
    .auth-label { display:block; font-size:13px; font-weight:600; color:#334155; margin-bottom:6px; }
    .auth-input { width:100%; box-sizing:border-box; border:1px solid #cbd5e1; border-radius:10px;
      padding:11px 13px; font-size:15px; margin-bottom:14px; }
    .auth-input:focus { outline:none; border-color:#4f46e5; box-shadow:0 0 0 3px rgba(79,70,229,.15); }
    .auth-btn { width:100%; background:#4f46e5; color:#fff; border:none; border-radius:10px;
      padding:12px; font-weight:700; font-size:15px; cursor:pointer; }
    .auth-btn:disabled { opacity:.6; cursor:not-allowed; }
    .auth-error { color:#dc2626; background:#fef2f2; border:1px solid #fecaca; border-radius:10px;
      padding:12px; font-size:14px; margin:0 0 8px; }
    .auth-done { color:#166534; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px;
      padding:14px; font-size:14px; }
    .auth-foot { margin-top:14px; font-size:14px; }
    .auth-foot a { color:#4f46e5; text-decoration:none; }
  `],
})
export class ResetPasswordComponent implements OnInit {
  private auth = inject(AuthService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private locale = inject(LocaleService);

  uid = '';
  token = '';
  newPassword = '';
  confirm = '';
  loading = false;
  done = false;
  error: string | null = null;

  get validLink(): boolean { return !!this.uid && !!this.token; }

  ngOnInit(): void {
    this.uid = this.route.snapshot.queryParamMap.get('uid') || '';
    this.token = this.route.snapshot.queryParamMap.get('token') || '';
  }

  submit(): void {
    this.error = null;
    if (this.newPassword.length < 8) { this.error = this.locale.t('auth.reset.tooShort'); return; }
    if (this.newPassword !== this.confirm) { this.error = this.locale.t('auth.reset.mismatch'); return; }
    this.loading = true;
    this.auth.resetPassword({
      uid: this.uid, token: this.token,
      new_password: this.newPassword, new_password_confirm: this.confirm,
    }).subscribe({
      next: () => { this.loading = false; this.done = true; },
      error: (err) => {
        this.loading = false;
        this.error = err?.error?.error || this.locale.t('auth.reset.failed');
      },
    });
  }
}
