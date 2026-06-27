import { Component, Input, OnInit, inject, signal, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { TranslatePipe } from '../../../i18n/translate.pipe';
import { LocaleService } from '../../../i18n/locale.service';

const ORIGIN = 'https://kalkulacky.sk';

/**
 * "Embed this calculator" box — shows a copy-paste <iframe> snippet so other
 * sites can embed the tool, each embed adding a backlink. Drop onto a calculator
 * page: <app-embed-snippet calculatorType="salary" height="520"></app-embed-snippet>
 */
@Component({
  selector: 'app-embed-snippet',
  standalone: true,
  imports: [CommonModule, TranslatePipe],
  template: `
    <details class="embed-snip">
      <summary>🔗 {{ 'embed.title' | t }}</summary>
      <div class="embed-snip-body">
        <textarea class="embed-snip-code" readonly rows="3" #code>{{ snippet }}</textarea>
        <button class="embed-snip-btn" type="button" (click)="copy(code)">
          {{ copied() ? ('embed.copied' | t) : ('embed.copy' | t) }}
        </button>
      </div>
    </details>
  `,
  styles: [`
    .embed-snip {
      border: 1px solid #e5e7eb; border-radius: 12px; padding: 12px 16px;
      margin: 16px 0; background: #f8fafc;
    }
    .embed-snip summary { cursor: pointer; font-weight: 600; color: #334155; }
    .embed-snip-body { display: flex; gap: 8px; margin-top: 12px; align-items: stretch; }
    .embed-snip-code {
      flex: 1; font-family: ui-monospace, monospace; font-size: 12px;
      border: 1px solid #cbd5e1; border-radius: 8px; padding: 8px; resize: vertical;
      background: #fff; color: #334155;
    }
    .embed-snip-btn {
      white-space: nowrap; background: #2563eb; color: #fff; border: none;
      border-radius: 8px; padding: 0 16px; font-weight: 600; cursor: pointer;
    }
    .embed-snip-btn:hover { background: #1d4ed8; }
    @media (max-width: 540px) { .embed-snip-body { flex-direction: column; }
      .embed-snip-btn { padding: 10px; } }
  `],
})
export class EmbedSnippetComponent implements OnInit {
  @Input() calculatorType = '';
  @Input() height = 560;

  private platformId = inject(PLATFORM_ID);
  private locale = inject(LocaleService);
  copied = signal(false);
  snippet = '';

  ngOnInit(): void {
    const lang = this.locale.locale();
    const src = `${ORIGIN}/embed/${this.calculatorType}?lang=${lang}`;
    this.snippet =
      `<iframe src="${src}" width="100%" height="${this.height}" ` +
      `style="border:1px solid #e5e7eb;border-radius:12px;max-width:600px" ` +
      `loading="lazy" title="Kalkulačka — Kalkulačky.sk"></iframe>`;
  }

  copy(el: HTMLTextAreaElement): void {
    if (!isPlatformBrowser(this.platformId)) return;
    el.select();
    try {
      navigator.clipboard.writeText(this.snippet);
    } catch {
      document.execCommand('copy');
    }
    this.copied.set(true);
    setTimeout(() => this.copied.set(false), 2000);
  }
}
