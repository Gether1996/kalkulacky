import { SeoData } from '../services/seo.service';
import { CALC_BY_ID } from './calculator-registry';
import { Locale } from '../i18n/locales';
import { SEO_SK_EXTRAS } from './seo-faq';

/**
 * Localized SEO for calculators + the home page, applied centrally by `App` on
 * every NavigationEnd (see app.ts). Calculator meta is built from the existing
 * `calc.<id>.name` / `calc.<id>.desc` i18n keys, so every calculator gets a
 * correct title + description in ALL five locales for free.
 *
 * Pages with data-driven SEO (blog-detail, salary-value-page, …) still set their
 * own SEO in ngOnInit; the central handler runs last on navigation and provides
 * the localized calculator meta on top, keeping every language self-canonical.
 */
const SITE_NAME = 'Kalkulačky.sk';

/** Per-locale SEO for the home page (short, keyword-rich, one per market). */
const HOME_SEO: Record<Locale, { title: string; description: string }> = {
  sk: {
    title: 'Kalkulačky.sk – čistá mzda, hypotéka, DPH a ďalšie 2026',
    description:
      'Bezplatné online kalkulačky: čistá mzda, hypotéka, DPH, dôchodok, dotácie a ďalšie. Presné výpočty pre rok 2026.',
  },
  cs: {
    title: 'Kalkulačky.sk – čistá mzda, hypotéka, DPH a další 2026',
    description:
      'Bezplatné online kalkulačky: čistá mzda, hypotéka, DPH, důchod, dotace a další. Přesné výpočty pro rok 2026.',
  },
  en: {
    title: 'Kalkulačky.sk – net salary, mortgage, VAT and more 2026',
    description:
      'Free online calculators: net salary, mortgage, VAT, pension, grants and more. Accurate results for 2026.',
  },
  pl: {
    title: 'Kalkulačky.sk – pensja netto, kredyt, VAT i więcej 2026',
    description:
      'Bezpłatne kalkulatory online: pensja netto, kredyt hipoteczny, VAT, emerytura, dotacje i więcej. Dokładne wyniki na 2026.',
  },
  hu: {
    title: 'Kalkulačky.sk – nettó bér, jelzáloghitel, ÁFA és több 2026',
    description:
      'Ingyenes online kalkulátorok: nettó bér, jelzáloghitel, ÁFA, nyugdíj, támogatások és több. Pontos eredmények 2026-ra.',
  },
};

export function buildHomeSeo(locale: Locale): SeoData {
  const h = HOME_SEO[locale] ?? HOME_SEO.sk;
  return { title: h.title, description: h.description, path: '/', isHomepage: true };
}

// Account/auth routes have no SEO owner; without this the previous page's
// title/canonical/OG lingered in <head>. These are robots-disallowed, so a
// generic site default is enough. (Explicit list avoids clobbering the pages
// that DO self-apply — blog, legal, not-found, salary-value, energia.)
const DEFAULT_SEO_ROUTES = new Set([
  '/login', '/register', '/dashboard', '/profile', '/forgot-password', '/reset-password',
]);

export function defaultSeoFor(path: string, locale: Locale): SeoData | null {
  if (!DEFAULT_SEO_ROUTES.has(path)) return null;
  const h = HOME_SEO[locale] ?? HOME_SEO.sk;
  return { title: SITE_NAME, description: h.description, path };
}

/**
 * Build localized SEO for a calculator from its translated name/description.
 * `t` is the LocaleService translate fn (already locale-aware).
 */
export function buildCalcSeo(
  id: string,
  locale: Locale,
  t: (key: string) => string,
): SeoData | null {
  const meta = CALC_BY_ID[id];
  if (!meta) return null;
  const name = t(`calc.${id}.name`);
  const desc = t(`calc.${id}.desc`);
  // Restore keyword + FAQ rich-result markup for the SK (primary) market.
  // Other locales get clean localized meta until the FAQ is translated.
  const extras = locale === 'sk' ? SEO_SK_EXTRAS[id] : undefined;
  return {
    title: name,
    description: desc,
    path: meta.route,
    isCalculator: true,
    keywords: extras?.keywords,
    faq: extras?.faq,
    breadcrumbs: [
      { name: SITE_NAME, path: '/' },
      { name, path: meta.route },
    ],
  };
}
