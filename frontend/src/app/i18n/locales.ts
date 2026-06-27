// Supported locales for the V4 cross-border strategy.
// SK is the base; CZ/EN/PL/HU are the expansion markets from the V4 report.

export type Locale = 'sk' | 'cs' | 'en' | 'pl' | 'hu';

export const DEFAULT_LOCALE: Locale = 'sk';

export const SUPPORTED_LOCALES: Locale[] = ['sk', 'cs', 'en', 'pl', 'hu'];

export interface LocaleMeta {
  code: Locale;
  /** BCP-47 tag for hreflang / Intl. */
  hreflang: string;
  label: string;   // native name shown in the switcher
  flag: string;    // emoji flag
}

export const LOCALE_META: Record<Locale, LocaleMeta> = {
  sk: { code: 'sk', hreflang: 'sk-SK', label: 'Slovenčina', flag: '🇸🇰' },
  cs: { code: 'cs', hreflang: 'cs-CZ', label: 'Čeština', flag: '🇨🇿' },
  en: { code: 'en', hreflang: 'en', label: 'English', flag: '🇬🇧' },
  pl: { code: 'pl', hreflang: 'pl-PL', label: 'Polski', flag: '🇵🇱' },
  hu: { code: 'hu', hreflang: 'hu-HU', label: 'Magyar', flag: '🇭🇺' },
};

export function isLocale(value: string | null | undefined): value is Locale {
  return !!value && (SUPPORTED_LOCALES as string[]).includes(value);
}
