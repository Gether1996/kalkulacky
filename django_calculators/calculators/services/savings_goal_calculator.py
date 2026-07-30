"""
Savings Goal Calculator
=======================

Compound-interest projections for a savings goal. Currency-agnostic — the
caller supplies the currency for display only; the maths is the same in EUR,
CZK, PLN or HUF.

Two questions a saver asks:

  * "How long until I reach my target?"  -> project_time_to_goal()
  * "How much must I save each month?"   -> required_monthly_contribution()

Interest is compounded monthly: each month the balance grows by the monthly
rate, then the contribution is added (contributions at period end / ordinary
annuity). This matches how a typical savings account / regular investment is
quoted from an annual nominal rate.

Money maths is done in ``Decimal`` (repo convention); values are returned as
plain floats rounded to cents (like the other calculators) so the JSON API
keeps returning numbers.
"""

from decimal import Decimal, ROUND_HALF_UP

MAX_MONTHS = 1200  # 100 years — hard cap so an unreachable goal can't loop forever

_CENT = Decimal('0.01')


def _d(value):
    """Coerce Decimal/str/int/float to Decimal for the money maths."""
    if value is None:
        return Decimal('0')
    if isinstance(value, Decimal):
        return value
    return Decimal(str(value))


def _money(value: Decimal) -> float:
    """Round a Decimal to cents and return a float for the JSON response."""
    return float(value.quantize(_CENT, rounding=ROUND_HALF_UP))


def project_time_to_goal(target_amount, initial_amount, monthly_contribution,
                         annual_rate):
    """
    Given a monthly contribution, work out when the balance first reaches the
    target. Iterates month-by-month (robust for rate == 0 and for the exact
    crossover month).

    Returns a dict with months/years to goal, whether it's reachable, the
    projected balance, total contributed and interest earned.
    """
    target = _d(target_amount)
    balance = _d(initial_amount)
    monthly = _d(monthly_contribution)
    r = _d(annual_rate) / Decimal('100') / Decimal('12')

    total_contributed = balance  # the starting balance is money you put in

    if balance >= target:
        return _projection_result(0, True, balance, total_contributed)

    # If neither interest nor contributions move the needle, the goal is
    # unreachable — say so instead of spinning to the cap.
    if monthly <= 0 and r <= 0:
        return _projection_result(None, False, balance, total_contributed)

    months = 0
    while balance < target and months < MAX_MONTHS:
        balance = balance * (Decimal('1') + r) + monthly
        total_contributed += monthly
        months += 1

    reached = balance >= target
    return _projection_result(
        months if reached else None, reached, balance, total_contributed,
    )


def required_monthly_contribution(target_amount, initial_amount, months,
                                  annual_rate):
    """
    Given a deadline (number of months), solve the ordinary-annuity formula for
    the monthly contribution needed to hit the target.

        FV = PV·(1+r)^n + C·[((1+r)^n − 1) / r]

    Solving for C. Falls back to the no-interest case when r == 0. Never returns
    a negative contribution (if the starting balance already grows past the
    target, the required contribution is 0).
    """
    target = _d(target_amount)
    pv = _d(initial_amount)
    n = int(months)
    r = _d(annual_rate) / Decimal('100') / Decimal('12')

    if n <= 0:
        return None

    if r == 0:
        monthly = (target - pv) / Decimal(n)
    else:
        growth = (Decimal('1') + r) ** n
        fv_initial = pv * growth
        annuity_factor = (growth - Decimal('1')) / r
        monthly = (target - fv_initial) / annuity_factor

    monthly = max(Decimal('0'), monthly)

    # Sanity projection so the response is self-describing.
    projection = project_time_to_goal(target, pv, monthly, annual_rate)
    return {
        'required_monthly': _money(monthly),
        'months': n,
        'years': round(n / 12.0, 1),
        'projected_balance': projection['projected_balance'],
        'total_contributed': projection['total_contributed'],
        'interest_earned': projection['interest_earned'],
    }


def _projection_result(months, reached, balance, total_contributed):
    interest = balance - total_contributed
    return {
        'reached': reached,
        'months': months,
        'years': round(months / 12.0, 1) if months is not None else None,
        'projected_balance': _money(balance),
        'total_contributed': _money(total_contributed),
        'interest_earned': _money(interest),
    }


def status_for_goal(target_amount, current_balance, monthly_contribution,
                    annual_rate, months_remaining):
    """
    Tracker helper: is the saver on track to hit the target by the deadline?

    Projects the *current balance* forward by `months_remaining` at the planned
    monthly contribution + rate and compares to target. `months_remaining` of
    None (no deadline) → status 'no_deadline'. Returns a small dict used by the
    dashboard to colour the goal.
    """
    target = _d(target_amount)
    balance = _d(current_balance)
    progress_pct = (
        round(float(balance / target * Decimal('100')), 1) if target > 0 else 0.0
    )

    if balance >= target:
        return {'status': 'reached', 'progress_pct': min(progress_pct, 100.0),
                'projected_balance': _money(balance), 'shortfall': 0.0}

    if months_remaining is None:
        return {'status': 'no_deadline', 'progress_pct': progress_pct,
                'projected_balance': None, 'shortfall': None}

    if months_remaining <= 0:
        # Deadline passed and target not met.
        return {'status': 'behind', 'progress_pct': progress_pct,
                'projected_balance': _money(balance),
                'shortfall': _money(target - balance)}

    monthly = _d(monthly_contribution)
    r = _d(annual_rate) / Decimal('100') / Decimal('12')
    projected = balance
    for _ in range(int(months_remaining)):
        projected = projected * (Decimal('1') + r) + monthly

    on_track = projected >= target
    return {
        'status': 'on_track' if on_track else 'behind',
        'progress_pct': progress_pct,
        'projected_balance': _money(projected),
        'shortfall': 0.0 if on_track else _money(target - projected),
    }
