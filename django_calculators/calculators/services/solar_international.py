"""
Czech (CZ) photovoltaic subsidy & payback estimator — Nová zelená úsporám 2026.

Returns the same result shape as the Slovak SolarSubsidyCalculator so the solar
frontend renders CZ figures in CZK. INDICATIVE — NZÚ amounts vary by configuration;
verify on novazelenausporam.cz. Constants centralised for yearly updates.
"""
from typing import Dict, Any

from .data import get_rates

# --- CZ indicative constants (CZK) loaded from data/cz_2026.json → solar -------
_S = get_rates('CZ')['solar']
YIELD_KWH_PER_KWP = _S['yield_kwh_per_kwp']
PRICE_PER_KWP = _S['price_per_kwp']              # turnkey PV price per kWp
BATTERY_PRICE_PER_KWH = _S['battery_price_per_kwh']
DEFAULT_SELF_CONSUMPTION = _S['default_self_consumption']
BATTERY_SELF_CONSUMPTION = _S['battery_self_consumption']
DEFAULT_ELECTRICITY_RATE = _S['default_electricity_rate']  # Kč/kWh
FEED_IN_PRICE = _S['feed_in_price']             # Kč/kWh
CO2_KG_PER_KWH = _S['co2_kg_per_kwh']           # CZ grid is more carbon-intensive than SK

# Nová zelená úsporám — FVE (INDICATIVE): base + per-kWp + battery bonus, ≤50 % cost.
NZU_BASE = _S['nzu_base']
NZU_PER_KWP = _S['nzu_per_kwp']
NZU_KWP_CAP = _S['nzu_kwp_cap']
NZU_BATTERY_BONUS = _S['nzu_battery_bonus']
SUBSIDY_RATE_OF_COST = _S['subsidy_rate_of_cost']

# System-sizing bounds (kWp / battery), also from the data file.
KWP_MIN = _S['kwp_min']
KWP_MAX = _S['kwp_max']
BATTERY_RATIO = _S['battery_ratio']
BATTERY_MAX = _S['battery_max']


def _r(x, d=0):
    return round(float(x) + 1e-9, d)


def calculate_cz_solar(annual_consumption_kwh, electricity_rate=None,
                       system_size_kwp=None, include_battery=False,
                       battery_capacity_kwh=0, **kwargs) -> Dict[str, Any]:
    annual_consumption = float(annual_consumption_kwh)
    if annual_consumption <= 0:
        raise ValueError('Zadejte roční spotřebu elektřiny (kWh).')
    rate = float(electricity_rate) if electricity_rate else DEFAULT_ELECTRICITY_RATE
    include_battery = bool(include_battery)

    kwp = float(system_size_kwp) if system_size_kwp else round(annual_consumption / YIELD_KWH_PER_KWP, 1)
    kwp = max(KWP_MIN, min(kwp, KWP_MAX))
    battery_kwh = float(battery_capacity_kwh or 0)
    if include_battery and battery_kwh <= 0:
        battery_kwh = round(min(kwp * BATTERY_RATIO, BATTERY_MAX), 1)
    if not include_battery:
        battery_kwh = 0.0

    annual_production = kwp * YIELD_KWH_PER_KWP
    pv_cost = kwp * PRICE_PER_KWP
    battery_cost = battery_kwh * BATTERY_PRICE_PER_KWH
    total_cost = pv_cost + battery_cost

    subsidy_by_scheme = NZU_BASE + NZU_PER_KWP * min(kwp, NZU_KWP_CAP) + (NZU_BATTERY_BONUS if include_battery else 0)
    subsidy_by_cost = SUBSIDY_RATE_OF_COST * total_cost
    total_subsidy = min(subsidy_by_scheme, subsidy_by_cost)
    limited_by = '50 % nákladů' if total_subsidy >= subsidy_by_cost else 'sazba programu'
    net_cost = max(total_cost - total_subsidy, 0)

    scr = BATTERY_SELF_CONSUMPTION if include_battery else DEFAULT_SELF_CONSUMPTION
    self_consumed = min(annual_production * scr, annual_consumption)
    exported = max(annual_production - self_consumed, 0)
    annual_savings = self_consumed * rate + exported * FEED_IN_PRICE
    payback = (net_cost / annual_savings) if annual_savings > 0 else None
    coverage = (self_consumed / annual_consumption * 100) if annual_consumption else 0

    return {
        'country': 'CZ', 'currency': 'CZK',
        'inputs': {
            'annual_consumption_kwh': _r(annual_consumption),
            'electricity_rate': round(rate, 4),
            'include_battery': include_battery,
        },
        'system': {
            'recommended_kwp': round(kwp, 1),
            'battery_capacity_kwh': round(battery_kwh, 1),
            'annual_production_kwh': _r(annual_production),
            'self_consumption_ratio': round(scr, 2),
        },
        'cost': {
            'pv_cost': _r(pv_cost), 'battery_cost': _r(battery_cost), 'total_cost': _r(total_cost),
        },
        'subsidy': {
            'eligible_kwp': round(min(kwp, NZU_KWP_CAP), 1),
            'rate_per_kwp': NZU_PER_KWP,
            'max_subsidy': _r(NZU_BASE + NZU_PER_KWP * NZU_KWP_CAP + NZU_BATTERY_BONUS),
            'total_subsidy': _r(total_subsidy),
            'limited_by': limited_by,
            'net_cost': _r(net_cost),
            'scheme': 'Nová zelená úsporám (orientačně)',
        },
        'savings': {
            'self_consumed_kwh': _r(self_consumed), 'exported_kwh': _r(exported),
            'annual_savings': _r(annual_savings), 'monthly_savings': _r(annual_savings / 12),
            'coverage_pct': round(coverage, 1),
        },
        'analysis': {
            'payback_years': round(payback, 1) if payback else None,
            'savings_30y': _r(annual_savings * 30 - net_cost),
            'co2_savings_kg': _r(annual_production * CO2_KG_PER_KWH),
        },
    }
