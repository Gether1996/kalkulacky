from calculators.services.salary_calculator import SalaryCalculator

calc = SalaryCalculator()

print("=" * 70)
print("TEST: VERIFIKÁCIA VÝPOČTU PRE 2000 EUR (podľa príkladu)")
print("=" * 70)
print()

# Test 1: S NČZD (default)
print("1️⃣ S NČZD (štandardný prípad):")
print("-" * 70)
result1 = calc.calculate(2000, 0, 0, apply_nontaxable_amount=True)
print(f"Hrubá mzda:              {result1['gross_salary']:.2f} €")
print(f"Sociálne (9.4%):         {result1['social_insurance']:.2f} €")
print(f"Zdravotné (5%):          {result1['health_insurance']:.2f} €")
print(f"Odvody spolu:            {result1['social_insurance'] + result1['health_insurance']:.2f} € (14.4%)")
print(f"= Daňový základ:         {result1['tax_base']:.2f} €")
print(f"- NČZD:                  {result1['non_taxable_amount']:.2f} €")
print(f"= Zdaniteľný základ:     {result1['taxable_base']:.2f} €")
print(f"Daň (19%):               {result1['income_tax']:.2f} €")
print(f"")
print(f"💰 ČISTÁ MZDA:           {result1['net_salary']:.2f} €")
print()
print("POROVNANIE S PRÍKLADOM:")
print("Očakávané:  Odvody 288 €, Daň 230.81 €, Čistá ≈1481 €")
print(f"Máme:       Odvody {result1['social_insurance'] + result1['health_insurance']:.2f} €, Daň {result1['income_tax']:.2f} €, Čistá {result1['net_salary']:.2f} €")
print()

# Overenie výpočtu
expected_net = 2000 - 288 - 230.81
difference = abs(result1['net_salary'] - expected_net)
if difference < 1:
    print("✅ VÝPOČET JE SPRÁVNY!")
else:
    print(f"⚠️  Odchýlka: {difference:.2f} € (môže byť zaokrúhlenie)")

print()
print("=" * 70)
print()

# Test 2: Bez NČZD (napr. dôchodca)
print("2️⃣ BEZ NČZD (napr. dôchodca, viacero zamestnávateľov):")
print("-" * 70)
result2 = calc.calculate(2000, 0, 0, apply_nontaxable_amount=False)
print(f"Hrubá mzda:              {result2['gross_salary']:.2f} €")
print(f"Odvody (14.4%):          {result2['social_insurance'] + result2['health_insurance']:.2f} €")
print(f"= Daňový základ:         {result2['tax_base']:.2f} €")
print(f"NČZD:                    {result2['non_taxable_amount']:.2f} € (NEUPLATNENÉ)")
print(f"= Zdaniteľný základ:     {result2['taxable_base']:.2f} €")
print(f"Daň (19%):               {result2['income_tax']:.2f} €")
print(f"")
print(f"💰 ČISTÁ MZDA:           {result2['net_salary']:.2f} €")
print()
print(f"Rozdiel oproti štandardu: {result1['net_salary'] - result2['net_salary']:.2f} € (o toľko viac platí daň)")
print()
print("=" * 70)

# Test 3: Minimálna mzda 915 EUR
print()
print("3️⃣ MINIMÁLNA MZDA 2026: 915 EUR")
print("-" * 70)
result3 = calc.calculate(915, 0, 0, apply_nontaxable_amount=True)
print(f"Hrubá:  {result3['gross_salary']:.2f} €")
print(f"Odvody: {result3['social_insurance'] + result3['health_insurance']:.2f} € (14.4%)")
print(f"Daň:    {result3['income_tax']:.2f} € (po NČZD)")
print(f"Čistá:  {result3['net_salary']:.2f} €")
print(f"")
print(f"Percento čistej z hrubej: {result3['net_salary'] / result3['gross_salary'] * 100:.1f}%")
