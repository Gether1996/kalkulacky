import { Pipe, PipeTransform, inject } from '@angular/core';
import { LocaleService } from './locale.service';

/**
 * Translate pipe: {{ 'nav.home' | t }}
 *
 * Impure so it re-evaluates when the locale signal changes (language switch
 * updates the whole UI without a reload).
 */
@Pipe({ name: 't', standalone: true, pure: false })
export class TranslatePipe implements PipeTransform {
  private locale = inject(LocaleService);

  transform(key: string): string {
    // Touch the signal so the pipe tracks locale changes.
    this.locale.locale();
    return this.locale.t(key);
  }
}
