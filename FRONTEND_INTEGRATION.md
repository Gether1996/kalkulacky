# Frontend Integration Guide - Notification & Tracking System

## API Endpoints

### 1. Uložiť výpočet s trackingom

**POST** `/api/saved-calculations/`

**Request Body:**
```json
{
  "session_key": "string",              // Required: Browser session ID
  "email": "user@example.com",          // Optional: Email pre notifikácie
  "calculator_type": "pregnancy",       // Required: pregnancy|vacation|mortgage|loan
  "name": "Moje tehotenstvo",          // Required: Názov výpočtu
  "params": {                           // Required: Input parameters
    "calculation_method": "lmp",
    "lmp_date": "2025-11-01",
    "current_date": "2026-03-06"
  },
  "result": {                           // Required: Calculation result
    "due_date": "2026-09-18",
    "current_week": 12,
    ...
  },
  "is_tracking": true,                  // Required: Enable tracking
  "notification_enabled": true          // Required: Enable notifications
}
```

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "session_key": "string",
    "email": "user@example.com",
    "calculator_type": "pregnancy",
    "name": "Moje tehotenstvo",
    "params": {...},
    "result": {...},
    "is_tracking": true,
    "is_favorite": false,
    "notification_enabled": true,
    "created_at": "2026-03-06T14:00:00Z",
    "last_accessed": "2026-03-06T14:00:00Z",
    "access_count": 0
  }
}
```

**Response (Error):**
```json
{
  "success": false,
  "errors": {
    "email": ["Enter a valid email address."]
  }
}
```

---

### 2. Získať všetky uložené výpočty

**GET** `/api/saved-calculations/?session_key={session_key}`

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "calculator_type": "pregnancy",
      "name": "Moje tehotenstvo",
      "is_tracking": true,
      "notification_enabled": true,
      "created_at": "2026-03-06T14:00:00Z",
      ...
    }
  ],
  "count": 1
}
```

---

### 3. Získať detail výpočtu

**GET** `/api/saved-calculations/{id}/`

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "calculator_type": "pregnancy",
    "name": "Moje tehotenstvo",
    "params": {...},
    "result": {...},
    "is_tracking": true,
    "notification_enabled": true,
    "access_count": 5,
    ...
  }
}
```

---

### 4. Aktualizovať výpočet

**PUT** `/api/saved-calculations/{id}/`

**Request Body (partial update):**
```json
{
  "name": "Updated name",
  "is_tracking": false,
  "notification_enabled": false
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Updated name",
    "is_tracking": false,
    ...
  }
}
```

---

### 5. Vymazať výpočet

**DELETE** `/api/saved-calculations/{id}/`

**Response:**
```json
{
  "success": true,
  "message": "Výpočet bol úspešne vymazaný"
}
```

---

### 6. Zapnúť tracking pre existujúci výpočet

**POST** `/api/saved-calculations/{id}/enable-tracking/`

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Tracking bol zapnutý. Bolo vytvorených 47 notifikácií.",
  "notifications_count": 47
}
```

---

## Angular Service Implementation

### `saved-calculations.service.ts`

```typescript
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface SavedCalculation {
  id?: number;
  session_key: string;
  email?: string;
  calculator_type: 'pregnancy' | 'vacation' | 'mortgage' | 'loan';
  name: string;
  params: any;
  result: any;
  is_tracking: boolean;
  is_favorite?: boolean;
  notification_enabled: boolean;
  created_at?: string;
  last_accessed?: string;
  access_count?: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  errors?: any;
  count?: number;
  message?: string;
}

@Injectable({
  providedIn: 'root'
})
export class SavedCalculationsService {
  private apiUrl = 'http://localhost:8000/api/saved-calculations';

  constructor(private http: HttpClient) {}

  /**
   * Get or generate session key for anonymous users
   */
  private getSessionKey(): string {
    let sessionKey = localStorage.getItem('kalkulacky_session_key');
    
    if (!sessionKey) {
      sessionKey = this.generateSessionKey();
      localStorage.setItem('kalkulacky_session_key', sessionKey);
    }
    
    return sessionKey;
  }

  /**
   * Generate unique session key
   */
  private generateSessionKey(): string {
    return `sess_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * Save calculation with tracking
   */
  saveCalculation(
    calculatorType: string,
    name: string,
    params: any,
    result: any,
    enableTracking: boolean = false,
    email?: string
  ): Observable<ApiResponse<SavedCalculation>> {
    const data: SavedCalculation = {
      session_key: this.getSessionKey(),
      calculator_type: calculatorType as any,
      name,
      params,
      result,
      is_tracking: enableTracking,
      notification_enabled: enableTracking,
      email: email || undefined
    };

    return this.http.post<ApiResponse<SavedCalculation>>(this.apiUrl + '/', data);
  }

  /**
   * Get all saved calculations for current session
   */
  getCalculations(): Observable<ApiResponse<SavedCalculation[]>> {
    const sessionKey = this.getSessionKey();
    return this.http.get<ApiResponse<SavedCalculation[]>>(
      `${this.apiUrl}/?session_key=${sessionKey}`
    );
  }

  /**
   * Get calculation by ID
   */
  getCalculation(id: number): Observable<ApiResponse<SavedCalculation>> {
    return this.http.get<ApiResponse<SavedCalculation>>(`${this.apiUrl}/${id}/`);
  }

  /**
   * Update calculation
   */
  updateCalculation(
    id: number,
    updates: Partial<SavedCalculation>
  ): Observable<ApiResponse<SavedCalculation>> {
    return this.http.put<ApiResponse<SavedCalculation>>(
      `${this.apiUrl}/${id}/`,
      updates
    );
  }

  /**
   * Delete calculation
   */
  deleteCalculation(id: number): Observable<ApiResponse<any>> {
    return this.http.delete<ApiResponse<any>>(`${this.apiUrl}/${id}/`);
  }

  /**
   * Enable tracking for existing calculation
   */
  enableTracking(id: number, email: string): Observable<ApiResponse<any>> {
    return this.http.post<ApiResponse<any>>(
      `${this.apiUrl}/${id}/enable-tracking/`,
      { email }
    );
  }
}
```

---

## Component Implementation Examples

### Pregnancy Calculator - Save with Tracking

```typescript
// pregnancy-calculator.component.ts
import { Component } from '@angular/core';
import { SavedCalculationsService } from '../../services/saved-calculations.service';

@Component({
  selector: 'app-pregnancy-calculator',
  templateUrl: './pregnancy-calculator.component.html'
})
export class PregnancyCalculatorComponent {
  result: any = null;
  params: any = {};
  showSaveDialog = false;
  saveName = '';
  saveEmail = '';
  enableTracking = false;
  saveSuccess = false;
  saveError = '';

  constructor(private savedCalcService: SavedCalculationsService) {}

  /**
   * Calculate pregnancy
   */
  calculate() {
    // ... calculation logic ...
    this.result = {
      due_date: '2026-09-18',
      current_week: 12,
      // ... other results
    };
  }

  /**
   * Show save dialog
   */
  showSave() {
    this.showSaveDialog = true;
    this.saveName = `Moje tehotenstvo - ${new Date().toLocaleDateString('sk')}`;
  }

  /**
   * Save calculation
   */
  saveCalculation() {
    if (!this.saveName) {
      this.saveError = 'Zadajte názov výpočtu';
      return;
    }

    if (this.enableTracking && !this.saveEmail) {
      this.saveError = 'Pre notifikácie je potrebný email';
      return;
    }

    this.savedCalcService.saveCalculation(
      'pregnancy',
      this.saveName,
      this.params,
      this.result,
      this.enableTracking,
      this.saveEmail
    ).subscribe({
      next: (response) => {
        if (response.success) {
          this.saveSuccess = true;
          this.showSaveDialog = false;
          
          if (this.enableTracking) {
            alert(`Výpočet uložený! Budete dostávať týždenné notifikácie na ${this.saveEmail}`);
          } else {
            alert('Výpočet bol úspešne uložený!');
          }
        } else {
          this.saveError = response.error || 'Chyba pri ukladaní';
        }
      },
      error: (err) => {
        this.saveError = 'Chyba pri ukladaní výpočtu';
        console.error(err);
      }
    });
  }
}
```

### HTML Template

```html
<!-- pregnancy-calculator.component.html -->

<!-- Calculation Form -->
<div class="calculator-form">
  <!-- ... input fields ... -->
  
  <button (click)="calculate()" class="btn-calculate">
    Vypočítať
  </button>
</div>

<!-- Results -->
<div *ngIf="result" class="results">
  <h2>Výsledok</h2>
  <p>Termín pôrodu: {{ result.due_date }}</p>
  <p>Aktuálny týždeň: {{ result.current_week }}</p>
  
  <button (click)="showSave()" class="btn-save">
    💾 Uložiť výpočet
  </button>
</div>

<!-- Save Dialog -->
<div *ngIf="showSaveDialog" class="save-dialog">
  <h3>Uložiť výpočet</h3>
  
  <label>
    Názov:
    <input [(ngModel)]="saveName" type="text" placeholder="Moje tehotenstvo">
  </label>
  
  <label>
    <input [(ngModel)]="enableTracking" type="checkbox">
    Zapnúť notifikácie (týždenné updaty)
  </label>
  
  <label *ngIf="enableTracking">
    Email:
    <input [(ngModel)]="saveEmail" type="email" placeholder="vas@email.com">
    <small>Budete dostávať týždenné emailové notifikácie o vývoji tehotenstva</small>
  </label>
  
  <div *ngIf="saveError" class="error">{{ saveError }}</div>
  
  <button (click)="saveCalculation()" class="btn-primary">Uložiť</button>
  <button (click)="showSaveDialog = false" class="btn-secondary">Zrušiť</button>
</div>
```

---

## Saved Calculations List Component

```typescript
// saved-calculations-list.component.ts
import { Component, OnInit } from '@angular/core';
import { SavedCalculationsService, SavedCalculation } from '../../services/saved-calculations.service';

@Component({
  selector: 'app-saved-calculations-list',
  templateUrl: './saved-calculations-list.component.html'
})
export class SavedCalculationsListComponent implements OnInit {
  calculations: SavedCalculation[] = [];
  loading = true;

  constructor(private savedCalcService: SavedCalculationsService) {}

  ngOnInit() {
    this.loadCalculations();
  }

  loadCalculations() {
    this.loading = true;
    this.savedCalcService.getCalculations().subscribe({
      next: (response) => {
        if (response.success && response.data) {
          this.calculations = response.data;
        }
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading calculations:', err);
        this.loading = false;
      }
    });
  }

  deleteCalculation(id: number) {
    if (!confirm('Naozaj chcete vymazať tento výpočet?')) {
      return;
    }

    this.savedCalcService.deleteCalculation(id).subscribe({
      next: () => {
        this.loadCalculations();
        alert('Výpočet bol vymazaný');
      },
      error: (err) => {
        console.error('Error deleting calculation:', err);
        alert('Chyba pri mazaní výpočtu');
      }
    });
  }

  toggleTracking(calc: SavedCalculation) {
    if (!calc.id) return;

    const newValue = !calc.is_tracking;
    
    if (newValue && !calc.email) {
      const email = prompt('Zadajte email pre notifikácie:');
      if (!email) return;
      
      this.savedCalcService.enableTracking(calc.id, email).subscribe({
        next: () => {
          this.loadCalculations();
          alert('Tracking bol zapnutý!');
        },
        error: (err) => {
          console.error('Error enabling tracking:', err);
        }
      });
    } else {
      this.savedCalcService.updateCalculation(calc.id, {
        is_tracking: newValue,
        notification_enabled: newValue
      }).subscribe({
        next: () => {
          this.loadCalculations();
        },
        error: (err) => {
          console.error('Error updating tracking:', err);
        }
      });
    }
  }
}
```

---

## Best Practices

### 1. Session Management
- Používajte `localStorage` pre session_key
- Vygenerujte session_key pri prvom použití
- Session ostáva konzistentný naprieč reloadami

### 2. Error Handling
- Vždy kontrolujte `success` flag v odpovedi
- Zobrazujte užívateľsky prívetivé chybové hlášky
- Logujte chyby do konzoly pre debugging

### 3. Email Validation
- Validujte email na frontende pred odoslaním
- Používajte HTML5 email input type
- Zobrazujte jasné inštrukcie o notifikáciách

### 4. UX Tips
- Ukážte počet vygenerovaných notifikácií
- Vysvetlite čo znamená "tracking" (týždenné emaily, atď.)
- Umožnite preview emailu pred zapnutím trackingu
- Pridajte FAQ o notifikáciách

### 5. Performance
- Cache-ujte saved calculations lokálne
- Používajte debounce pri auto-save
- Lazy load-ujte zoznam výpočtov

---

## Testing

```typescript
// saved-calculations.service.spec.ts
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { SavedCalculationsService } from './saved-calculations.service';

describe('SavedCalculationsService', () => {
  let service: SavedCalculationsService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [SavedCalculationsService]
    });
    
    service = TestBed.inject(SavedCalculationsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should save calculation with tracking', () => {
    const mockResponse = {
      success: true,
      data: { id: 1, name: 'Test' }
    };

    service.saveCalculation(
      'pregnancy',
      'Test',
      {},
      {},
      true,
      'test@example.com'
    ).subscribe(response => {
      expect(response.success).toBe(true);
      expect(response.data?.id).toBe(1);
    });

    const req = httpMock.expectOne('http://localhost:8000/api/saved-calculations/');
    expect(req.request.method).toBe('POST');
    expect(req.request.body.is_tracking).toBe(true);
    req.flush(mockResponse);
  });

  afterEach(() => {
    httpMock.verify();
  });
});
```

---

## Troubleshooting

### CORS Issues
Ak máte CORS problémy, skontrolujte `settings.py`:
```python
CORS_ALLOW_ALL_ORIGINS = True  # Development only
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
]
```

### API URL
Pre production zmeňte API URL:
```typescript
private apiUrl = environment.apiUrl + '/api/saved-calculations';
```

### Session Key Issues
Ak sa calculations nezobrazujú, skontrolujte session_key v localStorage:
```javascript
console.log(localStorage.getItem('kalkulacky_session_key'));
```

---

## Next Steps

1. Implementujte service vo vašej Angular aplikácii
2. Pridajte "Save" button na kalkulačky
3. Vytvorte stránku "Moje výpočty" so zoznamom
4. Otestujte tracking na testovacích emailoch
5. Nasaďte na production s SMTP backend-om

Pre otázky kontaktujte development team!
