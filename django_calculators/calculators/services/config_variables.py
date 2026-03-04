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
# METADATA
# ===========================

CONFIG_VERSION = "2026.1.0"
CONFIG_LAST_UPDATED = "2026-03-04"
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
