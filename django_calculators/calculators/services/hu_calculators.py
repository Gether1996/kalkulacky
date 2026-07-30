"""
Hungarian (HU) benefit / freelancer / pension / vacation / sick-leave / solar
calculators for 2026.

Each function mirrors the SIGNATURE and the RETURNED-DICT SHAPE of its Czech
counterpart (services/freelancer_international.py, services/international_benefits.py,
services/solar_international.py) so the existing frontend renders HU numbers in HUF
with the same templates. CZ/SK-only structural sub-items are kept (0/False/None) for
shape parity and gated off in the UI.

⚠️ INDICATIVE 2026 figures — approximations where the Hungarian rules are complex.
Verify against NAV, MÁK, TB, Kormányzat before relying. Constants live in the editable
data file (services/data/hu_2026.json); update once a year.

Sources (2026):
- Minimum wage 322 800 Ft / guaranteed 373 200 Ft; átalányadó revenue caps & the
  50 %-of-annual-minimum-wage tax-free band: helpers.hu, helpersfinance.hu, taxravens.com.
- SZJA flat 15 %; TB (employee social contribution) 18.5 % (10 % pension + 7 % health
  + 1.5 % labour-market); szocho (employer social tax) 13 %: PwC Worldwide Tax Summaries.
- Pension: retirement age 65, service-year multiplier table (30 y→68 %, 40 y→80 %,
  45 y→90 %), min old-age pension 28 500 Ft: officina.hu, adozona.hu.
- Vacation: alapszabadság 20 munkanap + életkori pótszabadság 1..10 days (Mt. §117):
  officina.hu, penzcentrum.hu.
- Sick pay: betegszabadság 15 munkanap @70 % (employer), then táppénz 60 % (50 %
  hospital/<2 y insurance) capped at 200 % of the daily minimum wage (~21 520 Ft/day):
  officina.hu, forvismazars.com.
- Parental: CSED 100 % for 24 weeks, GYED 70 % capped 451 920 Ft/month to age 2,
  GYES fixed 28 500 Ft/month to age 3: penzcentrum.hu, forvismazars.com, profession.hu.
- Solar: Otthoni Energiatároló / Napenergia Plusz — battery grant up to 2.5 M Ft
  (min 10 kWh): lakossagiakkumulatorprogram.hu.
"""
from datetime import datetime, timedelta, date
from typing import Dict, Any

from .data import get_rates

_HU = get_rates('HU')
_META = _HU.get('meta', {})
_FRE = _HU['freelancer']
_SICK = _HU['sick_leave']
_VAC = _HU['vacation']
_PEN = _HU['pension']
_PAR = _HU['parental']
_SOL = _HU['solar']


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


def _source():
    return (_META.get('sources') or [None])[0]


# ---------------------------------------------------------------------------
# Freelancer — átalányadó (flat-rate self-employment) 2026
# ---------------------------------------------------------------------------
def calculate_hu_freelancer(
    annual_revenue: float,
    annual_expenses: float = 0,
    use_flat_expenses: bool = True,
    include_sickness: bool = True,
    months_active: int = 12,
    **kwargs,
) -> Dict[str, Any]:
    """Hungarian egyéni vállalkozó — átalányadózás (flat-rate) 2026, INDICATIVE.

    Model (mainstream 15 % SZJA + 18.5 % TB + 13 % szocho):
    - Flat-rate expenses: standard 40 % expense ratio → 60 % of revenue is the tax
      base (`átalányban megállapított jövedelem`). (Alternate 80 %/90 % ratios exist
      for specific activities; not auto-applied here.)
    - SZJA 15 % on the tax base above the tax-free band (½ of the annual minimum
      wage = 1 936 800 Ft), which is exempt from personal income tax.
    - Contributions: TB 18.5 % (mapped to `social_insurance`) and szocho 13 %
      (mapped to `health_insurance` for shape parity) on a monthly base of at least
      the minimum wage (322 800 Ft) — the főfoglalkozású minimum-base rule.

    Mirrors calculate_cz_freelancer's signature and returned keys exactly; the szocho
    bucket is surfaced through the CZ `health_insurance` section.
    """
    PIT_RATE = _FRE['pit_rate']
    TB_RATE = _FRE['tb_rate']
    TB_PENSION_RATE = _FRE['tb_pension_rate']
    TB_HEALTH_LABOUR_RATE = _FRE['tb_health_labour_rate']
    SZOCHO_RATE = _FRE['szocho_rate']
    MIN_WAGE_M = _FRE['min_wage_monthly']
    TAX_FREE_ANNUAL = _FRE['tax_free_annual']
    FLAT_EXPENSE_RATE = _FRE['expense_ratio_standard']

    annual_revenue = float(annual_revenue)
    months_active = max(1, min(int(months_active or 12), 12))

    if use_flat_expenses:
        expenses = FLAT_EXPENSE_RATE * annual_revenue
        expenses_note = f'Átalány költséghányad ({int(FLAT_EXPENSE_RATE * 100)} %)'
    else:
        expenses = float(annual_expenses or 0)
        expenses_note = 'Tényleges költségek'

    profit = max(0.0, annual_revenue - expenses)  # átalányban megállapított jövedelem

    # Income tax: flat 15 % on the base above the tax-free band.
    taxable_income = max(0.0, profit - TAX_FREE_ANNUAL)
    income_tax = PIT_RATE * taxable_income
    tax_rate_applied = PIT_RATE

    # Contribution base: monthly profit, at least the minimum wage.
    contrib_base_monthly = max(profit / 12.0, MIN_WAGE_M)

    # TB (társadalombiztosítási járulék) 18.5 % -> social_insurance bucket.
    social_monthly = contrib_base_monthly * TB_RATE
    social_annual = social_monthly * months_active
    pension_monthly = contrib_base_monthly * TB_PENSION_RATE
    sickness_monthly = contrib_base_monthly * TB_HEALTH_LABOUR_RATE

    # Szocho (szociális hozzájárulási adó) 13 % -> health_insurance bucket.
    health_base_monthly = contrib_base_monthly
    health_monthly = contrib_base_monthly * SZOCHO_RATE
    health_annual = health_monthly * months_active

    total_contributions = health_annual + social_annual
    total = income_tax + total_contributions
    net_income = annual_revenue - expenses - total
    eff = (total / annual_revenue * 100) if annual_revenue > 0 else 0

    def item(monthly, rate, included=True):
        return {'monthly': _r(monthly), 'annual': _r(monthly * months_active),
                'rate': rate, 'included': included}

    return {
        'country': 'HU',
        'currency': 'HUF',
        'year': _META.get('year'),
        'source': _source(),
        'income': {
            'annual_revenue': _r(annual_revenue),
            'annual_expenses': _r(expenses),
            'expenses_note': expenses_note,
            'tax_base': _r(profit),
            'non_taxable_amount': _r(min(profit, TAX_FREE_ANNUAL)),
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
            'rate': float(SZOCHO_RATE * 100),
            'min_base': _r(MIN_WAGE_M),
        },
        'social_insurance': {
            'monthly_base': _r(contrib_base_monthly),
            'monthly_payment': _r(social_monthly),
            'annual_payment': _r(social_annual),
            'breakdown': {
                # HU TB split: 10 % pension + 8.5 % health/labour-market.
                'pension': item(pension_monthly, float(TB_PENSION_RATE * 100)),
                'sickness': item(sickness_monthly, float(TB_HEALTH_LABOUR_RATE * 100), include_sickness),
                # SK-only sub-items (hidden in the HU UI) — kept for shape parity.
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


# ---------------------------------------------------------------------------
# Sick leave — betegszabadság + táppénz 2026
# ---------------------------------------------------------------------------
def calculate_hu_sick_leave(gross_salary, days_sick, leave_type='illness', **kwargs):
    """Hungarian táppénz 2026. Employer pays betegszabadság for the first 15 working
    days at 70 % of the daily wage; from then the state (NEAK) pays táppénz at 60 %
    (50 % if hospitalised / <2 years insurance) of the daily base, capped at 200 % of
    the daily minimum wage (~21 520 Ft/day). Mirrors calculate_cz_sick_leave shape."""
    gross_salary = float(gross_salary)
    days_sick = int(days_sick)
    yearly = gross_salary * 12
    dvz = yearly / 365.0  # napi jövedelem (calendar-day base)

    MIN_WAGE_M = _SICK['min_wage_monthly']
    max_daily_base = (MIN_WAGE_M / 30.0) * _SICK['max_daily_multiplier']
    is_capped = dvz > max_daily_base
    capped = min(dvz, max_daily_base)  # táppénz base after the 200 % cap

    emp_rate = _SICK['employer_rate']         # 70 % betegszabadság
    tappenz_rate = _SICK['tappenz_rate']      # 60 % táppénz
    care_rate = _SICK['care_rate']            # 60 % gyermekápolási táppénz
    emp_cal = _SICK['employer_calendar_days']  # ~21 calendar days ≈ 15 working days
    wf_num = _SICK['working_day_factor_num']
    wf_den = _SICK['working_day_factor_den']
    bsz_max = _SICK['betegszabadsag_working_days']

    if leave_type == 'care':
        # Gyermekápolási táppénz: 60 % of capped base from day 1 (NEAK), no betegszabadság.
        employer_days, insurance_days = 0, days_sick
        employer_payment = 0.0
        insurance_payment = insurance_days * capped * care_rate
        ins_rate = care_rate * 100
    else:
        # Employer betegszabadság: working days within the first ~15 working days.
        emp_cal_days = min(days_sick, emp_cal)
        employer_days = min(round(emp_cal_days * wf_num / wf_den), bsz_max)
        employer_payment = employer_days * dvz * emp_rate  # 70 % of uncapped daily wage
        # NEAK táppénz for the remaining calendar days at 60 % of the capped base.
        insurance_days = max(0, days_sick - emp_cal)
        insurance_payment = insurance_days * capped * tappenz_rate
        ins_rate = tappenz_rate * 100

    total = employer_payment + insurance_payment
    avg_daily = total / days_sick if days_sick > 0 else 0.0
    full = (gross_salary / 30.0) * days_sick
    loss = full - total
    loss_pct = (loss / full * 100) if full > 0 else 0.0

    breakdown = []
    for day in range(1, days_sick + 1):
        if leave_type == 'care':
            payer, amount, rate_pct = 'NEAK (táppénz)', capped * care_rate, care_rate * 100
        elif day <= emp_cal:
            if (day % 7) not in (6, 0):
                payer, amount, rate_pct = 'Munkáltató (betegszabadság)', dvz * emp_rate, emp_rate * 100
            else:
                payer, amount, rate_pct = 'Hétvége (nem fizetett)', 0.0, 0.0
        else:
            payer, amount, rate_pct = 'NEAK (táppénz)', capped * tappenz_rate, tappenz_rate * 100
        breakdown.append({'day': day, 'payer': payer, 'rate_percent': _r(rate_pct),
                          'daily_amount': _r(amount)})

    return {
        'country': 'HU', 'currency': 'HUF',
        'year': _META.get('year'), 'source': _source(),
        'gross_salary': _r(gross_salary), 'days_sick': days_sick,
        'leave_type': leave_type,
        'leave_type_label': 'Betegség' if leave_type == 'illness' else 'Gyermekápolási táppénz',
        'yearly_salary': _r(yearly),
        'daily_assessment_base': _r(dvz),
        'capped_daily_base': _r(capped),
        'is_capped': is_capped,
        'max_daily_base': _r(max_daily_base),
        'employer_payment_days': employer_days,
        'insurance_payment_days': insurance_days,
        'employer_rate_percent': _r(emp_rate * 100),
        'insurance_rate_percent': _r(ins_rate),
        'employer_payment': _r(employer_payment),
        'insurance_payment': _r(insurance_payment),
        'total_sick_leave': _r(total),
        'avg_daily_rate': _r(avg_daily),
        'full_salary_for_period': _r(full),
        'loss_vs_full_salary': _r(loss),
        'loss_percentage': _r(loss_pct),
        'explanation': ('Az első 15 munkanapot a munkáltató fizeti betegszabadságként '
                        '(a távolléti díj 70 %-a), utána a NEAK folyósít táppénzt '
                        '(a napi jövedelem 60 %-a, kórházi ápolás vagy 2 évnél rövidebb '
                        'biztosítási idő esetén 50 %), maximum a napi minimálbér 200 %-áig.'),
        'breakdown': breakdown,
    }


# ---------------------------------------------------------------------------
# Vacation — alapszabadság + életkori pótszabadság 2026
# ---------------------------------------------------------------------------
def calculate_hu_vacation(age, employment_start_date, current_date=None,
                          vacation_days_used=0, days_carried_over=0,
                          planned_vacation_days=0, **kwargs):
    """Hungarian szabadság 2026: 20 working days base + age-based pótszabadság
    (1 day from 25, 2 from 28, 3 from 31, 4 from 33, 5 from 35, 6 from 37, 7 from 39,
    8 from 41, 9 from 43, 10 from 45+). Mirrors calculate_cz_vacation shape."""
    BASE_DAYS = _VAC['base_days']
    age = int(age)
    start = _parse_date(employment_start_date)
    cur = _parse_date(current_date)
    used = float(vacation_days_used or 0)
    carried = float(days_carried_over or 0)
    planned = float(planned_vacation_days or 0)
    if start > cur:
        raise ValueError('A belépés dátuma nem lehet a jövőben.')

    # Age-based supplementary days (highest matching threshold).
    age_bonus = 0
    age_threshold = 0
    for threshold, bonus in _VAC['age_bonus_table']:
        if age >= int(threshold):
            age_bonus = int(bonus)
            age_threshold = int(threshold)

    annual = BASE_DAYS + age_bonus
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
        'country': 'HU', 'currency': 'HUF',
        'year': _META.get('year'), 'source': _source(),
        'age': age,
        'employment_start_date': start.strftime('%Y-%m-%d'),
        'is_first_year': is_first_year,
        'entitlement': {
            'annual_entitlement': annual, 'base_days': BASE_DAYS,
            'age_bonus': age_bonus, 'has_age_bonus': age_bonus > 0,
            'age_threshold': age_threshold,
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
# Pension — öregségi nyugdíj 2026
# ---------------------------------------------------------------------------
def _pension_multiplier(years):
    """Hungarian service-year multiplier (nyugdíjszorzó), INDICATIVE.
    ~3.3 %/yr to 10 y (33 %), +2 %/yr to 25 y, +1 %/yr to 36 y, +1.5 %/yr to 40 y,
    +2 %/yr above 40. Checkpoints: 30 y→68 %, 40 y→80 %, 45 y→90 %."""
    y = max(0, int(years))
    r10 = float(_PEN['base_multiplier_at_10y']) / 10.0
    m = 0.0
    for yr in range(1, y + 1):
        if yr <= 10:
            m += r10
        elif yr <= 25:
            m += float(_PEN['mult_11_25_per_year'])
        elif yr <= 36:
            m += float(_PEN['mult_26_36_per_year'])
        elif yr <= 40:
            m += float(_PEN['mult_37_40_per_year'])
        else:
            m += float(_PEN['mult_41plus_per_year'])
    return m


def calculate_hu_pension(current_age, gross_salary, years_worked, gender='male',
                         include_second_pillar=False, second_pillar_rate=0, **kwargs):
    """Hungarian öregségi nyugdíj 2026: retirement age 65; pension = service-year
    multiplier × valorised average earnings (≈ current gross). Minimum old-age
    pension 28 500 Ft (frozen). No mandatory second pillar (abolished 2011).
    Mirrors calculate_cz_pension shape."""
    RETIREMENT_AGE = _PEN['retirement_age']
    MIN_PENSION = _PEN['min_pension']
    EMP_RATE = _PEN['employee_rate']       # 10 % nyugdíjjárulék (part of TB)
    EMPLOYER_RATE = _PEN['employer_rate']  # 13 % szocho (approx employer share)
    ELIG_YEARS = _PEN['eligibility_years_for_min']

    current_age = int(current_age)
    gross = float(gross_salary)
    years_worked = int(years_worked)
    if gross <= 0:
        raise ValueError('A bruttó bér nagyobb kell legyen mint 0.')

    years_to_ret = max(0, RETIREMENT_AGE - current_age)
    already_retired = current_age >= RETIREMENT_AGE
    total_years = years_worked + years_to_ret

    multiplier = _pension_multiplier(total_years)
    pension = multiplier * gross  # valorised average ≈ current monthly gross
    if pension < MIN_PENSION and total_years >= ELIG_YEARS:
        pension = MIN_PENSION

    employee_m = gross * EMP_RATE / 100
    employer_m = gross * EMPLOYER_RATE / 100
    total_m = employee_m + employer_m
    contributed = total_m * years_worked * 12
    future = total_m * years_to_ret * 12
    lifetime = contributed + future
    replacement = (pension / gross * 100) if gross > 0 else 0
    life_after = _PEN['life_expectancy_after_retirement']
    total_lifetime_pension = pension * 12 * life_after
    roi = ((total_lifetime_pension - lifetime) / lifetime * 100) if lifetime > 0 else 0

    return {
        'country': 'HU', 'currency': 'HUF',
        'year': _META.get('year'), 'source': _source(),
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
# Parental — CSED + GYED + GYES 2026
# ---------------------------------------------------------------------------
def calculate_hu_parental(birth_date, gross_salary=None, twins_or_more=False,
                          current_date=None, **kwargs):
    """Hungarian CSED + GYED + GYES 2026.
    CSED: 100 % of previous income for 24 weeks. GYED: 70 % of the base, capped at
    451 920 Ft/month, until the child turns 2. GYES: fixed 28 500 Ft/month until the
    child turns 3. Mirrors calculate_cz_parental shape (fixed-benefit variant)."""
    CSED_WEEKS = _PAR['csed_weeks']
    CSED_RATE = _PAR['csed_rate']
    GYED_RATE = _PAR['gyed_rate']
    GYED_MAX = _PAR['gyed_monthly_max']
    GYES_M = _PAR['gyes_monthly']
    gyed_until_m = _PAR['gyed_until_age_months']
    gyes_until_m = _PAR['gyes_until_age_months']
    total_months = _PAR['total_months'] + (_PAR['twins_extra_months'] if twins_or_more else 0)

    bd = _parse_date(birth_date)
    cur = _parse_date(current_date) if current_date else datetime.now().date()
    if bd > cur:
        raise ValueError('A születési dátum nem lehet a jövőben.')

    age_days = (cur - bd).days
    maternity_end = bd + timedelta(weeks=CSED_WEEKS)

    # CSED: 100 % of the calendar-day income (no reduction cap).
    maternity_benefit = None
    gyed_monthly = GYES_M  # fallback when no salary provided
    if gross_salary and float(gross_salary) > 0:
        g = float(gross_salary)
        dvz = g * 12 / 365.0
        daily = dvz * CSED_RATE
        maternity_benefit = {
            'daily_amount': _r(daily), 'weekly_amount': _r(daily * 7),
            'monthly_amount': _r(daily * 30), 'total_amount': _r(daily * CSED_WEEKS * 7),
            'duration_weeks': CSED_WEEKS, 'end_date': maternity_end.strftime('%Y-%m-%d'),
            'daily_assessment_base': _r(dvz),
        }
        gyed_monthly = min(g * GYED_RATE, GYED_MAX)

    # GYED (to age 2) then GYES (to age 3) — default "current phase" monthly amount.
    parental_start = maternity_end
    benefit_end = bd + timedelta(days=int(365.25 * (gyes_until_m / 12.0)))
    child_months = age_days / 30.44

    if cur < parental_start:
        default_monthly = gyed_monthly
        remaining_months, status = total_months, 'Még CSED-en van'
    elif child_months < gyed_until_m:
        default_monthly = gyed_monthly
        elapsed = (cur - parental_start).days // 30
        remaining_months = max(0, total_months - elapsed)
        status = 'GYED folyósítás alatt'
    elif child_months < gyes_until_m:
        default_monthly = GYES_M
        elapsed = (cur - parental_start).days // 30
        remaining_months = max(0, total_months - elapsed)
        status = 'GYES folyósítás alatt'
    else:
        default_monthly = 0.0
        remaining_months, status = 0, 'Az ellátás megszűnt'

    # Indicative total: CSED + GYED phase + GYES phase.
    csed_total = (maternity_benefit['total_amount'] if maternity_benefit else 0.0)
    gyed_months = max(0, gyed_until_m - CSED_WEEKS * 7 / 30.44)
    gyes_months = max(0, gyes_until_m - gyed_until_m)
    total_benefit = csed_total + gyed_monthly * gyed_months + GYES_M * gyes_months

    return {
        'country': 'HU', 'currency': 'HUF',
        'year': _META.get('year'), 'source': _source(),
        'birth_date': bd.strftime('%Y-%m-%d'),
        'child_age_days': age_days, 'child_age_months': age_days // 30,
        'child_age_years': age_days // 365,
        'maternity_benefit': maternity_benefit,
        'maternity_end_date': maternity_end.strftime('%Y-%m-%d'),
        'benefit_type': 'hu_gyed_gyes',
        'benefit_type_label': 'GYED (2 éves korig) + GYES (3 éves korig)',
        'monthly_benefit': _r(default_monthly),
        'parental_start_date': parental_start.strftime('%Y-%m-%d'),
        'parental_end_date': benefit_end.strftime('%Y-%m-%d'),
        'total_months': total_months,
        'remaining_months': max(0, remaining_months),
        'total_benefit': _r(total_benefit),
        'benefit_status': status,
        # GYED/GYES allow working (GYED from 168 days) — no CZ-style income limit → gated off.
        'can_work_and_receive': True,
        'work_income_limit': 0.0,
        'work_warning': None,
        'second_child_extension': None,
        'comparison': None,
        'notifications': [],
        'progress_percentage': round(((total_months - remaining_months) / total_months * 100)
                                     if total_months > 0 else 0, 1),
    }


# ---------------------------------------------------------------------------
# Solar — Otthoni Energiatároló / Napenergia Plusz 2026
# ---------------------------------------------------------------------------
def calculate_hu_solar(annual_consumption_kwh, electricity_rate=None,
                       system_size_kwp=None, include_battery=False,
                       battery_capacity_kwh=0, **kwargs) -> Dict[str, Any]:
    """Hungarian PV subsidy & payback estimator 2026, INDICATIVE. The 2026 residential
    scheme (Otthoni Energiatároló / Napenergia Plusz) funds battery storage (min
    10 kWh) up to 2.5 M Ft; PV panels themselves are not directly subsidised. Mirrors
    calculate_cz_solar signature and returned keys (subsidy surfaced via the same
    section, labelled for the HU programme)."""
    YIELD = _SOL['yield_kwh_per_kwp']
    PRICE_PER_KWP = _SOL['price_per_kwp']
    BATTERY_PRICE = _SOL['battery_price_per_kwh']
    DEFAULT_SCR = _SOL['default_self_consumption']
    BATTERY_SCR = _SOL['battery_self_consumption']
    DEFAULT_RATE = _SOL['default_electricity_rate']
    FEED_IN = _SOL['feed_in_price']
    CO2 = _SOL['co2_kg_per_kwh']
    NZU_BASE = _SOL['nzu_base']
    NZU_PER_KWP = _SOL['nzu_per_kwp']
    NZU_KWP_CAP = _SOL['nzu_kwp_cap']
    NZU_BATTERY_BONUS = _SOL['nzu_battery_bonus']
    SUBSIDY_RATE = _SOL['subsidy_rate_of_cost']
    BATTERY_MIN = _SOL['battery_min_kwh']
    KWP_MIN = _SOL['kwp_min']
    KWP_MAX = _SOL['kwp_max']
    BATTERY_RATIO = _SOL['battery_ratio']
    BATTERY_MAX = _SOL['battery_max']

    def _rr(x, d=0):
        return round(float(x) + 1e-9, d)

    annual_consumption = float(annual_consumption_kwh)
    if annual_consumption <= 0:
        raise ValueError('Adja meg az éves áramfogyasztást (kWh).')
    rate = float(electricity_rate) if electricity_rate else DEFAULT_RATE
    include_battery = bool(include_battery)

    kwp = float(system_size_kwp) if system_size_kwp else round(annual_consumption / YIELD, 1)
    kwp = max(KWP_MIN, min(kwp, KWP_MAX))
    battery_kwh = float(battery_capacity_kwh or 0)
    if include_battery and battery_kwh <= 0:
        battery_kwh = round(min(kwp * BATTERY_RATIO, BATTERY_MAX), 1)
    if include_battery and battery_kwh < BATTERY_MIN:
        battery_kwh = BATTERY_MIN  # programme requires ≥10 kWh
    if not include_battery:
        battery_kwh = 0.0

    annual_production = kwp * YIELD
    pv_cost = kwp * PRICE_PER_KWP
    battery_cost = battery_kwh * BATTERY_PRICE
    total_cost = pv_cost + battery_cost

    subsidy_by_scheme = NZU_BASE + NZU_PER_KWP * min(kwp, NZU_KWP_CAP) + (NZU_BATTERY_BONUS if include_battery else 0)
    subsidy_by_cost = SUBSIDY_RATE * (battery_cost if include_battery else total_cost)
    total_subsidy = min(subsidy_by_scheme, subsidy_by_cost)
    limited_by = 'költség (100 %)' if total_subsidy >= subsidy_by_cost else 'program felső határa'
    net_cost = max(total_cost - total_subsidy, 0)

    scr = BATTERY_SCR if include_battery else DEFAULT_SCR
    self_consumed = min(annual_production * scr, annual_consumption)
    exported = max(annual_production - self_consumed, 0)
    annual_savings = self_consumed * rate + exported * FEED_IN
    payback = (net_cost / annual_savings) if annual_savings > 0 else None
    coverage = (self_consumed / annual_consumption * 100) if annual_consumption else 0

    return {
        'country': 'HU', 'currency': 'HUF',
        'year': _META.get('year'), 'source': _source(),
        'inputs': {
            'annual_consumption_kwh': _rr(annual_consumption),
            'electricity_rate': round(rate, 4),
            'include_battery': include_battery,
        },
        'system': {
            'recommended_kwp': round(kwp, 1),
            'battery_capacity_kwh': round(battery_kwh, 1),
            'annual_production_kwh': _rr(annual_production),
            'self_consumption_ratio': round(scr, 2),
        },
        'cost': {
            'pv_cost': _rr(pv_cost), 'battery_cost': _rr(battery_cost), 'total_cost': _rr(total_cost),
        },
        'subsidy': {
            'eligible_kwp': round(min(kwp, NZU_KWP_CAP), 1),
            'rate_per_kwp': NZU_PER_KWP,
            'max_subsidy': _rr(NZU_BASE + NZU_PER_KWP * NZU_KWP_CAP + NZU_BATTERY_BONUS),
            'total_subsidy': _rr(total_subsidy),
            'limited_by': limited_by,
            'net_cost': _rr(net_cost),
            'scheme': 'Otthoni Energiatároló / Napenergia Plusz (tájékoztató jelleggel)',
        },
        'savings': {
            'self_consumed_kwh': _rr(self_consumed), 'exported_kwh': _rr(exported),
            'annual_savings': _rr(annual_savings), 'monthly_savings': _rr(annual_savings / 12),
            'coverage_pct': round(coverage, 1),
        },
        'analysis': {
            'payback_years': round(payback, 1) if payback else None,
            'savings_30y': _rr(annual_savings * 30 - net_cost),
            'co2_savings_kg': _rr(annual_production * CO2),
        },
    }
