"""
Solar / Photovoltaic Subsidy & Payback Calculator (Slovakia)

Estimates recommended PV system size, cost, the *Zelená domácnostiam* subsidy,
net investment, annual savings and payback period. This is the lead-gen anchor
of the "home-energy hub" (V4 report idea #1) — its purpose is to qualify a
homeowner and route them to an installer.

⚠️ All subsidy amounts, prices and yields are INDICATIVE estimates and change
per subsidy round. Constants are centralised below for easy yearly updates.
Always show results as "orientačné" (indicative) in the UI.
"""

from typing import Dict, Any
from .base_calculator import BaseCalculator
from .data import get_rates


# --- Constants loaded from the editable data file (data/sk_2026.json → solar) --
# This calculator is float-based, so the Decimal values are coerced to float/int.
# Update the numbers in sk_<year>.json (per subsidy round / market prices).
# Zelená domácnostiam (SIEA, programme 2023–2029): €500/kW, up to 7 kW eligible
# (=> €3 500 base cap), capped at ≤50 % of eligible costs.
_S = get_rates('SK')['solar']
SK_YIELD_KWH_PER_KWP = int(_S['yield_kwh_per_kwp'])          # avg annual production per kWp
PRICE_PER_KWP_EUR = int(_S['price_per_kwp_eur'])             # turnkey PV price per kWp incl. VAT
BATTERY_PRICE_PER_KWH_EUR = int(_S['battery_price_per_kwh_eur'])
DEFAULT_SELF_CONSUMPTION = float(_S['default_self_consumption'])
BATTERY_SELF_CONSUMPTION = float(_S['battery_self_consumption'])
FEED_IN_PRICE_EUR = float(_S['feed_in_price_eur'])
CO2_KG_PER_KWH = float(_S['co2_kg_per_kwh'])
SUBSIDY_PER_KWP_EUR = int(_S['subsidy_per_kwp_eur'])
SUBSIDY_ELIGIBLE_KWP_MAX = int(_S['subsidy_eligible_kwp_max'])  # max kW eligible
SUBSIDY_MAX_EUR = int(_S['subsidy_max_eur'])                 # base cap
SUBSIDY_RATE_OF_COST = float(_S['subsidy_rate_of_cost'])     # subsidy ≤ 50 % of eligible costs


class SolarSubsidyCalculator(BaseCalculator):
    """Photovoltaic subsidy + payback estimator for Slovak households."""

    def validate_inputs(self, **kwargs) -> bool:
        consumption = kwargs.get('annual_consumption_kwh')
        if consumption is None or float(consumption) <= 0:
            raise ValueError('Zadajte ročnú spotrebu elektriny (kWh).')
        return True

    def calculate(self, **kwargs) -> Dict[str, Any]:
        self.validate_inputs(**kwargs)

        annual_consumption = float(kwargs['annual_consumption_kwh'])
        electricity_rate = float(kwargs.get('electricity_rate') or 0.20)
        include_battery = bool(kwargs.get('include_battery', False))
        battery_kwh = float(kwargs.get('battery_capacity_kwh') or 0)

        # Recommend system size: cover consumption given SK yield, sensible bounds.
        system_kwp = kwargs.get('system_size_kwp')
        if system_kwp:
            system_kwp = float(system_kwp)
        else:
            system_kwp = round(annual_consumption / SK_YIELD_KWH_PER_KWP, 1)
        system_kwp = max(2.0, min(system_kwp, 10.0))

        if include_battery and battery_kwh <= 0:
            # default battery sizing ~ 1.5 kWh per kWp, capped
            battery_kwh = round(min(system_kwp * 1.5, 10.0), 1)
        if not include_battery:
            battery_kwh = 0.0

        annual_production = system_kwp * SK_YIELD_KWH_PER_KWP

        # Costs
        pv_cost = system_kwp * PRICE_PER_KWP_EUR
        battery_cost = battery_kwh * BATTERY_PRICE_PER_KWH_EUR
        total_cost = pv_cost + battery_cost

        # Subsidy — Zelená domácnostiam official rules:
        # €500/kW up to 7 kW eligible (=> €3 500 base cap), AND ≤ 50 % of costs.
        eligible_kwp = min(system_kwp, SUBSIDY_ELIGIBLE_KWP_MAX)
        subsidy_by_power = min(eligible_kwp * SUBSIDY_PER_KWP_EUR, SUBSIDY_MAX_EUR)
        subsidy_by_cost_cap = SUBSIDY_RATE_OF_COST * total_cost
        total_subsidy = min(subsidy_by_power, subsidy_by_cost_cap)

        if total_subsidy >= subsidy_by_cost_cap:
            subsidy_limited_by = '50 % oprávnených nákladov'
        elif eligible_kwp * SUBSIDY_PER_KWP_EUR >= SUBSIDY_MAX_EUR:
            # Derive the amount from the constant so it can't desync from SUBSIDY_MAX_EUR.
            subsidy_limited_by = f'maximálna dotácia ({SUBSIDY_MAX_EUR:,} €)'.replace(',', ' ')
        else:
            subsidy_limited_by = 'výkon (€500/kW, max 7 kW)'

        net_cost = max(total_cost - total_subsidy, 0)

        # Savings
        self_consumption_ratio = (
            BATTERY_SELF_CONSUMPTION if include_battery else DEFAULT_SELF_CONSUMPTION
        )
        self_consumed_kwh = min(annual_production * self_consumption_ratio,
                                annual_consumption)
        exported_kwh = max(annual_production - self_consumed_kwh, 0)

        savings_self = self_consumed_kwh * electricity_rate
        savings_export = exported_kwh * FEED_IN_PRICE_EUR
        annual_savings = savings_self + savings_export

        payback_years = (net_cost / annual_savings) if annual_savings > 0 else None
        coverage_pct = (self_consumed_kwh / annual_consumption * 100
                        if annual_consumption else 0)
        co2_savings_kg = annual_production * CO2_KG_PER_KWH

        return {
            'inputs': {
                'annual_consumption_kwh': round(annual_consumption, 0),
                'electricity_rate': round(electricity_rate, 4),
                'include_battery': include_battery,
            },
            'system': {
                'recommended_kwp': round(system_kwp, 1),
                'battery_capacity_kwh': round(battery_kwh, 1),
                'annual_production_kwh': round(annual_production, 0),
                'self_consumption_ratio': round(self_consumption_ratio, 2),
            },
            'cost': {
                'pv_cost': round(pv_cost, 0),
                'battery_cost': round(battery_cost, 0),
                'total_cost': round(total_cost, 0),
            },
            'subsidy': {
                'eligible_kwp': round(eligible_kwp, 1),
                'rate_per_kwp': SUBSIDY_PER_KWP_EUR,
                'max_subsidy': SUBSIDY_MAX_EUR,
                'total_subsidy': round(total_subsidy, 0),
                'limited_by': subsidy_limited_by,
                'net_cost': round(net_cost, 0),
                'scheme': 'Zelená domácnostiam (orientačne)',
            },
            'savings': {
                'self_consumed_kwh': round(self_consumed_kwh, 0),
                'exported_kwh': round(exported_kwh, 0),
                'annual_savings': round(annual_savings, 0),
                'monthly_savings': round(annual_savings / 12, 0),
                'coverage_pct': round(coverage_pct, 1),
            },
            'analysis': {
                'payback_years': round(payback_years, 1) if payback_years else None,
                'savings_30y': round(annual_savings * 30 - net_cost, 0),
                'co2_savings_kg': round(co2_savings_kg, 0),
            },
        }
