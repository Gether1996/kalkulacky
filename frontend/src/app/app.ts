import { Component, inject, signal, computed } from '@angular/core';
import { RouterOutlet, Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { NavbarComponent } from './components/navbar/navbar.component';
import { TranslatePipe } from './i18n/translate.pipe';
import { LocaleService } from './i18n/locale.service';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, NavbarComponent, TranslatePipe],
  template: `
    @if (showChrome()) {
      <app-navbar />
    }
    @if (showI18nNote()) {
      <div class="i18n-note">{{ 'i18n.skRulesNote' | t }}</div>
    }
    <router-outlet />
  `,
  styles: [],
})
export class App {
  private router = inject(Router);
  private locale = inject(LocaleService);

  // Hide site chrome on embeddable widget routes.
  showChrome = signal(true);
  private isCalcRoute = signal(false);

  // Localized "uses Slovak rules" note — only on calculator pages and only for
  // locales where the Slovak SEO content is hidden (everything except sk/cs).
  showI18nNote = computed(() => {
    const loc = this.locale.locale();
    return this.isCalcRoute() && loc !== 'sk' && loc !== 'cs';
  });

  constructor() {
    const update = (url: string) => {
      this.showChrome.set(!url.startsWith('/embed'));
      this.isCalcRoute.set(url.startsWith('/calculator'));
    };
    update(this.router.url);
    this.router.events
      .pipe(filter((e): e is NavigationEnd => e instanceof NavigationEnd))
      .subscribe((e) => update(e.urlAfterRedirects));
  }
}
