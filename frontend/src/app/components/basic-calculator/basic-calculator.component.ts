import { Component, OnInit, PLATFORM_ID, inject, HostListener } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TranslatePipe } from '../../i18n/translate.pipe';

interface CalculationHistory {
  expression: string;
  result: string;
  timestamp: Date;
}

@Component({
  selector: 'app-basic-calculator',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslatePipe],
  templateUrl: './basic-calculator.component.html',
  styleUrls: ['./basic-calculator.component.css']
})
export class BasicCalculatorComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  
  // Display values
  display: string = '0';
  previousValue: number = 0;
  currentOperation: string | null = null;
  waitingForOperand: boolean = false;
  
  // Memory
  memory: number = 0;
  
  // History
  history: CalculationHistory[] = [];
  showHistory: boolean = false;
  
  // Error state
  error: boolean = false;

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.loadHistory();
    }
  }

  // Number input
  inputNumber(num: string): void {
    if (this.waitingForOperand || this.display === '0' || this.error) {
      this.display = num;
      this.waitingForOperand = false;
      this.error = false;
    } else {
      this.display = this.display + num;
    }
  }

  // Decimal point
  inputDecimal(): void {
    if (this.waitingForOperand) {
      this.display = '0.';
      this.waitingForOperand = false;
    } else if (this.display.indexOf('.') === -1) {
      this.display = this.display + '.';
    }
  }

  // Clear all
  clear(): void {
    this.display = '0';
    this.previousValue = 0;
    this.currentOperation = null;
    this.waitingForOperand = false;
    this.error = false;
  }

  // Clear entry
  clearEntry(): void {
    this.display = '0';
    this.error = false;
  }

  // Backspace
  backspace(): void {
    if (this.display.length > 1) {
      this.display = this.display.slice(0, -1);
    } else {
      this.display = '0';
    }
  }

  // Change sign
  toggleSign(): void {
    if (this.display !== '0') {
      if (this.display.charAt(0) === '-') {
        this.display = this.display.slice(1);
      } else {
        this.display = '-' + this.display;
      }
    }
  }

  // Operations
  performOperation(nextOperation: string): void {
    const inputValue = parseFloat(this.display);

    if (this.currentOperation && this.waitingForOperand) {
      this.currentOperation = nextOperation;
      return;
    }

    if (this.previousValue === 0) {
      this.previousValue = inputValue;
    } else if (this.currentOperation) {
      const result = this.calculate(this.previousValue, inputValue, this.currentOperation);
      
      if (result === null) {
        this.error = true;
        this.display = 'Error';
        return;
      }
      
      this.display = String(result);
      this.previousValue = result;
    }

    this.waitingForOperand = true;
    this.currentOperation = nextOperation;
  }

  // Calculate result
  private calculate(firstValue: number, secondValue: number, operation: string): number | null {
    try {
      switch (operation) {
        case '+':
          return firstValue + secondValue;
        case '-':
          return firstValue - secondValue;
        case '×':
          return firstValue * secondValue;
        case '÷':
          if (secondValue === 0) {
            return null; // Division by zero
          }
          return firstValue / secondValue;
        default:
          return secondValue;
      }
    } catch (e) {
      return null;
    }
  }

  // Equals
  equals(): void {
    const inputValue = parseFloat(this.display);

    if (this.currentOperation) {
      const expression = `${this.previousValue} ${this.currentOperation} ${inputValue}`;
      const result = this.calculate(this.previousValue, inputValue, this.currentOperation);
      
      if (result === null) {
        this.error = true;
        this.display = 'Error';
        return;
      }
      
      this.display = String(result);
      
      // Add to history
      this.addToHistory(expression, this.display);
      
      this.previousValue = 0;
      this.currentOperation = null;
      this.waitingForOperand = true;
    }
  }

  // Percentage
  percentage(): void {
    const value = parseFloat(this.display);
    if (this.currentOperation && this.previousValue) {
      // Calculate percentage of previous value
      const percent = (this.previousValue * value) / 100;
      this.display = String(percent);
    } else {
      // Convert to percentage
      this.display = String(value / 100);
    }
  }

  // Square root
  squareRoot(): void {
    const value = parseFloat(this.display);
    if (value < 0) {
      this.error = true;
      this.display = 'Error';
      return;
    }
    this.display = String(Math.sqrt(value));
    this.addToHistory(`√${value}`, this.display);
  }

  // Square
  square(): void {
    const value = parseFloat(this.display);
    this.display = String(value * value);
    this.addToHistory(`${value}²`, this.display);
  }

  // Reciprocal
  reciprocal(): void {
    const value = parseFloat(this.display);
    if (value === 0) {
      this.error = true;
      this.display = 'Error';
      return;
    }
    this.display = String(1 / value);
    this.addToHistory(`1/${value}`, this.display);
  }

  // Memory functions
  memoryClear(): void {
    this.memory = 0;
  }

  memoryRecall(): void {
    this.display = String(this.memory);
    this.waitingForOperand = true;
  }

  memoryAdd(): void {
    this.memory += parseFloat(this.display);
    this.waitingForOperand = true;
  }

  memorySubtract(): void {
    this.memory -= parseFloat(this.display);
    this.waitingForOperand = true;
  }

  // History
  private addToHistory(expression: string, result: string): void {
    this.history.unshift({
      expression,
      result,
      timestamp: new Date()
    });
    
    // Keep only last 20 calculations
    if (this.history.length > 20) {
      this.history = this.history.slice(0, 20);
    }
    
    this.saveHistory();
  }

  toggleHistory(): void {
    this.showHistory = !this.showHistory;
  }

  clearHistory(): void {
    this.history = [];
    this.saveHistory();
  }

  useHistoryValue(value: string): void {
    this.display = value;
    this.waitingForOperand = true;
    this.showHistory = false;
  }

  private saveHistory(): void {
    if (isPlatformBrowser(this.platformId)) {
      try {
        localStorage.setItem('calculator-history', JSON.stringify(this.history));
      } catch (e) {
        console.error('Failed to save history', e);
      }
    }
  }

  private loadHistory(): void {
    if (isPlatformBrowser(this.platformId)) {
      try {
        const saved = localStorage.getItem('calculator-history');
        if (saved) {
          this.history = JSON.parse(saved);
        }
      } catch (e) {
        console.error('Failed to load history', e);
      }
    }
  }

  // Keyboard support
  @HostListener('document:keydown', ['$event'])
  handleKeyboard(event: KeyboardEvent): void {
    if (!isPlatformBrowser(this.platformId)) {
      return;
    }

    const key = event.key;
    
    // Numbers
    if (key >= '0' && key <= '9') {
      this.inputNumber(key);
      event.preventDefault();
    }
    
    // Operations
    if (key === '+' || key === '-' || key === '*' || key === '/') {
      const operation = key === '*' ? '×' : key === '/' ? '÷' : key;
      this.performOperation(operation);
      event.preventDefault();
    }
    
    // Decimal
    if (key === '.' || key === ',') {
      this.inputDecimal();
      event.preventDefault();
    }
    
    // Equals
    if (key === 'Enter' || key === '=') {
      this.equals();
      event.preventDefault();
    }
    
    // Clear
    if (key === 'Escape') {
      this.clear();
      event.preventDefault();
    }
    
    // Backspace
    if (key === 'Backspace') {
      this.backspace();
      event.preventDefault();
    }
    
    // Percentage
    if (key === '%') {
      this.percentage();
      event.preventDefault();
    }
  }

  // Format display for better readability
  getFormattedDisplay(): string {
    if (this.error) return this.display;
    
    const value = parseFloat(this.display);
    if (isNaN(value)) return this.display;
    
    // Format large numbers with spaces
    if (Math.abs(value) >= 1000) {
      return value.toLocaleString('sk-SK', { maximumFractionDigits: 8 });
    }
    
    return this.display;
  }
}
