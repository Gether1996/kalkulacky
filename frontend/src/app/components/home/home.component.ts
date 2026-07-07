import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';
import { Router } from '@angular/router';
import { CalculatorCard } from '../../models/calculator.models';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { LocaleService } from '../../i18n/locale.service';
import { FavoritesService } from '../../services/favorites.service';
import { AuthService } from '../../services/auth.service';
import { RecentCalculatorsService } from '../../services/recent-calculators.service';
import { CALC_BY_ID, CalcMeta } from '../../config/calculator-registry';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink, TranslatePipe],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  private locale = inject(LocaleService);
  private router = inject(Router);
  favorites = inject(FavoritesService);
  auth = inject(AuthService);
  recent = inject(RecentCalculatorsService);

  /** Live search term to filter the calculator grid. */
  searchTerm = '';

  /** Recently-visited calculators resolved to route + icon (most recent first). */
  get recentCalcs(): CalcMeta[] {
    return this.recent.recent()
      .map(id => CALC_BY_ID[id])
      .filter((c): c is CalcMeta => !!c);
  }

  calcName(id: string): string {
    return this.locale.t('calc.' + id + '.name');
  }

  /** Star toggle on a card. Stops navigation; sends anon users to login. */
  toggleFavorite(event: Event, calcId: string): void {
    event.preventDefault();
    event.stopPropagation();
    if (!this.auth.isAuthenticated()) {
      this.router.navigate(['/login'], { queryParams: { redirect: '/' } });
      return;
    }
    this.favorites.toggle(calcId);
  }

  /** Calculators matching the search (by localized name + description). */
  get filteredCalculators(): CalculatorCard[] {
    const q = this.searchTerm.trim().toLowerCase();
    if (!q) return this.calculators;
    return this.calculators.filter(c => {
      const name = this.locale.t('calc.' + c.id + '.name').toLowerCase();
      const desc = this.locale.t('calc.' + c.id + '.desc').toLowerCase();
      return name.includes(q) || desc.includes(q) || c.id.includes(q);
    });
  }

  calculators: CalculatorCard[] = [
    {
      id: 'basic',
      title: '🌟 Základná kalkulačka',
      description: 'Klasická vedecká kalkulačka s pokročilými funkciami - percentá, odmocniny, mocniny, pamäť a história výpočtov.',
      icon: '🧮',
      route: '/calculator/basic',
      searchVolume: 15000,
      color: 'from-yellow-400 to-orange-500'
    },
    {
      id: 'unit-converter',
      title: 'Konvertor jednotiek',
      description: 'Rýchla konverzia medzi rôznymi jednotkami - dĺžka, hmotnosť, objem, plocha a teplota. Podporuje 50+ jednotiek.',
      icon: '🔢',
      route: '/calculator/unit-converter',
      searchVolume: 12000,
      color: 'from-purple-400 to-indigo-500'
    },
    {
      id: 'salary',
      title: 'Čistá mzda',
      description: 'Vypočítajte si čistú mzdu zo svojej hrubej mzdy. Zohľadňuje všetky odvody a daňový bonus 2026.',
      icon: '💰',
      route: '/calculator/salary',
      searchVolume: 12000,
      color: 'from-blue-500 to-blue-600'
    },
    {
      id: 'mortgage',
      title: 'Hypotéka',
      description: 'Zistite mesačnú splátku hypotéky a celkové náklady. Obsahuje amortizačnú tabuľku.',
      icon: '🏠',
      route: '/calculator/mortgage',
      searchVolume: 8000,
      color: 'from-green-500 to-green-600'
    },
    {
      id: 'car-leasing',
      title: 'Lízing auta',
      description: 'Porovnanie finančného lízingu, operatívneho lízingu, úveru a kúpy na hotovosti. Zistite najlepší spôsob financovania auta.',
      icon: '🚗',
      route: '/calculator/car-leasing',
      searchVolume: 8000,
      color: 'from-indigo-500 to-purple-600'
    },
    {
      id: 'car-insurance',
      title: 'PZP a havarijné poistenie',
      description: 'Odhad ceny povinného zmluvného poistenia (PZP) a havarijného poistenia auta podľa parametrov vozidla.',
      icon: '🚙',
      route: '/calculator/car-insurance',
      searchVolume: 7000,
      color: 'from-cyan-500 to-blue-600'
    },
    {
      id: 'sick-leave',
      title: 'Pracovná neschopnosť (PN)',
      description: 'Vypočítajte výšku nemocenských dávok pri pracovnej neschopnosti alebo ošetrovaní člena rodiny podľa SK legislatívy.',
      icon: '🏥',
      route: '/calculator/sick-leave',
      searchVolume: 6000,
      color: 'from-green-400 to-emerald-500'
    },
    {
      id: 'vat',
      title: 'DPH kalkulačka',
      description: 'Rýchly výpočet DPH (20%). Prevod medzi sumou s DPH a bez DPH.',
      icon: '📊',
      route: '/calculator/vat',
      searchVolume: 5000,
      color: 'from-purple-500 to-purple-600'
    },
    {
      id: 'loan',
      title: 'Kalkulačka úveru',
      description: 'Vypočítajte si mesačnú splátku úveru, celkové úroky a splátkový kalendár.',
      icon: '💳',
      route: '/calculator/loan',
      searchVolume: 6000,
      color: 'from-orange-500 to-orange-600'
    },
    {
      id: 'car-insurance',
      title: '🚗 PZP – povinné zmluvné poistenie',
      description: 'Orientačná cena PZP podľa výkonu auta, veku vodiča a regiónu. Porovnajte ponuky poisťovní a získajte nezáväznú cenu PZP.',
      icon: '🚗',
      route: '/calculator/car-insurance',
      searchVolume: 9000,
      color: 'from-blue-400 to-sky-500'
    },
    {
      id: 'savings-goal',
      title: '🎯 Sporiaci cieľ',
      description: 'Naplánujte si sporenie: zistite, kedy dosiahnete cieľ alebo koľko mesačne odkladať. Prihlásení používatelia môžu sledovať pokrok a zaznamenávať vklady.',
      icon: '🎯',
      route: '/calculator/savings-goal',
      searchVolume: 6000,
      color: 'from-emerald-400 to-teal-500'
    },
    {
      id: 'fuel-cost',
      title: 'Spotreba auta',
      description: 'Vypočítajte náklady na palivo pre vašu cestu na základe vzdialenosti a spotreby.',
      icon: '⛽',
      route: '/calculator/fuel-cost',
      searchVolume: 3000,
      color: 'from-teal-500 to-teal-600'
    },
    {
      id: 'area-volume',
      title: 'Plocha a objem',
      description: 'Vypočítajte plochu alebo objem geometrických tvarov. Vhodné pre stavbu, záhradu, školu a domácnosť.',
      icon: '📐',
      route: '/calculator/area-volume',
      searchVolume: 3000,
      color: 'from-cyan-500 to-blue-500'
    },
    {
      id: 'split-bill',
      title: 'Rozdelenie účtu',
      description: 'Rozdeľte účet v reštaurácii alebo bare medzi priateľov. Spravodlivo a s prepitným.',
      icon: '🧾',
      route: '/calculator/split-bill',
      searchVolume: 2000,
      color: 'from-amber-500 to-orange-500'
    },
    {
      id: 'bmi',
      title: 'BMI Kalkulačka',
      description: 'Vypočítajte si index telesnej hmotnosti a zistite, či máte zdravú hmotnoť.',
      icon: '⚖️',
      route: '/calculator/bmi',
      searchVolume: 10000,
      color: 'from-pink-500 to-pink-600'
    },
    {
      id: 'percentage',
      title: 'Percentá a výpočty',
      description: 'Všeobecná kalkulačka na percentá - koľko je X% z Y, percentuálna zmena, pripočítanie/odpočítanie percent.',
      icon: '➗',
      route: '/calculator/percentage',
      searchVolume: 4000,
      color: 'from-purple-500 to-indigo-600'
    },
    {
      id: 'pregnancy',
      title: 'Kalkulačka tehotenstva',
      description: 'Vypočítajte termín pôrodu, týždeň tehotenstva a trimester podľa poslednej menštruácie alebo dátumu počatia.',
      icon: '🤰',
      route: '/calculator/pregnancy',
      searchVolume: 5000,
      color: 'from-pink-400 to-rose-500'
    },
    {
      id: 'parental-benefit',
      title: 'Rodičovský príspevok',
      description: 'Vypočítajte materské a rodičovské dávky, porovnajte osnovu vs alternatívu, zistite možnosť pracovať pri rodičovskej.',
      icon: '👶',
      route: '/calculator/parental-benefit',
      searchVolume: 6000,
      color: 'from-purple-400 to-pink-500'
    },
    {
      id: 'pension',
      title: 'Kalkulačka dôchodku',
      description: 'Vypočítajte odhad dôchodku, dôchodké odvody a náhradový pomer podľa slovenskej legislatívy.',
      icon: '💼',
      route: '/calculator/pension',
      searchVolume: 3000,
      color: 'from-blue-500 to-indigo-600'
    },
    {
      id: 'vacation',
      title: 'Kalkulačka dovolenky',
      description: 'Vypočítajte nárok na dovolenku podľa slovenského zákonníka práce - základný nárok plus věkový bonus.',
      icon: '🏖️',
      route: '/calculator/vacation',
      searchVolume: 2000,
      color: 'from-green-400 to-emerald-500'
    },
    {
      id: 'solar',
      title: '☀️ Fotovoltika – dotácia a návratnosť',
      description: 'Vypočítajte dotáciu Zelená domácnostiam, náklady, úsporu a návratnosť fotovoltiky. Získajte nezáväznú ponuku od montážnej firmy.',
      icon: '☀️',
      route: '/calculator/solar',
      searchVolume: 9000,
      color: 'from-amber-400 to-yellow-500'
    },
    {
      id: 'heat-pump',
      title: '♨️ Tepelné čerpadlo – výkon, cena a dotácia',
      description: 'Vypočítajte výkon tepelného čerpadla, cenu, ročnú úsporu oproti plynu či elektrine, dotáciu a návratnosť. Získajte nezáväznú ponuku od montážnej firmy.',
      icon: '♨️',
      route: '/calculator/heat-pump',
      searchVolume: 7000,
      color: 'from-sky-400 to-cyan-500'
    },
    {
      id: 'renovation',
      title: '🏚️ Obnov dom – dotácia na obnovu',
      description: 'Zistite, či máte nárok na dotáciu Obnov dom a koľko môžete získať na zateplenie, okná a zdroj tepla. Sprievodca oprávnenosťou a odhad dotácie.',
      icon: '🏚️',
      route: '/calculator/renovation',
      searchVolume: 6500,
      color: 'from-teal-400 to-emerald-500'
    },
    {
      id: 'energy',
      title: 'Kalkulačka nákladov na energiu',
      description: 'Vypočítajte mesačné a ročné náklady na elektrinu a plyn. Porovnajte svoju spotrebu s priemerom.',
      icon: '⚡',
      route: '/calculator/energy',
      searchVolume: 2000,
      color: 'from-yellow-400 to-orange-500'
    },
    {
      id: 'bmr',
      title: 'BMR Kalkulačka',
      description: 'Vypočítajte bazálny metabolizmus (BMR) a dennú potrebu kalórií podľa váhy, výšky, veku a aktivity.',
      icon: '🔥',
      route: '/calculator/bmr',
      searchVolume: 2000,
      color: 'from-red-400 to-pink-500'
    },
    {
      id: 'payment',
      title: 'Kalkulačka splátok úveru',
      description: 'Vypočítajte mesačnú splátku úveru, celkové náklady a rozdelenie na istinu a úro ky.',
      icon: '💰',
      route: '/calculator/payment',
      searchVolume: 2000,
      color: 'from-green-400 to-emerald-600'
    },
    {
      id: 'freelancer-tax',
      title: 'Kalkulačka daní SZČO',
      description: 'Vypočítajte dane a odvody pre samostatne zárobkovo činné osoby - daň, zdravotné a sociálne poistenie.',
      icon: '💼',
      route: '/calculator/freelancer-tax',
      searchVolume: 1500,
      color: 'from-purple-500 to-violet-600'
    },
    {
      id: 'inflation',
      title: 'Kalkulačka inflácie',
      description: 'Vypočítajte skutočnú hodnotu peňazí v čase s ohľadom na infláciu a kúpnu silu.',
      icon: '📉',
      route: '/calculator/inflation',
      searchVolume: 1500,
      color: 'from-pink-400 to-rose-600'
    },
    {
      id: 'roi',
      title: 'ROI Kalkulačka',
      description: 'Vypočítajte návratnosť investície (ROI), ziskovosť a výkonnosť vašich investícií.',
      icon: '📊',
      route: '/calculator/roi',
      searchVolume: 1000,
      color: 'from-indigo-500 to-purple-600'
    },
    {
      id: 'hours-worked',
      title: 'Kalkulačka odpracovaných hodín',
      description: 'Sledujte pracovné hodiny, nadčasy a výpočet zárobku s príplatkami za víkendy a sviatky.',
      icon: '⏰',
      route: '/calculator/hours-worked',
      searchVolume: 800,
      color: 'from-cyan-500 to-blue-500'
    }
  ];

  getTotalSearchVolume(): number {
    return this.calculators.reduce((sum, calc) => sum + calc.searchVolume, 0);
  }
}
