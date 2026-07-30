import { Injectable, PLATFORM_ID, inject, DOCUMENT } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { Meta, Title } from '@angular/platform-browser';
import { LOCALE_META, SUPPORTED_LOCALES, Locale } from '../i18n/locales';
import { LocaleService } from '../i18n/locale.service';

/** Open Graph locale codes (og:locale format) per UI locale. */
const OG_LOCALE: Record<Locale, string> = {
  sk: 'sk_SK', cs: 'cs_CZ', en: 'en_US', pl: 'pl_PL', hu: 'hu_HU',
};

export interface SeoData {
  title: string;
  description: string;
  /** Path without origin, e.g. '/calculator/mortgage'. */
  path?: string;
  keywords?: string;
  /** FAQ entries → FAQPage JSON-LD (great for SERP rich results). */
  faq?: { question: string; answer: string }[];
  /** If set, emits a WebApplication (calculator) JSON-LD block. */
  isCalculator?: boolean;
}

const SITE_NAME = 'Kalkulačky.sk';
const ORIGIN = 'https://kalkulacky.sk';
const LD_ID = 'seo-jsonld';

/**
 * Centralised SEO: sets <title>, meta description, Open Graph/Twitter tags,
 * canonical URL and JSON-LD structured data per page. Call from each
 * calculator's ngOnInit. Safe under SSR (uses Angular Meta/Title + DOCUMENT).
 */
@Injectable({ providedIn: 'root' })
export class SeoService {
  private title = inject(Title);
  private meta = inject(Meta);
  private doc = inject(DOCUMENT);
  private platformId = inject(PLATFORM_ID);
  private locale = inject(LocaleService);

  apply(data: SeoData): void {
    const fullTitle = data.title.includes(SITE_NAME)
      ? data.title
      : `${data.title} | ${SITE_NAME}`;
    const url = ORIGIN + (data.path ?? '');

    this.title.setTitle(fullTitle);
    this.setName('description', data.description);
    if (data.keywords) this.setName('keywords', data.keywords);

    // Open Graph
    this.setProp('og:title', fullTitle);
    this.setProp('og:description', data.description);
    this.setProp('og:type', 'website');
    this.setProp('og:site_name', SITE_NAME);
    this.setProp('og:url', url);
    this.setProp('og:locale', OG_LOCALE[this.locale.locale()] ?? 'sk_SK');

    // Twitter
    this.setName('twitter:card', 'summary_large_image');
    this.setName('twitter:title', fullTitle);
    this.setName('twitter:description', data.description);

    this.setCanonical(url);
    this.setHreflangAlternates(data.path ?? '');
    this.setJsonLd(this.buildJsonLd(data, fullTitle, url));
  }

  /**
   * Emit hreflang alternate links for every supported locale so Google serves
   * the right language version per market (the V4 cross-border strategy).
   * Phase 1 uses `?lang=` URLs; switch to path prefixes when locale routing lands.
   */
  private setHreflangAlternates(path: string): void {
    const head = this.doc.head;
    head
      .querySelectorAll("link[rel='alternate'][data-i18n='1']")
      .forEach((el) => el.remove());

    const add = (hreflang: string, href: string) => {
      const link = this.doc.createElement('link');
      link.setAttribute('rel', 'alternate');
      link.setAttribute('hreflang', hreflang);
      link.setAttribute('href', href);
      link.setAttribute('data-i18n', '1');
      head.appendChild(link);
    };

    for (const code of SUPPORTED_LOCALES) {
      add(LOCALE_META[code].hreflang, `${ORIGIN}${path}?lang=${code}`);
    }
    add('x-default', `${ORIGIN}${path}`);
  }

  private buildJsonLd(data: SeoData, title: string, url: string): object {
    const graph: object[] = [];

    if (data.isCalculator) {
      graph.push({
        '@type': 'WebApplication',
        name: title,
        url,
        applicationCategory: 'FinanceApplication',
        operatingSystem: 'All',
        offers: { '@type': 'Offer', price: '0', priceCurrency: 'EUR' },
        inLanguage: this.locale.locale(),
      });
    }

    if (data.faq?.length) {
      graph.push({
        '@type': 'FAQPage',
        mainEntity: data.faq.map((f) => ({
          '@type': 'Question',
          name: f.question,
          acceptedAnswer: { '@type': 'Answer', text: f.answer },
        })),
      });
    }

    return { '@context': 'https://schema.org', '@graph': graph };
  }

  private setName(name: string, content: string): void {
    this.meta.updateTag({ name, content });
  }

  private setProp(property: string, content: string): void {
    this.meta.updateTag({ property, content });
  }

  private setCanonical(url: string): void {
    const head = this.doc.head;
    let link = head.querySelector("link[rel='canonical']") as HTMLLinkElement | null;
    if (!link) {
      link = this.doc.createElement('link');
      link.setAttribute('rel', 'canonical');
      head.appendChild(link);
    }
    link.setAttribute('href', url);
  }

  private setJsonLd(data: object): void {
    const head = this.doc.head;
    let script = head.querySelector(`#${LD_ID}`) as HTMLScriptElement | null;
    if (!script) {
      script = this.doc.createElement('script');
      script.setAttribute('type', 'application/ld+json');
      script.setAttribute('id', LD_ID);
      head.appendChild(script);
    }
    script.textContent = JSON.stringify(data);
  }
}
