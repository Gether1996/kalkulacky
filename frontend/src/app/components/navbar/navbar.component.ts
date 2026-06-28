import { Component, OnInit, ElementRef, HostListener, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink, RouterLinkActive, Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { User } from '../../models/auth.models';
import { LanguageSwitcherComponent } from '../shared/language-switcher/language-switcher.component';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { ThemeService } from '../../services/theme.service';
import { FavoritesService } from '../../services/favorites.service';
import { RecentCalculatorsService } from '../../services/recent-calculators.service';
import { CALC_BY_ID, CALCULATOR_REGISTRY, CalcMeta } from '../../config/calculator-registry';

interface Category {
  id: string;
  name: string;
  icon: string;
  calculators: Calculator[];
}

interface Calculator {
  id: string;
  name: string;
  route: string;
  icon: string;
}

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, RouterLinkActive, LanguageSwitcherComponent, TranslatePipe],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  isMenuOpen = false;
  openCategory: string | null = null;
  isUserMenuOpen = false;
  currentUser: User | null = null;

  public theme = inject(ThemeService);
  public favorites = inject(FavoritesService);
  private recent = inject(RecentCalculatorsService);
  private locale = inject(LocaleService);
  private el = inject(ElementRef);

  // Quick search
  searchTerm = '';
  searchOpen = false;

  /** The user's pinned tools, in their chosen order, resolved to route + icon. */
  get favoriteCalcs(): CalcMeta[] {
    return this.favorites.favorites()
      .map(f => CALC_BY_ID[f.calculator_id])
      .filter((c): c is CalcMeta => !!c);
  }

  calcName(id: string): string {
    return this.locale.t('calc.' + id + '.name');
  }

  /** Search matches by localized name; when empty, suggest recent + favourites. */
  get searchResults(): CalcMeta[] {
    const q = this.searchTerm.trim().toLowerCase();
    if (!q) {
      const ids = [...this.recent.recent(), ...this.favorites.favorites().map(f => f.calculator_id)];
      return [...new Set(ids)].slice(0, 6).map(id => CALC_BY_ID[id]).filter((c): c is CalcMeta => !!c);
    }
    return CALCULATOR_REGISTRY
      .filter(c => this.calcName(c.id).toLowerCase().includes(q) || c.id.includes(q))
      .slice(0, 8);
  }

  submitSearch(): void {
    const first = this.searchResults[0];
    if (first) {
      this.router.navigate([first.route]);
      this.closeSearch();
    }
  }

  closeSearch(): void {
    this.searchOpen = false;
    this.searchTerm = '';
  }

  /** Close any open menus when clicking outside the navbar or pressing Escape. */
  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent): void {
    if (!this.el.nativeElement.contains(event.target)) {
      this.openCategory = null;
      this.isUserMenuOpen = false;
      this.searchOpen = false;
    }
  }

  @HostListener('document:keydown.escape')
  onEscape(): void {
    this.openCategory = null;
    this.isUserMenuOpen = false;
    this.searchOpen = false;
    this.isMenuOpen = false;
  }

  categories: Category[] = [
    {
      id: 'financial',
      name: 'Finančné',
      icon: '💰',
      calculators: [
        { id: 'salary', name: 'Čistá mzda', route: '/calculator/salary', icon: '💰' },
        { id: 'mortgage', name: 'Hypotéka', route: '/calculator/mortgage', icon: '🏠' },
        { id: 'vat', name: 'DPH kalkulačka', route: '/calculator/vat', icon: '📊' },
        { id: 'loan', name: 'Kalkulačka úveru', route: '/calculator/loan', icon: '💳' },
        { id: 'payment', name: 'Splátky úveru', route: '/calculator/payment', icon: '💰' },
        { id: 'pension', name: 'Dôchodok', route: '/calculator/pension', icon: '👴' },
        { id: 'freelancer-tax', name: 'Dane SZČO', route: '/calculator/freelancer-tax', icon: '💼' },
        { id: 'inflation', name: 'Inflácia', route: '/calculator/inflation', icon: '📉' },
        { id: 'roi', name: 'ROI Kalkulačka', route: '/calculator/roi', icon: '📊' },
        { id: 'car-leasing', name: 'Lízing auta', route: '/calculator/car-leasing', icon: '🚗' },
        { id: 'car-insurance', name: 'PZP poistenie', route: '/calculator/car-insurance', icon: '🚗' },
        { id: 'savings-goal', name: 'Sporiaci cieľ', route: '/calculator/savings-goal', icon: '🎯' },
        { id: 'sick-leave', name: 'Pracovná neschopnosť (PN)', route: '/calculator/sick-leave', icon: '🏥' }
      ]
    },
    {
      id: 'health',
      name: 'Zdravie',
      icon: '⚕️',
      calculators: [
        { id: 'bmi', name: 'BMI Kalkulačka', route: '/calculator/bmi', icon: '⚖️' },
        { id: 'bmr', name: 'BMR Kalkulačka', route: '/calculator/bmr', icon: '🔥' },
        { id: 'pregnancy', name: 'Tehotenstvo', route: '/calculator/pregnancy', icon: '🤰' },
        { id: 'parental-benefit', name: 'Rodičovský príspevok', route: '/calculator/parental-benefit', icon: '👶' }
      ]
    },
    {
      id: 'lifestyle',
      name: 'Životný štýl',
      icon: '🌟',
      calculators: [
        { id: 'fuel-cost', name: 'Spotreba auta', route: '/calculator/fuel-cost', icon: '⛽' },
        { id: 'percentage', name: 'Percentá', route: '/calculator/percentage', icon: '➗' },
        { id: 'vacation', name: 'Dovolenka', route: '/calculator/vacation', icon: '🏖️' },
        { id: 'solar', name: 'Fotovoltika (dotácia)', route: '/calculator/solar', icon: '☀️' },
        { id: 'heat-pump', name: 'Tepelné čerpadlo', route: '/calculator/heat-pump', icon: '♨️' },
        { id: 'renovation', name: 'Obnov dom (dotácia)', route: '/calculator/renovation', icon: '🏚️' },
        { id: 'energy', name: 'Náklady na energiu', route: '/calculator/energy', icon: '⚡' },
        { id: 'hours-worked', name: 'Odpracované hodiny', route: '/calculator/hours-worked', icon: '⏰' },
        { id: 'split-bill', name: 'Rozdelenie účtu', route: '/calculator/split-bill', icon: '🧾' },
        { id: 'area-volume', name: 'Plocha a objem', route: '/calculator/area-volume', icon: '📐' },
        { id: 'unit-converter', name: 'Prevod jednotiek', route: '/calculator/unit-converter', icon: '🔄' }
      ]
    }
  ];

  constructor(
    private router: Router,
    public authService: AuthService
  ) {}

  ngOnInit() {
    // Subscribe to current user
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });
  }

  toggleMenu() {
    this.isMenuOpen = !this.isMenuOpen;
  }

  toggleCategory(categoryId: string) {
    this.openCategory = this.openCategory === categoryId ? null : categoryId;
  }

  toggleMobileCategory(categoryId: string) {
    this.openCategory = this.openCategory === categoryId ? null : categoryId;
  }

  closeMenu() {
    this.isMenuOpen = false;
    this.openCategory = null;
    this.isUserMenuOpen = false;
  }

  toggleUserMenu() {
    this.isUserMenuOpen = !this.isUserMenuOpen;
  }

  logout() {
    this.authService.logout().subscribe({
      next: () => {
        this.isMenuOpen = false;
        this.isUserMenuOpen = false;
      },
      error: (err) => {
        console.error('Logout failed', err);
        this.isMenuOpen = false;
        this.isUserMenuOpen = false;
      }
    });
  }

  getUserInitials(): string {
    if (!this.currentUser) return '?';
    if (this.currentUser.first_name && this.currentUser.last_name) {
      return (this.currentUser.first_name[0] + this.currentUser.last_name[0]).toUpperCase();
    }
    return this.currentUser.email[0].toUpperCase();
  }

  getUserDisplayName(): string {
    if (!this.currentUser) return '';
    if (this.currentUser.first_name && this.currentUser.last_name) {
      return `${this.currentUser.first_name} ${this.currentUser.last_name}`;
    }
    return this.currentUser.email;
  }

  getCurrentCategory(): string | null {
    const currentUrl = this.router.url;
    
    for (const category of this.categories) {
      const hasActiveCalculator = category.calculators.some(
        calc => currentUrl.includes(calc.route)
      );
      if (hasActiveCalculator) {
        return category.id;
      }
    }
    
    return null;
  }

  isCategoryActive(categoryId: string): boolean {
    return this.getCurrentCategory() === categoryId;
  }
}
