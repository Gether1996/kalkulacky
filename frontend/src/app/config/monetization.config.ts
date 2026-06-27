import { CalculatorMonetization } from '../models/monetization.models';

/**
 * Central monetization configuration — one entry per calculator.
 *
 * This is the single place to wire revenue onto calculators:
 *   - leadOffer        → high-value qualified lead capture (€3–40/lead)
 *   - affiliateOffers  → contextual partner CTAs (commission per click/sale)
 *   - showAds          → display-ad slots (AdSense/Ezoic)
 *
 * ⚠️ The affiliate `url`s below are PLACEHOLDERS. Replace each with your real
 *    tracking deeplink from the relevant network once partner deals are signed:
 *    Dognet (V4-wide), eHUB.sk/.cz, VIVnetworks, Heureka affiliate, or direct
 *    partner programs. The report's Part 6 step 2 ("email 5–10 buyers, get a
 *    price") should be done before relying on lead values.
 */

export const MONETIZATION_CONFIG: Record<string, CalculatorMonetization> = {
  // ---- HIGHEST-VALUE LEAD-GEN VERTICALS ----
  mortgage: {
    calculatorType: 'mortgage',
    showAds: true,
    leadOffer: {
      vertical: 'mortgage',
      headline: 'Získajte 3 nezáväzné ponuky na hypotéku',
      subtext: 'Porovnáme za vás banky a ozve sa vám overený hypotekárny špecialista. Zdarma a nezáväzne.',
      ctaLabel: 'Chcem nezáväznú ponuku',
      fields: ['name', 'phone', 'region'],
      estimatedValueEur: 25,
    },
    affiliateOffers: [
      {
        id: 'mortgage-broker-generic',
        partner: 'Partner',
        title: 'Refinancovanie hypotéky – ušetrite na splátke',
        description: 'Porovnanie aktuálnych sadzieb a refinancovania od overených sprostredkovateľov.',
        ctaLabel: 'Porovnať sadzby',
        url: 'https://example.com/affiliate/hypoteka',
        icon: '🏦',
        badge: 'Sponzorované',
      },
    ],
  },

  solar: {
    calculatorType: 'solar',
    showAds: true,
    leadOffer: {
      vertical: 'solar',
      headline: 'Získajte nezáväznú ponuku na fotovoltiku',
      subtext: 'Spojíme vás s overenou montážnou firmou vo vašom regióne a poradíme s dotáciou Zelená domácnostiam. Zdarma a nezáväzne.',
      ctaLabel: 'Chcem ponuku na fotovoltiku',
      fields: ['name', 'phone', 'region'],
      estimatedValueEur: 18,
    },
    affiliateOffers: [
      {
        id: 'solar-financing',
        partner: 'Partner',
        title: 'Financovanie fotovoltiky',
        description: 'Zelená pôžička alebo úver na fotovoltiku s výhodnou sadzbou.',
        ctaLabel: 'Zobraziť ponuky',
        url: 'https://example.com/affiliate/fotovoltika-financovanie',
        icon: '🔆',
      },
    ],
  },

  salary: {
    calculatorType: 'salary',
    showAds: true,
    affiliateOffers: [
      {
        id: 'salary-accounting-saas',
        partner: 'Partner',
        title: 'Účtovný a mzdový softvér',
        description: 'Vyskúšajte online mzdy a fakturáciu zadarmo – ideálne pre malé firmy a SZČO.',
        ctaLabel: 'Vyskúšať zadarmo',
        url: 'https://example.com/affiliate/uctovny-softver',
        icon: '🧾',
      },
      {
        id: 'salary-banking',
        partner: 'Partner',
        title: 'Účet, na ktorý vám príde výplata',
        description: 'Bežný účet bez poplatkov a s odmenou za aktivitu.',
        ctaLabel: 'Zobraziť ponuku',
        url: 'https://example.com/affiliate/banka',
        icon: '💳',
      },
    ],
  },

  'freelancer-tax': {
    calculatorType: 'freelancer-tax',
    showAds: true,
    leadOffer: {
      vertical: 'accounting',
      headline: 'Nechajte si dane a odvody spočítať účtovníkom',
      subtext: 'Spojíme vás s overeným účtovníkom pre SZČO. Prvá konzultácia nezáväzne.',
      ctaLabel: 'Chcem účtovníka',
      fields: ['name', 'email', 'region'],
      estimatedValueEur: 12,
    },
    affiliateOffers: [
      {
        id: 'freelancer-invoicing',
        partner: 'Partner',
        title: 'Fakturácia a evidencia pre živnostníkov',
        description: 'Vystavte faktúru za minútu, sledujte odvody a termíny. Zadarmo na vyskúšanie.',
        ctaLabel: 'Vyskúšať zadarmo',
        url: 'https://example.com/affiliate/fakturacia',
        icon: '📑',
      },
    ],
  },

  energy: {
    calculatorType: 'energy',
    showAds: true,
    leadOffer: {
      vertical: 'solar',
      headline: 'Oplatí sa vám fotovoltika? Získajte nezáväznú ponuku',
      subtext: 'Spojíme vás s overenou montážnou firmou a poradíme s dotáciou Zelená domácnostiam.',
      ctaLabel: 'Chcem ponuku na fotovoltiku',
      fields: ['name', 'phone', 'region'],
      estimatedValueEur: 15,
    },
    affiliateOffers: [
      {
        id: 'energy-switch',
        partner: 'Partner',
        title: 'Porovnanie dodávateľov energií',
        description: 'Nájdite lacnejšieho dodávateľa elektriny a plynu.',
        ctaLabel: 'Porovnať ceny',
        url: 'https://example.com/affiliate/energie',
        icon: '⚡',
      },
    ],
  },

  loan: {
    calculatorType: 'loan',
    showAds: true,
    affiliateOffers: [
      {
        id: 'loan-compare',
        partner: 'Partner',
        title: 'Porovnanie spotrebných úverov',
        description: 'Nájdite úver s najnižšou úrokovou sadzbou a bez skrytých poplatkov.',
        ctaLabel: 'Porovnať úvery',
        url: 'https://example.com/affiliate/uver',
        icon: '💶',
      },
    ],
  },

  'car-leasing': {
    calculatorType: 'car-leasing',
    showAds: true,
    affiliateOffers: [
      {
        id: 'car-financing',
        partner: 'Partner',
        title: 'Financovanie auta na mieru',
        description: 'Porovnajte lízing a úver na auto od viacerých poskytovateľov.',
        ctaLabel: 'Zobraziť ponuky',
        url: 'https://example.com/affiliate/auto-financovanie',
        icon: '🚗',
      },
    ],
  },

  pension: {
    calculatorType: 'pension',
    showAds: true,
    affiliateOffers: [
      {
        id: 'pension-pillar3',
        partner: 'Partner',
        title: 'III. pilier – sporenie na dôchodok s príspevkom',
        description: 'Daňová úľava a možný príspevok od zamestnávateľa.',
        ctaLabel: 'Zistiť viac',
        url: 'https://example.com/affiliate/dochodok',
        icon: '💼',
      },
    ],
  },

  'sick-leave': { calculatorType: 'sick-leave', showAds: true },
  'parental-benefit': { calculatorType: 'parental-benefit', showAds: true },
  vat: { calculatorType: 'vat', showAds: true },
  inflation: { calculatorType: 'inflation', showAds: true },
  roi: { calculatorType: 'roi', showAds: true },
};

export function getCalculatorMonetization(
  calculatorType: string
): CalculatorMonetization | undefined {
  return MONETIZATION_CONFIG[calculatorType];
}
