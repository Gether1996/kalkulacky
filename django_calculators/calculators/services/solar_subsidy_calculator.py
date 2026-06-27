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


# --- Tunable constants (update per subsidy round / market prices) -------------
# Sources (verified 2026-06): zelenadomacnostiam.sk (SIEA official), ZSE/VSE,
# Slovak installer pricing (solarsystem.sk, vainex.sk, energala.sk).
SK_YIELD_KWH_PER_KWP = 1000      # avg annual production per kWp in SK (~1000) [VSE]
PRICE_PER_KWP_EUR = 1100         # turnkey PV price per kWp incl. VAT (~900–1200) [installers]
BATTERY_PRICE_PER_KWH_EUR = 550  # usable storage price per kWh (indicative)
DEFAULT_SELF_CONSUMPTION = 0.40  # share used directly without battery (~30–40 %)
BATTERY_SELF_CONSUMPTION = 0.75  # raised self-consumption with a battery (~70–80 %)
FEED_IN_PRICE_EUR = 0.05         # export/feed-in value per kWh (indicative)
CO2_KG_PER_KWH = 0.20            # grid CO2 intensity (kg/kWh)

# Zelená domácnostiam (SIEA, programme 2023–2029) — verified official rules:
#   • €500 per kW of installed PV output.
#   • Eligible power: 3 kW by default, up to 7 kW with documented consumption.
#   • Max PV subsidy €3 500 (base), up to €4 025 with the +15 % bonus
#     (air-quality zone / ceasing solid-fuel heating).
#   • Capped at 50 % of total eligible costs (battery counts into eligible costs,
#     there is no separate per-kWh battery voucher).
SUBSIDY_PER_KWP_EUR = 500
SUBSIDY_ELIGIBLE_KWP_MAX = 7     # max kW eligible (with consumption documentation)
SUBSIDY_MAX_EUR = 3500           # base cap (€4 025 only with the +15 % bonus)
SUBSIDY_RATE_OF_COST = 0.50      # subsidy ≤ 50 % of eligible costs


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
            subsidy_limited_by = 'maximálna dotácia (3 500 €)'
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
