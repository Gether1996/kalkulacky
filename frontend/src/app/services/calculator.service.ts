import { Injectable, PLATFORM_ID, inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import {
  SalaryCalculationRequest,
  SalaryCalculationResponse,
  MortgageCalculationRequest,
  MortgageCalculationResponse,
  VATCalculationRequest,
  VATCalculationResponse,
  LoanCalculationRequest,
  LoanCalculationResponse,
  FuelCostCalculationRequest,
  FuelCostCalculationResponse,
  BMICalculationRequest,
  BMICalculationResponse,
  PercentageCalculationRequest,
  PercentageCalculationResponse,
  PregnancyCalculationRequest,
  PregnancyCalculationResponse,
  PensionCalculationRequest,
  PensionCalculationResponse,
  VacationCalculationRequest,
  VacationCalculationResponse,
  EnergyCalculationRequest,
  EnergyCalculationResponse,
  BMRCalculationRequest,
  BMRCalculationResponse,
  PaymentCalculationRequest,
  PaymentCalculationResponse,
  FreelancerTaxCalculationRequest,
  FreelancerTaxCalculationResponse,
  InflationCalculationRequest,
  InflationCalculationResponse,
  ROICalculationRequest,
  ROICalculationResponse,
  HoursWorkedCalculationRequest,
  HoursWorkedCalculationResponse,
  UnitConverterRequest,
  UnitConverterResponse,
  UnitCategory,
  UnitOption,
  SickLeaveCalculationRequest,
  SickLeaveCalculationResponse,
  CarLeasingCalculationRequest,
  CarLeasingCalculationResponse,
  AreaVolumeCalculationRequest,
  AreaVolumeCalculationResponse,
  AvailableShapes,
  SplitBillCalculationRequest,
  SplitBillCalculationResponse,
  TipSuggestionsResponse
} from '../models/calculator.models';

@Injectable({
  providedIn: 'root'
})
export class CalculatorService {
  private platformId = inject(PLATFORM_ID);
  private apiUrl: string;

  constructor(private http: HttpClient) {
    // Use different API URL based on environment
    // In Docker SSR context, use 'backend', otherwise use 'localhost'
    if (isPlatformBrowser(this.platformId)) {
      // Browser: use localhost
      this.apiUrl = 'http://localhost:8000/api';
      console.log('🌐 CalculatorService: Using browser API URL:', this.apiUrl);
    } else {
      // SSR: use Docker service name
      this.apiUrl = 'http://backend:8000/api';
      console.log('🖥️ CalculatorService: Using SSR API URL:', this.apiUrl);
    }
  }

  // Salary Calculator
  calculateSalary(data: SalaryCalculationRequest): Observable<SalaryCalculationResponse> {
    console.log('📤 API Request to:', `${this.apiUrl}/calculators/salary/`, data);
    return this.http.post<{success: boolean, data: SalaryCalculationResponse}>(
      `${this.apiUrl}/calculators/salary/`, data
    ).pipe(map(response => response.data));
  }

  // Mortgage Calculator
  calculateMortgage(data: MortgageCalculationRequest): Observable<MortgageCalculationResponse> {
    return this.http.post<{success: boolean, data: MortgageCalculationResponse}>(
      `${this.apiUrl}/calculators/mortgage/`, data
    ).pipe(map(response => response.data));
  }

  // VAT Calculator
  calculateVAT(data: VATCalculationRequest): Observable<VATCalculationResponse> {
    return this.http.post<{success: boolean, data: VATCalculationResponse}>(
      `${this.apiUrl}/calculators/vat/`, data
    ).pipe(map(response => response.data));
  }

  // Loan Calculator
  calculateLoan(data: LoanCalculationRequest): Observable<LoanCalculationResponse> {
    return this.http.post<{success: boolean, data: LoanCalculationResponse}>(
      `${this.apiUrl}/calculators/loan/`, data
    ).pipe(map(response => response.data));
  }

  // Fuel Cost Calculator
  calculateFuelCost(data: FuelCostCalculationRequest): Observable<FuelCostCalculationResponse> {
    return this.http.post<{success: boolean, data: FuelCostCalculationResponse}>(
      `${this.apiUrl}/calculators/fuel-cost/`, data
    ).pipe(map(response => response.data));
  }

  // BMI Calculator
  calculateBMI(data: BMICalculationRequest): Observable<BMICalculationResponse> {
    return this.http.post<{success: boolean, data: BMICalculationResponse}>(
      `${this.apiUrl}/calculators/bmi/`, data
    ).pipe(map(response => response.data));
  }

  // Percentage/Math Calculator
  calculatePercentage(data: PercentageCalculationRequest): Observable<PercentageCalculationResponse> {
    return this.http.post<{success: boolean, data: PercentageCalculationResponse}>(
      `${this.apiUrl}/calculators/percentage/`, data
    ).pipe(map(response => response.data));
  }

  // Pregnancy Calculator
  calculatePregnancy(data: PregnancyCalculationRequest): Observable<PregnancyCalculationResponse> {
    return this.http.post<{success: boolean, data: PregnancyCalculationResponse}>(
      `${this.apiUrl}/calculators/pregnancy/`, data
    ).pipe(map(response => response.data));
  }

  // Pension Calculator
  calculatePension(data: PensionCalculationRequest): Observable<PensionCalculationResponse> {
    return this.http.post<{success: boolean, data: PensionCalculationResponse}>(
      `${this.apiUrl}/calculators/pension/`, data
    ).pipe(map(response => response.data));
  }

  // Vacation Days Calculator
  calculateVacation(data: VacationCalculationRequest): Observable<VacationCalculationResponse> {
    return this.http.post<{success: boolean, data: VacationCalculationResponse}>(
      `${this.apiUrl}/calculators/vacation/`, data
    ).pipe(map(response => response.data));
  }

  // Energy Cost Calculator
  calculateEnergy(data: EnergyCalculationRequest): Observable<EnergyCalculationResponse> {
    return this.http.post<{success: boolean, data: EnergyCalculationResponse}>(
      `${this.apiUrl}/calculators/energy/`, data
    ).pipe(map(response => response.data));
  }

  // BMR Calculator
  calculateBMR(data: BMRCalculationRequest): Observable<BMRCalculationResponse> {
    return this.http.post<{success: boolean, data: BMRCalculationResponse}>(
      `${this.apiUrl}/calculators/bmr/`, data
    ).pipe(map(response => response.data));
  }

  // Payment Calculator
  calculatePayment(data: PaymentCalculationRequest): Observable<PaymentCalculationResponse> {
    return this.http.post<{success: boolean, data: PaymentCalculationResponse}>(
      `${this.apiUrl}/calculators/payment/`, data
    ).pipe(map(response => response.data));
  }

  calculateFreelancerTax(data: FreelancerTaxCalculationRequest): Observable<FreelancerTaxCalculationResponse> {
    return this.http.post<{success: boolean, data: FreelancerTaxCalculationResponse}>(
      `${this.apiUrl}/calculators/freelancer-tax/`, data
    ).pipe(map(response => response.data));
  }

  calculateInflation(data: InflationCalculationRequest): Observable<InflationCalculationResponse> {
    return this.http.post<{success: boolean, data: InflationCalculationResponse}>(
      `${this.apiUrl}/calculators/inflation/`, data
    ).pipe(map(response => response.data));
  }

  calculateROI(data: ROICalculationRequest): Observable<ROICalculationResponse> {
    return this.http.post<{success: boolean, data: ROICalculationResponse}>(
      `${this.apiUrl}/calculators/roi/`, data
    ).pipe(map(response => response.data));
  }

  calculateHoursWorked(data: HoursWorkedCalculationRequest): Observable<HoursWorkedCalculationResponse> {
    return this.http.post<{success: boolean, data: HoursWorkedCalculationResponse}>(
      `${this.apiUrl}/calculators/hours-worked/`, data
    ).pipe(map(response => response.data));
  }

  // Unit Converter
  convertUnit(data: UnitConverterRequest): Observable<UnitConverterResponse> {
    return this.http.post<{success: boolean, data: UnitConverterResponse}>(
      `${this.apiUrl}/calculators/unit-converter/`, data
    ).pipe(map(response => response.data));
  }

  getUnitCategories(): Observable<UnitCategory[]> {
    return this.http.get<{success: boolean, data: UnitCategory[]}>(
      `${this.apiUrl}/calculators/unit-converter/categories/`
    ).pipe(map(response => response.data));
  }

  getUnitsForCategory(category: string): Observable<UnitOption[]> {
    return this.http.get<{success: boolean, data: UnitOption[]}>(
      `${this.apiUrl}/calculators/unit-converter/units/?category=${category}`
    ).pipe(map(response => response.data));
  }

  // Sick Leave Calculator
  calculateSickLeave(data: SickLeaveCalculationRequest): Observable<SickLeaveCalculationResponse> {
    return this.http.post<{success: boolean, data: SickLeaveCalculationResponse}>(
      `${this.apiUrl}/calculators/sick-leave/`, data
    ).pipe(map(response => response.data));
  }

  // Car Leasing Calculator
  calculateCarLeasing(data: CarLeasingCalculationRequest): Observable<CarLeasingCalculationResponse> {
    return this.http.post<{success: boolean, data: CarLeasingCalculationResponse}>(
      `${this.apiUrl}/calculators/car-leasing/`, data
    ).pipe(map(response => response.data));
  }

  // Area & Volume Calculator
  calculateAreaVolume(data: AreaVolumeCalculationRequest): Observable<AreaVolumeCalculationResponse> {
    return this.http.post<{success: boolean, data: AreaVolumeCalculationResponse}>(
      `${this.apiUrl}/calculators/area-volume/`, data
    ).pipe(map(response => response.data));
  }

  getAvailableShapes(): Observable<AvailableShapes> {
    return this.http.get<{success: boolean, data: AvailableShapes}>(
      `${this.apiUrl}/calculators/area-volume/shapes/`
    ).pipe(map(response => response.data));
  }

  // Split Bill Calculator
  calculateSplitBill(data: SplitBillCalculationRequest): Observable<SplitBillCalculationResponse> {
    return this.http.post<{success: boolean, data: SplitBillCalculationResponse}>(
      `${this.apiUrl}/calculators/split-bill/`, data
    ).pipe(map(response => response.data));
  }

  getTipSuggestions(amount: number): Observable<TipSuggestionsResponse> {
    return this.http.get<{success: boolean, data: TipSuggestionsResponse}>(
      `${this.apiUrl}/calculators/split-bill/tip-suggestions/?amount=${amount}`
    ).pipe(map(response => response.data));
  }
}

