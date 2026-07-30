"""
International net-salary calculators (Czechia, Poland, Hungary) for 2026.

These complement the Slovak `SalaryCalculator`. Each country has a structurally
DIFFERENT payroll-tax system (not just different numbers), so each is its own
function. All return a result shape compatible with the Slovak one (same keys)
plus `currency` / `country`, so the frontend can render them uniformly.

⚠️ Figures are 2026 parameters gathered from public payroll/tax guides and are
INDICATIVE — verify against the official authority before relying on them. Each
country's constants are centralised at the top of its function for yearly updates.
Sources captured 2026-06 (PwC Worldwide Tax Summaries, OECD Taxing Wages 2026,
getsix.eu ZUS 2026, helpers.hu, taxsummaries / countrytaxcalc).
"""

from typing import Dict, Any

from .data import get_rates


def _round(x: float) -> float:
    return round(float(x) + 1e-9, 2)


def _result(*, country, currency, gross, social, health, income_tax,
            child_bonus, net, employer_cost=0.0, extra=None) -> Dict[str, Any]:
    total_deductions = social + health + income_tax
    eff = (total_deductions / gross * 100) if gross > 0 else 0
    out = {
        'country': country,
        'currency': currency,
        'gross_salary': _round(gross),
        'social_insurance': _round(social),
        'health_insurance': _round(health),
        'income_tax': _round(income_tax),
        'child_tax_bonus': _round(child_bonus),
        'final_tax': _round(income_tax),
        'net_salary': _round(net),
        'total_insurance': _round(social + health),
        'total_deductions': _round(total_deductions),
        'effective_tax_rate': _round(eff),
        'super_gross_salary': _round(gross + employer_cost),
        'total_employer_contributions': _round(employer_cost),
        # SK-only concepts — kept for response compatibility, not applicable here.
        'non_taxable_amount': 0.0,
        'tax_base': _round(gross - social - health),
        'taxable_base': _round(gross - social - health),
        'breakdown': {
            'gross_salary': _round(gross),
            'minus_social_insurance': _round(social),
            'minus_health_insurance': _round(health),
            'final_tax': _round(income_tax),
            'net_salary': _round(net),
        },
        'yearly': {
            'gross': _round(gross * 12),
            'net': _round(net * 12),
            'total_deductions': _round(total_deductions * 12),
        },
    }
    if extra:
        out.update(extra)
    return out


def calculate_cz(gross_salary: float, children_under_15: int = 0,
                 children_15_to_18: int = 0, **kwargs) -> Dict[str, Any]:
    """Czech Republic 2026 (monthly, CZK). Super-gross abolished; tax base = gross."""
    # 2026 constants loaded from the editable data file (data/cz_2026.json → salary).
    c = get_rates('CZ')['salary']
    SOCIAL_RATE = c['social_rate']            # employee: 6.5% pension + 0.6% sickness
    HEALTH_RATE = c['health_rate']            # employee health insurance
    TAX_RATE_1 = c['tax_rate_1']
    TAX_RATE_2 = c['tax_rate_2']
    TAX_THRESHOLD_MONTHLY = c['tax_threshold_monthly']   # 36× avg wage / 12
    TAXPAYER_CREDIT_MONTHLY = c['taxpayer_credit_monthly']  # sleva na poplatníka / 12
    CHILD_CREDIT = c['child_credit']          # monthly per 1st/2nd/3rd+ child
    EMPLOYER_RATE = c['employer_rate']        # 24.8% social + 9% health (employer)

    gross = float(gross_salary)
    social = gross * SOCIAL_RATE
    health = gross * HEALTH_RATE

    taxable = gross  # tax base is the gross salary
    tax_gross = (TAX_RATE_1 * min(taxable, TAX_THRESHOLD_MONTHLY)
                 + TAX_RATE_2 * max(0.0, taxable - TAX_THRESHOLD_MONTHLY))
    tax_after_credit = max(0.0, tax_gross - TAXPAYER_CREDIT_MONTHLY)

    # Child tax advantage reduces tax (can go negative as a bonus in CZ, but we
    # floor at 0 here for a conservative net estimate).
    n = int(children_under_15 or 0) + int(children_15_to_18 or 0)
    child_credit = sum(CHILD_CREDIT[min(i, len(CHILD_CREDIT) - 1)] for i in range(n))
    child_bonus = min(tax_after_credit, child_credit)
    income_tax = max(0.0, tax_after_credit - child_bonus)

    net = gross - social - health - income_tax
    return _result(country='CZ', currency='CZK', gross=gross, social=social,
                   health=health, income_tax=income_tax, child_bonus=child_bonus,
                   net=net, employer_cost=gross * EMPLOYER_RATE)


def calculate_pl(gross_salary: float, children_under_15: int = 0,
                 children_15_to_18: int = 0, **kwargs) -> Dict[str, Any]:
    """Poland 2026 (monthly, PLN). ZUS social, then 9% health on (gross−social)."""
    # 2026 constants loaded from the editable data file (data/pl_2026.json → salary).
    c = get_rates('PL')['salary']
    SOCIAL_RATE = c['social_rate']       # 9.76% pension + 1.5% disability + 2.45% sickness
    HEALTH_RATE = c['health_rate']       # on (gross − social); NOT tax-deductible
    TAX_RATE_1 = c['tax_rate_1']
    TAX_RATE_2 = c['tax_rate_2']
    TAX_THRESHOLD_MONTHLY = c['tax_threshold_monthly']   # 120,000 / yr
    MONTHLY_TAX_REDUCING = c['monthly_tax_reducing']     # kwota wolna
    EMPLOYEE_COSTS = c['employee_costs']                 # standard KUP / month
    EMPLOYER_RATE = c['employer_rate']                   # ~ employer ZUS

    gross = float(gross_salary)
    social = gross * SOCIAL_RATE
    health = (gross - social) * HEALTH_RATE

    tax_base = round(gross - social - EMPLOYEE_COSTS)
    tax_base = max(0.0, tax_base)
    tax_gross = (TAX_RATE_1 * min(tax_base, TAX_THRESHOLD_MONTHLY)
                 + TAX_RATE_2 * max(0.0, tax_base - TAX_THRESHOLD_MONTHLY))
    income_tax = max(0.0, round(tax_gross - MONTHLY_TAX_REDUCING))

    net = gross - social - health - income_tax
    return _result(country='PL', currency='PLN', gross=gross, social=social,
                   health=health, income_tax=income_tax, child_bonus=0.0,
                   net=net, employer_cost=gross * EMPLOYER_RATE)


def calculate_hu(gross_salary: float, children_under_15: int = 0,
                 children_15_to_18: int = 0, **kwargs) -> Dict[str, Any]:
    """Hungary 2026 (monthly, HUF). Flat 15% PIT + 18.5% employee social."""
    # 2026 constants loaded from the editable data file (data/hu_2026.json → salary).
    c = get_rates('HU')['salary']
    SOCIAL_RATE = c['social_rate']       # employee total social security contribution
    PIT_RATE = c['pit_rate']             # flat personal income tax
    # Family allowance = monthly tax-BASE reduction (doubled from Jan 2026),
    # indexed by number of children [0, 1, 2]; 3+ handled separately.
    FAMILY_ALLOWANCE = c['family_allowance']
    FAMILY_ALLOWANCE_3PLUS = c['family_allowance_3plus']
    EMPLOYER_RATE = c['employer_rate']   # szociális hozzájárulási adó

    gross = float(gross_salary)
    social = gross * SOCIAL_RATE

    n = int(children_under_15 or 0) + int(children_15_to_18 or 0)
    allowance = FAMILY_ALLOWANCE_3PLUS if n >= 3 else FAMILY_ALLOWANCE[n]
    pit_base = max(0.0, gross - allowance)
    income_tax = pit_base * PIT_RATE

    net = gross - social - income_tax
    # Surface the family allowance as a "child bonus"-style line for the UI.
    child_bonus = _round((gross * 0 + (gross - pit_base) * PIT_RATE)) if allowance else 0.0
    return _result(country='HU', currency='HUF', gross=gross, social=social,
                   health=0.0, income_tax=income_tax, child_bonus=child_bonus,
                   net=net, employer_cost=gross * EMPLOYER_RATE)


CALCULATORS = {
    'CZ': calculate_cz,
    'PL': calculate_pl,
    'HU': calculate_hu,
}


def calculate_international(country: str, **kwargs) -> Dict[str, Any]:
    fn = CALCULATORS[country.upper()]
    return fn(**kwargs)
