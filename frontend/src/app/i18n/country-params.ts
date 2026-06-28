import { Locale } from './locales';

/**
 * Per-country real-world parameters, keyed by UI locale. The site is ONE app
 * that loads values for the country of the currently selected language.
 *
 * ⚠️ IMPORTANT distinction:
 *   - Values that are pure NUMBERS/RATES (VAT %, currency) are safe to localise
 *     per country and are USED today (see the VAT calculator).
 *   - The tax/levy/benefit calculators (salary, freelancer, pension, parental,
 *     sick-leave, solar/heat-pump/renovation subsidies) implement a country's
 *     *tax SYSTEM*, not just its numbers — these systems differ structurally
 *     between SK/CZ/PL/HU. They currently all implement `taxLogic: 'SK'`. Until
 *     a country gets its own engine, those calculators show SK figures and the
 *     app shows the "uses Slovak rules" banner for non-SK/CZ locales.
 *
 * This registry is the foundation: add a country's engine, flip `taxLogic`, and
 * the per-locale wiring is already in place.
 */
export interface VatRates {
  standard: number;
  reduced: number[];
}

export interface EnergyProgram {
  /** Official home-energy subsidy programme name in this country. */
  name: string;
  url: string;
}

export interface CountryParams {
  countryCode: string;     // ISO 3166-1 alpha-2
  countryName: string;     // native name
  currency: string;        // ISO 4217
  currencySymbol: string;
  numberLocale: string;    // BCP-47 for Intl number/currency formatting
  vat: VatRates;
  energyProgram: EnergyProgram;
  /** Representative monthly gross salaries [minimum, average] for quick presets. */
  salaryPresets: number[];
  /** Whether the net-salary calculator has a real engine for this country. */
  salaryEngine: boolean;
  /** Which country's tax rules the OTHER (not-yet-localised) calculators use. */
  taxLogic: 'SK';
}

export const COUNTRY_PARAMS: Record<Locale, CountryParams> = {
  sk: {
    countryCode: 'SK', countryName: 'Slovensko',
    currency: 'EUR', currencySymbol: '€', numberLocale: 'sk-SK',
    vat: { standard: 23, reduced: [19, 5] },
    energyProgram: { name: 'Zelená domácnostiam', url: 'https://zelenadomacnostiam.sk' },
    salaryPresets: [915, 1500], salaryEngine: true,
    taxLogic: 'SK',
  },
  cs: {
    countryCode: 'CZ', countryName: 'Česko',
    currency: 'CZK', currencySymbol: 'Kč', numberLocale: 'cs-CZ',
    vat: { standard: 21, reduced: [12] },
    energyProgram: { name: 'Nová zelená úsporám', url: 'https://novazelenausporam.cz' },
    salaryPresets: [20800, 46000], salaryEngine: true,
    taxLogic: 'SK',
  },
  // English has no country; default to the home market (Slovakia), EUR.
  en: {
    countryCode: 'SK', countryName: 'Slovakia',
    currency: 'EUR', currencySymbol: '€', numberLocale: 'en-IE',
    vat: { standard: 23, reduced: [19, 5] },
    energyProgram: { name: 'Zelená domácnostiam', url: 'https://zelenadomacnostiam.sk' },
    salaryPresets: [915, 1500], salaryEngine: true,
    taxLogic: 'SK',
  },
  pl: {
    countryCode: 'PL', countryName: 'Polska',
    currency: 'PLN', currencySymbol: 'zł', numberLocale: 'pl-PL',
    vat: { standard: 23, reduced: [8, 5] },
    energyProgram: { name: 'Czyste Powietrze', url: 'https://czystepowietrze.gov.pl' },
    salaryPresets: [4666, 8000], salaryEngine: true,
    taxLogic: 'SK',
  },
  hu: {
    countryCode: 'HU', countryName: 'Magyarország',
    currency: 'HUF', currencySymbol: 'Ft', numberLocale: 'hu-HU',
    vat: { standard: 27, reduced: [18, 5] },
    energyProgram: { name: 'Otthonfelújítási támogatás', url: 'https://kormany.hu' },
    salaryPresets: [290800, 500000], salaryEngine: true,
    taxLogic: 'SK',
  },
};

export function getCountryParams(locale: Locale): CountryParams {
  return COUNTRY_PARAMS[locale] ?? COUNTRY_PARAMS.sk;
}
