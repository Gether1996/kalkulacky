import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { SeoService } from '../../services/seo.service';

/**
 * Terms of use. ⚠️ Template — complete operator details and have it reviewed.
 */
@Component({
  selector: 'app-terms',
  standalone: true,
  imports: [CommonModule, RouterLink],
  template: `
    <div class="legal-page">
      <h1>Podmienky používania</h1>
      <p class="legal-updated">Účinné od: 1. 1. 2026</p>

      <p class="legal-note">⚠️ Vzorový dokument. Pred spustením doplňte údaje prevádzkovateľa
        a nechajte ho skontrolovať právnikom.</p>

      <h2>1. Úvodné ustanovenia</h2>
      <p>Tieto podmienky upravujú používanie webu Kalkulačky.sk prevádzkovaného [DOPLŇTE: obchodné meno,
        IČO, sídlo]. Používaním webu s nimi vyjadrujete súhlas.</p>

      <h2>2. Charakter služby</h2>
      <p>Web poskytuje <strong>orientačné</strong> kalkulačky a informačný obsah. Výsledky sú odhady
        vychádzajúce zo zadaných údajov a verejne dostupných pravidiel (napr. dane, odvody, dotácie)
        a <strong>nie sú daňovým, právnym, finančným ani iným odborným poradenstvom</strong>. Pred
        rozhodnutím si overte aktuálne podmienky u príslušného úradu alebo odborníka.</p>

      <h2>3. Obmedzenie zodpovednosti</h2>
      <p>Prevádzkovateľ nezodpovedá za škody vzniknuté spoliehaním sa na výsledky kalkulačiek ani za
        nepresnosti spôsobené zmenami legislatívy. Web sa poskytuje „tak ako je", bez záruk dostupnosti
        a bezchybnosti.</p>

      <h2>4. Používateľské účty</h2>
      <p>Za aktivitu na účte a dôvernosť hesla zodpovedáte vy. Je zakázané zneužívať službu, pokúšať sa
        o neoprávnený prístup alebo ju zaťažovať automatizovanými požiadavkami. Účet môžete kedykoľvek
        zrušiť v sekcii <a routerLink="/profile">Profil</a>.</p>

      <h2>5. Sprostredkovanie ponúk (lead-gen)</h2>
      <p>Ak požiadate o nezáväznú ponuku, váš dopyt so súhlasom postúpime overeným partnerom, ktorí vás
        môžu kontaktovať. Uzatvorenie zmluvy s partnerom je výlučne medzi vami a partnerom.</p>

      <h2>6. Duševné vlastníctvo</h2>
      <p>Obsah a kód webu sú chránené. Bez súhlasu ich nie je dovolené kopírovať okrem bežného používania
        služby a embedovateľných widgetov v súlade s ich podmienkami.</p>

      <h2>7. Zmeny a rozhodné právo</h2>
      <p>Podmienky môžeme aktualizovať; o podstatných zmenách budeme informovať na webe. Vzťahy sa riadia
        právnym poriadkom Slovenskej republiky.</p>

      <h2>8. Kontakt</h2>
      <p><a href="mailto:[DOPLNTE]">[DOPLŇTE e-mail]</a></p>
    </div>
  `,
})
export class TermsComponent implements OnInit {
  private seo = inject(SeoService);
  ngOnInit(): void {
    this.seo.apply({
      title: 'Podmienky používania',
      description: 'Podmienky používania webu Kalkulačky.sk – orientačný charakter výpočtov, účty a zodpovednosť.',
      path: '/terms',
    });
  }
}
