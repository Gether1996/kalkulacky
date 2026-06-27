// Monetization models — lead-gen, affiliate offers and ad placements.
// These power the "harvest layer" on top of the existing calculators:
// display ads, affiliate CTAs and qualified lead capture.

export type LeadVertical =
  | 'mortgage'
  | 'solar'
  | 'heat_pump'
  | 'renovation'
  | 'insurance_car'
  | 'accounting'
  | 'pension'
  | 'energy'
  | 'loan'
  | 'other';

/**
 * A contextual partner/affiliate offer shown on a calculator page.
 * `url` is the affiliate/deeplink — replace placeholders with real tracking links.
 */
export interface AffiliateOffer {
  id: string;            // stable id used for click tracking
  partner: string;       // partner/network name (e.g. 'Dognet', 'eHUB')
  title: string;         // headline shown to the user
  description: string;   // 1–2 line pitch
  ctaLabel: string;      // button text
  url: string;           // affiliate deeplink (outbound)
  icon?: string;         // emoji/icon
  badge?: string;        // optional badge e.g. "TOP", "Sponzorované"
}

/**
 * A lead-gen offer: instead of sending the user away, we capture a qualified
 * enquiry and route/sell it to a partner (€3–40 per lead).
 */
export interface LeadOffer {
  vertical: LeadVertical;
  headline: string;        // e.g. "Získajte 3 nezáväzné ponuky hypoték"
  subtext: string;         // reassurance / what happens next
  ctaLabel: string;        // submit button
  fields?: LeadFieldKey[]; // which optional fields to show (name/phone/region/message)
  estimatedValueEur?: number; // internal — indicative lead value
}

export type LeadFieldKey = 'name' | 'email' | 'phone' | 'region' | 'message';

/**
 * Full monetization config for a single calculator.
 */
export interface CalculatorMonetization {
  calculatorType: string;       // matches backend calculator_type / route id
  leadOffer?: LeadOffer;        // primary lead-gen offer (highest value)
  affiliateOffers?: AffiliateOffer[];
  showAds?: boolean;            // whether to render display-ad slots
}

export interface LeadSubmission {
  vertical: LeadVertical;
  calculator_type: string;
  name?: string;
  email?: string;
  phone?: string;
  region?: string;
  message?: string;
  context?: Record<string, any>;
  consent: boolean;
  source_url?: string;
}
