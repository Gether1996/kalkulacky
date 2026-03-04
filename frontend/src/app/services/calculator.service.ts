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
  VATCalculationResponse
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
}
