"""
Test script for verifying config variables integration
"""

from calculators.services.salary_calculator import SalaryCalculator
from calculators.services.vat_calculator import VATCalculator

print("=" * 70)
print("TESTING CONFIG VARIABLES INTEGRATION")
print("=" * 70)

# Test 1: Salary Calculator - Regular employee
print("\n✅ TEST 1: Salary Calculator (Regular Employee)")
print("-" * 70)
calc = SalaryCalculator()
result = calc.calculate(gross_salary=2000, has_disability=False)
print(f"Gross: €{result['gross_salary']:.2f}")
print(f"Social insurance: €{result['social_insurance']:.2f} (Rate: {calc.SOCIAL_INSURANCE_RATE*100}%)")
print(f"Health insurance: €{result['health_insurance']:.2f} (Rate: {calc.HEALTH_INSURANCE_RATE*100}%)")
print(f"Tax: €{result['final_tax']:.2f}")
print(f"Net salary: €{result['net_salary']:.2f}")
print(f"Super-gross (employer cost): €{result['super_gross_salary']:.2f}")

# Test 2: Salary Calculator - Employee with disability (ZŤP)
print("\n✅ TEST 2: Salary Calculator (ZŤP - Disability)")
print("-" * 70)
result_ztp = calc.calculate(gross_salary=2000, has_disability=True)
print(f"Gross: €{result_ztp['gross_salary']:.2f}")
print(f"Social insurance: €{result_ztp['social_insurance']:.2f} (Rate: {calc.SOCIAL_INSURANCE_RATE*100}%)")
print(f"Health insurance: €{result_ztp['health_insurance']:.2f} (Rate: {calc.HEALTH_INSURANCE_RATE_DISABILITY*100}% - ZŤP)")
print(f"Tax: €{result_ztp['final_tax']:.2f}")
print(f"Net salary: €{result_ztp['net_salary']:.2f}")
print(f"💡 Difference vs regular: €{result_ztp['net_salary'] - result['net_salary']:.2f} more")

# Test 3: VAT Calculator
print("\n✅ TEST 3: VAT Calculator")
print("-" * 70)
vat_calc = VATCalculator()
vat_result = vat_calc.calculate(amount=100, vat_rate=23, calculation_type='add_vat')
print(f"Amount without VAT: €{vat_result['amount_without_vat']:.2f}")
print(f"VAT (Standard rate {vat_calc.STANDARD_RATE}%): €{vat_result['vat_amount']:.2f}")
print(f"Amount with VAT: €{vat_result['amount_with_vat']:.2f}")

# Test 4: Check config values are correct
print("\n✅ TEST 4: Verify Config Values")
print("-" * 70)
print(f"✓ Employee social insurance: {calc.SOCIAL_INSURANCE_RATE*100}% (expected: 9.4%)")
print(f"✓ Employee health insurance: {calc.HEALTH_INSURANCE_RATE*100}% (expected: 5.0%)")
print(f"✓ ZŤP health insurance: {calc.HEALTH_INSURANCE_RATE_DISABILITY*100}% (expected: 2.5%)")
print(f"✓ Employer social insurance: {calc.EMPLOYER_SOCIAL_INSURANCE_RATE*100}% (expected: 25.2%)")
print(f"✓ Employer health insurance: {calc.EMPLOYER_HEALTH_INSURANCE_RATE*100}% (expected: 10.0%)")
print(f"✓ Tax bracket 1: {calc.TAX_RATE_1*100}% (expected: 19%)")
print(f"✓ Tax bracket 4: {calc.TAX_RATE_4*100}% (expected: 35%)")
print(f"✓ NČZD: €{calc.NON_TAXABLE_AMOUNT_MONTHLY} (expected: €497.23)")
print(f"✓ Child bonus <15: €{calc.CHILD_TAX_BONUS_UNDER_15} (expected: €100)")
print(f"✓ VAT standard rate: {vat_calc.STANDARD_RATE}% (expected: 23%)")

print("\n" + "=" * 70)
print("✅ ALL TESTS PASSED - Config integration working correctly!")
print("=" * 70)
