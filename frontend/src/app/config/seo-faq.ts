// Recovered SK SEO extras (keywords + FAQ) for calculators — restores the
// FAQPage rich results + keyword meta that were inlined per-component before
// SEO was centralized. Emitted for the SK locale only (primary market);
// translate per-locale later to extend rich results to cs/en/pl/hu.
export interface SeoExtra { keywords?: string; faq?: { question: string; answer: string }[]; }
export const SEO_SK_EXTRAS: Record<string, SeoExtra> = {
  'car-insurance': { keywords: 'PZP kalkulačka, najlacnejšie PZP, porovnanie PZP, povinné zmluvné poistenie 2026, PZP pre mladých vodičov', faq: [
        {
          question: 'Od čoho závisí cena PZP?',
          answer: 'Cena PZP závisí najmä od výkonu a typu vozidla, veku a bydliska vodiča, jeho histórie škôd (bonus/malus) a zvoleného krytia. Mladší vodiči a silnejšie autá majú spravidla vyššie poistné.',
        },
        {
          question: 'Ako získať najlacnejšie PZP?',
          answer: 'Porovnajte ponuky viacerých poisťovní – ceny za rovnaké krytie sa výrazne líšia. Cez tento formulár vám pripravíme nezáväzné porovnanie na mieru.',
        },
      ], },
  'energy': { keywords: 'kalkulačka energie, náklady na elektrinu, cena plynu, fotovoltika návratnosť, dotácia zelená domácnostiam', faq: [
        {
          question: 'Oplatí sa mi fotovoltika?',
          answer: 'Návratnosť fotovoltiky závisí od spotreby, ceny elektriny a výšky dotácie (Zelená domácnostiam). Pri vyššej spotrebe a samospotrebe je návratnosť rýchlejšia. Pre presný odhad získajte nezáväznú ponuku od montážnej firmy.',
        },
        {
          question: 'Aká je priemerná spotreba elektriny domácnosti?',
          answer: 'Priemerná domácnosť spotrebuje rádovo 2 000–4 000 kWh ročne podľa počtu osôb a vykurovania. Kalkulačka porovná vašu spotrebu s priemerom.',
        },
      ], },
  'freelancer-tax': { keywords: 'odvody SZČO 2026 kalkulačka, daň živnostník, paušálne výdavky, čistý príjem živnostník', faq: [
        {
          question: 'Aké sú minimálne odvody SZČO v roku 2026?',
          answer: 'Živnostník platí minimálne zdravotné aj sociálne odvody odvodené od minimálneho vymeriavacieho základu. Kalkulačka zohľadní aktuálne sadzby pre rok 2026.',
        },
        {
          question: 'Kedy sa oplatia paušálne výdavky 60 %?',
          answer: 'Paušálne výdavky (60 % z príjmu, do zákonného limitu) sa oplatia, ak sú vaše skutočné náklady nižšie. Pri vysokých reálnych nákladoch je výhodnejšie účtovať skutočné výdavky.',
        },
      ], },
  'heat-pump': { keywords: 'kalkulačka tepelného čerpadla, tepelné čerpadlo cena, tepelné čerpadlo dotácia, aké tepelné čerpadlo do domu, úspora tepelné čerpadlo', faq: [
        {
          question: 'Aký výkon tepelného čerpadla potrebujem na môj dom?',
          answer: 'Výkon závisí od tepelnej straty domu – tá sa odvíja od plochy a zateplenia. Orientačne pri čiastočne zateplenom dome ide o ~0,06 kW na m². Kalkulačka odhadne potrebný výkon, presné dimenzovanie urobí projektant podľa tepelnoizolačných vlastností.',
        },
        {
          question: 'Akú dotáciu môžem získať na tepelné čerpadlo?',
          answer: 'Cez program Zelená domácnostiam je príspevok orientačne stanovený za kW inštalovaného výkonu s maximálnym stropom a zároveň najviac 50 % oprávnených nákladov. Presná sadzba a podmienky sa menia podľa aktuálneho kola SIEA – overte si ich na zelenadomacnostiam.sk.',
        },
        {
          question: 'Oplatí sa tepelné čerpadlo oproti plynu?',
          answer: 'Tepelné čerpadlo s ročnou účinnosťou (SCOP) okolo 3,5 vyrobí z 1 kWh elektriny ~3,5 kWh tepla, čím môže výrazne znížiť náklady oproti plynovému kotlu. Návratnosť býva orientačne 7–12 rokov v závislosti od spotreby, cien a dotácie.',
        },
      ], },
  'mortgage': { keywords: 'hypotéka kalkulačka, výpočet splátky hypotéky, refinancovanie hypotéky, hypotekárna kalkulačka 2026', faq: [
        {
          question: 'Ako sa počíta mesačná splátka hypotéky?',
          answer: 'Mesačná splátka sa počíta anuitne z výšky úveru, ročnej úrokovej sadzby a doby splácania. Kalkulačka zohľadňuje istinu aj úroky a zobrazí celkové preplatenie.',
        },
        {
          question: 'Oplatí sa refinancovať hypotéku?',
          answer: 'Refinancovanie sa zvyčajne oplatí, ak je nová sadzba výrazne nižšia alebo končí fixácia. Porovnajte súčasnú splátku s ponukou a zohľadnite poplatky za predčasné splatenie.',
        },
      ], },
  'renovation': { keywords: 'Obnov dom dotácia, dotácia na zateplenie 2026, dotácia na rekonštrukciu, obnova rodinného domu dotácia, energetický audítor', faq: [
        {
          question: 'Kto má nárok na dotáciu Obnov dom?',
          answer: 'Dotácia je určená pre vlastníkov starších rodinných domov (postavených spravidla pred rokom 2013), ktorí obnovou dosiahnu úsporu primárnej energie aspoň 30 %. Presné podmienky aktuálneho kola nájdete na obnovdom.sk.',
        },
        {
          question: 'Koľko peňazí môžem z Obnov dom získať?',
          answer: 'Dotácia pokrýva orientačne do 60 % oprávnených nákladov. Pri úspore energie ≥30 % je strop nižší, pri komplexnej obnove s úsporou ≥60 % je strop vyšší. Kalkulačka uvádza orientačný odhad – výška sa mení podľa aktuálnej výzvy.',
        },
        {
          question: 'Aké opatrenia sa do dotácie počítajú?',
          answer: 'Najčastejšie zateplenie obvodových stien a strechy, výmena okien a dverí, výmena zdroja tepla (napr. tepelné čerpadlo), fotovoltika, rekuperácia a vonkajšie tienenie. Kombinácia viacerých opatrení zvyšuje dosiahnutú úsporu a tým aj možnú dotáciu.',
        },
      ], },
  'salary': { keywords: 'čistá mzda kalkulačka, výpočet čistej mzdy 2026, hrubá mzda na čistú, výplata kalkulačka', faq: [
        {
          question: 'Ako sa počíta čistá mzda z hrubej?',
          answer: 'Od hrubej mzdy sa odpočítajú odvody do Sociálnej a zdravotnej poisťovne (9,4 % + 5 %), uplatní sa nezdaniteľná časť základu dane a vypočíta sa daň z príjmu. Výsledok znížený o daň je čistá mzda, ku ktorej sa pripočíta daňový bonus na deti.',
        },
        {
          question: 'Aký je daňový bonus na dieťa v roku 2026?',
          answer: 'Daňový bonus závisí od veku dieťaťa a výšky príjmu. Kalkulačka ho automaticky zohľadní podľa počtu detí do 15 rokov a od 15 do 18 rokov.',
        },
      ], },
  'savings-goal': { keywords: 'kalkulačka sporenia, sporiaci cieľ, koľko sporiť mesačne, zložené úročenie, finančná rezerva, sporenie kalkulačka', faq: [
        {
          question: 'Ako funguje zložené úročenie?',
          answer: 'Úrok sa pripisuje k zostatku a v ďalšom období sa úročí už aj tento úrok. Čím dlhšie a skôr sporíte, tým väčší podiel na výsledku má práve úrok.',
        },
        {
          question: 'Koľko mám mesačne odkladať?',
          answer: 'Zadajte cieľovú sumu a termín a kalkulačka vypočíta potrebný mesačný vklad. Bežné odporúčanie je odkladať si aspoň 10–20 % z príjmu.',
        },
      ], },
  'solar': { keywords: 'kalkulačka fotovoltiky, dotácia na fotovoltiku 2026, zelená domácnostiam, návratnosť fotovoltiky, cena fotovoltiky', faq: [
        {
          question: 'Akú dotáciu môžem získať na fotovoltiku?',
          answer: 'Cez program Zelená domácnostiam je príspevok 500 €/kW inštalovaného výkonu, oprávnené sú 3 kW (po preukázaní spotreby až 7 kW). Maximálna dotácia je 3 500 € (so zvýhodnením +15 % až 4 025 €) a zároveň najviac 50 % oprávnených nákladov. Výška a podmienky sa menia podľa aktuálneho kola SIEA.',
        },
        {
          question: 'Aká je návratnosť fotovoltiky na Slovensku?',
          answer: 'Návratnosť závisí od spotreby, ceny elektriny, samospotreby a dotácie. Pri bežnej domácnosti býva orientačne 7–11 rokov, pričom panely vydržia 25+ rokov.',
        },
        {
          question: 'Oplatí sa k fotovoltike batéria?',
          answer: 'Batéria zvyšuje podiel vlastnej spotreby (z ~40 % na ~75 %), čím rastie úspora, no predlžuje návratnosť kvôli vyššej cene. Vyplatí sa pri vyššej večernej spotrebe.',
        },
      ], },
};
