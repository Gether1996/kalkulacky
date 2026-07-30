"""
Polish (PL) freelancer / benefit / pension / vacation / sick-leave / solar
calculators for 2026.

Each function mirrors the SIGNATURE and the returned result-dict SHAPE of its
Czech counterpart (``services/freelancer_international.py``,
``services/international_benefits.py``, ``services/solar_international.py``) so
the existing frontend renders PL numbers in PLN using the same templates. Only
``'country'``/``'currency'`` and the figures differ; CZ/SK-only structural
sub-items that have no PL equivalent are kept as ``0``/``False`` for shape parity.

Float-based maths (like the CZ engines), values loaded from
``data/pl_2026.json`` via ``get_rates('PL')``. Round with the local ``_r`` helper.

⚠️ INDICATIVE 2026 figures — approximations where the real rules are complex
(e.g. the NDC pension is reduced to an accumulated-capital / life-expectancy
estimate, and PL general-rules PIT has no statutory flat expense so a 20 %
placeholder is used for the "flat expenses" toggle). Verify against the official
source before relying.

Sources (2026-07):
  - Skladki ZUS 2026 (duzy ZUS base 60 % of PLN 9,420 forecast avg wage =
    PLN 5,652.60): ifirma.pl, poradnikprzedsiebiorcy.pl, symfonia.pl.
  - Skladka zdrowotna 2026 skala 9 %, min PLN 432.54 (9 % of PLN 4,806 min wage):
    infakt.pl, gofin.pl, pit.pl.
  - PIT skala 2026: 12 % to PLN 120,000 / 32 % above, kwota zmniejszajaca
    PLN 3,600 (kwota wolna PLN 30,000): pit.pl, e-pity.pl.
  - Najnizsza emerytura from 2026-03: PLN 1,978.49 brutto; retirement age 65 M /
    60 F; ZUS avg further life at 65 = 220.8 months: zus.pl, infor.pl.
  - Urlop wypoczynkowy 20 dni (<10 lat stazu) / 26 dni (>=10 lat), art. 154 KP:
    infor.pl, gazetaprawna.pl.
  - Wynagrodzenie chorobowe 80 %, pracodawca dni 1-33, potem zasilek ZUS 80 %:
    poradnikprzedsiebiorcy.pl.
  - Urlop macierzynski 20 tyg. (100 %) + rodzicielski 41 tyg. (70 %) lub
    usredniony wariant 81,5 %: gazetaprawna.pl, egospodarka.pl.
  - Moj Prad 6.0 2026: PV 2-20 kW do 50 %/PLN 7,000, magazyn energii do
    PLN 16,000: rmf24.pl, energetyka.pl, NFOSiGW.
"""
from datetime import datetime, timedelta, date
from typing import Dict, Any

from .data import get_rates

_PL = get_rates('PL')
_META = _PL.get('meta', {})
_YEAR = _META.get('year')
_SOURCE = (_META.get('sources') or [None])[0]

_FREE = _PL['freelancer']
_SICK = _PL['sick_leave']
_VAC = _PL['vacation']
_PEN = _PL['pension']
_PAR = _PL['parental']


def _r(x, d=2):
    return round(float(x) + 1e-9, d)


def _parse_date(v):
    if v is None:
        return datetime.now().date()
    if isinstance(v, date) and not isinstance(v, datetime):
        return v
    if isinstance(v, datetime):
        return v.date()
    return datetime.strptime(str(v), '%Y-%m-%d').date()


# ---------------------------------------------------------------------------
# Freelancer / self-employed (skala podatkowa 2026)
# ---------------------------------------------------------------------------
def calculate_pl_freelancer(
    annual_revenue: float,
    annual_expenses: float = 0,
    use_flat_expenses: bool = True,
    include_sickness: bool = True,
    months_active: int = 12,
    **kwargs,
) -> Dict[str, Any]:
    """Polish JDG on skala podatkowa (PIT 12 %/32 %) + ZUS + skladka zdrowotna.

    ZUS social contributions use the fixed "duzy ZUS" assessment base (60 % of
    the forecast average wage = PLN 5,652.60/month) — independent of profit,
    unlike the CZ profit-share model. Skladka zdrowotna on skala is 9 % of income
    (min PLN 432.54). ZUS spoleczne are deductible from the PIT base; the health
    contribution is not (post-2022). ``use_flat_expenses`` applies an INDICATIVE
    20 % cost proxy (skala has no statutory flat expense — actual costs apply).
    """
    c = _FREE
    HEALTH_RATE = c['health_rate']
    HEALTH_MIN_BASE_MONTHLY = c['health_min_base_monthly']
    HEALTH_MIN_PAYMENT_MONTHLY = c['health_min_payment_monthly']

    SOCIAL_BASE_MONTHLY = c['social_base_monthly']
    PENSION_RATE = c['pension_rate']       # emerytalne
    DISABILITY_RATE = c['disability_rate']  # rentowe
    SICKNESS_RATE = c['sickness_rate']     # chorobowe (voluntary)
    ACCIDENT_RATE = c['accident_rate']     # wypadkowe
    RESERVE_RATE = c['reserve_rate']       # Fundusz Pracy

    TAX_RATE_1 = c['tax_rate_1']
    TAX_RATE_2 = c['tax_rate_2']
    TAX_THRESHOLD_YEARLY = c['tax_threshold_yearly']
    TAX_REDUCING_YEARLY = c['tax_reducing_yearly']  # kwota zmniejszajaca podatek
    FLAT_EXPENSE_RATE = c['flat_expense_rate']
    FLAT_EXPENSE_REVENUE_CAP = c['flat_expense_revenue_cap']

    annual_revenue = float(annual_revenue)
    months_active = max(1, min(int(months_active or 12), 12))

    if use_flat_expenses:
        expenses = FLAT_EXPENSE_RATE * min(annual_revenue, FLAT_EXPENSE_REVENUE_CAP)
        expenses_note = 'Ryczaltowe koszty (orientacyjnie 20 %)'
    else:
        expenses = float(annual_expenses or 0)
        expenses_note = 'Rzeczywiste koszty'

    profit = max(0.0, annual_revenue - expenses)  # dochod (przed odliczeniem ZUS)

    # ZUS spoleczne — fixed base, one rate per component.
    pension_monthly = SOCIAL_BASE_MONTHLY * PENSION_RATE
    disability_monthly = SOCIAL_BASE_MONTHLY * DISABILITY_RATE
    sickness_monthly = (SOCIAL_BASE_MONTHLY * SICKNESS_RATE) if include_sickness else 0.0
    accident_monthly = SOCIAL_BASE_MONTHLY * ACCIDENT_RATE
    reserve_monthly = SOCIAL_BASE_MONTHLY * RESERVE_RATE  # Fundusz Pracy
    social_monthly = (pension_monthly + disability_monthly + sickness_monthly
                      + accident_monthly + reserve_monthly)
    social_annual = social_monthly * months_active

    # PIT — ZUS spoleczne deductible from income; then 12 %/32 %, minus credit.
    taxable_income = max(0.0, profit - social_annual)
    tax_gross = (TAX_RATE_1 * min(taxable_income, TAX_THRESHOLD_YEARLY)
                 + TAX_RATE_2 * max(0.0, taxable_income - TAX_THRESHOLD_YEARLY))
    income_tax = max(0.0, tax_gross - TAX_REDUCING_YEARLY)
    tax_rate_applied = TAX_RATE_2 if taxable_income > TAX_THRESHOLD_YEARLY else TAX_RATE_1

    # Skladka zdrowotna — 9 % of income (after ZUS spoleczne), min applies.
    monthly_dochod = max((profit - social_annual) / 12.0, 0.0)
    health_base_monthly = max(monthly_dochod, HEALTH_MIN_BASE_MONTHLY)
    health_monthly = max(monthly_dochod * HEALTH_RATE, HEALTH_MIN_PAYMENT_MONTHLY)
    health_annual = health_monthly * months_active

    total_contributions = health_annual + social_annual
    total = income_tax + total_contributions
    net_income = annual_revenue - expenses - total
    eff = (total / annual_revenue * 100) if annual_revenue > 0 else 0

    def item(monthly, rate, included=True):
        return {'monthly': _r(monthly), 'annual': _r(monthly * months_active),
                'rate': rate, 'included': included}

    return {
        'country': 'PL',
        'currency': 'PLN',
        'year': _YEAR,
        'source': _SOURCE,
        'income': {
            'annual_revenue': _r(annual_revenue),
            'annual_expenses': _r(expenses),
            'expenses_note': expenses_note,
            'tax_base': _r(profit),
            # ZUS spoleczne deducted from the PIT base (odliczenie).
            'non_taxable_amount': _r(social_annual),
            'taxable_income': _r(taxable_income),
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
            'monthly_base': _r(SOCIAL_BASE_MONTHLY),
            'monthly_payment': _r(social_monthly),
            'annual_payment': _r(social_annual),
            'breakdown': {
                'pension': item(pension_monthly, float(PENSION_RATE * 100)),
                'sickness': item(sickness_monthly, float(SICKNESS_RATE * 100), include_sickness),
                'disability': item(disability_monthly, float(DISABILITY_RATE * 100)),
                'accident': item(accident_monthly, float(ACCIDENT_RATE * 100)),
                # PL has no employer guarantee fund for the self-employed.
                'guarantee': item(0, 0, False),
                # Fundusz Pracy (Labour Fund) — mapped to the "reserve" slot.
                'reserve': item(reserve_monthly, float(RESERVE_RATE * 100)),
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


# ---------------------------------------------------------------------------
# Sick leave (wynagrodzenie chorobowe + zasilek chorobowy 2026)
# ---------------------------------------------------------------------------
def calculate_pl_sick_leave(gross_salary, days_sick, leave_type='illness', **kwargs):
    """Polish L4 2026. The employer pays wynagrodzenie chorobowe for calendar
    days 1-33 in a year (80 %); ZUS pays zasilek chorobowy from day 34 (80 %).
    The benefit base is the gross salary reduced by 13.71 % (employee ZUS
    spoleczne). Unlike CZ, PL pays every calendar day (weekends included) and
    there is no daily reduction-bracket schedule. Assumes the insured is under
    50 (employer window 33 days; it would be 14 days from age 50)."""
    gross_salary = float(gross_salary)
    days_sick = int(days_sick)
    yearly = gross_salary * 12

    reduce_share = _SICK['reduce_share']
    rate = _SICK['rate_care'] if leave_type == 'care' else _SICK['rate_illness']
    emp_cal = _SICK['employer_calendar_days']
    max_base_monthly = _SICK['max_base_monthly']

    # Daily benefit base: monthly gross - 13.71 %, divided by 30.
    monthly_base = gross_salary * (1 - reduce_share)
    max_daily_base = max_base_monthly * (1 - reduce_share) / 30.0
    dvz = gross_salary / 30.0                 # gross daily (pre-reduction)
    reduced = monthly_base / 30.0             # daily benefit base
    is_capped = reduced > max_daily_base
    if is_capped:
        reduced = max_daily_base

    if leave_type == 'care':
        # Zasilek opiekunczy: 80 % from day 1, paid by ZUS (max 60 days/year).
        employer_days, insurance_days = 0, days_sick
        employer_payment = 0.0
        insurance_payment = insurance_days * reduced * rate
    else:
        employer_days = min(days_sick, emp_cal)
        insurance_days = max(0, days_sick - emp_cal)
        employer_payment = employer_days * reduced * rate
        insurance_payment = insurance_days * reduced * rate

    total = employer_payment + insurance_payment
    avg_daily = total / days_sick if days_sick > 0 else 0.0
    full = (gross_salary / 30.0) * days_sick
    loss = full - total
    loss_pct = (loss / full * 100) if full > 0 else 0.0
    rate_pct = _r(rate * 100)

    breakdown = []
    for day in range(1, days_sick + 1):
        if leave_type == 'care':
            payer = 'ZUS'
        elif day <= emp_cal:
            payer = 'Pracodawca'
        else:
            payer = 'ZUS'
        breakdown.append({'day': day, 'payer': payer, 'rate_percent': rate_pct,
                          'daily_amount': _r(reduced * rate)})

    return {
        'country': 'PL', 'currency': 'PLN',
        'year': _YEAR, 'source': _SOURCE,
        'gross_salary': _r(gross_salary), 'days_sick': days_sick,
        'leave_type': leave_type,
        'leave_type_label': 'Choroba' if leave_type == 'illness' else 'Opieka nad czlonkiem rodziny',
        'yearly_salary': _r(yearly),
        'daily_assessment_base': _r(dvz),
        'capped_daily_base': _r(reduced),
        'is_capped': is_capped,
        'max_daily_base': _r(max_daily_base),
        'employer_payment_days': employer_days,
        'insurance_payment_days': insurance_days,
        'employer_rate_percent': rate_pct,
        'insurance_rate_percent': rate_pct,
        'employer_payment': _r(employer_payment),
        'insurance_payment': _r(insurance_payment),
        'total_sick_leave': _r(total),
        'avg_daily_rate': _r(avg_daily),
        'full_salary_for_period': _r(full),
        'loss_vs_full_salary': _r(loss),
        'loss_percentage': _r(loss_pct),
        'explanation': ('Pierwsze 33 dni w roku (14 dni dla osob 50+) oplaca pracodawca '
                        'jako wynagrodzenie chorobowe (80 % podstawy = wynagrodzenie brutto '
                        'pomniejszone o 13,71 % skladek spolecznych). Od 34. dnia zasilek '
                        'chorobowy wyplaca ZUS (80 %). Wyplacane za kazdy dzien kalendarzowy.'),
        'breakdown': breakdown,
    }


# ---------------------------------------------------------------------------
# Vacation (urlop wypoczynkowy 2026)
# ---------------------------------------------------------------------------
def calculate_pl_vacation(age, employment_start_date, current_date=None,
                          vacation_days_used=0, days_carried_over=0,
                          planned_vacation_days=0, **kwargs):
    """Polish urlop wypoczynkowy 2026 (art. 154 KP): 20 days with under 10 years
    of service, 26 days from 10 years. The tenure bonus is approximated from the
    current-employer start date only (real staz pracy also counts prior jobs and
    education — up to 8 years for higher education — so entitlement may be higher).
    The "age_*" fields carry the tenure logic to keep shape parity with CZ."""
    BASE_DAYS = _VAC['base_days']
    HIGHER_DAYS = _VAC['higher_days']
    TENURE_THRESHOLD = int(_VAC['tenure_threshold_years'])
    BONUS_DAYS = _VAC['bonus_days']

    age = int(age)
    start = _parse_date(employment_start_date)
    cur = _parse_date(current_date)
    used = float(vacation_days_used or 0)
    carried = float(days_carried_over or 0)
    planned = float(planned_vacation_days or 0)
    if start > cur:
        raise ValueError('Data rozpoczecia pracy nie moze byc w przyszlosci.')

    tenure_years = (cur - start).days / 365.25
    has_bonus = tenure_years >= TENURE_THRESHOLD
    annual = HIGHER_DAYS if has_bonus else BASE_DAYS

    is_first_year = start.year == cur.year
    if is_first_year:
        months = (cur.year - start.year) * 12 + cur.month - start.month + 1
        accrued = round(annual * months / 12.0, 1)
    else:
        accrued = float(annual)

    total_available = accrued + carried
    remaining = total_available - used
    after_planned = remaining - planned
    accrual_pm = annual / 12.0
    months_to_eoy = 12 - cur.month
    projected = accrued + accrual_pm * months_to_eoy

    return {
        'country': 'PL', 'currency': 'PLN',
        'year': _YEAR, 'source': _SOURCE,
        'age': age,
        'employment_start_date': start.strftime('%Y-%m-%d'),
        'is_first_year': is_first_year,
        'entitlement': {
            'annual_entitlement': annual, 'base_days': BASE_DAYS,
            'age_bonus': BONUS_DAYS if has_bonus else 0,
            'has_age_bonus': has_bonus, 'age_threshold': TENURE_THRESHOLD,
        },
        'current_year': {
            'days_accrued': _r(accrued, 1), 'days_carried_over': _r(carried, 1),
            'total_available': _r(total_available, 1), 'days_used': _r(used, 1),
            'remaining_days': _r(remaining, 1),
            'weeks_available': _r(remaining / 5.0, 1), 'weeks_used': _r(used / 5.0, 1),
        },
        'planning': {
            'planned_vacation_days': _r(planned, 1),
            'days_after_planned': _r(after_planned, 1),
            'can_take_planned': remaining >= planned,
        },
        'accrual': {
            'accrual_per_month': _r(accrual_pm, 2),
            'months_until_year_end': months_to_eoy,
            'projected_accrual_by_year_end': _r(projected, 1),
        },
        'status': {
            'is_over_limit': used > total_available,
            'usage_percentage': _r((used / total_available * 100) if total_available > 0 else 0, 1),
        },
    }


# ---------------------------------------------------------------------------
# Pension (emerytura ZUS 2026)
# ---------------------------------------------------------------------------
def calculate_pl_pension(current_age, gross_salary, years_worked, gender='male',
                         include_second_pillar=False, second_pillar_rate=0, **kwargs):
    """Polish starobna emerytura 2026 (NDC — zdefiniowana skladka).

    Approximated: accumulated pension capital = monthly emerytalne contribution
    (19.52 % of gross) x total contributory months, divided by the ZUS average
    further life expectancy at retirement (220.8 months). Real ZUS uses valorised
    capital + sub-account + initial capital, so this is INDICATIVE. Retirement
    age is 65 (men) / 60 (women); guaranteed minimum from 2026-03 is PLN 1,978.49
    (requires 25 years for men / 20 for women). PL has no mandatory second pillar
    (OFE wound down; PPK is voluntary) — kept off, mirroring the CZ engine."""
    PENSION_RATE = _PEN['pension_rate']
    EMP_RATE, EMPLOYER_RATE = _PEN['employee_rate'], _PEN['employer_rate']
    MIN_PENSION = _PEN['min_pension']
    DIVISOR_MONTHS = _PEN['divisor_months']
    life_after = _PEN['life_expectancy_after_retirement']

    gender = 'female' if str(gender).lower().startswith('f') else 'male'
    RETIREMENT_AGE = _PEN['retirement_age_female'] if gender == 'female' else _PEN['retirement_age_male']
    MIN_YEARS = _PEN['min_years_female'] if gender == 'female' else _PEN['min_years_male']

    current_age = int(current_age)
    gross = float(gross_salary)
    years_worked = int(years_worked)
    if gross <= 0:
        raise ValueError('Wynagrodzenie brutto musi byc wieksze niz 0.')

    years_to_ret = max(0, RETIREMENT_AGE - current_age)
    already_retired = current_age >= RETIREMENT_AGE
    total_years = years_worked + years_to_ret

    # NDC estimate: capital = pension contributions accumulated, / life expectancy.
    monthly_pension_contribution = gross * PENSION_RATE
    capital = monthly_pension_contribution * total_years * 12
    pension = capital / DIVISOR_MONTHS if DIVISOR_MONTHS > 0 else 0.0
    if pension < MIN_PENSION and total_years >= MIN_YEARS:
        pension = MIN_PENSION

    employee_m = gross * EMP_RATE / 100
    employer_m = gross * EMPLOYER_RATE / 100
    total_m = employee_m + employer_m
    contributed = total_m * years_worked * 12
    future = total_m * years_to_ret * 12
    lifetime = contributed + future
    replacement = (pension / gross * 100) if gross > 0 else 0
    total_lifetime_pension = pension * 12 * life_after
    roi = ((total_lifetime_pension - lifetime) / lifetime * 100) if lifetime > 0 else 0

    return {
        'country': 'PL', 'currency': 'PLN',
        'year': _YEAR, 'source': _SOURCE,
        'current_age': current_age, 'retirement_age': RETIREMENT_AGE,
        'years_to_retirement': years_to_ret, 'already_retired': already_retired,
        'years_worked': years_worked, 'total_years_at_retirement': total_years,
        'gross_salary': _r(gross),
        'estimated_monthly_pension': _r(pension),
        'replacement_rate': _r(replacement, 1),
        'contributions': {
            'employee_monthly': _r(employee_m), 'employer_monthly': _r(employer_m),
            'total_monthly': _r(total_m),
            'first_pillar_monthly': _r(total_m), 'second_pillar_monthly': 0.0,
            'total_contributed_so_far': _r(contributed),
            'total_future_contributions': _r(future),
            'total_lifetime_contributions': _r(lifetime),
        },
        'pension_system': {
            'include_second_pillar': False,
            'first_pillar_rate': _r(EMP_RATE + EMPLOYER_RATE, 1),
            'second_pillar_rate': 0.0,
            'minimum_pension': _r(MIN_PENSION),
        },
        'projections': {
            'life_expectancy_after_retirement': life_after,
            'total_pension_lifetime': _r(total_lifetime_pension),
            'roi_percentage': _r(roi, 1),
        },
    }


# ---------------------------------------------------------------------------
# Parental (urlop macierzynski + rodzicielski 2026)
# ---------------------------------------------------------------------------
def calculate_pl_parental(birth_date, gross_salary=None, twins_or_more=False,
                          current_date=None, **kwargs):
    """Polish urlop macierzynski + rodzicielski 2026.
    Macierzynski: 20 weeks (31 for multiples) at 100 % of the benefit base.
    Rodzicielski: 41 weeks (43 for multiples) at 70 %. The averaged 81.5 % option
    (single application within 21 days) is noted for reference. The benefit base
    is gross salary reduced by 13.71 % (employee ZUS spoleczne)."""
    mat_weeks = _PAR['mat_weeks_multiple'] if twins_or_more else _PAR['mat_weeks_single']
    parental_weeks = _PAR['parental_weeks_multiple'] if twins_or_more else _PAR['parental_weeks_single']
    MAT_RATE = _PAR['mat_rate']
    PARENTAL_RATE = _PAR['parental_rate']
    reduce_share = _PAR['reduce_share']

    bd = _parse_date(birth_date)
    cur = _parse_date(current_date) if current_date else datetime.now().date()
    if bd > cur:
        raise ValueError('Data urodzenia nie moze byc w przyszlosci.')

    age_days = (cur - bd).days
    maternity_end = bd + timedelta(weeks=mat_weeks)

    maternity_benefit = None
    daily = 0.0
    if gross_salary and float(gross_salary) > 0:
        base_monthly = float(gross_salary) * (1 - reduce_share)
        dvz = base_monthly / 30.0
        daily = dvz * MAT_RATE
        maternity_benefit = {
            'daily_amount': _r(daily), 'weekly_amount': _r(daily * 7),
            'monthly_amount': _r(daily * 30), 'total_amount': _r(daily * mat_weeks * 7),
            'duration_weeks': mat_weeks, 'end_date': maternity_end.strftime('%Y-%m-%d'),
            'daily_assessment_base': _r(dvz),
        }

    # Rodzicielski — 70 % of base, drawn after maternity leave.
    parental_start = maternity_end
    benefit_end = parental_start + timedelta(weeks=parental_weeks)
    total_months = max(1, round(parental_weeks * 7 / 30.0))
    parental_daily = (float(gross_salary) * (1 - reduce_share) / 30.0 * PARENTAL_RATE) \
        if (gross_salary and float(gross_salary) > 0) else 0.0
    default_monthly = parental_daily * 30
    total_benefit = parental_daily * parental_weeks * 7

    if cur < parental_start:
        remaining_months, status = total_months, 'Trwa urlop macierzynski'
    elif cur >= benefit_end:
        remaining_months, status = 0, 'Urlop rodzicielski zakonczony'
    else:
        elapsed = (cur - parental_start).days // 30
        remaining_months, status = max(0, total_months - elapsed), 'Pobierasz zasilek rodzicielski'

    return {
        'country': 'PL', 'currency': 'PLN',
        'year': _YEAR, 'source': _SOURCE,
        'birth_date': bd.strftime('%Y-%m-%d'),
        'child_age_days': age_days, 'child_age_months': age_days // 30,
        'child_age_years': age_days // 365,
        'maternity_benefit': maternity_benefit,
        'maternity_end_date': maternity_end.strftime('%Y-%m-%d'),
        'benefit_type': 'pl_leave',
        'benefit_type_label': 'Zasilek rodzicielski (70 % podstawy)',
        'monthly_benefit': _r(default_monthly),
        'parental_start_date': parental_start.strftime('%Y-%m-%d'),
        'parental_end_date': benefit_end.strftime('%Y-%m-%d'),
        'total_months': total_months,
        'remaining_months': max(0, remaining_months),
        'total_benefit': _r(total_benefit),
        'benefit_status': status,
        # PL allows part-time work during rodzicielski; no fixed income cap here.
        'can_work_and_receive': True,
        'work_income_limit': 0.0,
        'work_warning': None,
        'second_child_extension': None,
        # CZ leaves this None (SK-only osnova/alternatíva comparison); mirror it.
        # The averaged 81.5 % variant is documented in the docstring.
        'comparison': None,
        'notifications': [],
        'progress_percentage': round(((total_months - remaining_months) / total_months * 100)
                                     if total_months > 0 else 0, 1),
    }


# ---------------------------------------------------------------------------
# Solar (fotowoltaika + Moj Prad 6.0 2026)
# ---------------------------------------------------------------------------
def calculate_pl_solar(annual_consumption_kwh, electricity_rate=None,
                       system_size_kwp=None, include_battery=False,
                       battery_capacity_kwh=0, **kwargs) -> Dict[str, Any]:
    """Polish PV subsidy & payback estimator — Moj Prad 6.0 (2026, INDICATIVE).
    PV 2-20 kW: up to 50 % of cost, max PLN 7,000; energy storage bonus up to
    PLN 16,000 — capped at 50 % of total cost. Feed-in valued at net-billing RCEm.
    Verify amounts on mojprad.gov.pl / NFOSiGW."""
    _S = _PL['solar']
    YIELD_KWH_PER_KWP = _S['yield_kwh_per_kwp']
    PRICE_PER_KWP = _S['price_per_kwp']
    BATTERY_PRICE_PER_KWH = _S['battery_price_per_kwh']
    DEFAULT_SELF_CONSUMPTION = _S['default_self_consumption']
    BATTERY_SELF_CONSUMPTION = _S['battery_self_consumption']
    DEFAULT_ELECTRICITY_RATE = _S['default_electricity_rate']
    FEED_IN_PRICE = _S['feed_in_price']
    CO2_KG_PER_KWH = _S['co2_kg_per_kwh']
    NZU_BASE = _S['nzu_base']
    NZU_PER_KWP = _S['nzu_per_kwp']
    NZU_KWP_CAP = _S['nzu_kwp_cap']
    NZU_BATTERY_BONUS = _S['nzu_battery_bonus']
    SUBSIDY_RATE_OF_COST = _S['subsidy_rate_of_cost']
    KWP_MIN = _S['kwp_min']
    KWP_MAX = _S['kwp_max']
    BATTERY_RATIO = _S['battery_ratio']
    BATTERY_MAX = _S['battery_max']

    def _rs(x, d=0):
        return round(float(x) + 1e-9, d)

    annual_consumption = float(annual_consumption_kwh)
    if annual_consumption <= 0:
        raise ValueError('Podaj roczne zuzycie energii elektrycznej (kWh).')
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
    limited_by = '50 % kosztow' if total_subsidy >= subsidy_by_cost else 'limit programu'
    net_cost = max(total_cost - total_subsidy, 0)

    scr = BATTERY_SELF_CONSUMPTION if include_battery else DEFAULT_SELF_CONSUMPTION
    self_consumed = min(annual_production * scr, annual_consumption)
    exported = max(annual_production - self_consumed, 0)
    annual_savings = self_consumed * rate + exported * FEED_IN_PRICE
    payback = (net_cost / annual_savings) if annual_savings > 0 else None
    coverage = (self_consumed / annual_consumption * 100) if annual_consumption else 0

    return {
        'country': 'PL', 'currency': 'PLN',
        'year': _YEAR, 'source': _SOURCE,
        'inputs': {
            'annual_consumption_kwh': _rs(annual_consumption),
            'electricity_rate': round(rate, 4),
            'include_battery': include_battery,
        },
        'system': {
            'recommended_kwp': round(kwp, 1),
            'battery_capacity_kwh': round(battery_kwh, 1),
            'annual_production_kwh': _rs(annual_production),
            'self_consumption_ratio': round(scr, 2),
        },
        'cost': {
            'pv_cost': _rs(pv_cost), 'battery_cost': _rs(battery_cost), 'total_cost': _rs(total_cost),
        },
        'subsidy': {
            'eligible_kwp': round(min(kwp, NZU_KWP_CAP), 1),
            'rate_per_kwp': NZU_PER_KWP,
            'max_subsidy': _rs(NZU_BASE + NZU_PER_KWP * NZU_KWP_CAP + NZU_BATTERY_BONUS),
            'total_subsidy': _rs(total_subsidy),
            'limited_by': limited_by,
            'net_cost': _rs(net_cost),
            'scheme': 'Moj Prad 6.0 (orientacyjnie)',
        },
        'savings': {
            'self_consumed_kwh': _rs(self_consumed), 'exported_kwh': _rs(exported),
            'annual_savings': _rs(annual_savings), 'monthly_savings': _rs(annual_savings / 12),
            'coverage_pct': round(coverage, 1),
        },
        'analysis': {
            'payback_years': round(payback, 1) if payback else None,
            'savings_30y': _rs(annual_savings * 30 - net_cost),
            'co2_savings_kg': _rs(annual_production * CO2_KG_PER_KWH),
        },
    }
