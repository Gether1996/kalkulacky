"""
Slovak Tax & Calculator Configuration Variables (compatibility shim).

⚠️ The actual numbers now live in the editable data file
``calculators/services/data/sk_<year>.json`` — update THAT once a year (or add a
new ``sk_<year+1>.json``). This module simply loads the latest SK dataset and
re-exports every constant under its historical name, so existing
``from ...config_variables import X`` imports keep working unchanged.

Derived values (monthly = yearly / 12, etc.) are computed here exactly as before.
"""

from decimal import Decimal

from .data import get_rates, config_info, latest_year

# --- Load the latest available Slovak dataset ---------------------------------
SK_YEAR = latest_year('SK')
_R = get_rates('SK', SK_YEAR)
_salary = _R['salary']
_vat = _R['vat']
_mortgage = _R['mortgage']
_leasing = _R['leasing']
_energy = _R['energy']
_pension = _R['pension']
_sick = _R['sick_leave']
_free = _R['freelancer']
_fuel = _R['fuel']
_parental = _R['parental']


# ===========================
# SALARY CALCULATOR
# ===========================

# --- EMPLOYEE CONTRIBUTIONS ---
SOCIAL_INSURANCE_RATE_EMPLOYEE = _salary['social_insurance_rate_employee']   # 9.4%
HEALTH_INSURANCE_RATE_EMPLOYEE = _salary['health_insurance_rate_employee']   # 5.0%
HEALTH_INSURANCE_RATE_DISABILITY = _salary['health_insurance_rate_disability']  # 2.5% (ZŤP)

# --- EMPLOYER CONTRIBUTIONS ---
EMPLOYER_CONTRIBUTIONS_RATE = _salary['employer_contributions_rate']         # 36.2%
SOCIAL_INSURANCE_RATE_EMPLOYER = _salary['social_insurance_rate_employer']   # 26.2% (ref)
HEALTH_INSURANCE_RATE_EMPLOYER = _salary['health_insurance_rate_employer']   # 10.0% (ref)

# --- SOCIAL INSURANCE LIMITS ---
SOCIAL_INSURANCE_MAX_BASE_MONTHLY = _salary['social_insurance_max_base_monthly']
SOCIAL_INSURANCE_MAX_BASE_YEARLY = SOCIAL_INSURANCE_MAX_BASE_MONTHLY * 12

# --- INCOME TAX BRACKETS ---
# From 1.1.2026 SK employee PIT is a 4-bracket progressive scale (19/25/30/35 %),
# split at 154.8× / 212.4× / 264× the subsistence minimum. Verified 2026.
TAX_RATE_BRACKET_1 = _salary['tax_rate_bracket_1']  # 19%
TAX_RATE_BRACKET_2 = _salary['tax_rate_bracket_2']  # 25%
TAX_RATE_BRACKET_3 = _salary['tax_rate_bracket_3']  # 30%
TAX_RATE_BRACKET_4 = _salary['tax_rate_bracket_4']  # 35%

TAX_THRESHOLD_1_YEARLY = _salary['tax_threshold_1_yearly']
TAX_THRESHOLD_2_YEARLY = _salary['tax_threshold_2_yearly']
TAX_THRESHOLD_3_YEARLY = _salary['tax_threshold_3_yearly']
TAX_THRESHOLD_1_MONTHLY = TAX_THRESHOLD_1_YEARLY / 12
TAX_THRESHOLD_2_MONTHLY = TAX_THRESHOLD_2_YEARLY / 12
TAX_THRESHOLD_3_MONTHLY = TAX_THRESHOLD_3_YEARLY / 12

# --- NON-TAXABLE AMOUNT (NČZD) ---
NON_TAXABLE_AMOUNT_YEARLY = _salary['non_taxable_amount_yearly']
NON_TAXABLE_AMOUNT_MONTHLY = _salary['non_taxable_amount_monthly']
NON_TAXABLE_AMOUNT_DISABILITY_YEARLY = _salary['non_taxable_amount_disability_yearly']
NON_TAXABLE_AMOUNT_DISABILITY_MONTHLY = _salary['non_taxable_amount_disability_monthly']

# --- CHILD TAX BONUS ---
CHILD_TAX_BONUS_UNDER_15 = _salary['child_tax_bonus_under_15']
CHILD_TAX_BONUS_15_TO_18 = _salary['child_tax_bonus_15_to_18']

# --- MINIMUM / AVERAGE WAGE ---
MINIMUM_WAGE_MONTHLY = _salary['minimum_wage_monthly']
MINIMUM_WAGE_HOURLY = _salary['minimum_wage_hourly']
AVERAGE_WAGE_MONTHLY = _salary['average_wage_monthly']


# ===========================
# VAT CALCULATOR (DPH)
# ===========================
VAT_RATE_STANDARD = _vat['standard']
VAT_RATE_REDUCED_1 = _vat['reduced_1']
VAT_RATE_REDUCED_2 = _vat['reduced_2']
VAT_RATE_ZERO = _vat['zero']


# ===========================
# MORTGAGE CALCULATOR (reference only)
# ===========================
TYPICAL_MORTGAGE_TERM_YEARS = _mortgage['typical_term_years']
TYPICAL_INTEREST_RATE_2026 = _mortgage['typical_interest_rate']
TYPICAL_LTV_RATIO = _mortgage['typical_ltv_ratio']


# ===========================
# CAR LEASING CALCULATOR
# ===========================
LEASING_DEFAULT_INTEREST_RATE = _leasing['default_interest_rate']
LEASING_DEFAULT_LOAN_RATE = _leasing['default_loan_rate']
LEASING_DEFAULT_RESIDUAL_VALUE = _leasing['default_residual_value']


# ===========================
# INFLATION CALCULATOR
# ===========================
DEFAULT_INFLATION_RATE = _R['inflation']['default_rate']


# ===========================
# ENERGY CALCULATOR
# ===========================
ELECTRICITY_RATE_LOW = _energy['electricity_rate_low']
ELECTRICITY_RATE_HIGH = _energy['electricity_rate_high']
ELECTRICITY_FIXED_MONTHLY = _energy['electricity_fixed_monthly']
GAS_RATE = _energy['gas_rate']
GAS_FIXED_MONTHLY = _energy['gas_fixed_monthly']
AVG_ELECTRICITY_MONTHLY = _energy['avg_electricity_monthly']
AVG_GAS_MONTHLY = _energy['avg_gas_monthly']


# ===========================
# PENSION CALCULATOR
# ===========================
RETIREMENT_AGE_MALE = _pension['retirement_age_male']
RETIREMENT_AGE_FEMALE = _pension['retirement_age_female']
PENSION_EMPLOYEE_CONTRIBUTION_RATE = _pension['employee_contribution_rate']
PENSION_EMPLOYER_CONTRIBUTION_RATE = _pension['employer_contribution_rate']
PENSION_TOTAL_CONTRIBUTION_RATE = PENSION_EMPLOYEE_CONTRIBUTION_RATE + PENSION_EMPLOYER_CONTRIBUTION_RATE
AVERAGE_PENSION_SK = _pension['average_pension']
PENSION_POINT_VALUE = _pension['pension_point_value']
MINIMUM_PENSION_SK = _pension['minimum_pension']
SECOND_PILLAR_DEFAULT_RATE = _pension['second_pillar_default_rate']
LIFE_EXPECTANCY_AFTER_RETIREMENT = _pension['life_expectancy_after_retirement']


# ===========================
# SICK LEAVE CALCULATOR (PN)
# ===========================
SICK_LEAVE_EMPLOYER_PAYMENT_DAYS = _sick['employer_payment_days']
SICK_LEAVE_EMPLOYER_TIER1_DAYS = _sick['employer_tier1_days']
SICK_LEAVE_EMPLOYER_RATE = _sick['employer_rate']
SICK_LEAVE_INSURANCE_RATE_ILLNESS = _sick['insurance_rate_illness']
SICK_LEAVE_INSURANCE_RATE_CARE = _sick['insurance_rate_care']
SICK_LEAVE_MAX_ASSESSMENT_BASE_YEARLY = _sick['max_assessment_base_yearly']
SICK_LEAVE_MAX_ASSESSMENT_BASE_DAILY = SICK_LEAVE_MAX_ASSESSMENT_BASE_YEARLY / 365
SICK_LEAVE_MIN_WAGE_MONTHLY = _sick['min_wage_monthly']
SICK_LEAVE_MIN_WAGE_DAILY = SICK_LEAVE_MIN_WAGE_MONTHLY * 12 / 365


# ===========================
# FREELANCER TAX CALCULATOR (SZČO)
# ===========================
FREELANCER_TAX_RATE_1 = _free['tax_rate_1']  # 15%
FREELANCER_TAX_RATE_2 = _free['tax_rate_2']  # 19%
FREELANCER_TAX_RATE_3 = _free['tax_rate_3']  # 25%
FREELANCER_TAX_RATE_4 = _free['tax_rate_4']  # 30% (legacy/unused)
FREELANCER_TAX_RATE_5 = _free['tax_rate_5']  # 35% (legacy/unused)

FREELANCER_TAX_THRESHOLD_1 = _free['tax_threshold_1']  # 20000 (legacy label; real gate is turnover_15_limit)
FREELANCER_TAX_THRESHOLD_2 = TAX_THRESHOLD_1_YEARLY
FREELANCER_TAX_THRESHOLD_3 = TAX_THRESHOLD_2_YEARLY
FREELANCER_TAX_THRESHOLD_4 = TAX_THRESHOLD_3_YEARLY

FREELANCER_HEALTH_INSURANCE_RATE = _free['health_insurance_rate']  # 16%
FREELANCER_MIN_HEALTH_BASE_MONTHLY = _free['min_health_base_monthly']

FREELANCER_SOCIAL_SICKNESS_RATE = _free['social_sickness_rate']    # 4.4%
FREELANCER_SOCIAL_PENSION_RATE = _free['social_pension_rate']      # 18%
FREELANCER_SOCIAL_DISABILITY_RATE = _free['social_disability_rate']  # 6%
FREELANCER_SOCIAL_ACCIDENT_RATE = _free['social_accident_rate']   # 0%
FREELANCER_SOCIAL_GUARANTEE_RATE = _free['social_guarantee_rate']  # 0%
FREELANCER_SOCIAL_RESERVE_RATE = _free['social_reserve_rate']     # 4.75%
FREELANCER_MIN_SOCIAL_BASE_MONTHLY = _free['min_social_base_monthly']

FREELANCER_FLAT_EXPENSE_RATE = _free['flat_expense_rate']         # 60%
FREELANCER_FLAT_EXPENSE_CAP = _free['flat_expense_cap']           # €20,000/yr paušál cap
FREELANCER_TURNOVER_15_LIMIT = _free['turnover_15_limit']         # €100,000 gate for 15% rate

FREELANCER_NON_TAXABLE_AMOUNT_ANNUAL = NON_TAXABLE_AMOUNT_YEARLY
FREELANCER_NON_TAXABLE_AMOUNT_MONTHLY = NON_TAXABLE_AMOUNT_MONTHLY


# ===========================
# FUEL COST CALCULATOR (reference only)
# ===========================
TYPICAL_FUEL_PRICE_PETROL = _fuel['price_petrol']
TYPICAL_FUEL_PRICE_DIESEL = _fuel['price_diesel']
TYPICAL_CONSUMPTION_CITY = _fuel['consumption_city']
TYPICAL_CONSUMPTION_HIGHWAY = _fuel['consumption_highway']
TYPICAL_CONSUMPTION_COMBINED = _fuel['consumption_combined']


# ===========================
# PARENTAL BENEFIT CALCULATOR
# ===========================
MATERNITY_BENEFIT_RATE = _parental['maternity_benefit_rate']
MATERNITY_BENEFIT_WEEKS = _parental['maternity_weeks']
MATERNITY_BENEFIT_WEEKS_TWINS = _parental['maternity_weeks_twins']
PARENTAL_BENEFIT_BASIC_MONTHLY = _parental['basic_monthly']
PARENTAL_BENEFIT_BASIC_YEARS = _parental['basic_years']
PARENTAL_BENEFIT_ALT_MONTHLY = _parental['alt_monthly']
PARENTAL_BENEFIT_ALT_YEARS = _parental['alt_years']
PARENTAL_WORK_INCOME_LIMIT_BASIC = _parental['work_income_limit_basic']
PARENTAL_WORK_INCOME_LIMIT_ALT = _parental['work_income_limit_alt']
PARENTAL_MIN_ASSESSMENT_BASE = _parental['min_assessment_base']


# ===========================
# VACATION CALCULATOR (SK labour-law constants)
# ===========================
VACATION_BASE_DAYS = _R['vacation']['base_days']
VACATION_EXTRA_DAYS_FROM_AGE = _R['vacation']['extra_days_from_age']
VACATION_AGE_THRESHOLD = _R['vacation']['age_threshold']


# ===========================
# METADATA
# ===========================
_meta = _R['meta']
CONFIG_VERSION = _meta['version']
CONFIG_LAST_UPDATED = _meta['last_updated']
CONFIG_VALID_FROM = _meta['valid_from']
CONFIG_VALID_UNTIL = _meta['valid_until']


def get_config_info() -> dict:
    """Get configuration metadata (version, validity, description)."""
    return {
        'version': CONFIG_VERSION,
        'last_updated': CONFIG_LAST_UPDATED,
        'valid_from': CONFIG_VALID_FROM,
        'valid_until': CONFIG_VALID_UNTIL,
        'description': f'Slovak Tax & Calculator Configuration ({SK_YEAR})',
    }


def validate_config_year(year: int) -> bool:
    """True if a Slovak dataset for ``year`` exists (i.e. config is valid for it)."""
    from .data import available_years
    return year in available_years('SK')
