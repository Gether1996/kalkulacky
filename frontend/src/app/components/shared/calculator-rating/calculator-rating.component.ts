import { Component, OnInit, PLATFORM_ID, DestroyRef, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { TranslatePipe } from '../../../i18n/translate.pipe';
import { LocaleService } from '../../../i18n/locale.service';
import { AuthService } from '../../../services/auth.service';
import { RatingService, RatingAggregate } from '../../../services/rating.service';
import { calcIdFromPath } from '../../../config/calculator-registry';

/**
 * Global calculator rating widget (1–5 stars + comment). Mounted once in the app
 * shell; it derives the calculator id from the current /calculator/<slug> route
 * (like the data-report widget) and renders nothing elsewhere. Anyone can see the
 * average + recent comments; logged-in users can submit/update their own rating.
 */
@Component({
  selector: 'app-calculator-rating',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslatePipe],
  template: `
    <section class="rating-box" *ngIf="calcId()">
      <h3 class="rating-title">{{ 'rate.title' | t }}</h3>

      <!-- Average summary -->
      <div class="rating-summary">
        <div class="stars" aria-hidden="true">
          <span *ngFor="let s of [1,2,3,4,5]"
                class="star" [class.filled]="s <= roundedAvg()">★</span>
        </div>
        <span class="avg-text" *ngIf="agg() && agg()!.count > 0">
          {{ agg()!.average }} / 5 · {{ agg()!.count }} {{ 'rate.count' | t }}
        </span>
        <span class="avg-text muted" *ngIf="!agg() || agg()!.count === 0">
          {{ 'rate.avgNone' | t }}
        </span>
      </div>

      <!-- Submit / edit (logged-in) -->
      <div class="rating-form" *ngIf="auth.isAuthenticated(); else loginTpl">
        <div class="rating-label">{{ 'rate.yourRating' | t }}</div>
        <div class="stars input" role="radiogroup">
          <button type="button" *ngFor="let s of [1,2,3,4,5]"
                  class="star btn" [class.filled]="s <= (hover() || myRating())"
                  (mouseenter)="hover.set(s)" (mouseleave)="hover.set(0)"
                  (click)="myRating.set(s)"
                  [attr.aria-label]="s + '/5'">★</button>
        </div>
        <textarea class="rating-comment" rows="2" [(ngModel)]="myComment"
                  [placeholder]="'rate.commentPh' | t"></textarea>
        <div class="rating-actions">
          <button type="button" class="rating-submit" (click)="submit()"
                  [disabled]="!myRating() || saving()">
            {{ hasExisting() ? ('rate.update' | t) : ('rate.submit' | t) }}
          </button>
          <span class="rating-thanks" *ngIf="submitted()">{{ 'rate.thanks' | t }}</span>
        </div>
      </div>
      <ng-template #loginTpl>
        <div class="rating-login">
          {{ 'rate.loginPrompt' | t }}
          <a (click)="goLogin()" class="rating-login-link">{{ 'rate.login' | t }}</a>
        </div>
      </ng-template>

      <!-- Recent comments -->
      <div class="rating-recent" *ngIf="agg() && agg()!.recent.length">
        <div class="recent-title">{{ 'rate.recent' | t }}</div>
        <div class="recent-item" *ngFor="let r of agg()!.recent">
          <div class="recent-head">
            <span class="recent-stars" aria-hidden="true">
              <span *ngFor="let s of [1,2,3,4,5]" class="star sm" [class.filled]="s <= r.rating">★</span>
            </span>
            <span class="recent-author">{{ r.author }}</span>
          </div>
          <div class="recent-comment">{{ r.comment }}</div>
        </div>
      </div>
    </section>
  `,
  styles: [`
    .rating-box { max-width: 720px; margin: 1.5rem auto; padding: 1.25rem 1.5rem;
      border: 1px solid #e2e8f0; border-radius: 14px; background: #fff;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    .rating-title { font-size: 1.15rem; font-weight: 700; color: #1e293b; margin: 0 0 0.75rem; }
    .rating-summary { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.75rem; flex-wrap: wrap; }
    .stars { display: inline-flex; gap: 2px; font-size: 1.3rem; }
    .stars.input .star.btn { background: none; border: none; cursor: pointer; padding: 0 1px; font-size: 1.6rem; line-height: 1; }
    .star { color: #cbd5e1; }
    .star.filled { color: #f59e0b; }
    .star.sm { font-size: 0.95rem; }
    .avg-text { color: #475569; font-weight: 600; font-size: 0.95rem; }
    .avg-text.muted { color: #94a3b8; font-weight: 500; }
    .rating-label { font-size: 0.85rem; font-weight: 600; color: #475569; margin-bottom: 0.25rem; }
    .rating-comment { width: 100%; border: 1px solid #cbd5e1; border-radius: 10px; padding: 0.6rem 0.75rem;
      font-size: 0.95rem; margin: 0.5rem 0; resize: vertical; box-sizing: border-box; }
    .rating-comment:focus { outline: none; border-color: #f59e0b; box-shadow: 0 0 0 3px rgba(245,158,11,.15); }
    .rating-actions { display: flex; align-items: center; gap: 0.75rem; }
    .rating-submit { background: #f59e0b; color: #fff; border: none; border-radius: 10px;
      padding: 0.6rem 1.2rem; font-weight: 700; cursor: pointer; }
    .rating-submit:disabled { opacity: 0.55; cursor: not-allowed; }
    .rating-thanks { color: #16a34a; font-weight: 600; font-size: 0.9rem; }
    .rating-login { color: #475569; font-size: 0.95rem; }
    .rating-login-link { color: #2563eb; cursor: pointer; text-decoration: underline; margin-left: 0.35rem; }
    .rating-recent { margin-top: 1rem; border-top: 1px solid #f1f5f9; padding-top: 0.85rem; }
    .recent-title { font-size: 0.85rem; font-weight: 700; color: #475569; margin-bottom: 0.5rem; }
    .recent-item { padding: 0.5rem 0; border-bottom: 1px solid #f8fafc; }
    .recent-head { display: flex; align-items: center; gap: 0.5rem; }
    .recent-author { font-size: 0.82rem; color: #94a3b8; font-weight: 600; }
    .recent-comment { color: #334155; font-size: 0.92rem; margin-top: 0.15rem; }
  `],
})
export class CalculatorRatingComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private router = inject(Router);
  private ratingApi = inject(RatingService);
  auth = inject(AuthService);
  private locale = inject(LocaleService);
  private destroyRef = inject(DestroyRef);

  calcId = signal<string | null>(null);
  agg = signal<RatingAggregate | null>(null);
  myRating = signal(0);
  hover = signal(0);
  myComment = '';
  saving = signal(false);
  submitted = signal(false);
  hasExisting = signal(false);

  roundedAvg(): number {
    return Math.round(this.agg()?.average ?? 0);
  }

  ngOnInit(): void {
    this.apply(this.router.url);
    this.router.events
      .pipe(
        filter((e): e is NavigationEnd => e instanceof NavigationEnd),
        takeUntilDestroyed(this.destroyRef),
      )
      .subscribe(e => this.apply(e.urlAfterRedirects));
  }

  private apply(url: string): void {
    const path = url.split('?')[0];
    const id = calcIdFromPath(path);
    this.calcId.set(id);
    // Reset per-calculator state.
    this.agg.set(null);
    this.myRating.set(0);
    this.myComment = '';
    this.submitted.set(false);
    this.hasExisting.set(false);
    if (id && isPlatformBrowser(this.platformId)) {
      this.load(id);
    }
  }

  private load(id: string): void {
    this.ratingApi.getRatings(id).subscribe({
      next: (res) => {
        this.agg.set(res);
        if (res.my_rating) {
          this.myRating.set(res.my_rating.rating);
          this.myComment = res.my_rating.comment || '';
          this.hasExisting.set(true);
        }
      },
      error: () => { /* leave empty */ },
    });
  }

  submit(): void {
    const id = this.calcId();
    if (!id || !this.myRating()) return;
    this.saving.set(true);
    this.ratingApi.submitRating(id, this.myRating(), this.myComment).subscribe({
      next: (res) => {
        this.saving.set(false);
        this.submitted.set(true);
        this.hasExisting.set(true);
        // Refresh aggregate + recent comments.
        this.load(id);
      },
      error: () => { this.saving.set(false); },
    });
  }

  goLogin(): void {
    this.router.navigate(['/login'], { queryParams: { redirect: this.router.url } });
  }
}
