"""
Czech (CZ) benefit / pension / vacation / sick-leave calculators for 2026.

Each returns a result shape compatible with the corresponding Slovak service so
the existing frontends render with CZ numbers in CZK (Czech readers understand
Slovak labels — the project's i18n strategy). CZ-specific structural sections
that have no SK equivalent are gated off in the templates.

⚠️ INDICATIVE 2026 figures from public CZ guides (vypocet.cz, mesec.cz,
finance.cz, penize.cz, ČSSZ, ÚP, zakonik-prace.cz). Verify before relying.
Constants centralised per function for yearly updates.
"""
from datetime import datetime, timedelta, date
from typing import Dict, Any


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


# --- CZ daily-assessment-base reduction (nemocenská/PPM redukční hranice 2026) -
RH1, RH2, RH3 = 1633.0, 2449.0, 4897.0


def _reduce_dvz(dvz, r1=0.90, r2=0.60, r3=0.30):
    """Reduce the daily assessment base through the 3 reduction brackets."""
    part1 = min(dvz, RH1) * r1
    part2 = (min(dvz, RH2) - RH1) * r2 if dvz > RH1 else 0.0
    part3 = (min(dvz, RH3) - RH2) * r3 if dvz > RH2 else 0.0
    return part1 + part2 + part3


def calculate_cz_sick_leave(gross_salary, days_sick, leave_type='illness', **kwargs):
    """Czech nemocenská 2026. Employer pays náhrada mzdy for working days 1–14
    (60 % of reduced DVZ); ČSSZ pays from day 15 (60/66/72 %)."""
    gross_salary = float(gross_salary)
    days_sick = int(days_sick)
    yearly = gross_salary * 12
    dvz = yearly / 365.0
    reduced = _reduce_dvz(dvz)
    is_capped = dvz > RH3

    if leave_type == 'care':
        # Ošetřovné: 60 % of reduced DVZ from day 1 (ČSSZ), typically max 9 days.
        employer_days, insurance_days = 0, days_sick
        employer_payment = 0.0
        insurance_payment = insurance_days * reduced * 0.60
        ins_rate = 60.0
    else:
        # Employer náhrada mzdy: working days within the first 14 calendar days.
        emp_cal_days = min(days_sick, 14)
        employer_days = round(emp_cal_days * 5 / 7)          # working days only
        employer_payment = employer_days * reduced * 0.60
        # ČSSZ nemocenská from day 15 (calendar days), tiered.
        insurance_days = max(0, days_sick - 14)
        ins_payment = 0.0
        for day in range(15, days_sick + 1):
            if day <= 30:
                rate = 0.60
            elif day <= 60:
                rate = 0.66
            else:
                rate = 0.72
            ins_payment += reduced * rate
        insurance_payment = ins_payment
        ins_rate = 60.0

    total = employer_payment + insurance_payment
    avg_daily = total / days_sick if days_sick > 0 else 0.0
    full = (gross_salary / 30.0) * days_sick
    loss = full - total
    loss_pct = (loss / full * 100) if full > 0 else 0.0

    breakdown = []
    for day in range(1, days_sick + 1):
        if leave_type == 'care':
            payer, rate = 'ČSSZ', 0.60
        elif day <= 14:
            payer, rate = ('Zaměstnavatel', 0.60) if (day % 7) not in (6, 0) else ('Víkend (neplaceno)', 0.0)
        elif day <= 30:
            payer, rate = 'ČSSZ', 0.60
        elif day <= 60:
            payer, rate = 'ČSSZ', 0.66
        else:
            payer, rate = 'ČSSZ', 0.72
        breakdown.append({'day': day, 'payer': payer, 'rate_percent': _r(rate * 100),
                          'daily_amount': _r(reduced * rate)})

    return {
        'country': 'CZ', 'currency': 'CZK',
        'gross_salary': _r(gross_salary), 'days_sick': days_sick,
        'leave_type': leave_type,
        'leave_type_label': 'Nemoc' if leave_type == 'illness' else 'Ošetřovné člena rodiny',
        'yearly_salary': _r(yearly),
        'daily_assessment_base': _r(dvz),
        'capped_daily_base': _r(reduced),
        'is_capped': is_capped,
        'max_daily_base': _r(RH3),
        'employer_payment_days': employer_days,
        'insurance_payment_days': insurance_days,
        'employer_rate_percent': 60.0,
        'insurance_rate_percent': ins_rate,
        'employer_payment': _r(employer_payment),
        'insurance_payment': _r(insurance_payment),
        'total_sick_leave': _r(total),
        'avg_daily_rate': _r(avg_daily),
        'full_salary_for_period': _r(full),
        'loss_vs_full_salary': _r(loss),
        'loss_percentage': _r(loss_pct),
        'explanation': ('První 14 dní hradí zaměstnavatel náhradu mzdy (60 % redukovaného '
                        'denního vyměřovacího základu za pracovní dny), od 15. dne platí ČSSZ '
                        '(60 % do 30. dne, 66 % do 60. dne, 72 % od 61. dne).'),
        'breakdown': breakdown,
    }


def calculate_cz_vacation(age, employment_start_date, current_date=None,
                          vacation_days_used=0, days_carried_over=0,
                          planned_vacation_days=0, **kwargs):
    """Czech dovolená 2026: basic 4 weeks (20 days), no age bonus."""
    BASE_DAYS = 20  # 4 weeks (legal minimum; many employers grant 5)
    age = int(age)
    start = _parse_date(employment_start_date)
    cur = _parse_date(current_date)
    used = float(vacation_days_used or 0)
    carried = float(days_carried_over or 0)
    planned = float(planned_vacation_days or 0)
    if start > cur:
        raise ValueError('Datum nástupu nemůže být v budoucnosti.')

    annual = BASE_DAYS
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
        'country': 'CZ', 'currency': 'CZK',
        'age': age,
        'employment_start_date': start.strftime('%Y-%m-%d'),
        'is_first_year': is_first_year,
        'entitlement': {
            'annual_entitlement': annual, 'base_days': BASE_DAYS,
            'age_bonus': 0, 'has_age_bonus': False, 'age_threshold': 0,
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


def calculate_cz_pension(current_age, gross_salary, years_worked, gender='male',
                         include_second_pillar=False, second_pillar_rate=0, **kwargs):
    """Czech starobní důchod 2026: základní výměra 4 900 Kč + procentní výměra
    1,495 % za rok z redukovaného výpočtového základu. Min 9 800 Kč."""
    BASIC_AMOUNT = 4900.0
    PCT_PER_YEAR = 0.01495
    MIN_PENSION = 9800.0
    RETIREMENT_AGE = 65
    EMP_RATE, EMPLOYER_RATE = 6.5, 21.5   # pension portion of social insurance
    # Computing-base reduction (2026): 99 % up to 21 546, 26 % to 195 868.
    RB1, RB2 = 21546.0, 195868.0

    current_age = int(current_age)
    gross = float(gross_salary)
    years_worked = int(years_worked)
    if gross <= 0:
        raise ValueError('Hrubá mzda musí být větší než 0.')

    years_to_ret = max(0, RETIREMENT_AGE - current_age)
    already_retired = current_age >= RETIREMENT_AGE
    total_years = years_worked + years_to_ret

    vz = gross  # approximate osobní vyměřovací základ ≈ current monthly gross
    comp_base = 0.99 * min(vz, RB1) + (0.26 * (min(vz, RB2) - RB1) if vz > RB1 else 0.0)
    pct_amount = PCT_PER_YEAR * total_years * comp_base
    pension = BASIC_AMOUNT + pct_amount
    if pension < MIN_PENSION and total_years >= 30:
        pension = MIN_PENSION

    employee_m = gross * EMP_RATE / 100
    employer_m = gross * EMPLOYER_RATE / 100
    total_m = employee_m + employer_m
    contributed = total_m * years_worked * 12
    future = total_m * years_to_ret * 12
    lifetime = contributed + future
    replacement = (pension / gross * 100) if gross > 0 else 0
    life_after = 20
    total_lifetime_pension = pension * 12 * life_after
    roi = ((total_lifetime_pension - lifetime) / lifetime * 100) if lifetime > 0 else 0

    return {
        'country': 'CZ', 'currency': 'CZK',
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


def calculate_cz_parental(birth_date, gross_salary=None, twins_or_more=False,
                          current_date=None, **kwargs):
    """Czech mateřská (PPM) + rodičovský příspěvek 2026.
    PPM: 70 % of reduced daily DVZ, 28 weeks (37 for multiples).
    Rodičovský příspěvek: fixed pot 350 000 Kč (700 000 for multiples)."""
    PPM_WEEKS = 37 if twins_or_more else 28
    PARENTAL_TOTAL = 700000.0 if twins_or_more else 350000.0
    PARENTAL_MONTHLY_MAX = 15000.0  # default cap; parents may draw faster
    bd = _parse_date(birth_date)
    cur = _parse_date(current_date) if current_date else datetime.now().date()
    if bd > cur:
        raise ValueError('Datum narození nemůže být v budoucnosti.')

    age_days = (cur - bd).days
    maternity_end = bd + timedelta(weeks=PPM_WEEKS)

    maternity_benefit = None
    if gross_salary and float(gross_salary) > 0:
        dvz = float(gross_salary) * 12 / 365.0
        # PPM reduction: 100 % / 60 % / 30 % through the brackets.
        reduced = _reduce_dvz(dvz, r1=1.00, r2=0.60, r3=0.30)
        daily = reduced * 0.70
        maternity_benefit = {
            'daily_amount': _r(daily), 'weekly_amount': _r(daily * 7),
            'monthly_amount': _r(daily * 30), 'total_amount': _r(daily * PPM_WEEKS * 7),
            'duration_weeks': PPM_WEEKS, 'end_date': maternity_end.strftime('%Y-%m-%d'),
            'daily_assessment_base': _r(dvz),
        }

    # Rodičovský příspěvek — fixed pot drawn flexibly until the child turns ~3–4.
    parental_start = maternity_end
    benefit_end = bd + timedelta(days=365 * 3)
    default_monthly = min(PARENTAL_MONTHLY_MAX, PARENTAL_TOTAL / 36.0)
    total_months = 36

    if cur < parental_start:
        remaining_months, status = total_months, 'Ještě jste na mateřské'
    elif cur >= benefit_end:
        remaining_months, status = 0, 'Rodičovský příspěvek skončil'
    else:
        elapsed = (cur - parental_start).days // 30
        remaining_months, status = max(0, total_months - elapsed), 'Pobíráte rodičovský příspěvek'

    return {
        'country': 'CZ', 'currency': 'CZK',
        'birth_date': bd.strftime('%Y-%m-%d'),
        'child_age_days': age_days, 'child_age_months': age_days // 30,
        'child_age_years': age_days // 365,
        'maternity_benefit': maternity_benefit,
        'maternity_end_date': maternity_end.strftime('%Y-%m-%d'),
        'benefit_type': 'cz_fixed',
        'benefit_type_label': 'Rodičovský příspěvek (pevný celkový limit)',
        'monthly_benefit': _r(default_monthly),
        'parental_start_date': parental_start.strftime('%Y-%m-%d'),
        'parental_end_date': benefit_end.strftime('%Y-%m-%d'),
        'total_months': total_months,
        'remaining_months': max(0, remaining_months),
        'total_benefit': _r(PARENTAL_TOTAL),
        'benefit_status': status,
        # CZ has no income limit / osnova-vs-alternatíva → gated off in the UI.
        'can_work_and_receive': True,
        'work_income_limit': 0.0,
        'work_warning': None,
        'second_child_extension': None,
        'comparison': None,
        'notifications': [],
        'progress_percentage': round(((total_months - remaining_months) / total_months * 100)
                                     if total_months > 0 else 0, 1),
    }
