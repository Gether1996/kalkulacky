import { Component, PLATFORM_ID, inject, ChangeDetectorRef, OnInit } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { CalculatorService } from '../../services/calculator.service';
import { PercentageCalculationResponse } from '../../models/calculator.models';
import { TranslatePipe } from '../../i18n/translate.pipe';

interface CalculationType {
  id: string;
  label: string;
  description: string;
  icon: string;
}

@Component({
  selector: 'app-percentage-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, TranslatePipe],
  templateUrl: './percentage-calculator.component.html',
  styleUrls: ['./percentage-calculator.component.css']
})
export class PercentageCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  
  calculationTypes: CalculationType[] = [
    {
      id: 'percent_of',
      label: 'X% z Y',
      description: 'Koľko je X% z Y?',
      icon: '➗'
    },
    {
      id: 'is_what_percent',
      label: 'X je koľko % z Y',
      description: 'X je koľko percent z Y?',
      icon: '❓'
    },
    {
      id: 'percentage_change',
      label: 'Percentuálna zmena',
      description: 'Zmena z X na Y v percentách',
      icon: '📊'
    },
    {
      id: 'add_percent',
      label: 'Pridať X%',
      description: 'Pridať X% k Y',
      icon: '➕'
    },
    {
      id: 'subtract_percent',
      label: 'Odčítať X%',
      description: 'Odčítať X% z Y',
      icon: '➖'
    }
  ];
  
  selectedType: string = 'percent_of';
  value1: number = 100;
  value2: number = 200;
  percent: number = 20;
  
  result: PercentageCalculationResponse | null = null;
  loading: boolean = false;
  error: string | null = null;

  constructor(private calculatorService: CalculatorService) {}

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
    }
  }

  selectType(typeId: string): void {
    this.selectedType = typeId;
    this.calculate();
  }

  calculate(): void {
    this.loading = true;
    this.error = null;

    const data: any = {
      calculation_type: this.selectedType
    };

    // Add required fields based on calculation type
    if (['percent_of', 'add_percent', 'subtract_percent'].includes(this.selectedType)) {
      data.percent = this.percent;
      data.value2 = this.value2;
    } else if (['is_what_percent', 'percentage_change'].includes(this.selectedType)) {
      data.value1 = this.value1;
      data.value2 = this.value2;
    }

    this.calculatorService.calculatePercentage(data).subscribe({
      next: (response) => {
        this.result = response;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Percentage calculation error:', err);
        this.error = err.error?.error || 'Chyba pri výpočte';
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }

  needsValue1(): boolean {
    return ['is_what_percent', 'percentage_change'].includes(this.selectedType);
  }

  needsValue2(): boolean {
    return true; // All types need value2
  }

  needsPercent(): boolean {
    return ['percent_of', 'add_percent', 'subtract_percent'].includes(this.selectedType);
  }

  getInputLabel1(): string {
    if (this.selectedType === 'percentage_change') return 'Pôvodná hodnota';
    return 'Hodnota 1';
  }

  getInputLabel2(): string {
    if (this.selectedType === 'percentage_change') return 'Nová hodnota';
    if (this.needsPercent()) return 'Základná hodnota';
    return 'Hodnota 2';
  }

  formatNumber(num: number): string {
    return new Intl.NumberFormat('sk-SK', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(num);
  }

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('sk-SK', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount);
  }

  abs(value: number): number {
    return Math.abs(value);
  }
}
