import { Injectable, PLATFORM_ID, REQUEST, inject, signal, computed } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import {
  DEFAULT_LOCALE,
  Locale,
  LOCALE_META,
  SUPPORTED_LOCALES,
  isLocale,
} from './locales';
import { TRANSLATIONS, TranslationDict } from './translations';
import { APP_TRANSLATIONS } from './translations.app';
import { CALC_TRANSLATIONS } from './translations.calc';

// Merge base (nav/monetization) + app-wide (chrome) + calculator-body dicts.
const MERGED: Record<Locale, TranslationDict> = {
  sk: { ...TRANSLATIONS.sk, ...APP_TRANSLATIONS.sk, ...CALC_TRANSLATIONS.sk },
  cs: { ...TRANSLATIONS.cs, ...APP_TRANSLATIONS.cs, ...CALC_TRANSLATIONS.cs },
  en: { ...TRANSLATIONS.en, ...APP_TRANSLATIONS.en, ...CALC_TRANSLATIONS.en },
  pl: { ...TRANSLATIONS.pl, ...APP_TRANSLATIONS.pl, ...CALC_TRANSLATIONS.pl },
  hu: { ...TRANSLATIONS.hu, ...APP_TRANSLATIONS.hu, ...CALC_TRANSLATIONS.hu },
};

const STORAGE_KEY = 'kalk_locale';

/**
 * Runtime locale + translation service (signal-based, SSR-safe).
 *
 * - `locale()` — current locale signal
 * - `t(key)`   — translate a key (falls back to SK, then the raw key)
 * - `setLocale()` — switch language (persists in browser)
 *
 * Phase 1 keeps locale in localStorage + an optional `?lang=` query param.
 * A later phase moves to locale-prefixed URLs (/sk, /cs, /en, /pl, /hu) for
 * fully separate per-language SEO surfaces.
 */
@Injectable({ providedIn: 'root' })
export class LocaleService {
  private platformId = inject(PLATFORM_ID);
  // The incoming HTTP request during SSR (null in the browser). Lets the server
  // render in the requested language instead of always defaulting to Slovak.
  private request = inject(REQUEST, { optional: true });

  readonly locale = signal<Locale>(DEFAULT_LOCALE);
  readonly supported = SUPPORTED_LOCALES;
  readonly meta = computed(() => LOCALE_META[this.locale()]);

  constructor() {
    if (isPlatformBrowser(this.platformId)) {
      const initial = this.detectInitialLocale();
      this.locale.set(initial);
      this.syncDocumentLang(initial);
    } else {
      // SSR: pick the locale from the request's ?lang= so server-rendered HTML
      // (content + SEO meta + <html lang>) matches the language crawlers ask for.
      this.locale.set(this.detectServerLocale());
    }
  }

  private detectServerLocale(): Locale {
    try {
      const url = this.request?.url;
      if (url) {
        const lang = new URL(url, 'http://localhost').searchParams.get('lang');
        if (isLocale(lang)) return lang;
      }
    } catch { /* fall through to default */ }
    return DEFAULT_LOCALE;
  }

  setLocale(locale: Locale): void {
    if (!isLocale(locale)) return;
    this.locale.set(locale);
    if (isPlatformBrowser(this.platformId)) {
      try {
        localStorage.setItem(STORAGE_KEY, locale);
      } catch { /* storage unavailable */ }
      this.syncDocumentLang(locale);
    }
  }

  /** Translate a key for the current locale (falls back to SK, then the key). */
  t(key: string): string {
    const current = MERGED[this.locale()];
    if (current && current[key] != null) return current[key];
    const base = MERGED[DEFAULT_LOCALE];
    return base[key] ?? key;
  }

  metaFor(locale: Locale) {
    return LOCALE_META[locale];
  }

  private detectInitialLocale(): Locale {
    // 1) explicit ?lang= override
    try {
      const param = new URLSearchParams(window.location.search).get('lang');
      if (isLocale(param)) return param;
    } catch { /* ignore */ }
    // 2) stored preference
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (isLocale(stored)) return stored;
    } catch { /* ignore */ }
    // 3) browser language
    try {
      const nav = navigator.language?.slice(0, 2).toLowerCase();
      if (isLocale(nav)) return nav;
    } catch { /* ignore */ }
    return DEFAULT_LOCALE;
  }

  private syncDocumentLang(locale: Locale): void {
    try {
      document.documentElement.lang = locale;
    } catch { /* ignore */ }
  }
}
