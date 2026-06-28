/**
 * Flat registry of every calculator (id -> route + icon). Used wherever we need
 * to render a calculator reference from just its id — favourites in the navbar,
 * the "My tools" manager on the dashboard, etc. Display names come from i18n
 * (`calc.<id>.name`), so they are not duplicated here.
 */
export interface CalcMeta {
  id: string;
  route: string;
  icon: string;
}

export const CALCULATOR_REGISTRY: CalcMeta[] = [
  { id: 'basic', route: '/calculator/basic', icon: '🧮' },
  { id: 'salary', route: '/calculator/salary', icon: '💰' },
  { id: 'mortgage', route: '/calculator/mortgage', icon: '🏠' },
  { id: 'vat', route: '/calculator/vat', icon: '📊' },
  { id: 'loan', route: '/calculator/loan', icon: '💳' },
  { id: 'payment', route: '/calculator/payment', icon: '💰' },
  { id: 'pension', route: '/calculator/pension', icon: '👴' },
  { id: 'freelancer-tax', route: '/calculator/freelancer-tax', icon: '💼' },
  { id: 'inflation', route: '/calculator/inflation', icon: '📉' },
  { id: 'roi', route: '/calculator/roi', icon: '📊' },
  { id: 'car-leasing', route: '/calculator/car-leasing', icon: '🚗' },
  { id: 'car-insurance', route: '/calculator/car-insurance', icon: '🚗' },
  { id: 'savings-goal', route: '/calculator/savings-goal', icon: '🎯' },
  { id: 'sick-leave', route: '/calculator/sick-leave', icon: '🏥' },
  { id: 'bmi', route: '/calculator/bmi', icon: '⚖️' },
  { id: 'bmr', route: '/calculator/bmr', icon: '🔥' },
  { id: 'pregnancy', route: '/calculator/pregnancy', icon: '🤰' },
  { id: 'parental-benefit', route: '/calculator/parental-benefit', icon: '👶' },
  { id: 'fuel-cost', route: '/calculator/fuel-cost', icon: '⛽' },
  { id: 'percentage', route: '/calculator/percentage', icon: '➗' },
  { id: 'vacation', route: '/calculator/vacation', icon: '🏖️' },
  { id: 'solar', route: '/calculator/solar', icon: '☀️' },
  { id: 'heat-pump', route: '/calculator/heat-pump', icon: '♨️' },
  { id: 'renovation', route: '/calculator/renovation', icon: '🏚️' },
  { id: 'energy', route: '/calculator/energy', icon: '⚡' },
  { id: 'hours-worked', route: '/calculator/hours-worked', icon: '⏰' },
  { id: 'split-bill', route: '/calculator/split-bill', icon: '🧾' },
  { id: 'area-volume', route: '/calculator/area-volume', icon: '📐' },
  { id: 'unit-converter', route: '/calculator/unit-converter', icon: '🔄' },
];

export const CALC_BY_ID: Record<string, CalcMeta> =
  Object.fromEntries(CALCULATOR_REGISTRY.map(c => [c.id, c]));

/** Map a /calculator/<slug> path to a calculator id (or null). */
export function calcIdFromPath(path: string): string | null {
  const m = /^\/calculator\/([a-z0-9-]+)/.exec(path);
  return m ? m[1] : null;
}
