import { Locale } from './locales';

/**
 * Runtime translation dictionaries.
 *
 * Keys are dot-namespaced. SK is the source of truth; other locales mirror its
 * keys. Add new shared/UI strings here. Long-form SEO article content stays in
 * component templates and is translated per-locale in a later phase.
 *
 * Coverage so far: language switcher, navbar, shared monetization components,
 * common calculator actions. Extend incrementally as calculators are localized.
 */

export type TranslationDict = Record<string, string>;

const sk: TranslationDict = {
  // language switcher
  'lang.label': 'Jazyk',

  // navbar / common
  'nav.home': 'Domov',
  'nav.blog': 'Blog',
  'nav.login': 'Prihlásiť sa',
  'nav.register': 'Registrácia',
  'nav.dashboard': 'Môj prehľad',
  'nav.profile': 'Profil',
  'nav.logout': 'Odhlásiť sa',
  'nav.cat.financial': 'Finančné',
  'nav.cat.health': 'Zdravie',
  'nav.cat.lifestyle': 'Životný štýl',

  // common calculator actions
  'common.calculate': 'Vypočítať',
  'common.result': 'Výsledok',
  'common.loading': 'Počítam…',
  'common.reset': 'Vynulovať',

  // monetization — lead form
  'lead.consent': 'Súhlasím so spracovaním údajov za účelom kontaktovania s nezáväznou ponukou.',
  'lead.error.contact': 'Zadajte e-mail alebo telefón, aby sme vás mohli kontaktovať.',
  'lead.error.consent': 'Pre pokračovanie potvrďte súhlas so spracovaním údajov.',
  'lead.error.submit': 'Odoslanie zlyhalo. Skúste to prosím znova alebo nás kontaktujte.',
  'lead.sending': 'Odosielam…',
  'lead.success': 'Ďakujeme! Ozveme sa vám čo najskôr.',
  'lead.field.name': 'Meno',
  'lead.field.email': 'E-mail',
  'lead.field.phone': 'Telefón',
  'lead.field.region': 'Mesto / región',
  'lead.field.message': 'Poznámka (nepovinné)',

  // monetization — affiliate / ads
  'aff.disclosure': 'Niektoré odkazy sú reklamné/partnerské.',
  'ad.placeholder': 'Reklamný priestor',

  // embed widget
  'embed.poweredBy': 'Kalkulačka od',
  'embed.openFull': 'Otvoriť plnú kalkulačku',
  'embed.copy': 'Kopírovať kód',
  'embed.copied': 'Skopírované!',
  'embed.title': 'Vložte túto kalkulačku na svoj web',
};

const cs: TranslationDict = {
  'lang.label': 'Jazyk',
  'nav.home': 'Domů',
  'nav.blog': 'Blog',
  'nav.login': 'Přihlásit se',
  'nav.register': 'Registrace',
  'nav.dashboard': 'Můj přehled',
  'nav.profile': 'Profil',
  'nav.logout': 'Odhlásit se',
  'nav.cat.financial': 'Finanční',
  'nav.cat.health': 'Zdraví',
  'nav.cat.lifestyle': 'Životní styl',
  'common.calculate': 'Vypočítat',
  'common.result': 'Výsledek',
  'common.loading': 'Počítám…',
  'common.reset': 'Vynulovat',
  'lead.consent': 'Souhlasím se zpracováním údajů za účelem kontaktování s nezávaznou nabídkou.',
  'lead.error.contact': 'Zadejte e-mail nebo telefon, abychom vás mohli kontaktovat.',
  'lead.error.consent': 'Pro pokračování potvrďte souhlas se zpracováním údajů.',
  'lead.error.submit': 'Odeslání selhalo. Zkuste to prosím znovu nebo nás kontaktujte.',
  'lead.sending': 'Odesílám…',
  'lead.success': 'Děkujeme! Ozveme se vám co nejdříve.',
  'lead.field.name': 'Jméno',
  'lead.field.email': 'E-mail',
  'lead.field.phone': 'Telefon',
  'lead.field.region': 'Město / region',
  'lead.field.message': 'Poznámka (nepovinné)',
  'aff.disclosure': 'Některé odkazy jsou reklamní/partnerské.',
  'ad.placeholder': 'Reklamní prostor',
  'embed.poweredBy': 'Kalkulačka od',
  'embed.openFull': 'Otevřít plnou kalkulačku',
  'embed.copy': 'Kopírovat kód',
  'embed.copied': 'Zkopírováno!',
  'embed.title': 'Vložte tuto kalkulačku na svůj web',
};

const en: TranslationDict = {
  'lang.label': 'Language',
  'nav.home': 'Home',
  'nav.blog': 'Blog',
  'nav.login': 'Log in',
  'nav.register': 'Sign up',
  'nav.dashboard': 'Dashboard',
  'nav.profile': 'Profile',
  'nav.logout': 'Log out',
  'nav.cat.financial': 'Financial',
  'nav.cat.health': 'Health',
  'nav.cat.lifestyle': 'Lifestyle',
  'common.calculate': 'Calculate',
  'common.result': 'Result',
  'common.loading': 'Calculating…',
  'common.reset': 'Reset',
  'lead.consent': 'I agree to the processing of my data for the purpose of being contacted with a non-binding offer.',
  'lead.error.contact': 'Enter an email or phone number so we can contact you.',
  'lead.error.consent': 'Please confirm consent to data processing to continue.',
  'lead.error.submit': 'Submission failed. Please try again or contact us.',
  'lead.sending': 'Sending…',
  'lead.success': 'Thank you! We will get back to you shortly.',
  'lead.field.name': 'Name',
  'lead.field.email': 'Email',
  'lead.field.phone': 'Phone',
  'lead.field.region': 'City / region',
  'lead.field.message': 'Note (optional)',
  'aff.disclosure': 'Some links are ads/affiliate links.',
  'ad.placeholder': 'Advertisement',
  'embed.poweredBy': 'Calculator by',
  'embed.openFull': 'Open full calculator',
  'embed.copy': 'Copy code',
  'embed.copied': 'Copied!',
  'embed.title': 'Embed this calculator on your site',
};

const pl: TranslationDict = {
  'lang.label': 'Język',
  'nav.home': 'Strona główna',
  'nav.blog': 'Blog',
  'nav.login': 'Zaloguj się',
  'nav.register': 'Rejestracja',
  'nav.dashboard': 'Panel',
  'nav.profile': 'Profil',
  'nav.logout': 'Wyloguj się',
  'nav.cat.financial': 'Finanse',
  'nav.cat.health': 'Zdrowie',
  'nav.cat.lifestyle': 'Styl życia',
  'common.calculate': 'Oblicz',
  'common.result': 'Wynik',
  'common.loading': 'Obliczanie…',
  'common.reset': 'Wyczyść',
  'lead.consent': 'Wyrażam zgodę na przetwarzanie danych w celu kontaktu z niezobowiązującą ofertą.',
  'lead.error.contact': 'Podaj e-mail lub telefon, abyśmy mogli się z Tobą skontaktować.',
  'lead.error.consent': 'Aby kontynuować, potwierdź zgodę na przetwarzanie danych.',
  'lead.error.submit': 'Wysłanie nie powiodło się. Spróbuj ponownie lub skontaktuj się z nami.',
  'lead.sending': 'Wysyłanie…',
  'lead.success': 'Dziękujemy! Skontaktujemy się wkrótce.',
  'lead.field.name': 'Imię',
  'lead.field.email': 'E-mail',
  'lead.field.phone': 'Telefon',
  'lead.field.region': 'Miasto / region',
  'lead.field.message': 'Uwaga (opcjonalnie)',
  'aff.disclosure': 'Niektóre linki są reklamowe/afiliacyjne.',
  'ad.placeholder': 'Miejsce na reklamę',
  'embed.poweredBy': 'Kalkulator od',
  'embed.openFull': 'Otwórz pełny kalkulator',
  'embed.copy': 'Kopiuj kod',
  'embed.copied': 'Skopiowano!',
  'embed.title': 'Umieść ten kalkulator na swojej stronie',
};

const hu: TranslationDict = {
  'lang.label': 'Nyelv',
  'nav.home': 'Főoldal',
  'nav.blog': 'Blog',
  'nav.login': 'Bejelentkezés',
  'nav.register': 'Regisztráció',
  'nav.dashboard': 'Irányítópult',
  'nav.profile': 'Profil',
  'nav.logout': 'Kijelentkezés',
  'nav.cat.financial': 'Pénzügyi',
  'nav.cat.health': 'Egészség',
  'nav.cat.lifestyle': 'Életmód',
  'common.calculate': 'Számítás',
  'common.result': 'Eredmény',
  'common.loading': 'Számolás…',
  'common.reset': 'Visszaállítás',
  'lead.consent': 'Hozzájárulok adataim kezeléséhez, hogy kötelezettség nélküli ajánlattal megkereshessenek.',
  'lead.error.contact': 'Adjon meg e-mailt vagy telefonszámot, hogy felvehessük Önnel a kapcsolatot.',
  'lead.error.consent': 'A folytatáshoz erősítse meg az adatkezelési hozzájárulást.',
  'lead.error.submit': 'A küldés nem sikerült. Kérjük, próbálja újra, vagy lépjen kapcsolatba velünk.',
  'lead.sending': 'Küldés…',
  'lead.success': 'Köszönjük! Hamarosan jelentkezünk.',
  'lead.field.name': 'Név',
  'lead.field.email': 'E-mail',
  'lead.field.phone': 'Telefon',
  'lead.field.region': 'Város / régió',
  'lead.field.message': 'Megjegyzés (opcionális)',
  'aff.disclosure': 'Egyes linkek hirdetések/partneri linkek.',
  'ad.placeholder': 'Hirdetési hely',
  'embed.poweredBy': 'Kalkulátor:',
  'embed.openFull': 'Teljes kalkulátor megnyitása',
  'embed.copy': 'Kód másolása',
  'embed.copied': 'Másolva!',
  'embed.title': 'Ágyazza be ezt a kalkulátort a webhelyére',
};

export const TRANSLATIONS: Record<Locale, TranslationDict> = { sk, cs, en, pl, hu };
