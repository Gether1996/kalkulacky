/**
 * Per-country energy / home-improvement parameters for the FRONTEND-ONLY
 * calculators (heat-pump, renovation grant), which compute client-side and so
 * cannot read the backend rate data. This is the single editable source of
 * truth for their yearly-changing numbers — a sibling of `country-params.ts`.
 *
 * ⚠️ INDICATIVE figures — verify per subsidy round (Zelená domácnostiam / Obnov
 * dom / Nová zelená úsporám). Update the numbers here once a year; the
 * components read from these constants and need no code changes.
 *
 * NOTE: the SK PV/solar subsidy numbers also live on the backend
 * (`services/data/sk_2026.json` → solar, exposed via GET /api/calculators/config/).
 * Keep the two in sync each round, or migrate the frontend-only tools to read
 * the backend config endpoint to remove the duplication entirely.
 */

/** Heat-pump per-country pricing, subsidy and fuel costs. */
export interface CountryHeatPumpConfig {
  electricityPrice: number;     // per kWh for the HP's electricity
  costBase: number;             // min turnkey cost
  costPerKw: number;            // turnkey cost per kW of output
  subsidyPerKw: number;         // subsidy per kW
  subsidyMax: number;           // subsidy cap
  fuel: Record<string, number>; // cost per kWh of delivered heat by fuel
}

export const HEAT_PUMP_PARAMS: Record<'SK' | 'CZ', CountryHeatPumpConfig> = {
  // SK — Zelená domácnostiam (INDICATIVE).
  SK: {
    electricityPrice: 0.18, costBase: 9000, costPerKw: 1400,
    subsidyPerKw: 380, subsidyMax: 3400,
    fuel: { gas: 0.10, electric: 0.18, coal: 0.08, oil: 0.13, wood: 0.06 },
  },
  // CZ — Nová zelená úsporám (INDICATIVE, CZK). Flat ~80 000 Kč air-water grant.
  CZ: {
    electricityPrice: 5.0, costBase: 220000, costPerKw: 30000,
    subsidyPerKw: 8000, subsidyMax: 80000,
    fuel: { gas: 2.0, electric: 5.0, coal: 1.5, oil: 3.0, wood: 1.2 },
  },
};

/** Heat-pump constants shared across countries. */
export const HEAT_PUMP_SHARED = {
  dhwKwhPerYear: 1800,       // hot-water demand (indicative)
  scop: 3.5,                 // seasonal COP for a modern air-water HP
  co2KgPerKwhGrid: 0.20,     // grid CO2 intensity
  subsidyRateOfCost: 0.5,    // ≤ 50 % of eligible cost (both countries)
};

/** Renovation-grant per-country caps and rules. */
export interface RenoConfig {
  rate: number;             // share of eligible cost covered
  maxBasic: number;         // cap, ≥30 % savings tier
  maxComprehensive: number; // cap, ≥60 % savings tier
  defaultCost: number;      // default project-cost input
  requiresOldHouse: boolean;// SK Obnov dom requires a pre-2013 house
}

export const RENOVATION_PARAMS: Record<'SK' | 'CZ', RenoConfig> = {
  // SK — Obnov dom (Plán obnovy), INDICATIVE.
  SK: { rate: 0.60, maxBasic: 14000, maxComprehensive: 19000, defaultCost: 25000, requiresOldHouse: true },
  // CZ — Nová zelená úsporám, INDICATIVE (CZK). Broader eligibility, higher caps.
  CZ: { rate: 0.50, maxBasic: 150000, maxComprehensive: 500000, defaultCost: 600000, requiresOldHouse: false },
};
