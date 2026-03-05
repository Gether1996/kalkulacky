import { Component, PLATFORM_ID, inject, ChangeDetectorRef, OnInit } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CalculatorService } from '../../services/calculator.service';
import { SplitBillCalculationResponse, TipSuggestionsResponse, BillItem, CustomAmount } from '../../models/calculator.models';

@Component({
  selector: 'app-split-bill-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './split-bill-calculator.component.html',
  styleUrls: ['./split-bill-calculator.component.css']
})
export class SplitBillCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  
  // Make Math accessible in template
  Math = Math;
  
  // Split type
  splitType: 'equal' | 'by_items' | 'custom' = 'equal';
  
  // Equal split
  totalAmount: number = 100;
  numPeople: number = 4;
  tipPercent: number = 10;
  
  // By items split
  items: BillItem[] = [
    { person: 'Osoba 1', amount: 25 },
    { person: 'Osoba 2', amount: 30 }
  ];
  
  // Custom split
  customAmounts: CustomAmount[] = [
    { person: 'Osoba 1', amount: 40 },
    { person: 'Osoba 2', amount: 60 }
  ];

  result: SplitBillCalculationResponse | null = null;
  tipSuggestions: TipSuggestionsResponse | null = null;
  loading: boolean = false;
  error: string | null = null;

  constructor(private calculatorService: CalculatorService) {}

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.calculate();
      this.loadTipSuggestions();
    }
  }

  calculate(): void {
    console.log('🧾 Calculating split bill, type:', this.splitType);
    this.loading = true;
    this.error = null;

    let requestData: any = {
      split_type: this.splitType,
      tip_percent: this.tipPercent
    };

    if (this.splitType === 'equal') {
      if (!this.totalAmount || this.totalAmount <= 0) {
        this.error = 'Zadajte platnú sumu účtu';
        this.loading = false;
        return;
      }
      if (!this.numPeople || this.numPeople < 1) {
        this.error = 'Počet ľudí musí byť aspoň 1';
        this.loading = false;
        return;
      }
      requestData.total_amount = this.totalAmount;
      requestData.num_people = this.numPeople;
    } else if (this.splitType === 'by_items') {
      if (this.items.length < 1) {
        this.error = 'Pridajte aspoň jednu položku';
        this.loading = false;
        return;
      }
      requestData.items = this.items;
    } else if (this.splitType === 'custom') {
      if (this.customAmounts.length < 1) {
        this.error = 'Pridajte aspoň jednu osobu';
        this.loading = false;
        return;
      }
      requestData.custom_amounts = this.customAmounts;
    }

    this.calculatorService.calculateSplitBill(requestData)
      .subscribe({
        next: (data) => {
          console.log('✅ Split bill calculated:', data);
          this.result = data;
          this.loading = false;
          this.cdr.detectChanges();
        },
        error: (err) => {
          console.error('❌ Split bill calculation error:', err);
          this.error = 'Chyba pri výpočte. Skúste znova.';
          this.loading = false;
          this.cdr.detectChanges();
        }
      });
  }

  loadTipSuggestions(): void {
    const amount = this.splitType === 'equal' ? this.totalAmount : this.getTotalFromItems();
    if (amount <= 0) return;

    this.calculatorService.getTipSuggestions(amount)
      .subscribe({
        next: (data) => {
          console.log('✅ Tip suggestions loaded:', data);
          this.tipSuggestions = data;
          this.cdr.detectChanges();
        },
        error: (err) => {
          console.error('❌ Error loading tip suggestions:', err);
        }
      });
  }

  getTotalFromItems(): number {
    if (this.splitType === 'by_items') {
      return this.items.reduce((sum, item) => sum + item.amount, 0);
    } else if (this.splitType === 'custom') {
      return this.customAmounts.reduce((sum, item) => sum + item.amount, 0);
    }
    return this.totalAmount;
  }

  changeSplitType(type: 'equal' | 'by_items' | 'custom'): void {
    this.splitType = type;
    this.calculate();
  }

  addItem(): void {
    const newName = `Osoba ${this.items.length + 1}`;
    this.items.push({ person: newName, amount: 0 });
  }

  removeItem(index: number): void {
    if (this.items.length > 1) {
      this.items.splice(index, 1);
      this.calculate();
    }
  }

  addCustomPerson(): void {
    const newName = `Osoba ${this.customAmounts.length + 1}`;
    this.customAmounts.push({ person: newName, amount: 0 });
  }

  removeCustomPerson(index: number): void {
    if (this.customAmounts.length > 1) {
      this.customAmounts.splice(index, 1);
      this.calculate();
    }
  }

  setTipPercent(percent: number): void {
    this.tipPercent = percent;
    this.calculate();
  }

  formatCurrency(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.00 €';
    }
    return value.toFixed(2) + ' €';
  }

  formatPercentage(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0%';
    }
    return value.toFixed(0) + '%';
  }

  scrollToResults(): void {
    if (isPlatformBrowser(this.platformId)) {
      const element = document.getElementById('results');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  }
}
