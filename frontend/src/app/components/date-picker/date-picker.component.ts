import { Component, Input, Output, EventEmitter, forwardRef, HostListener, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ControlValueAccessor, NG_VALUE_ACCESSOR } from '@angular/forms';

interface CalendarDay {
  date: Date;
  day: number;
  isCurrentMonth: boolean;
  isToday: boolean;
  isSelected: boolean;
  isDisabled: boolean;
}

@Component({
  selector: 'app-date-picker',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './date-picker.component.html',
  styleUrls: ['./date-picker.component.css'],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => DatePickerComponent),
      multi: true
    }
  ]
})
export class DatePickerComponent implements ControlValueAccessor {
  @Input() label: string = '';
  @Input() placeholder: string = 'Vyberte dátum';
  @Input() minDate: Date | null = null;
  @Input() maxDate: Date | null = null;
  @Input() required: boolean = false;
  @Output() dateChange = new EventEmitter<string>();

  selectedDate: Date | null = null;
  displayValue: string = '';
  isOpen: boolean = false;
  
  currentMonth: Date = new Date();
  calendarDays: CalendarDay[] = [];
  
  monthNames = [
    'Január', 'Február', 'Marec', 'Apríl', 'Máj', 'Jún',
    'Júl', 'August', 'September', 'Október', 'November', 'December'
  ];
  
  dayNames = ['Po', 'Ut', 'St', 'Št', 'Pi', 'So', 'Ne'];

  private onChange: (value: string | null) => void = () => {};
  private onTouched: () => void = () => {};

  constructor(private elementRef: ElementRef) {
    this.generateCalendar();
  }

  writeValue(value: string | null): void {
    if (value) {
      this.selectedDate = new Date(value);
      this.displayValue = this.formatDate(this.selectedDate);
      this.currentMonth = new Date(this.selectedDate);
    } else {
      this.selectedDate = null;
      this.displayValue = '';
    }
    this.generateCalendar();
  }

  registerOnChange(fn: any): void {
    this.onChange = fn;
  }

  registerOnTouched(fn: any): void {
    this.onTouched = fn;
  }

  toggleCalendar(): void {
    this.isOpen = !this.isOpen;
    if (this.isOpen) {
      this.onTouched();
    }
  }

  closeCalendar(): void {
    this.isOpen = false;
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent): void {
    if (!this.elementRef.nativeElement.contains(event.target)) {
      this.closeCalendar();
    }
  }

  selectDate(day: CalendarDay): void {
    if (day.isDisabled) return;
    
    this.selectedDate = day.date;
    this.displayValue = this.formatDate(this.selectedDate);
    this.isOpen = false;
    
    const dateString = this.selectedDate.toISOString().split('T')[0];
    this.onChange(dateString);
    this.dateChange.emit(dateString);
    this.generateCalendar();
  }

  previousMonth(): void {
    this.currentMonth = new Date(
      this.currentMonth.getFullYear(),
      this.currentMonth.getMonth() - 1,
      1
    );
    this.generateCalendar();
  }

  nextMonth(): void {
    this.currentMonth = new Date(
      this.currentMonth.getFullYear(),
      this.currentMonth.getMonth() + 1,
      1
    );
    this.generateCalendar();
  }

  goToToday(): void {
    const today = new Date();
    this.currentMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    this.generateCalendar();
  }

  generateCalendar(): void {
    const year = this.currentMonth.getFullYear();
    const month = this.currentMonth.getMonth();
    
    const firstDayOfMonth = new Date(year, month, 1);
    const lastDayOfMonth = new Date(year, month + 1, 0);
    
    // Get day of week (0 = Sunday, adjust to Monday = 0)
    let firstDayWeek = firstDayOfMonth.getDay() - 1;
    if (firstDayWeek < 0) firstDayWeek = 6;
    
    const daysInMonth = lastDayOfMonth.getDate();
    const daysInPrevMonth = new Date(year, month, 0).getDate();
    
    this.calendarDays = [];
    
    // Previous month days
    for (let i = firstDayWeek - 1; i >= 0; i--) {
      const date = new Date(year, month - 1, daysInPrevMonth - i);
      this.calendarDays.push(this.createCalendarDay(date, false));
    }
    
    // Current month days
    for (let i = 1; i <= daysInMonth; i++) {
      const date = new Date(year, month, i);
      this.calendarDays.push(this.createCalendarDay(date, true));
    }
    
    // Next month days to fill the grid
    const remainingDays = 42 - this.calendarDays.length;
    for (let i = 1; i <= remainingDays; i++) {
      const date = new Date(year, month + 1, i);
      this.calendarDays.push(this.createCalendarDay(date, false));
    }
  }

  createCalendarDay(date: Date, isCurrentMonth: boolean): CalendarDay {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const dateOnly = new Date(date);
    dateOnly.setHours(0, 0, 0, 0);
    
    const isToday = dateOnly.getTime() === today.getTime();
    const isSelected = this.selectedDate 
      ? dateOnly.getTime() === new Date(this.selectedDate).setHours(0, 0, 0, 0)
      : false;
    
    let isDisabled = false;
    if (this.minDate) {
      const minDateOnly = new Date(this.minDate);
      minDateOnly.setHours(0, 0, 0, 0);
      if (dateOnly < minDateOnly) isDisabled = true;
    }
    if (this.maxDate) {
      const maxDateOnly = new Date(this.maxDate);
      maxDateOnly.setHours(0, 0, 0, 0);
      if (dateOnly > maxDateOnly) isDisabled = true;
    }
    
    return {
      date,
      day: date.getDate(),
      isCurrentMonth,
      isToday,
      isSelected,
      isDisabled
    };
  }

  formatDate(date: Date): string {
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    return `${day}.${month}.${year}`;
  }

  getCurrentMonthYear(): string {
    return `${this.monthNames[this.currentMonth.getMonth()]} ${this.currentMonth.getFullYear()}`;
  }

  clearDate(): void {
    this.selectedDate = null;
    this.displayValue = '';
    this.onChange(null);
    this.dateChange.emit('');
    this.generateCalendar();
  }
}
