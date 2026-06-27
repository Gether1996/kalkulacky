"""
Slovak Tax & Calculator Configuration Variables (2026)

Central configuration file for all tax rates, thresholds, and calculator constants.
Update this file annually or when Slovak tax legislation changes.

Last updated: March 2026
"""

from decimal import Decimal


# ===========================
# SALARY CALCULATOR - 2026
# ===========================

# --- EMPLOYEE CONTRIBUTIONS (Odvody zamestnanca) ---
SOCIAL_INSURANCE_RATE_EMPLOYEE = Decimal('0.094')  # 9.4% - Sociálne poistenie
HEALTH_INSURANCE_RATE_EMPLOYEE = Decimal('0.05')   # 5.0% - Zdravotné poistenie (bežný zamestnanec)
HEALTH_INSURANCE_RATE_DISABILITY = Decimal('0.025')  # 2.5% - Zdravotné poistenie (ZŤP - osoba so zdravotným postihnutím)

# Total employee contributions:
# - Regular employee: 14.4% (9.4% + 5.0%)
# - Employee with disability (ZŤP): 11.9% (9.4% + 2.5%)

# --- EMPLOYER CONTRIBUTIONS (Odvody zamestnávateľa) ---
# Simplified: Total employer contributions as single rate
EMPLOYER_CONTRIBUTIONS_RATE = Decimal('0.362')  # 36.2% - Celkové odvody zamestnávateľa (sociálne + zdravotné + úrazové)

# Detailed breakdown (for reference only, not used in calculations):
SOCIAL_INSURANCE_RATE_EMPLOYER = Decimal('0.262')  # 26.2% - Sociálne poistenie (vrátane úrazového)
HEALTH_INSURANCE_RATE_EMPLOYER = Decimal('0.10')   # 10.0% - Zdravotné poistenie

# Total employer contributions: 36.2%
# Super-gross salary = Gross × 1.362

# --- SOCIAL INSURANCE LIMITS ---
SOCIAL_INSURANCE_MAX_BASE_MONTHLY = Decimal('8862')  # €8,862/month - Maximum assessment base for social insurance
SOCIAL_INSURANCE_MAX_BASE_YEARLY = SOCIAL_INSURANCE_MAX_BASE_MONTHLY * 12  # €106,344/year

# --- INCOME TAX - PROGRESSIVE 4-BRACKET SYSTEM (2026) ---
TAX_RATE_BRACKET_1 = Decimal('0.19')  # 19% - First bracket
TAX_RATE_BRACKET_2 = Decimal('0.25')  # 25% - Second bracket
TAX_RATE_BRACKET_3 = Decimal('0.30')  # 30% - Third bracket
TAX_RATE_BRACKET_4 = Decimal('0.35')  # 35% - Fourth bracket (highest)

# Tax bracket thresholds (yearly amounts)
TAX_THRESHOLD_1_YEARLY = Decimal('43983.32')   # Up to €43,983.32/year → 19%
TAX_THRESHOLD_2_YEARLY = Decimal('60349.21')   # Up to €60,349.21/year → 25%
TAX_THRESHOLD_3_YEARLY = Decimal('75010.32')   # Up to €75,010.32/year → 30%
# Above €75,010.32/year → 35%

# Tax bracket thresholds (monthly equivalents)
TAX_THRESHOLD_1_MONTHLY = TAX_THRESHOLD_1_YEARLY / 12  # €3,665.28/month
TAX_THRESHOLD_2_MONTHLY = TAX_THRESHOLD_2_YEARLY / 12  # €5,029.10/month
TAX_THRESHOLD_3_MONTHLY = TAX_THRESHOLD_3_YEARLY / 12  # €6,250.86/month

# --- NON-TAXABLE AMOUNT (Nezdaniteľná časť základu dane - NČZD) ---
NON_TAXABLE_AMOUNT_YEARLY = Decimal('5966.76')    # €5,966.76/year (2026)
NON_TAXABLE_AMOUNT_MONTHLY = Decimal('497.23')    # €497.23/month (2026)

# Non-taxable amount for persons with severe disability (Ťažké zdravotné postihnutie - TP)
# Based on 19.32x životné minimum (life minimum for 2026)
NON_TAXABLE_AMOUNT_DISABILITY_YEARLY = Decimal('59825.28')   # €59,825.28/year
NON_TAXABLE_AMOUNT_DISABILITY_MONTHLY = Decimal('4985.44')   # €4,985.44/month

# --- CHILD TAX BONUS (Daňový bonus na dieťa) - 2026 ---
CHILD_TAX_BONUS_UNDER_15 = Decimal('100.00')  # €100/month for children under 15 years
CHILD_TAX_BONUS_15_TO_18 = Decimal('50.00')   # €50/month for children 15-18 years old

# --- MINIMUM WAGE (Minimálna mzda) - 2026 ---
MINIMUM_WAGE_MONTHLY = Decimal('915')  # €915/month (2026)
MINIMUM_WAGE_HOURLY = Decimal('5.28')  # €5.28/hour (2026)

# --- AVERAGE WAGE (Priemerná mzda) - 2026 estimate ---
AVERAGE_WAGE_MONTHLY = Decimal('1400')  # €1,400/month (estimated for 2026)


# ===========================
# VAT CALCULATOR (DPH) - 2026
# ===========================

# Slovak VAT rates (changed from 1.1.2026)
VAT_RATE_STANDARD = Decimal('23')      # 23% - Základná sadzba (standard rate)
VAT_RATE_REDUCED_1 = Decimal('19')     # 19% - Prvá znížená sadzba (books, medicines, most foods)
VAT_RATE_REDUCED_2 = Decimal('5')      # 5% - Druhá znížená sadzba (selected foods, medical devices)
VAT_RATE_ZERO = Decimal('0')           # 0% - Nulová sadzba (exports, international transport)

# Most commonly used: 23% standard rate


# ===========================
# MORTGAGE CALCULATOR
# ===========================

# No specific constants - all values come from user input
# Typical Slovak mortgage parameters (for reference only):
TYPICAL_MORTGAGE_TERM_YEARS = 25  # years
TYPICAL_INTEREST_RATE_2026 = Decimal('3.5')  # 3.5% (example, varies by bank)
TYPICAL_LTV_RATIO = Decimal('0.80')  # 80% Loan-to-Value ratio


# ===========================
# CAR LEASING CALCULATOR
# ===========================

# Interest rates for leasing and loans (2026 estimates)
LEASING_DEFAULT_INTEREST_RATE = Decimal('0.05')  # 5% - Typical leasing interest rate
LEASING_DEFAULT_LOAN_RATE = Decimal('0.06')  # 6% - Typical car loan interest rate
LEASING_DEFAULT_RESIDUAL_VALUE = Decimal('0.30')  # 30% - Default residual value for operational leasing


# ===========================
# INFLATION CALCULATOR
# ===========================

# Default inflation rate for calculations
DEFAULT_INFLATION_RATE = Decimal('3.0')  # 3% - Average expected inflation rate


# ===========================
# ENERGY CALCULATOR
# ===========================

# Slovak electricity rates (2026 estimates)
ELECTRICITY_RATE_LOW = Decimal('0.15')  # EUR/kWh - Low tariff (night rate)
ELECTRICITY_RATE_HIGH = Decimal('0.20')  # EUR/kWh - High tariff (day rate)
ELECTRICITY_FIXED_MONTHLY = Decimal('8.00')  # EUR/month - Fixed monthly charge

# Slovak gas rates (2026 estimates)
GAS_RATE = Decimal('0.06')  # EUR/kWh - Gas rate
GAS_FIXED_MONTHLY = Decimal('6.00')  # EUR/month - Fixed monthly charge

# Average consumption (Slovakia)
AVG_ELECTRICITY_MONTHLY = Decimal('250')  # kWh/month - Average household electricity consumption
AVG_GAS_MONTHLY = Decimal('500')  # kWh/month - Average household gas consumption


# ===========================
# PENSION CALCULATOR
# ===========================

# Slovak pension system parameters (2026)
RETIREMENT_AGE_MALE = 64  # years - Retirement age for men
RETIREMENT_AGE_FEMALE = 64  # years - Retirement age for women (unified)

# Pension contribution rates (% of gross salary)
PENSION_EMPLOYEE_CONTRIBUTION_RATE = Decimal('4.0')  # 4% - Employee pension contribution
PENSION_EMPLOYER_CONTRIBUTION_RATE = Decimal('14.0')  # 14% - Employer pension contribution
PENSION_TOTAL_CONTRIBUTION_RATE = PENSION_EMPLOYEE_CONTRIBUTION_RATE + PENSION_EMPLOYER_CONTRIBUTION_RATE  # 18%

# Pension system values
AVERAGE_PENSION_SK = Decimal('650.00')  # EUR - Average monthly pension in Slovakia (2026)
PENSION_POINT_VALUE = Decimal('14.50')  # EUR - Value of one pension point
MINIMUM_PENSION_SK = Decimal('370.00')  # EUR - Minimum monthly pension (30+ years of contributions)

# Second pillar (private pension savings)
SECOND_PILLAR_DEFAULT_RATE = Decimal('6.0')  # 6% - Default contribution rate to second pillar

# Life expectancy
LIFE_EXPECTANCY_AFTER_RETIREMENT = 20  # years - Average years in retirement


# ===========================
# SICK LEAVE CALCULATOR (PRACOVNÁ NESCHOPNOSŤ / PN)
# ===========================

# Payment periods and rates (SK: employer pays days 1-10, Sociálna poisťovňa 11+)
SICK_LEAVE_EMPLOYER_PAYMENT_DAYS = 10  # Employer pays the first 10 days
SICK_LEAVE_EMPLOYER_TIER1_DAYS = 3  # Days 1-3 at the lower 25% rate
SICK_LEAVE_EMPLOYER_RATE = Decimal('0.25')  # 25% of DVZ (days 1-3)
SICK_LEAVE_INSURANCE_RATE_ILLNESS = Decimal('0.55')  # 55% of DVZ (days 4-10 employer, 11+ insurer)
SICK_LEAVE_INSURANCE_RATE_CARE = Decimal('0.55')  # 55% for family member care

# Assessment base limits for sick leave (2026)
SICK_LEAVE_MAX_ASSESSMENT_BASE_YEARLY = Decimal('88200')  # €88,200/year
SICK_LEAVE_MAX_ASSESSMENT_BASE_DAILY = SICK_LEAVE_MAX_ASSESSMENT_BASE_YEARLY / 365  # €241.64/day
SICK_LEAVE_MIN_WAGE_MONTHLY = Decimal('750')  # €750/month (2026 estimate)
SICK_LEAVE_MIN_WAGE_DAILY = SICK_LEAVE_MIN_WAGE_MONTHLY * 12 / 365  # Daily minimum


# ===========================
# FREELANCER TAX CALCULATOR (SZČO)
# ===========================

# Income tax rates for freelancers - Progressive 5-bracket system (2026)
FREELANCER_TAX_RATE_1 = Decimal('0.15')  # 15% - First bracket (low incomes)
FREELANCER_TAX_RATE_2 = Decimal('0.19')  # 19% - Second bracket
FREELANCER_TAX_RATE_3 = Decimal('0.25')  # 25% - Third bracket
FREELANCER_TAX_RATE_4 = Decimal('0.30')  # 30% - Fourth bracket
FREELANCER_TAX_RATE_5 = Decimal('0.35')  # 35% - Fifth bracket (high incomes)

# Tax thresholds (annual income) - 2026
FREELANCER_TAX_THRESHOLD_1 = Decimal('20000')  # €20,000/year - Threshold for 15% rate (low income SZČO)
FREELANCER_TAX_THRESHOLD_2 = TAX_THRESHOLD_1_YEARLY  # €43,983.32/year - Same as employees
FREELANCER_TAX_THRESHOLD_3 = TAX_THRESHOLD_2_YEARLY  # €76,553.08/year
FREELANCER_TAX_THRESHOLD_4 = TAX_THRESHOLD_3_YEARLY  # €165,005.40/year

# Health insurance for freelancers
FREELANCER_HEALTH_INSURANCE_RATE = Decimal('0.14')  # 14% - Total health insurance rate for SZČO
FREELANCER_MIN_HEALTH_BASE_MONTHLY = Decimal('570')  # €570/month - Minimum assessment base (2026)

# Social insurance contributions for freelancers (SZČO)
FREELANCER_SOCIAL_SICKNESS_RATE = Decimal('0.014')  # 1.4% - Voluntary sickness insurance
FREELANCER_SOCIAL_PENSION_RATE = Decimal('0.18')  # 18% - Old-age pension insurance
FREELANCER_SOCIAL_DISABILITY_RATE = Decimal('0.06')  # 6% - Disability insurance
FREELANCER_SOCIAL_ACCIDENT_RATE = Decimal('0.008')  # 0.8% - Accident insurance
FREELANCER_SOCIAL_GUARANTEE_RATE = Decimal('0.0025')  # 0.25% - Guarantee insurance
FREELANCER_SOCIAL_RESERVE_RATE = Decimal('0.0475')  # 4.75% - Reserve fund
FREELANCER_MIN_SOCIAL_BASE_MONTHLY = Decimal('570')  # €570/month - Minimum assessment base (2026)

# Flat expense rate
FREELANCER_FLAT_EXPENSE_RATE = Decimal('0.60')  # 60% - Paušálne výdavky (flat expense deduction)

# Non-taxable amount for freelancers (same as employees)
FREELANCER_NON_TAXABLE_AMOUNT_ANNUAL = Decimal('4579.26')  # €4,579.26/year (2026)
FREELANCER_NON_TAXABLE_AMOUNT_MONTHLY = Decimal('381.61')  # €381.61/month


# ===========================
# FUEL COST CALCULATOR
# ===========================

# Typical fuel prices (reference only, user provides actual price)
TYPICAL_FUEL_PRICE_PETROL = Decimal('1.65')  # EUR/liter - Average petrol price (2026 estimate)
TYPICAL_FUEL_PRICE_DIESEL = Decimal('1.55')  # EUR/liter - Average diesel price (2026 estimate)

# Average consumption ranges
TYPICAL_CONSUMPTION_CITY = Decimal('8.0')  # liters/100km - City driving
TYPICAL_CONSUMPTION_HIGHWAY = Decimal('6.0')  # liters/100km - Highway driving
TYPICAL_CONSUMPTION_COMBINED = Decimal('7.0')  # liters/100km - Combined


# ===========================
# PARENTAL BENEFIT CALCULATOR (RODIČOVSKÝ PRÍSPEVOK)
# ===========================

# Maternity benefit (Materské)
MATERNITY_BENEFIT_RATE = Decimal('0.75')  # 75% of daily assessment base (SK materské)
MATERNITY_BENEFIT_WEEKS = 34  # 34 weeks for single child (43 for twins+)
MATERNITY_BENEFIT_WEEKS_TWINS = 43  # 43 weeks for twins or more

# Parental benefit - basic (osnova)
PARENTAL_BENEFIT_BASIC_MONTHLY = Decimal('381.90')  # €381.90/month (2026)
PARENTAL_BENEFIT_BASIC_YEARS = 3  # Until child is 3 years old

# Parental benefit - alternative (alternatíva)
PARENTAL_BENEFIT_ALT_MONTHLY = Decimal('270.00')  # €270.00/month (2026)
PARENTAL_BENEFIT_ALT_YEARS = 6  # Until child is 6 years old

# Work income limits while receiving parental benefit
PARENTAL_WORK_INCOME_LIMIT_BASIC = Decimal('635.70')  # €635.70/month for osnova (2026)
PARENTAL_WORK_INCOME_LIMIT_ALT = Decimal('635.70')  # €635.70/month for alternatíva (2026)

# Minimum assessment base (Minimálny vymeriavací základ)
PARENTAL_MIN_ASSESSMENT_BASE = Decimal('750.00')  # €750/month - Minimum wage 2026


# ===========================
# METADATA
# ===========================

CONFIG_VERSION = "2026.1.0"
CONFIG_LAST_UPDATED = "2026-03-06"
CONFIG_VALID_FROM = "2026-01-01"
CONFIG_VALID_UNTIL = "2026-12-31"

# Data sources:
# - Financial Administration of the Slovak Republic (Finančná správa SR)
# - Social Insurance Agency (Sociálna poisťovňa)
# - Ministry of Finance SR (Ministerstvo financií SR)
# - Act No. 595/2003 Coll. on Income Tax (Zákon o dani z príjmov)
# - Act No. 461/2003 Coll. on Social Insurance (Zákon o sociálnom poistení)


def get_config_info() -> dict:
    """
    Get configuration metadata.
    
    Returns:
        Dictionary with config version, dates, and validity information
    """
    return {
        'version': CONFIG_VERSION,
        'last_updated': CONFIG_LAST_UPDATED,
        'valid_from': CONFIG_VALID_FROM,
        'valid_until': CONFIG_VALID_UNTIL,
        'description': 'Slovak Tax & Calculator Configuration (2026)',
    }


def validate_config_year(year: int) -> bool:
    """
    Check if current configuration is valid for specified year.
    
    Args:
        year: Year to validate (e.g., 2026)
        
    Returns:
        True if config is valid for that year
    """
    return year == 2026


# Helper function to display all rates
def print_all_rates():
    """Print all configured rates for quick reference"""
    print("=" * 60)
    print(f"SLOVAK TAX CONFIGURATION {CONFIG_VERSION}")
    print(f"Valid: {CONFIG_VALID_FROM} to {CONFIG_VALID_UNTIL}")
    print("=" * 60)
    
    print("\n📊 EMPLOYEE CONTRIBUTIONS (Odvody zamestnanca):")
    print(f"   Social Insurance: {float(SOCIAL_INSURANCE_RATE_EMPLOYEE * 100):.1f}%")
    print(f"   Health Insurance (regular): {float(HEALTH_INSURANCE_RATE_EMPLOYEE * 100):.1f}%")
    print(f"   Health Insurance (ZŤP): {float(HEALTH_INSURANCE_RATE_DISABILITY * 100):.1f}%")
    print(f"   → Total (regular): {float((SOCIAL_INSURANCE_RATE_EMPLOYEE + HEALTH_INSURANCE_RATE_EMPLOYEE) * 100):.1f}%")
    print(f"   → Total (ZŤP): {float((SOCIAL_INSURANCE_RATE_EMPLOYEE + HEALTH_INSURANCE_RATE_DISABILITY) * 100):.1f}%")
    
    print("\n🏢 EMPLOYER CONTRIBUTIONS (Odvody zamestnávateľa):")
    print(f"   Social Insurance: {float(SOCIAL_INSURANCE_RATE_EMPLOYER * 100):.1f}%")
    print(f"   Health Insurance: {float(HEALTH_INSURANCE_RATE_EMPLOYER * 100):.1f}%")
    print(f"   → Total: {float((SOCIAL_INSURANCE_RATE_EMPLOYER + HEALTH_INSURANCE_RATE_EMPLOYER) * 100):.1f}%")
    
    print("\n💰 INCOME TAX BRACKETS (Daň z príjmov):")
    print(f"   Bracket 1: {float(TAX_RATE_BRACKET_1 * 100):.0f}% (up to €{float(TAX_THRESHOLD_1_MONTHLY):,.2f}/month)")
    print(f"   Bracket 2: {float(TAX_RATE_BRACKET_2 * 100):.0f}% (up to €{float(TAX_THRESHOLD_2_MONTHLY):,.2f}/month)")
    print(f"   Bracket 3: {float(TAX_RATE_BRACKET_3 * 100):.0f}% (up to €{float(TAX_THRESHOLD_3_MONTHLY):,.2f}/month)")
    print(f"   Bracket 4: {float(TAX_RATE_BRACKET_4 * 100):.0f}% (above €{float(TAX_THRESHOLD_3_MONTHLY):,.2f}/month)")
    
    print("\n🎯 NON-TAXABLE AMOUNT (NČZD):")
    print(f"   Regular: €{float(NON_TAXABLE_AMOUNT_MONTHLY):,.2f}/month")
    print(f"   Disability (TP): €{float(NON_TAXABLE_AMOUNT_DISABILITY_MONTHLY):,.2f}/month")
    
    print("\n👶 CHILD TAX BONUS (Daňový bonus):")
    print(f"   Under 15 years: €{float(CHILD_TAX_BONUS_UNDER_15):,.2f}/month")
    print(f"   15-18 years: €{float(CHILD_TAX_BONUS_15_TO_18):,.2f}/month")
    
    print("\n📈 VAT RATES (DPH):")
    print(f"   Standard: {float(VAT_RATE_STANDARD):.0f}%")
    print(f"   Reduced 1: {float(VAT_RATE_REDUCED_1):.0f}%")
    print(f"   Reduced 2: {float(VAT_RATE_REDUCED_2):.0f}%")
    print(f"   Zero: {float(VAT_RATE_ZERO):.0f}%")
    
    print("\n" + "=" * 60)


if __name__ == '__main__':
    # Display all rates when run directly
    print_all_rates()
    print("\n✅ Configuration loaded successfully!")
    print(f"📅 Config info: {get_config_info()}")
