import { Component, PLATFORM_ID, inject, ChangeDetectorRef, OnInit } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CalculatorService } from '../../services/calculator.service';
import { AreaVolumeCalculationResponse, ShapeInfo, AvailableShapes } from '../../models/calculator.models';
import { TranslatePipe } from '../../i18n/translate.pipe';

@Component({
  selector: 'app-area-volume-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslatePipe],
  templateUrl: './area-volume-calculator.component.html',
  styleUrls: ['./area-volume-calculator.component.css']
})
export class AreaVolumeCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private cdr = inject(ChangeDetectorRef);
  
  shapes: AvailableShapes | null = null;
  selectedShape: string = 'rectangle';
  selectedShapeInfo: ShapeInfo | null = null;
  dimensions: { [key: string]: number } = {
    length: 10,
    width: 5
  };

  result: AreaVolumeCalculationResponse | null = null;
  loading: boolean = false;
  error: string | null = null;
  shapesLoading: boolean = true;

  constructor(private calculatorService: CalculatorService) {}

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.loadShapes();
    }
  }

  loadShapes(): void {
    this.shapesLoading = true;
    this.calculatorService.getAvailableShapes()
      .subscribe({
        next: (data) => {
          this.shapes = data;
          this.shapesLoading = false;
          this.selectShape('rectangle');
          this.cdr.detectChanges();
        },
        error: (err) => {
          console.error('❌ Error loading shapes:', err);
          this.error = 'Chyba pri načítaní tvarov';
          this.shapesLoading = false;
          this.cdr.detectChanges();
        }
      });
  }

  selectShape(shapeId: string): void {
    this.selectedShape = shapeId;
    
    // Find shape info
    if (this.shapes) {
      const allShapes = [...this.shapes['2d'], ...this.shapes['3d']];
      this.selectedShapeInfo = allShapes.find(s => s.id === shapeId) || null;
      
      if (this.selectedShapeInfo && this.selectedShapeInfo.dimensions) {
        // Initialize dimensions with default values
        this.dimensions = {};
        this.selectedShapeInfo.dimensions.forEach(dim => {
          this.dimensions[dim] = 10;
        });
      }
    }
    
    this.calculate();
  }

  calculate(): void {
    if (!this.selectedShape || !this.selectedShapeInfo) {
      return;
    }

    // Validate all dimensions are positive
    let valid = true;
    for (const key in this.dimensions) {
      if (this.dimensions[key] <= 0) {
        this.error = 'Všetky rozmery musia byť kladné čísla';
        valid = false;
        break;
      }
    }

    if (!valid) {
      return;
    }

    this.loading = true;
    this.error = null;

    this.calculatorService.calculateAreaVolume({
      shape: this.selectedShape,
      dimensions: this.dimensions
    })
      .subscribe({
        next: (data) => {
          this.result = data;
          this.loading = false;
          this.cdr.detectChanges();
        },
        error: (err) => {
          console.error('❌ Area/volume calculation error:', err);
          this.error = 'Chyba pri výpočte. Skúste znova.';
          this.loading = false;
          this.cdr.detectChanges();
        }
      });
  }

  getDimensionLabel(dimension: string): string {
    if (!this.selectedShapeInfo) return dimension;
    return this.selectedShapeInfo.dimension_labels[dimension] || dimension;
  }

  formatNumber(value: number | undefined): string {
    if (value === undefined || value === null || isNaN(value)) {
      return '0.00';
    }
    return value.toFixed(2);
  }

  getShapesByType(type: string): ShapeInfo[] {
    if (!this.shapes) return [];
    return type === '2d' ? this.shapes['2d'] : this.shapes['3d'];
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
