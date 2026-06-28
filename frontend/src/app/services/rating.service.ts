import { Injectable, PLATFORM_ID, inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface CalculatorRating {
  id: number;
  calculator_id: string;
  rating: number;
  comment: string;
  author: string;
  created_at?: string;
  updated_at?: string;
}

export interface RatingAggregate {
  success: boolean;
  calculator_id: string;
  average: number;
  count: number;
  distribution: Record<string, number>;
  recent: CalculatorRating[];
  my_rating: CalculatorRating | null;
}

export interface RatingSubmitResponse {
  success: boolean;
  data: CalculatorRating;
  average: number;
  count: number;
}

/** Public calculator ratings (1–5 stars + comment). */
@Injectable({ providedIn: 'root' })
export class RatingService {
  private platformId = inject(PLATFORM_ID);
  private http = inject(HttpClient);
  private apiUrl: string;

  constructor() {
    this.apiUrl = isPlatformBrowser(this.platformId)
      ? environment.apiUrl
      : 'http://backend:8000/api';
  }

  getRatings(calculatorId: string): Observable<RatingAggregate> {
    return this.http.get<RatingAggregate>(
      `${this.apiUrl}/calculators/ratings/?calculator_id=${encodeURIComponent(calculatorId)}`,
    );
  }

  submitRating(calculatorId: string, rating: number, comment: string):
    Observable<RatingSubmitResponse> {
    return this.http.post<RatingSubmitResponse>(`${this.apiUrl}/calculators/ratings/`,
      { calculator_id: calculatorId, rating, comment });
  }
}
