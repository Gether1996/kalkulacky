import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { TranslatePipe } from '../../i18n/translate.pipe';

/**
 * "Forgot password" page — asks for an email and triggers a reset link.
 * Always shows the same confirmation (no email enumeration). Delivery needs
 * SMTP configured; until then the backend uses the console email backend.
 */
@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, TranslatePipe],
  template: `
    <div class="auth-card">
      <h1>{{ 'auth.forgot.title' | t }}</h1>
      <p class="auth-sub">{{ 'auth.forgot.sub' | t }}</p>

      <form *ngIf="!sent" (ngSubmit)="submit()">
        <label class="auth-label" for="fp-email">{{ 'auth.email' | t }}</label>
        <input id="fp-email" class="auth-input" type="email" name="email"
               [(ngModel)]="email" autocomplete="email" required />
        <button class="auth-btn" type="submit" [disabled]="loading || !email">
          {{ loading ? ('common.loading' | t) : ('auth.forgot.cta' | t) }}
        </button>
      </form>

      <div *ngIf="sent" class="auth-done">✅ {{ 'auth.forgot.done' | t }}</div>

      <p class="auth-foot"><a routerLink="/login">← {{ 'auth.backToLogin' | t }}</a></p>
    </div>
  `,
  styles: [`
    .auth-card { max-width: 420px; margin: 48px auto; background:#fff; border:1px solid #e5e7eb;
      border-radius:16px; padding:28px; }
    h1 { font-size:24px; margin:0 0 6px; color:#1e293b; }
    .auth-sub { color:#64748b; font-size:14px; margin:0 0 18px; }
    .auth-label { display:block; font-size:13px; font-weight:600; color:#334155; margin-bottom:6px; }
    .auth-input { width:100%; box-sizing:border-box; border:1px solid #cbd5e1; border-radius:10px;
      padding:11px 13px; font-size:15px; margin-bottom:14px; }
    .auth-input:focus { outline:none; border-color:#4f46e5; box-shadow:0 0 0 3px rgba(79,70,229,.15); }
    .auth-btn { width:100%; background:#4f46e5; color:#fff; border:none; border-radius:10px;
      padding:12px; font-weight:700; font-size:15px; cursor:pointer; }
    .auth-btn:disabled { opacity:.6; cursor:not-allowed; }
    .auth-done { color:#166534; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px;
      padding:14px; font-size:14px; }
    .auth-foot { margin-top:18px; font-size:14px; }
    .auth-foot a { color:#4f46e5; text-decoration:none; }
  `],
})
export class ForgotPasswordComponent {
  private auth = inject(AuthService);
  email = '';
  loading = false;
  sent = false;

  submit(): void {
    if (!this.email) return;
    this.loading = true;
    this.auth.forgotPassword(this.email).subscribe({
      next: () => { this.loading = false; this.sent = true; },
      error: () => { this.loading = false; this.sent = true; }, // same UX regardless
    });
  }
}
