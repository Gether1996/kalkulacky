"""
International freelancer/self-employed tax calculators (currently Czechia).

Mirrors the Slovak `FreelancerTaxCalculator` result shape so the frontend can
render CZ with the same template (SK-specific social sub-items are gated off in
the UI). Czech OSVČ 2026 — INDICATIVE; verify against Finanční správa / ČSSZ /
health insurer before relying. Constants centralised below for yearly updates.

Sources (2026-06): portal.pohoda.cz, fakturoid.cz almanach, ČSOB průvodce
podnikáním, podnikatel.cz — OSVČ 2026.
"""

from typing import Dict, Any


def _r(x: float) -> float:
    return round(float(x) + 1e-9, 2)


def calculate_cz_freelancer(
    annual_revenue: float,
    annual_expenses: float = 0,
    use_flat_expenses: bool = True,
    include_sickness: bool = True,
    months_active: int = 12,
    **kwargs,
) -> Dict[str, Any]:
    # --- Czech OSVČ 2026 constants (CZK) --------------------------------------
    HEALTH_RATE = 0.135          # zdravotní pojištění
    HEALTH_BASE_SHARE = 0.50     # assessment base = 50 % of profit
    HEALTH_MIN_BASE_MONTHLY = 24483.50   # 50 % of avg wage 48,967
    HEALTH_MIN_PAYMENT_MONTHLY = 3306.0  # 13.5 % of the min base

    SOCIAL_RATE = 0.292          # důchodové (28%) + státní pol. zaměstnanosti (1.2%)
    SOCIAL_BASE_SHARE = 0.55     # assessment base = 55 % of profit (2024+)
    SOCIAL_MIN_PAYMENT_MONTHLY = 5720.0  # 2026 minimum monthly social advance

    SICKNESS_RATE = 0.027        # nemocenské (voluntary) ~2.7 % of base
    TAX_RATE_1 = 0.15
    TAX_RATE_2 = 0.23
    TAX_THRESHOLD_YEARLY = 1762812.0     # 36× avg wage
    TAXPAYER_CREDIT_YEARLY = 30840.0     # sleva na poplatníka
    FLAT_EXPENSE_RATE = 0.60             # paušální výdaje 60 %
    FLAT_EXPENSE_REVENUE_CAP = 2000000.0 # 60 % applies up to 2M revenue

    annual_revenue = float(annual_revenue)
    months_active = max(1, min(int(months_active or 12), 12))

    if use_flat_expenses:
        expenses = FLAT_EXPENSE_RATE * min(annual_revenue, FLAT_EXPENSE_REVENUE_CAP)
        expenses_note = 'Paušální výdaje (60 %)'
    else:
        expenses = float(annual_expenses or 0)
        expenses_note = 'Skutečné výdaje'

    profit = max(0.0, annual_revenue - expenses)  # daňový základ

    # Income tax: 15 % / 23 %, then minus taxpayer credit.
    tax_gross = (TAX_RATE_1 * min(profit, TAX_THRESHOLD_YEARLY)
                 + TAX_RATE_2 * max(0.0, profit - TAX_THRESHOLD_YEARLY))
    income_tax = max(0.0, tax_gross - TAXPAYER_CREDIT_YEARLY)
    tax_rate_applied = TAX_RATE_2 if profit > TAX_THRESHOLD_YEARLY else TAX_RATE_1

    # Health insurance — base 50 % of profit, min applies.
    health_base_monthly = max(profit * HEALTH_BASE_SHARE / 12.0, HEALTH_MIN_BASE_MONTHLY)
    health_monthly = max(health_base_monthly * HEALTH_RATE, HEALTH_MIN_PAYMENT_MONTHLY)
    health_annual = health_monthly * months_active

    # Social insurance — base 55 % of profit, min applies.
    social_base_monthly = profit * SOCIAL_BASE_SHARE / 12.0
    pension_monthly = max(social_base_monthly * SOCIAL_RATE, SOCIAL_MIN_PAYMENT_MONTHLY)
    sickness_monthly = (social_base_monthly * SICKNESS_RATE) if include_sickness else 0.0
    social_monthly = pension_monthly + sickness_monthly
    social_annual = social_monthly * months_active

    total_contributions = health_annual + social_annual
    total = income_tax + total_contributions
    net_income = annual_revenue - expenses - total
    eff = (total / annual_revenue * 100) if annual_revenue > 0 else 0

    def item(monthly, rate, included=True):
        return {'monthly': _r(monthly), 'annual': _r(monthly * months_active),
                'rate': rate, 'included': included}

    return {
        'country': 'CZ',
        'currency': 'CZK',
        'income': {
            'annual_revenue': _r(annual_revenue),
            'annual_expenses': _r(expenses),
            'expenses_note': expenses_note,
            'tax_base': _r(profit),
            'non_taxable_amount': 0.0,
            'taxable_income': _r(profit),
        },
        'tax': {
            'income_tax': _r(income_tax),
            'tax_rate_applied': float(tax_rate_applied * 100),
            'monthly_average': _r(income_tax / 12.0),
        },
        'health_insurance': {
            'monthly_base': _r(health_base_monthly),
            'monthly_payment': _r(health_monthly),
            'annual_payment': _r(health_annual),
            'rate': float(HEALTH_RATE * 100),
            'min_base': _r(HEALTH_MIN_BASE_MONTHLY),
        },
        'social_insurance': {
            'monthly_base': _r(social_base_monthly),
            'monthly_payment': _r(social_monthly),
            'annual_payment': _r(social_annual),
            'breakdown': {
                # CZ has one combined social contribution; map it to "pension".
                'pension': item(pension_monthly, float(SOCIAL_RATE * 100)),
                'sickness': item(sickness_monthly, float(SICKNESS_RATE * 100), include_sickness),
                # SK-only sub-items (hidden in the CZ UI) — kept for shape parity.
                'disability': item(0, 0, False),
                'accident': item(0, 0, False),
                'guarantee': item(0, 0, False),
                'reserve': item(0, 0, False),
            },
        },
        'summary': {
            'total_contributions': _r(total_contributions),
            'total_tax_and_contributions': _r(total),
            'net_income': _r(net_income),
            'effective_rate': _r(eff),
            'monthly_revenue': _r(annual_revenue / 12.0),
            'monthly_deductions': _r(total / 12.0),
            'monthly_net': _r(net_income / 12.0),
            'months_active': months_active,
        },
    }
