import { Locale, SUPPORTED_LOCALES } from './locales';
import { TranslationDict } from './translations';

/**
 * Calculator-body UI translations (input labels, result labels, buttons,
 * errors, section headings). Key-first layout: each string lists all 5 locales
 * adjacently so it is easy to author and review. Long-form SEO/FAQ article
 * sections inside calculator templates are intentionally NOT translated here.
 *
 * Pivoted into per-locale dictionaries and merged in locale.service.
 */

type LangMap = Record<Locale, string>;

const ENTRIES: Record<string, LangMap> = {
  // ============ shared extras ============
  'common.quickSelect': { sk: 'Rýchly výber:', cs: 'Rychlý výběr:', en: 'Quick select:', pl: 'Szybki wybór:', hu: 'Gyors választás:' },
  'common.detailedCalc': { sk: '📋 Detailný výpočet', cs: '📋 Detailní výpočet', en: '📋 Detailed calculation', pl: '📋 Szczegółowe obliczenie', hu: '📋 Részletes számítás' },

  // ============ salary ============
  'salary.title': { sk: '💰 Kalkulačka čistej mzdy 2026', cs: '💰 Kalkulačka čisté mzdy 2026', en: '💰 Net Salary Calculator 2026', pl: '💰 Kalkulator wynagrodzenia netto 2026', hu: '💰 Nettó bér kalkulátor 2026' },
  'salary.subtitle': { sk: 'Vypočítajte si čistú mzdu zo svojej hrubej mzdy. Zohľadňuje všetky odvody a daňový bonus 2026.', cs: 'Spočítejte si čistou mzdu z hrubé mzdy. Zohledňuje všechny odvody a daňový bonus 2026.', en: 'Calculate your net salary from your gross salary. Includes all levies and the 2026 child tax bonus.', pl: 'Oblicz wynagrodzenie netto z brutto. Uwzględnia wszystkie składki i ulgę na dzieci 2026.', hu: 'Számítsa ki nettó bérét a bruttóból. Tartalmazza az összes járulékot és a 2026-os gyermekkedvezményt.' },
  'salary.gross': { sk: 'Hrubá mzda (€)', cs: 'Hrubá mzda (€)', en: 'Gross salary (€)', pl: 'Wynagrodzenie brutto (€)', hu: 'Bruttó bér (€)' },
  'salary.nczd': { sk: 'Uplatňujem si nezdaniteľnú časť (NČZD)', cs: 'Uplatňuji nezdanitelnou část', en: 'Apply the non-taxable allowance', pl: 'Stosuję kwotę wolną od podatku', hu: 'Adómentes rész igénylése' },
  'salary.nczdHint': { sk: '497,23 € mesačne - štandardne áno', cs: '497,23 € měsíčně – standardně ano', en: '€497.23 per month – usually yes', pl: '497,23 € miesięcznie – zwykle tak', hu: '497,23 € havonta – általában igen' },
  'salary.disability': { sk: 'Osoba so zdravotným postihnutím (ZŤP)', cs: 'Osoba se zdravotním postižením', en: 'Person with a disability', pl: 'Osoba z niepełnosprawnością', hu: 'Fogyatékossággal élő személy' },
  'salary.disabilityHint': { sk: 'Znížené zdravotné poistenie 2,5 % (namiesto 5 %)', cs: 'Snížené zdravotní pojištění 2,5 % (místo 5 %)', en: 'Reduced health insurance 2.5% (instead of 5%)', pl: 'Obniżona składka zdrowotna 2,5% (zamiast 5%)', hu: 'Csökkentett egészségbiztosítás 2,5% (5% helyett)' },
  'salary.children': { sk: '👶 Vyživované deti', cs: '👶 Vyživované děti', en: '👶 Dependent children', pl: '👶 Dzieci na utrzymaniu', hu: '👶 Eltartott gyermekek' },
  'salary.childrenUnder15': { sk: 'Do 15 rokov', cs: 'Do 15 let', en: 'Under 15', pl: 'Do 15 lat', hu: '15 év alatt' },
  'salary.children15to18': { sk: '15-18 rokov', cs: '15–18 let', en: '15–18 years', pl: '15–18 lat', hu: '15–18 év' },
  'salary.infoTitle': { sk: 'ℹ️ Odvody a dane 2026', cs: 'ℹ️ Odvody a daně 2026', en: 'ℹ️ Levies and taxes 2026', pl: 'ℹ️ Składki i podatki 2026', hu: 'ℹ️ Járulékok és adók 2026' },
  'salary.net': { sk: '💰 Čistá mzda', cs: '💰 Čistá mzda', en: '💰 Net salary', pl: '💰 Wynagrodzenie netto', hu: '💰 Nettó bér' },
  'salary.fromGrossPre': { sk: 'z', cs: 'z', en: 'from', pl: 'z', hu: 'ebből:' },
  'salary.fromGrossPost': { sk: 'hrubej', cs: 'hrubé', en: 'gross', pl: 'brutto', hu: 'bruttó' },
  'salary.social': { sk: 'Sociálne', cs: 'Sociální', en: 'Social', pl: 'Społeczne', hu: 'Társadalombiztosítás' },
  'salary.health': { sk: 'Zdravotné', cs: 'Zdravotní', en: 'Health', pl: 'Zdrowotne', hu: 'Egészségügyi' },
  'salary.tax': { sk: 'Daň', cs: 'Daň', en: 'Tax', pl: 'Podatek', hu: 'Adó' },
  'salary.afterBonus': { sk: 'Po bonuse', cs: 'Po bonusu', en: 'After bonus', pl: 'Po uldze', hu: 'Bónusz után' },
  'salary.effective': { sk: 'Efektívna', cs: 'Efektivní', en: 'Effective', pl: 'Efektywna', hu: 'Tényleges' },
  'salary.effectiveHint': { sk: 'Celkom', cs: 'Celkem', en: 'Total', pl: 'Razem', hu: 'Összesen' },
  'salary.taxBase': { sk: 'Daňový základ', cs: 'Daňový základ', en: 'Tax base', pl: 'Podstawa opodatkowania', hu: 'Adóalap' },
  'salary.nczdRow': { sk: '📋 NČZD', cs: '📋 Nezdanitelná část', en: '📋 Non-taxable allowance', pl: '📋 Kwota wolna', hu: '📋 Adómentes rész' },
  'salary.taxableBase': { sk: 'Zdaniteľný základ', cs: 'Zdanitelný základ', en: 'Taxable base', pl: 'Podstawa do opodatkowania', hu: 'Adóköteles alap' },
  'salary.taxProgressive': { sk: '📊 Daň (progresívna)', cs: '📊 Daň (progresivní)', en: '📊 Tax (progressive)', pl: '📊 Podatek (progresywny)', hu: '📊 Adó (progresszív)' },
  'salary.childBonus': { sk: '👶 Bonus za deti', cs: '👶 Bonus na děti', en: '👶 Child bonus', pl: '👶 Ulga na dzieci', hu: '👶 Gyermekbónusz' },
  'salary.employerCosts': { sk: '🏭 Náklady zamestnávateľa', cs: '🏭 Náklady zaměstnavatele', en: '🏭 Employer costs', pl: '🏭 Koszty pracodawcy', hu: '🏭 Munkáltatói költségek' },
  'salary.employeeGross': { sk: 'Hrubá mzda zamestnanca', cs: 'Hrubá mzda zaměstnance', en: 'Employee gross salary', pl: 'Wynagrodzenie brutto pracownika', hu: 'Munkavállalói bruttó bér' },
  'salary.employerContrib': { sk: '🏭 Odvody zamestnávateľa (36.2%)', cs: '🏭 Odvody zaměstnavatele (36,2 %)', en: '🏭 Employer contributions (36.2%)', pl: '🏭 Składki pracodawcy (36,2%)', hu: '🏭 Munkáltatói járulékok (36,2%)' },
  'salary.superGross': { sk: '💸 Superhrubá mzda', cs: '💸 Superhrubá mzda', en: '💸 Super-gross salary', pl: '💸 Wynagrodzenie superbrutto', hu: '💸 Szuperbruttó bér' },

  'common.years': { sk: 'rokov', cs: 'let', en: 'years', pl: 'lat', hu: 'év' },
  'common.months': { sk: 'mesiacov', cs: 'měsíců', en: 'months', pl: 'miesięcy', hu: 'hónap' },

  // ============ mortgage body ============
  'mortgage.inputTitle': { sk: 'Zadajte parametre hypotéky', cs: 'Zadejte parametry hypotéky', en: 'Enter mortgage parameters', pl: 'Wprowadź parametry kredytu', hu: 'Adja meg a jelzálog paramétereit' },
  'mortgage.loanAmount': { sk: 'Výška úveru (€)', cs: 'Výše úvěru (€)', en: 'Loan amount (€)', pl: 'Kwota kredytu (€)', hu: 'Hitelösszeg (€)' },
  'mortgage.rate': { sk: 'Úroková sadzba (%)', cs: 'Úroková sazba (%)', en: 'Interest rate (%)', pl: 'Oprocentowanie (%)', hu: 'Kamatláb (%)' },
  'mortgage.term': { sk: 'Dĺžka splácania (roky)', cs: 'Doba splácení (roky)', en: 'Loan term (years)', pl: 'Okres spłaty (lata)', hu: 'Futamidő (év)' },
  'mortgage.chooseScenario': { sk: 'Alebo vyberte scenár:', cs: 'Nebo vyberte scénář:', en: 'Or pick a scenario:', pl: 'Lub wybierz scenariusz:', hu: 'Vagy válasszon forgatókönyvet:' },
  'mortgage.monthlyPayment': { sk: 'Mesačná splátka', cs: 'Měsíční splátka', en: 'Monthly payment', pl: 'Rata miesięczna', hu: 'Havi törlesztés' },
  'mortgage.during': { sk: 'počas', cs: 'po dobu', en: 'over', pl: 'przez', hu: 'futamidő:' },
  'mortgage.principal': { sk: 'Výška úveru', cs: 'Výše úvěru', en: 'Loan amount', pl: 'Kwota kredytu', hu: 'Hitelösszeg' },
  'mortgage.principalHint': { sk: 'Hlavnica', cs: 'Jistina', en: 'Principal', pl: 'Kapitał', hu: 'Tőke' },
  'mortgage.totalToPay': { sk: 'Celkovo zaplatíte', cs: 'Celkem zaplatíte', en: 'Total you pay', pl: 'Łącznie zapłacisz', hu: 'Összesen fizet' },
  'mortgage.principalPlusInterest': { sk: 'Hlavnica + úroky', cs: 'Jistina + úroky', en: 'Principal + interest', pl: 'Kapitał + odsetki', hu: 'Tőke + kamat' },
  'mortgage.totalInterest': { sk: 'Celkové úroky', cs: 'Celkové úroky', en: 'Total interest', pl: 'Odsetki łącznie', hu: 'Összes kamat' },
  'mortgage.ofLoan': { sk: 'z úveru', cs: 'z úvěru', en: 'of the loan', pl: 'kredytu', hu: 'a hitelből' },
  'mortgage.annually': { sk: 'Ročne', cs: 'Ročně', en: 'Annually', pl: 'Rocznie', hu: 'Évente' },
  'mortgage.rateLabel': { sk: 'Úroková sadzba', cs: 'Úroková sazba', en: 'Interest rate', pl: 'Oprocentowanie', hu: 'Kamatláb' },
  'mortgage.interestShort': { sk: 'Úroky', cs: 'Úroky', en: 'Interest', pl: 'Odsetki', hu: 'Kamat' },
  'mortgage.summaryTitle': { sk: 'Prehľad splácania', cs: 'Přehled splácení', en: 'Repayment overview', pl: 'Podsumowanie spłaty', hu: 'Törlesztési áttekintés' },
  'mortgage.duration': { sk: 'Dĺžka splácania', cs: 'Doba splácení', en: 'Loan term', pl: 'Okres spłaty', hu: 'Futamidő' },
  'mortgage.firstYearTitle': { sk: 'Prvý rok splácania', cs: 'První rok splácení', en: 'First year of repayment', pl: 'Pierwszy rok spłaty', hu: 'A törlesztés első éve' },
  'mortgage.payTotal': { sk: 'Zaplatíte celkom', cs: 'Zaplatíte celkem', en: 'You pay in total', pl: 'Zapłacisz łącznie', hu: 'Összesen fizet' },
  'mortgage.ofWhichPrincipal': { sk: 'Z toho hlavnica', cs: 'Z toho jistina', en: 'Of which principal', pl: 'W tym kapitał', hu: 'Ebből tőke' },
  'mortgage.ofWhichInterest': { sk: 'Z toho úroky', cs: 'Z toho úroky', en: 'Of which interest', pl: 'W tym odsetki', hu: 'Ebből kamat' },
  'mortgage.remainingY1': { sk: 'Zostávajúci dlh po 1. roku', cs: 'Zbývající dluh po 1. roce', en: 'Remaining debt after year 1', pl: 'Pozostały dług po 1. roku', hu: 'Fennmaradó tartozás 1 év után' },
  'mortgage.amortShow': { sk: '▶ Zobraziť amortizačnú tabuľku', cs: '▶ Zobrazit amortizační tabulku', en: '▶ Show amortization table', pl: '▶ Pokaż tabelę amortyzacji', hu: '▶ Amortizációs tábla megjelenítése' },
  'mortgage.amortHide': { sk: '▼ Skryť amortizačnú tabuľku', cs: '▼ Skrýt amortizační tabulku', en: '▼ Hide amortization table', pl: '▼ Ukryj tabelę amortyzacji', hu: '▼ Amortizációs tábla elrejtése' },
  'mortgage.amortTitle': { sk: 'Amortizačná tabuľka (ročný prehľad)', cs: 'Amortizační tabulka (roční přehled)', en: 'Amortization table (yearly)', pl: 'Tabela amortyzacji (rocznie)', hu: 'Amortizációs tábla (éves)' },
  'mortgage.thYear': { sk: 'Rok', cs: 'Rok', en: 'Year', pl: 'Rok', hu: 'Év' },
  'mortgage.thBalance': { sk: 'Zostatok', cs: 'Zůstatek', en: 'Balance', pl: 'Saldo', hu: 'Egyenleg' },

  // ============ solar body ============
  'solar.consumption': { sk: 'Ročná spotreba elektriny (kWh)', cs: 'Roční spotřeba elektřiny (kWh)', en: 'Annual electricity consumption (kWh)', pl: 'Roczne zużycie energii (kWh)', hu: 'Éves áramfogyasztás (kWh)' },
  'solar.rate': { sk: 'Cena elektriny (€/kWh)', cs: 'Cena elektřiny (€/kWh)', en: 'Electricity price (€/kWh)', pl: 'Cena energii (€/kWh)', hu: 'Áram ára (€/kWh)' },
  'solar.includeBattery': { sk: 'Zahrnúť batériové úložisko', cs: 'Zahrnout bateriové úložiště', en: 'Include battery storage', pl: 'Uwzględnij magazyn energii', hu: 'Akkumulátoros tárolás beszámítása' },
  'solar.payback': { sk: 'Návratnosť investície', cs: 'Návratnost investice', en: 'Payback period', pl: 'Zwrot z inwestycji', hu: 'Megtérülési idő' },
  'solar.estSubsidy': { sk: 'Odhadovaná dotácia', cs: 'Odhadovaná dotace', en: 'Estimated subsidy', pl: 'Szacowana dotacja', hu: 'Becsült támogatás' },
  'solar.netCost': { sk: 'Cena po dotácii', cs: 'Cena po dotaci', en: 'Cost after subsidy', pl: 'Cena po dotacji', hu: 'Ár támogatás után' },
  'solar.annualSavings': { sk: 'Ročná úspora', cs: 'Roční úspora', en: 'Annual savings', pl: 'Roczne oszczędności', hu: 'Éves megtakarítás' },
  'solar.recommendedPower': { sk: 'Odporúčaný výkon', cs: 'Doporučený výkon', en: 'Recommended capacity', pl: 'Zalecana moc', hu: 'Ajánlott teljesítmény' },
  'solar.battery': { sk: 'Batéria', cs: 'Baterie', en: 'Battery', pl: 'Akumulator', hu: 'Akkumulátor' },
  'solar.annualProduction': { sk: 'Ročná výroba', cs: 'Roční výroba', en: 'Annual production', pl: 'Roczna produkcja', hu: 'Éves termelés' },
  'solar.coverage': { sk: 'Pokrytie spotreby', cs: 'Pokrytí spotřeby', en: 'Consumption covered', pl: 'Pokrycie zużycia', hu: 'Fogyasztás lefedése' },
  'solar.totalCost': { sk: 'Celková cena systému', cs: 'Celková cena systému', en: 'Total system cost', pl: 'Całkowity koszt systemu', hu: 'Teljes rendszerköltség' },
  'solar.savings30': { sk: 'Úspora za 30 rokov', cs: 'Úspora za 30 let', en: 'Savings over 30 years', pl: 'Oszczędności przez 30 lat', hu: 'Megtakarítás 30 év alatt' },
  'solar.co2': { sk: 'Zníženie CO₂ ročne', cs: 'Snížení CO₂ ročně', en: 'CO₂ reduction per year', pl: 'Redukcja CO₂ rocznie', hu: 'Éves CO₂-csökkentés' },

  // ============ calculator page titles (subtitles reuse calc.<id>.desc) ============
  'mortgage.title': { sk: '🏠 Kalkulačka hypotéky', cs: '🏠 Hypoteční kalkulačka', en: '🏠 Mortgage calculator', pl: '🏠 Kalkulator kredytu hipotecznego', hu: '🏠 Jelzáloghitel-kalkulátor' },
  'solar.title': { sk: '☀️ Kalkulačka fotovoltiky 2026 – dotácia a návratnosť', cs: '☀️ Kalkulačka fotovoltaiky 2026 – dotace a návratnost', en: '☀️ Solar PV calculator 2026 – subsidy & payback', pl: '☀️ Kalkulator fotowoltaiki 2026 – dotacja i zwrot', hu: '☀️ Napelem-kalkulátor 2026 – támogatás és megtérülés' },
  'energy.title': { sk: '⚡ Kalkulačka nákladov na energiu', cs: '⚡ Kalkulačka nákladů na energie', en: '⚡ Energy cost calculator', pl: '⚡ Kalkulator kosztów energii', hu: '⚡ Energiaköltség-kalkulátor' },
  'freelancer.title': { sk: '💼 Kalkulačka daní SZČO', cs: '💼 Kalkulačka daní OSVČ', en: '💼 Freelancer tax calculator', pl: '💼 Kalkulator podatków dla samozatrudnionych', hu: '💼 Egyéni vállalkozói adókalkulátor' },
  'loan.title': { sk: '💰 Kalkulačka úveru', cs: '💰 Kalkulačka úvěru', en: '💰 Loan calculator', pl: '💰 Kalkulator kredytu', hu: '💰 Hitelkalkulátor' },
  'pension.title': { sk: '💼 Kalkulačka dôchodku', cs: '💼 Kalkulačka důchodu', en: '💼 Pension calculator', pl: '💼 Kalkulator emerytury', hu: '💼 Nyugdíjkalkulátor' },
  'vat.title': { sk: '🧾 DPH Kalkulačka', cs: '🧾 Kalkulačka DPH', en: '🧾 VAT calculator', pl: '🧾 Kalkulator VAT', hu: '🧾 ÁFA-kalkulátor' },
  'bmi.title': { sk: '⚖️ Kalkulačka BMI', cs: '⚖️ BMI kalkulačka', en: '⚖️ BMI calculator', pl: '⚖️ Kalkulator BMI', hu: '⚖️ BMI-kalkulátor' },
  'bmr.title': { sk: '🔥 BMR Kalkulačka - Bazálny metabolizmus', cs: '🔥 BMR kalkulačka – bazální metabolismus', en: '🔥 BMR calculator – basal metabolism', pl: '🔥 Kalkulator BMR – metabolizm podstawowy', hu: '🔥 BMR-kalkulátor – alapanyagcsere' },
  'basic.title': { sk: '🧮 Základná kalkulačka', cs: '🧮 Základní kalkulačka', en: '🧮 Basic calculator', pl: '🧮 Kalkulator podstawowy', hu: '🧮 Alap kalkulátor' },
  'percentage.title': { sk: '🔢 Kalkulačka percent a matematiky', cs: '🔢 Kalkulačka procent a matematiky', en: '🔢 Percentage & math calculator', pl: '🔢 Kalkulator procentów i matematyki', hu: '🔢 Százalék- és matematikai kalkulátor' },
  'payment.title': { sk: '💰 Kalkulačka splátok úveru', cs: '💰 Kalkulačka splátek úvěru', en: '💰 Loan payment calculator', pl: '💰 Kalkulator rat kredytu', hu: '💰 Hiteltörlesztési kalkulátor' },
  'pregnancy.title': { sk: '🤰 Kalkulačka tehotenstva', cs: '🤰 Těhotenská kalkulačka', en: '🤰 Pregnancy calculator', pl: '🤰 Kalkulator ciąży', hu: '🤰 Terhességi kalkulátor' },
  'parental.title': { sk: '👶 Rodičovský príspevok kalkulačka', cs: '👶 Kalkulačka rodičovského příspěvku', en: '👶 Parental benefit calculator', pl: '👶 Kalkulator zasiłku rodzicielskiego', hu: '👶 Szülői ellátás kalkulátor' },
  'sickleave.title': { sk: '🏥 Kalkulačka pracovnej neschopnosti (PN)', cs: '🏥 Kalkulačka pracovní neschopnosti', en: '🏥 Sick leave calculator', pl: '🏥 Kalkulator zwolnienia chorobowego', hu: '🏥 Táppénzkalkulátor' },
  'vacation.title': { sk: '🏖️ Kalkulačka dovolenky', cs: '🏖️ Kalkulačka dovolené', en: '🏖️ Vacation days calculator', pl: '🏖️ Kalkulator urlopu', hu: '🏖️ Szabadságkalkulátor' },
  'fuelcost.title': { sk: '🚗 Kalkulačka spotreby auta', cs: '🚗 Kalkulačka spotřeby auta', en: '🚗 Fuel cost calculator', pl: '🚗 Kalkulator spalania auta', hu: '🚗 Üzemanyagköltség-kalkulátor' },
  'inflation.title': { sk: '📉 Kalkulačka inflácie', cs: '📉 Kalkulačka inflace', en: '📉 Inflation calculator', pl: '📉 Kalkulator inflacji', hu: '📉 Inflációs kalkulátor' },
  'roi.title': { sk: '📊 ROI Kalkulačka', cs: '📊 ROI kalkulačka', en: '📊 ROI calculator', pl: '📊 Kalkulator ROI', hu: '📊 ROI-kalkulátor' },
  'hoursworked.title': { sk: '⏰ Kalkulačka odpracovaných hodín', cs: '⏰ Kalkulačka odpracovaných hodin', en: '⏰ Hours worked calculator', pl: '⏰ Kalkulator przepracowanych godzin', hu: '⏰ Ledolgozott órák kalkulátor' },
  'carleasing.title': { sk: '🚗 Kalkulačka lízingu auta', cs: '🚗 Kalkulačka leasingu auta', en: '🚗 Car leasing calculator', pl: '🚗 Kalkulator leasingu samochodu', hu: '🚗 Autólízing-kalkulátor' },
  'areavolume.title': { sk: '📐 Kalkulačka plochy a objemu', cs: '📐 Kalkulačka plochy a objemu', en: '📐 Area & volume calculator', pl: '📐 Kalkulator pola i objętości', hu: '📐 Terület- és térfogatkalkulátor' },
  'splitbill.title': { sk: '🧾 Kalkulačka rozdelenia účtu', cs: '🧾 Kalkulačka rozdělení účtu', en: '🧾 Bill splitting calculator', pl: '🧾 Kalkulator podziału rachunku', hu: '🧾 Számlamegosztó kalkulátor' },
  'unitconverter.title': { sk: '🔢 Prevod jednotiek', cs: '🔢 Převod jednotek', en: '🔢 Unit converter', pl: '🔢 Konwerter jednostek', hu: '🔢 Mértékegység-átváltó' },
};

function pivot(): Record<Locale, TranslationDict> {
  const out = {} as Record<Locale, TranslationDict>;
  for (const loc of SUPPORTED_LOCALES) out[loc] = {};
  for (const [key, map] of Object.entries(ENTRIES)) {
    for (const loc of SUPPORTED_LOCALES) out[loc][key] = map[loc];
  }
  return out;
}

export const CALC_TRANSLATIONS: Record<Locale, TranslationDict> = pivot();
