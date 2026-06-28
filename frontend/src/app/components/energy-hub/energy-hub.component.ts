import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { SeoService } from '../../services/seo.service';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';

/**
 * Home-energy hub landing page (V4 report Part 5 strategy: bundle solar #1 +
 * renovation grants #5 + heat pumps #8 under ONE topical authority so link
 * equity and the shared installer lead-buyers compound). Server-rendered for SEO.
 */
@Component({
  selector: 'app-energy-hub',
  standalone: true,
  imports: [CommonModule, RouterLink, TranslatePipe, AdSlotComponent],
  templateUrl: './energy-hub.component.html',
  styleUrls: ['./energy-hub.component.css'],
})
export class EnergyHubComponent implements OnInit {
  private seo = inject(SeoService);

  pillars = [
    { id: 'solar', icon: '☀️', route: '/calculator/solar', accent: 'amber' },
    { id: 'heat-pump', icon: '♨️', route: '/calculator/heat-pump', accent: 'sky' },
    { id: 'renovation', icon: '🏚️', route: '/calculator/renovation', accent: 'teal' },
    { id: 'energy', icon: '⚡', route: '/calculator/energy', accent: 'orange' },
  ];

  ngOnInit(): void {
    this.seo.apply({
      title: 'Úspory energie v dome 2026 – fotovoltika, tepelné čerpadlo, dotácie',
      description: 'Jedno miesto pre úsporu energie v dome: kalkulačka fotovoltiky, tepelného čerpadla a dotácie Obnov dom. Zistite dotácie, náklady, úsporu a návratnosť a získajte nezáväzné ponuky od overených firiem.',
      path: '/energia',
      keywords: 'úspora energie dom, fotovoltika dotácia, tepelné čerpadlo dotácia, Obnov dom, zelená domácnostiam, zníženie nákladov na vykurovanie',
      faq: [
        {
          question: 'Aké dotácie na úsporu energie môžem získať?',
          answer: 'Na Slovensku bežia dva hlavné programy: Zelená domácnostiam (fotovoltika, tepelné čerpadlá, solárne kolektory) a Obnov dom (komplexná obnova rodinných domov – zateplenie, okná, zdroj tepla). Naše kalkulačky odhadnú výšku dotácie aj návratnosť.',
        },
        {
          question: 'Čo sa oplatí riešiť ako prvé – fotovoltiku, tepelné čerpadlo alebo zateplenie?',
          answer: 'Najlepší pomer cena/úspora má zvyčajne zateplenie a výmena zdroja tepla. Fotovoltika potom pokryje spotrebu (vrátane tepelného čerpadla a ohrevu vody). Ideálne je riešiť ich spolu – kombinácia opatrení zvyšuje aj dosiahnutú dotáciu z Obnov dom.',
        },
      ],
    });
  }
}
