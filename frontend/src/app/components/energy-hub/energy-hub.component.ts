import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { SeoService } from '../../services/seo.service';
import { TranslatePipe } from '../../i18n/translate.pipe';
import { AdSlotComponent } from '../shared/ad-slot/ad-slot.component';
import { LocaleService } from '../../i18n/locale.service';
import { getSeoContent } from '../../i18n/seo';

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
  private locale = inject(LocaleService);

  pillars = [
    { id: 'solar', icon: '☀️', route: '/calculator/solar', accent: 'amber' },
    { id: 'heat-pump', icon: '♨️', route: '/calculator/heat-pump', accent: 'sky' },
    { id: 'renovation', icon: '🏚️', route: '/calculator/renovation', accent: 'teal' },
    { id: 'energy', icon: '⚡', route: '/calculator/energy', accent: 'orange' },
  ];

  ngOnInit(): void {
    const s = getSeoContent('energy-hub', this.locale.locale());
    this.seo.apply({
      title: s.title,
      description: s.description,
      keywords: s.keywords,
      faq: s.faq,
      path: '/energia',
    });
  }
}
