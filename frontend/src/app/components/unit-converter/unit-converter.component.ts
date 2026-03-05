import { Component, OnInit, PLATFORM_ID, inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CalculatorService } from '../../services/calculator.service';
import { UnitCategory, UnitOption, UnitConverterResponse } from '../../models/calculator.models';

@Component({
  selector: 'app-unit-converter',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './unit-converter.component.html',
  styleUrls: ['./unit-converter.component.css']
})
export class UnitConverterComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);

  // Form fields
  category: string = 'length';
  fromUnit: string = 'meter';
  toUnit: string = 'kilometer';
  value: number = 1;

  // Categories and units
  categories: UnitCategory[] = [];
  availableUnits: UnitOption[] = [];

  // Result
  result: UnitConverterResponse | null = null;
  isLoading: boolean = false;
  error: string = '';

  constructor(private calculatorService: CalculatorService) {}

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {
      this.loadCategories();
    }
  }

  loadCategories() {
    this.calculatorService.getUnitCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
        if (categories.length > 0 && !this.category) {
          this.category = categories[0].value;
        }
        this.onCategoryChange();
      },
      error: (err) => {
        console.error('Error loading categories:', err);
        this.error = 'Nepodarilo sa načítať kategórie jednotiek';
      }
    });
  }

  onCategoryChange() {
    this.calculatorService.getUnitsForCategory(this.category).subscribe({
      next: (units) => {
        this.availableUnits = units;
        
        // Set default units based on category
        if (units.length > 0) {
          // Set from_unit to first unit
          this.fromUnit = units[0].value;
          
          // Set to_unit to second unit if available, otherwise same as from_unit
          this.toUnit = units.length > 1 ? units[1].value : units[0].value;
        }
        
        // Auto-calculate with new category
        this.calculate();
      },
      error: (err) => {
        console.error('Error loading units:', err);
        this.error = 'Nepodarilo sa načítať jednotky pre túto kategóriu';
      }
    });
  }

  calculate() {
    if (!this.value || !this.fromUnit || !this.toUnit || !this.category) {
      return;
    }

    this.isLoading = true;
    this.error = '';

    this.calculatorService.convertUnit({
      value: this.value,
      from_unit: this.fromUnit,
      to_unit: this.toUnit,
      category: this.category
    }).subscribe({
      next: (response) => {
        this.result = response;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Calculation error:', err);
        this.error = err.error?.error || 'Nastala chyba pri výpočte. Skúste to znova.';
        this.isLoading = false;
        this.result = null;
      }
    });
  }

  swapUnits() {
    // Swap from_unit and to_unit
    const temp = this.fromUnit;
    this.fromUnit = this.toUnit;
    this.toUnit = temp;
    
    // If we have a result, use the result value as the new input
    if (this.result) {
      this.value = this.result.result;
    }
    
    this.calculate();
  }

  getCategoryIcon(categoryValue: string): string {
    const icons: {[key: string]: string} = {
      'length': '📏',
      'weight': '⚖️',
      'volume': '🧪',
      'area': '📐',
      'temperature': '🌡️'
    };
    return icons[categoryValue] || '🔢';
  }

  resetForm() {
    this.value = 1;
    this.result = null;
    this.error = '';
    
    // Reset to default units for current category
    if (this.availableUnits.length > 0) {
      this.fromUnit = this.availableUnits[0].value;
      this.toUnit = this.availableUnits.length > 1 ? this.availableUnits[1].value : this.availableUnits[0].value;
    }
    
    this.calculate();
  }

  // Common conversions for quick access
  getCommonConversions(): Array<{from: string, to: string, category: string, label: string}> {
    return [
      { from: 'kilometer', to: 'mile', category: 'length', label: 'km → míle' },
      { from: 'meter', to: 'foot', category: 'length', label: 'm → stopy' },
      { from: 'kilogram', to: 'pound', category: 'weight', label: 'kg → libry' },
      { from: 'celsius', to: 'fahrenheit', category: 'temperature', label: '°C → °F' },
      { from: 'liter', to: 'gallon_us', category: 'volume', label: 'l → galóny' },
      { from: 'square_meter', to: 'square_foot', category: 'area', label: 'm² → ft²' }
    ];
  }

  useCommonConversion(conv: {from: string, to: string, category: string}) {
    this.category = conv.category;
    this.onCategoryChange();
    
    // Wait a bit for units to load, then set them
    setTimeout(() => {
      this.fromUnit = conv.from;
      this.toUnit = conv.to;
      this.calculate();
    }, 100);
  }
}
