import {
  Component,
  Input,
  AfterViewInit,
  PLATFORM_ID,
  inject,
} from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { environment } from '../../../../environments/environment';
import { TranslatePipe } from '../../../i18n/translate.pipe';

/**
 * Display-ad slot (Google AdSense ready).
 *
 * Set `adsensePublisherId` in environment to activate. Until then the slot
 * renders nothing in production and a labelled placeholder in dev, so the
 * layout is reserved without shipping empty/abusive ad markup.
 *
 *   <app-ad-slot slot="1234567890"></app-ad-slot>
 *
 * Remember to add the AdSense loader script to index.html once approved:
 *   <script async
 *     src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXX"
 *     crossorigin="anonymous"></script>
 */
@Component({
  selector: 'app-ad-slot',
  standalone: true,
  imports: [CommonModule, TranslatePipe],
  template: `
    <ng-container *ngIf="publisherId; else placeholder">
      <ins
        class="adsbygoogle"
        style="display:block"
        [attr.data-ad-client]="publisherId"
        [attr.data-ad-slot]="slot"
        data-ad-format="auto"
        data-full-width-responsive="true"
      ></ins>
    </ng-container>
    <ng-template #placeholder>
      <div class="ad-placeholder" *ngIf="!production">
        <span>{{ 'ad.placeholder' | t }}</span>
        <small>slot: {{ slot || 'n/a' }}</small>
      </div>
    </ng-template>
  `,
  styles: [`
    :host { display: block; margin: 18px 0; }
    .ad-placeholder {
      border: 1px dashed #cbd5e1; border-radius: 12px;
      min-height: 90px; display: flex; flex-direction: column;
      align-items: center; justify-content: center; gap: 2px;
      color: #94a3b8; background: #f8fafc; font-size: 13px;
    }
    .ad-placeholder small { font-size: 11px; opacity: .7; }
  `],
})
export class AdSlotComponent implements AfterViewInit {
  @Input() slot = '';
  private platformId = inject(PLATFORM_ID);

  // AdSense publisher id (e.g. "ca-pub-XXXXXXXXXXXXXXXX"); empty = inactive.
  publisherId = (environment as any).adsensePublisherId || '';
  production = environment.production;

  ngAfterViewInit(): void {
    if (!isPlatformBrowser(this.platformId) || !this.publisherId) return;
    try {
      const w = window as any;
      (w.adsbygoogle = w.adsbygoogle || []).push({});
    } catch {
      /* AdSense not loaded yet — ignore */
    }
  }
}
