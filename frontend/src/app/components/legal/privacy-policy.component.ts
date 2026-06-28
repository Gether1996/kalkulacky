import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { SeoService } from '../../services/seo.service';

/**
 * Privacy policy (GDPR Art. 13). SK content covering the site's real data flows
 * (accounts, lead-gen passed to partners, reminders, data reports, cookies).
 * ⚠️ Operator-specific details are placeholders [DOPLŇTE…] — complete and have
 * a lawyer review before launch.
 */
@Component({
  selector: 'app-privacy-policy',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="legal-page">
      <h1>Zásady ochrany osobných údajov</h1>
      <p class="legal-updated">Účinné od: 1. 1. 2026</p>

      <p class="legal-note">⚠️ Vzorový dokument. Pred spustením doplňte údaje prevádzkovateľa
        a nechajte ho skontrolovať právnikom.</p>

      <h2>1. Prevádzkovateľ</h2>
      <p>Prevádzkovateľom je [DOPLŇTE: obchodné meno], IČO: [DOPLŇTE], so sídlom [DOPLŇTE],
        e-mail: <a href="mailto:[DOPLNTE]">[DOPLŇTE e-mail]</a> (ďalej len „prevádzkovateľ").</p>

      <h2>2. Aké údaje spracúvame</h2>
      <ul>
        <li><strong>Účet:</strong> e-mailová adresa, meno a priezvisko (ak ich uvediete), heslo
          (v zašifrovanej podobe), prípadne identifikátor z prihlásenia cez Google.</li>
        <li><strong>Dopyty (lead-gen):</strong> ak požiadate o nezáväznú ponuku, spracúvame meno,
          e-mail, telefón, región a kontext výpočtu, ktorý ste zadali.</li>
        <li><strong>Pripomienky a uložené výpočty:</strong> názvy, poznámky, dátumy a vstupy výpočtov,
          ktoré si uložíte vo svojom účte.</li>
        <li><strong>Hlásenia nesprávnych údajov:</strong> text správy a nepovinný kontaktný e-mail.</li>
        <li><strong>Technické údaje:</strong> IP adresa, typ prehliadača, cookies a údaje v lokálnom
          úložisku (jazyk, téma, súhlas s cookies, prihlasovacie tokeny).</li>
      </ul>

      <h2>3. Účely a právne základy spracúvania</h2>
      <ul>
        <li><strong>Poskytovanie služby a správa účtu</strong> – plnenie zmluvy (čl. 6 ods. 1 písm. b GDPR).</li>
        <li><strong>Sprostredkovanie ponúk od partnerov (lead-gen)</strong> – na základe vášho súhlasu
          (čl. 6 ods. 1 písm. a GDPR); bez súhlasu dopyt neodošleme.</li>
        <li><strong>E-mailové pripomienky a upozornenia</strong> – súhlas, ktorý môžete kedykoľvek odvolať.</li>
        <li><strong>Reklama a analytika (cookies)</strong> – iba na základe súhlasu v cookie lište.</li>
        <li><strong>Bezpečnosť a prevencia zneužitia</strong> – oprávnený záujem (čl. 6 ods. 1 písm. f GDPR).</li>
      </ul>

      <h2>4. Komu údaje poskytujeme</h2>
      <p>Vaše údaje môžeme poskytnúť: partnerom, ktorým postupujeme dopyty (napr. montážne firmy,
        hypotekárni sprostredkovatelia, poisťovne/makléri, účtovníci) – iba s vaším súhlasom;
        poskytovateľom IT služieb (hosting, e-mail), spoločnosti Google (prihlásenie, prípadne reklama
        AdSense, ak ju povolíte). Niektorí príjemcovia môžu spracúvať údaje mimo EÚ na základe
        primeraných záruk podľa GDPR.</p>

      <h2>5. Doba uchovávania</h2>
      <p>Údaje účtu uchovávame, kým máte účet aktívny; po jeho zrušení ich vymažeme alebo anonymizujeme.
        Dopyty uchovávame po dobu nevyhnutnú na ich vybavenie a preukázanie súhlasu. Daňové a účtovné
        doklady uchovávame podľa zákonných lehôt.</p>

      <h2>6. Vaše práva</h2>
      <p>Máte právo na prístup, opravu, vymazanie, obmedzenie spracúvania, prenosnosť údajov, namietať
        proti spracúvaniu a kedykoľvek odvolať súhlas. Účet a uložené údaje môžete vymazať priamo v sekcii
        <a routerLink="/profile">Profil</a>. Sťažnosť môžete podať na Úrad na ochranu osobných údajov SR
        (dataprotection.gov.sk), v ČR na ÚOOÚ (uoou.gov.cz).</p>

      <h2>7. Cookies</h2>
      <p>Používanie cookies a lokálneho úložiska je opísané v <a routerLink="/cookies">Zásadách používania cookies</a>.</p>

      <h2>8. Kontakt</h2>
      <p>V otázkach ochrany údajov nás kontaktujte na <a href="mailto:[DOPLNTE]">[DOPLŇTE e-mail]</a>.</p>
    </div>
  `,
})
export class PrivacyPolicyComponent implements OnInit {
  private seo = inject(SeoService);
  ngOnInit(): void {
    this.seo.apply({
      title: 'Zásady ochrany osobných údajov',
      description: 'Ako Kalkulačky.sk spracúva osobné údaje – účet, dopyty, cookies a vaše práva podľa GDPR.',
      path: '/privacy',
    });
  }
}
