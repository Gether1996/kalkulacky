from calculators.services.salary_calculator import SalaryCalculator

calc = SalaryCalculator()

# Test 1: Minimálna mzda 2026 = 915 EUR
print("=" * 70)
print("TEST 1: MINIMÁLNA MZDA 2026 = 915 EUR")
print("=" * 70)
result = calc.calculate(915, 0, 0)
print(f"Hrubá mzda:         {result['gross_salary']:.2f} €")
print(f"Sociálne poistenie: {result['social_insurance']:.2f} € ({calc.SOCIAL_INSURANCE_RATE*100}%)")
print(f"Zdravotné poistenie:{result['health_insurance']:.2f} € ({calc.HEALTH_INSURANCE_RATE*100}%)")
print(f"Celkové odvody:     {result['social_insurance'] + result['health_insurance']:.2f} € ({(result['social_insurance'] + result['health_insurance'])/result['gross_salary']*100:.2f}%)")
print(f"Čistá mzda:         {result['net_salary']:.2f} €")
print()
print("POROVNANIE S TEXTOM:")
print("Text hovorí: 728,90 EUR čistá pri 915 EUR hrubej")
print(f"Máme:        {result['net_salary']:.2f} EUR")
print(f"Rozdiel:     {728.90 - result['net_salary']:.2f} EUR")
print()

# Test 2: Overenie odvodov
print("=" * 70)
print("TEST 2: ANALÝZA ODVODOV")
print("=" * 70)
result2 = calc.calculate(2000, 0, 0)
total_insurance = result2['social_insurance'] + result2['health_insurance']
insurance_percent = (total_insurance / result2['gross_salary']) * 100
print(f"Hrubá mzda:         {result2['gross_salary']:.2f} €")
print(f"Sociálne:           {result2['social_insurance']:.2f} € ({calc.SOCIAL_INSURANCE_RATE*100}%)")
print(f"Zdravotné:          {result2['health_insurance']:.2f} € ({calc.HEALTH_INSURANCE_RATE*100}%)")
print(f"Celkové odvody:     {total_insurance:.2f} € ({insurance_percent:.2f}%)")
print()
print("ČO HOVORÍ TEXT:")
print("'tie sú u klasického zamestnanca spolu 14,4 % z hrubej mzdy'")
print()
print("PROBLÉM:")
if insurance_percent > 14.5:
    print(f"❌ MÁME {insurance_percent:.1f}% namiesto 14.4%!")
    print(f"❌ ROZDIEL: {insurance_percent - 14.4:.1f} percentuálnych bodov")
else:
    print("✓ Odvody sú správne")
