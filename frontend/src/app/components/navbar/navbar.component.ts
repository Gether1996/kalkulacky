import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink, RouterLinkActive, Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { User } from '../../models/auth.models';
import { LanguageSwitcherComponent } from '../shared/language-switcher/language-switcher.component';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { ThemeService } from '../../services/theme.service';

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
  imports: [CommonModule, RouterLink, RouterLinkActive, LanguageSwitcherComponent, TranslatePipe],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  isMenuOpen = false;
  openCategory: string | null = null;
  isUserMenuOpen = false;
  currentUser: User | null = null;

  public theme = inject(ThemeService);

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
