import { Injectable, signal, inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

export type Theme = 'light' | 'dark';

/**
 * Light/dark theme. Persisted in localStorage, falls back to the OS preference.
 * The actual `data-theme` attribute on <html> is set very early by an inline
 * script in index.html (no flash); this service keeps the signal in sync and
 * handles the toggle. SSR-safe (no-op on the server).
 */
@Injectable({ providedIn: 'root' })
export class ThemeService {
  private platformId = inject(PLATFORM_ID);
  readonly theme = signal<Theme>('light');

  constructor() {
    if (isPlatformBrowser(this.platformId)) {
      // Honour what the early inline script already applied, else derive it.
      const current = document.documentElement.getAttribute('data-theme') as Theme | null;
      this.theme.set(current === 'dark' ? 'dark' : 'light');
    }
  }

  toggle(): void {
    this.apply(this.theme() === 'dark' ? 'light' : 'dark');
  }

  set(theme: Theme): void {
    this.apply(theme);
  }

  private apply(theme: Theme): void {
    this.theme.set(theme);
    if (!isPlatformBrowser(this.platformId)) return;
    document.documentElement.setAttribute('data-theme', theme);
    try { localStorage.setItem('kalk_theme', theme); } catch { /* ignore */ }
  }
}
