import { Injectable, PLATFORM_ID, inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import {
  AffiliateOffer,
  CalculatorMonetization,
  LeadSubmission,
} from '../models/monetization.models';
import { getCalculatorMonetization } from '../config/monetization.config';
import { environment } from '../../environments/environment';

interface LeadResponse {
  success: boolean;
  message?: string;
  lead_id?: number;
  errors?: any;
}

@Injectable({ providedIn: 'root' })
export class MonetizationService {
  private platformId = inject(PLATFORM_ID);
  private http = inject(HttpClient);
  private apiUrl: string;

  constructor() {
    this.apiUrl = isPlatformBrowser(this.platformId)
      ? environment.apiUrl
      : 'http://backend:8000/api';
  }

  /** Returns the monetization config (lead/affiliate/ads) for a calculator. */
  getConfig(calculatorType: string): CalculatorMonetization | undefined {
    return getCalculatorMonetization(calculatorType);
  }

  /** Submit a qualified lead. Backend stores it for routing/selling. */
  submitLead(lead: LeadSubmission): Observable<LeadResponse> {
    const payload: LeadSubmission = {
      ...lead,
      source_url: this.currentUrl(),
    };
    return this.http
      .post<LeadResponse>(`${this.apiUrl}/calculators/leads/`, payload, {
        withCredentials: true,
      })
      .pipe(
        catchError((err) =>
          of({
            success: false,
            errors: err?.error?.errors ?? { detail: 'Network error' },
          } as LeadResponse)
        )
      );
  }

  /**
   * Track an outbound affiliate click (fire-and-forget) then let the browser
   * follow the link. Tracking failure must never block the user.
   */
  trackAffiliateClick(offer: AffiliateOffer, calculatorType: string): void {
    if (!isPlatformBrowser(this.platformId)) return;
    this.http
      .post(
        `${this.apiUrl}/calculators/affiliate-click/`,
        {
          partner: offer.partner,
          offer_id: offer.id,
          calculator_type: calculatorType,
          target_url: offer.url,
          source_url: this.currentUrl(),
        },
        { withCredentials: true }
      )
      .pipe(catchError(() => of(null)))
      .subscribe();
  }

  /**
   * Submit a "this data is wrong" report. The backend stores it and emails the
   * operator so real-world figures (tax rates, subsidies, prices) stay correct.
   */
  submitDataReport(report: {
    calculator_type: string;
    message: string;
    reporter_email?: string;
    locale?: string;
  }): Observable<{ success: boolean; message?: string; errors?: any }> {
    const payload = { ...report, page_url: this.currentUrl() };
    return this.http
      .post<{ success: boolean; message?: string; errors?: any }>(
        `${this.apiUrl}/calculators/data-report/`,
        payload,
        { withCredentials: true }
      )
      .pipe(
        catchError((err) =>
          of({
            success: false,
            errors: err?.error?.errors ?? { detail: 'Network error' },
          })
        )
      );
  }

  private currentUrl(): string {
    if (isPlatformBrowser(this.platformId) && typeof window !== 'undefined') {
      return window.location.href;
    }
    return '';
  }
}
