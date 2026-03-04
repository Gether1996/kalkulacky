import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { CalculatorCard } from '../../models/calculator.models';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  calculators: CalculatorCard[] = [
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
      id: 'vat',
      title: 'DPH kalkulačka',
      description: 'Rýchly výpočet DPH (20%). Prevod medzi sumou s DPH a bez DPH.',
      icon: '📊',
      route: '/calculator/vat',
      searchVolume: 5000,
      color: 'from-purple-500 to-purple-600'
    }
  ];

  getTotalSearchVolume(): number {
    return this.calculators.reduce((sum, calc) => sum + calc.searchVolume, 0);
  }
}
