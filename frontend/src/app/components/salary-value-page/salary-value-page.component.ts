import { Component, OnInit, PLATFORM_ID, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { SalaryCalculationResponse } from '../../models/calculator.models';
import { SeoService } from '../../services/seo.service';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';
import { AffiliateCtaComponent } from '../shared/affiliate-cta/affiliate-cta.component';
import { TranslatePipe } from '../../i18n/translate.pipe';

/**
 * Programmatic gross→net landing page (V4 report SEO plan #3): a unique,
 * server-rendered URL per gross amount — "čistá mzda z [suma] eur". These
 * long-tail pages are a large low-competition surface that a single hero
 * calculator can't target. Route: /cista-mzda/:amount.
 */
@Component({
  selector: 'app-salary-value-page',
  standalone: true,
  imports: [CommonModule, RouterLink, AdSlotComponent, AffiliateCtaComponent, TranslatePipe],
  templateUrl: './salary-value-page.component.html',
  styleUrls: ['./salary-value-page.component.css'],
})
export class SalaryValuePageComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  private route = inject(ActivatedRoute);
  private seo = inject(SeoService);
  private calc = inject(CalculatorService);

  gross = 0;
  result: SalaryCalculationResponse | null = null;
  related: number[] = [];

  ngOnInit(): void {
    const raw = this.route.snapshot.paramMap.get('amount') || '0';
    this.gross = Math.max(0, Math.round(parseInt(raw.replace(/\D/g, ''), 10) || 0));

    this.seo.apply({
      title: `Čistá mzda z ${this.gross} € 2026 – koľko dostanete na ruku`,
      description: `Koľko je čistá mzda z hrubej mzdy ${this.gross} € v roku 2026? Presný výpočet odvodov, dane a čistého príjmu podľa slovenských pravidiel 2026.`,
      path: `/cista-mzda/${this.gross}`,
      keywords: `čistá mzda z ${this.gross} eur, ${this.gross} hrubého čistého, výplata ${this.gross}`,
      isCalculator: true,
      faq: [
        {
          question: `Koľko je čistá mzda z ${this.gross} € hrubého v roku 2026?`,
          answer: `Z hrubej mzdy ${this.gross} € sa odpočítajú sociálne (9,4 %) a zdravotné (5 %) odvody zamestnanca a daň z príjmu po uplatnení nezdaniteľnej časti. Presnú čistú mzdu zobrazuje tento výpočet pre rok 2026.`,
        },
      ],
    });

    // Related amounts for internal interlinking (programmatic link graph).
    const step = this.gross >= 2000 ? 200 : 100;
    this.related = [this.gross - 2 * step, this.gross - step, this.gross + step, this.gross + 2 * step]
      .filter(v => v >= 400 && v !== this.gross);

    if (isPlatformBrowser(this.platformId) && this.gross > 0) {
      this.calc.calculateSalary({ gross_salary: this.gross }).subscribe({
        next: (data) => { this.result = data; this.cdr.detectChanges(); },
        error: () => { /* keep SEO shell even if calc fails */ },
      });
    }
  }

  formatCurrency(value: number | null | undefined): string {
    if (value === undefined || value === null || isNaN(value)) return '0 €';
    return value.toLocaleString('sk-SK', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + ' €';
  }
}
