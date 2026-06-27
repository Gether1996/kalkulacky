import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LocaleService } from '../../../i18n/locale.service';
import { Locale, LOCALE_META } from '../../../i18n/locales';

/**
 * Language switcher dropdown (SK / CS / EN / PL / HU).
 * Switching updates the whole UI live via the locale signal.
 */
@Component({
  selector: 'app-language-switcher',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="ls" (mouseleave)="open.set(false)">
      <button class="ls-btn" type="button" (click)="open.set(!open())"
              [attr.aria-expanded]="open()" aria-haspopup="listbox">
        <span class="ls-flag">{{ current.flag }}</span>
        <span class="ls-code">{{ current.code | uppercase }}</span>
        <span class="ls-caret">▾</span>
      </button>
      <ul class="ls-menu" *ngIf="open()" role="listbox">
        <li *ngFor="let l of locales">
          <button type="button" class="ls-item" role="option"
                  [class.active]="l === locale.locale()"
                  (click)="choose(l)">
            <span class="ls-flag">{{ meta[l].flag }}</span>
            <span>{{ meta[l].label }}</span>
          </button>
        </li>
      </ul>
    </div>
  `,
  styles: [`
    .ls { position: relative; display: inline-block; }
    .ls-btn {
      display: inline-flex; align-items: center; gap: 6px;
      background: transparent; border: 1px solid #e2e8f0; border-radius: 8px;
      padding: 6px 10px; cursor: pointer; font-size: 14px; color: inherit;
    }
    .ls-btn:hover { background: rgba(0,0,0,.04); }
    .ls-flag { font-size: 16px; line-height: 1; }
    .ls-code { font-weight: 600; }
    .ls-caret { font-size: 10px; opacity: .6; }
    .ls-menu {
      position: absolute; right: 0; top: calc(100% + 4px); margin: 0; padding: 4px;
      list-style: none; background: #fff; border: 1px solid #e2e8f0;
      border-radius: 10px; box-shadow: 0 8px 24px rgba(0,0,0,.12);
      min-width: 160px; z-index: 1000;
    }
    .ls-item {
      display: flex; align-items: center; gap: 8px; width: 100%;
      background: transparent; border: none; border-radius: 7px;
      padding: 8px 10px; cursor: pointer; font-size: 14px; color: #1e293b;
      text-align: left;
    }
    .ls-item:hover { background: #f1f5f9; }
    .ls-item.active { background: #eff6ff; font-weight: 600; color: #1d4ed8; }
  `],
})
export class LanguageSwitcherComponent {
  locale = inject(LocaleService);
  open = signal(false);
  meta = LOCALE_META;
  locales: Locale[] = this.locale.supported;

  get current() {
    return this.locale.meta();
  }

  choose(l: Locale): void {
    this.locale.setLocale(l);
    this.open.set(false);
  }
}
