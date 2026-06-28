import { Component, Input, forwardRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, NG_VALUE_ACCESSOR, ControlValueAccessor } from '@angular/forms';
import { TranslatePipe } from '../../../i18n/translate.pipe';
import { LocaleService } from '../../../i18n/locale.service';

/**
 * Reusable password field with a show/hide toggle and an optional strength meter.
 * Implements ControlValueAccessor, so it works with both reactive forms
 * (formControlName) and template forms ([(ngModel)]).
 */
@Component({
  selector: 'app-password-input',
  standalone: true,
  imports: [CommonModule, FormsModule, TranslatePipe],
  providers: [{
    provide: NG_VALUE_ACCESSOR,
    useExisting: forwardRef(() => PasswordInputComponent),
    multi: true,
  }],
  template: `
    <div class="pw-wrap">
      <input
        [id]="inputId"
        [type]="show ? 'text' : 'password'"
        class="pw-input form-control"
        [class.is-invalid]="invalid"
        [placeholder]="placeholder"
        [attr.autocomplete]="autocomplete"
        [disabled]="disabled"
        [ngModel]="value"
        (ngModelChange)="update($event)"
        (blur)="onTouched()" />
      <button type="button" class="pw-toggle" (click)="show = !show" tabindex="-1"
              [attr.aria-label]="(show ? 'pw.hide' : 'pw.show') | t"
              [title]="(show ? 'pw.hide' : 'pw.show') | t">
        {{ show ? '🙈' : '👁️' }}
      </button>
    </div>

    <div class="pw-strength" *ngIf="showStrength && value">
      <div class="pw-bar">
        <span class="pw-seg" *ngFor="let i of [1,2,3,4]"
              [class.on]="strength >= i" [attr.data-level]="strength"></span>
      </div>
      <span class="pw-label" [attr.data-level]="strength">{{ strengthKey | t }}</span>
    </div>
  `,
  styles: [`
    .pw-wrap { position: relative; }
    .pw-input {
      width: 100%; box-sizing: border-box;
      border: 1px solid #cbd5e1; border-radius: 10px;
      padding: 11px 42px 11px 13px; font-size: 15px;
    }
    .pw-input:focus { outline: none; border-color: #4f46e5; box-shadow: 0 0 0 3px rgba(79,70,229,.15); }
    .pw-input.is-invalid { border-color: #dc2626; }
    .pw-toggle {
      position: absolute; top: 50%; right: 8px; transform: translateY(-50%);
      background: none; border: none; cursor: pointer; font-size: 1.05rem; line-height: 1;
      padding: 4px;
    }
    .pw-strength { display: flex; align-items: center; gap: 0.5rem; margin: -6px 0 12px; }
    .pw-bar { display: flex; gap: 3px; flex: 1; }
    .pw-seg { height: 5px; flex: 1; border-radius: 3px; background: #e2e8f0; transition: background-color .15s; }
    .pw-seg.on[data-level="1"] { background: #ef4444; }
    .pw-seg.on[data-level="2"] { background: #f59e0b; }
    .pw-seg.on[data-level="3"] { background: #eab308; }
    .pw-seg.on[data-level="4"] { background: #22c55e; }
    .pw-label { font-size: 0.78rem; font-weight: 600; min-width: 70px; text-align: right; }
    .pw-label[data-level="1"] { color: #ef4444; }
    .pw-label[data-level="2"] { color: #f59e0b; }
    .pw-label[data-level="3"] { color: #ca8a04; }
    .pw-label[data-level="4"] { color: #16a34a; }
  `],
})
export class PasswordInputComponent implements ControlValueAccessor {
  @Input() inputId = '';
  @Input() placeholder = '';
  @Input() autocomplete = 'current-password';
  @Input() showStrength = false;
  @Input() invalid = false;

  private locale = inject(LocaleService);

  value = '';
  show = false;
  disabled = false;

  onChange: (v: string) => void = () => {};
  onTouched: () => void = () => {};

  writeValue(v: string): void { this.value = v || ''; }
  registerOnChange(fn: (v: string) => void): void { this.onChange = fn; }
  registerOnTouched(fn: () => void): void { this.onTouched = fn; }
  setDisabledState(d: boolean): void { this.disabled = d; }

  update(v: string): void {
    this.value = v;
    this.onChange(v);
  }

  /** 0–4 score from length + character-class variety. */
  get strength(): number {
    const v = this.value || '';
    if (!v) return 0;
    let score = 0;
    if (v.length >= 8) score++;
    if (v.length >= 12) score++;
    if (/[a-z]/.test(v) && /[A-Z]/.test(v)) score++;
    if (/\d/.test(v) && /[^A-Za-z0-9]/.test(v)) score++;
    return Math.min(4, Math.max(1, score));
  }

  get strengthKey(): string {
    return ['pw.weak', 'pw.weak', 'pw.fair', 'pw.good', 'pw.strong'][this.strength] || 'pw.weak';
  }
}
