import { Locale } from '../locales';

/** Per-page SEO content (title/description/keywords/FAQ) for one locale. */
export interface SeoEntry {
  title: string;
  description: string;
  keywords?: string;
  faq?: { question: string; answer: string }[];
}

/** All 5 locales for one page. */
export type LocaleSeo = Record<Locale, SeoEntry>;

/** id (route slug) → localized SEO content. */
export type SeoContentMap = Record<string, LocaleSeo>;
