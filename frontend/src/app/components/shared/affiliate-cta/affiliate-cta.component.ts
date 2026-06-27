import { Component, Input, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MonetizationService } from '../../../services/monetization.service';
import { AffiliateOffer } from '../../../models/monetization.models';
import { TranslatePipe } from '../../../i18n/translate.pipe';

/**
 * Renders contextual partner/affiliate offers for a calculator and tracks
 * outbound clicks. Drop into any calculator template:
 *
 *   <app-affiliate-cta calculatorType="mortgage"></app-affiliate-cta>
 */
@Component({
  selector: 'app-affiliate-cta',
  standalone: true,
  imports: [CommonModule, TranslatePipe],
  template: `
    <div class="aff-wrap" *ngIf="offers.length">
      <div class="aff-card" *ngFor="let offer of offers">
        <div class="aff-icon" *ngIf="offer.icon">{{ offer.icon }}</div>
        <div class="aff-body">
          <div class="aff-head">
            <span class="aff-title">{{ offer.title }}</span>
            <span class="aff-badge" *ngIf="offer.badge">{{ offer.badge }}</span>
          </div>
          <p class="aff-desc">{{ offer.description }}</p>
        </div>
        <a
          class="aff-cta"
          [href]="offer.url"
          target="_blank"
          rel="nofollow sponsored noopener"
          (click)="onClick(offer)"
        >{{ offer.ctaLabel }}</a>
      </div>
      <p class="aff-disclosure">{{ 'aff.disclosure' | t }}</p>
    </div>
  `,
  styles: [`
    .aff-wrap { display: flex; flex-direction: column; gap: 12px; margin: 16px 0; }
    .aff-card {
      display: flex; align-items: center; gap: 14px;
      border: 1px solid #e5e7eb; border-radius: 12px; padding: 14px 16px;
      background: #fff; box-shadow: 0 1px 2px rgba(0,0,0,.04);
    }
    .aff-icon { font-size: 28px; line-height: 1; flex-shrink: 0; }
    .aff-body { flex: 1; min-width: 0; }
    .aff-head { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
    .aff-title { font-weight: 600; color: #111827; }
    .aff-badge {
      font-size: 11px; text-transform: uppercase; letter-spacing: .03em;
      background: #fef3c7; color: #92400e; padding: 2px 8px; border-radius: 999px;
    }
    .aff-desc { margin: 4px 0 0; font-size: 14px; color: #6b7280; }
    .aff-cta {
      flex-shrink: 0; white-space: nowrap; text-decoration: none;
      background: #2563eb; color: #fff; font-weight: 600; font-size: 14px;
      padding: 10px 16px; border-radius: 10px; transition: background .15s;
    }
    .aff-cta:hover { background: #1d4ed8; }
    .aff-disclosure { font-size: 12px; color: #9ca3af; margin: 2px 0 0; }
    @media (max-width: 540px) {
      .aff-card { flex-direction: column; align-items: stretch; text-align: left; }
      .aff-cta { text-align: center; }
    }
  `],
})
export class AffiliateCtaComponent implements OnInit {
  @Input() calculatorType = '';
  private monetization = inject(MonetizationService);
  offers: AffiliateOffer[] = [];

  ngOnInit(): void {
    const config = this.monetization.getConfig(this.calculatorType);
    this.offers = config?.affiliateOffers ?? [];
  }

  onClick(offer: AffiliateOffer): void {
    this.monetization.trackAffiliateClick(offer, this.calculatorType);
  }
}
