#!/usr/bin/env python
"""Test výpočtu superhrubej mzdy"""

from calculators.services.salary_calculator import SalaryCalculator

calc = SalaryCalculator()
result = calc.calculate(gross_salary=2000)

print("="*60)
print("VÝPOČET SUPERHRUBEJ MZDY - 2000 € hrubá")
print("="*60)
print(f"\n💼 Hrubá mzda: {result['gross_salary']:.2f} €")
print(f"\n📊 Odvody zamestnávateľa:")
print(f"   • Celkovo (36.2%):  {result['total_employer_contributions']:.2f} €")
print(f"\n💰 Superhrubá mzda: {result['super_gross_salary']:.2f} €")
print(f"\n💵 Čistá mzda: {result['net_salary']:.2f} €")

print(f"\n" + "="*60)
print(f"PREHĽAD:")
print(f"="*60)
print(f"  Firma zaplatí:     {result['super_gross_salary']:.2f} €")
print(f"  Zamestnanec dostane: {result['net_salary']:.2f} €")
print(f"  Štát zoberie:      {(result['super_gross_salary'] - result['net_salary']):.2f} €")
print(f"\n  % z ceny práce pre štát: {((result['super_gross_salary'] - result['net_salary']) / result['super_gross_salary'] * 100):.1f}%")
print("="*60)
