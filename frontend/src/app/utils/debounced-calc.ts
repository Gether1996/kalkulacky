import { Observable, Subject, Subscription, EMPTY } from 'rxjs';
import { debounceTime, switchMap, catchError } from 'rxjs/operators';

/**
 * Shared debounced + cancellable calculation runner for the calculator
 * components. Fixes the per-keystroke API storm (debounce) AND the stale-result
 * race (switchMap cancels an in-flight request when a newer one starts, so a
 * slow earlier response can never overwrite a newer result).
 *
 * Usage in a component:
 *
 *   private calc = new DebouncedCalc(
 *     () => this.calculatorService.calculateX(this.buildRequest()),
 *     (res) => { this.result = res; this.loading = false; this.cdr.detectChanges(); },
 *     (err) => { this.error = 'Chyba pri výpočte'; this.loading = false; this.cdr.detectChanges(); },
 *   );
 *
 *   calculate() {           // called from (ngModelChange) / sliders
 *     // ...synchronous validation, set this.loading = true...
 *     this.calc.trigger();  // debounced; the factory reads the latest inputs
 *   }
 *
 *   ngOnDestroy() { this.calc.destroy(); }
 *
 * The `run` factory is invoked at emit time, so it always reads the component's
 * current field values.
 */
export class DebouncedCalc<T> {
  private trigger$ = new Subject<void>();
  private sub: Subscription;

  constructor(
    run: () => Observable<T>,
    onResult: (result: T) => void,
    onError: (err: unknown) => void,
    debounceMs = 300,
  ) {
    this.sub = this.trigger$
      .pipe(
        debounceTime(debounceMs),
        switchMap(() =>
          run().pipe(
            catchError((err) => {
              onError(err);
              return EMPTY; // swallow so a failed call doesn't kill the stream
            }),
          ),
        ),
      )
      .subscribe((result) => onResult(result));
  }

  /** Queue a (debounced) run using the latest component inputs. */
  trigger(): void {
    this.trigger$.next();
  }

  /** Tear down the subscription — call from ngOnDestroy. */
  destroy(): void {
    this.sub.unsubscribe();
  }
}
