import { Locale } from '../locales';

export const ENTRIES: Record<string, Record<Locale, string>> = {
  'pregnancy.kw1': { sk: 'Termín pôrodu', cs: 'Termín porodu', en: 'Due date', pl: 'Termin porodu', hu: 'Szülés várható időpontja' },
  'pregnancy.kw2': { sk: 'Týždne tehotenstva', cs: 'Týdny těhotenství', en: 'Weeks of pregnancy', pl: 'Tygodnie ciąży', hu: 'Terhességi hetek' },
  'pregnancy.kw3': { sk: 'Trimestre', cs: 'Trimestry', en: 'Trimesters', pl: 'Trymestry', hu: 'Trimeszterek' },

  'pregnancy.inputTitle': { sk: 'Výpočet termínu pôrodu', cs: 'Výpočet termínu porodu', en: 'Due date calculation', pl: 'Obliczenie terminu porodu', hu: 'Szülési időpont kiszámítása' },

  'pregnancy.methodLmp': { sk: 'Z poslednej menštruácie', cs: 'Z poslední menstruace', en: 'From last menstrual period', pl: 'Z ostatniej miesiączki', hu: 'Utolsó menstruáció alapján' },
  'pregnancy.methodLmpDesc': { sk: 'Najčastejšia metóda', cs: 'Nejčastější metoda', en: 'Most common method', pl: 'Najczęstsza metoda', hu: 'Leggyakoribb módszer' },
  'pregnancy.methodConception': { sk: 'Z dátumu počatia', cs: 'Z data početí', en: 'From conception date', pl: 'Z daty poczęcia', hu: 'Fogantatás dátuma alapján' },
  'pregnancy.methodConceptionDesc': { sk: 'Ak poznáte presný dátum', cs: 'Pokud znáte přesné datum', en: 'If you know the exact date', pl: 'Jeśli znasz dokładną datę', hu: 'Ha ismeri a pontos dátumot' },

  'pregnancy.lmpLabel': { sk: 'Prvý deň poslednej menštruácie', cs: 'První den poslední menstruace', en: 'First day of last menstrual period', pl: 'Pierwszy dzień ostatniej miesiączki', hu: 'Az utolsó menstruáció első napja' },
  'pregnancy.lmpTooltip': { sk: 'Prvý deň vašej poslednej menštruácie', cs: 'První den vaší poslední menstruace', en: 'The first day of your last menstrual period', pl: 'Pierwszy dzień Twojej ostatniej miesiączki', hu: 'Az utolsó menstruációja első napja' },
  'pregnancy.conceptionLabel': { sk: 'Dátum počatia (ovulácie)', cs: 'Datum početí (ovulace)', en: 'Date of conception (ovulation)', pl: 'Data poczęcia (owulacji)', hu: 'A fogantatás (peteérés) dátuma' },
  'pregnancy.conceptionTooltip': { sk: 'Približný dátum počatia alebo ovulácie', cs: 'Přibližné datum početí nebo ovulace', en: 'Approximate date of conception or ovulation', pl: 'Przybliżona data poczęcia lub owulacji', hu: 'A fogantatás vagy peteérés hozzávetőleges dátuma' },
  'pregnancy.currentDateLabel': { sk: 'Aktuálny dátum', cs: 'Aktuální datum', en: 'Current date', pl: 'Aktualna data', hu: 'Aktuális dátum' },
  'pregnancy.currentDateTooltip': { sk: 'Dátum, ku ktorému počítame (predvolene dnes)', cs: 'Datum, ke kterému počítáme (výchozí dnes)', en: 'The date we calculate to (today by default)', pl: 'Data, do której liczymy (domyślnie dziś)', hu: 'A dátum, amelyre számolunk (alapértelmezetten ma)' },

  'pregnancy.howTitle': { sk: '💡 Ako to funguje?', cs: '💡 Jak to funguje?', en: '💡 How does it work?', pl: '💡 Jak to działa?', hu: '💡 Hogyan működik?' },
  'pregnancy.howLmp': { sk: 'Termín pôrodu sa počíta podľa Naegelovho pravidla: prvý deň poslednej menštruácie + 280 dní (40 týždňov).', cs: 'Termín porodu se počítá podle Naegelova pravidla: první den poslední menstruace + 280 dní (40 týdnů).', en: "The due date is calculated using Naegele's rule: the first day of the last menstrual period + 280 days (40 weeks).", pl: 'Termin porodu oblicza się według reguły Naegelego: pierwszy dzień ostatniej miesiączki + 280 dni (40 tygodni).', hu: 'A szülés időpontját a Naegele-szabály szerint számítjuk: az utolsó menstruáció első napja + 280 nap (40 hét).' },
  'pregnancy.howConception': { sk: 'Termín pôrodu je 266 dní (38 týždňov) od dátumu počatia. Počatie zvyčajne nastáva 14 dní po začiatku poslednej menštruácie.', cs: 'Termín porodu je 266 dní (38 týdnů) od data početí. Početí obvykle nastává 14 dní po začátku poslední menstruace.', en: 'The due date is 266 days (38 weeks) from the date of conception. Conception usually occurs 14 days after the start of the last menstrual period.', pl: 'Termin porodu to 266 dni (38 tygodni) od daty poczęcia. Poczęcie zwykle następuje 14 dni po rozpoczęciu ostatniej miesiączki.', hu: 'A szülés időpontja a fogantatás dátumától számított 266 nap (38 hét). A fogantatás általában 14 nappal az utolsó menstruáció kezdete után történik.' },

  'pregnancy.resultsTitle': { sk: 'Výsledky', cs: 'Výsledky', en: 'Results', pl: 'Wyniki', hu: 'Eredmények' },
  'pregnancy.dueDateLabel': { sk: 'Predpokladaný termín pôrodu', cs: 'Předpokládaný termín porodu', en: 'Estimated due date', pl: 'Przewidywany termin porodu', hu: 'Várható szülési időpont' },
  'pregnancy.pastDue': { sk: '⚠️ Po termíne', cs: '⚠️ Po termínu', en: '⚠️ Past due', pl: '⚠️ Po terminie', hu: '⚠️ Túlhordás' },

  'pregnancy.progressTitle': { sk: 'Aktuálny stav tehotenstva', cs: 'Aktuální stav těhotenství', en: 'Current pregnancy status', pl: 'Aktualny stan ciąży', hu: 'A terhesség aktuális állapota' },
  'pregnancy.weeksLabel': { sk: 'týždňov', cs: 'týdnů', en: 'weeks', pl: 'tygodni', hu: 'hét' },
  'pregnancy.daysLabel': { sk: 'dní', cs: 'dní', en: 'days', pl: 'dni', hu: 'nap' },
  'pregnancy.progressCompleted': { sk: '% tehotenstva dokončené', cs: '% těhotenství dokončeno', en: '% of pregnancy completed', pl: '% ciąży ukończone', hu: '%-a a terhességnek eltelt' },
  'pregnancy.daysToBirth': { sk: 'dní do pôrodu', cs: 'dní do porodu', en: 'days until birth', pl: 'dni do porodu', hu: 'nap a szülésig' },
  'pregnancy.daysPregnant': { sk: 'dní v tehotenstve', cs: 'dní v těhotenství', en: 'days pregnant', pl: 'dni w ciąży', hu: 'nap terhesen' },

  'pregnancy.trimesterProgressLabel': { sk: 'Pokrok v trimestrze:', cs: 'Pokrok v trimestru:', en: 'Progress in trimester:', pl: 'Postęp w trymestrze:', hu: 'Előrehaladás a trimeszterben:' },
  'pregnancy.datesTitle': { sk: 'Dôležité dátumy', cs: 'Důležitá data', en: 'Important dates', pl: 'Ważne daty', hu: 'Fontos dátumok' },
  'pregnancy.lastMenstruation': { sk: 'Posledná menštruácia:', cs: 'Poslední menstruace:', en: 'Last menstrual period:', pl: 'Ostatnia miesiączka:', hu: 'Utolsó menstruáció:' },
  'pregnancy.approxConception': { sk: 'Približné počatie:', cs: 'Přibližné početí:', en: 'Approximate conception:', pl: 'Przybliżone poczęcie:', hu: 'Hozzávetőleges fogantatás:' },
  'pregnancy.dueDateShort': { sk: 'Termín pôrodu:', cs: 'Termín porodu:', en: 'Due date:', pl: 'Termin porodu:', hu: 'Szülés időpontja:' },

  'pregnancy.trimester1': { sk: 'Prvý trimester', cs: 'První trimestr', en: 'First trimester', pl: 'Pierwszy trymestr', hu: 'Első trimeszter' },
  'pregnancy.trimester2': { sk: 'Druhý trimester', cs: 'Druhý trimestr', en: 'Second trimester', pl: 'Drugi trymestr', hu: 'Második trimeszter' },
  'pregnancy.trimester3': { sk: 'Tretí trimester', cs: 'Třetí trimestr', en: 'Third trimester', pl: 'Trzeci trymestr', hu: 'Harmadik trimeszter' },
  'pregnancy.trimWeeks1': { sk: '1-12 týždňov', cs: '1-12 týdnů', en: '1-12 weeks', pl: '1-12 tygodni', hu: '1-12. hét' },
  'pregnancy.trimWeeks2': { sk: '13-26 týždňov', cs: '13-26 týdnů', en: '13-26 weeks', pl: '13-26 tygodni', hu: '13-26. hét' },
  'pregnancy.trimWeeks3': { sk: '27-40 týždňov', cs: '27-40 týdnů', en: '27-40 weeks', pl: '27-40 tygodni', hu: '27-40. hét' },
  'pregnancy.trimDesc1': { sk: 'Embryo sa vyvíja, tvoria sa základné orgány', cs: 'Embryo se vyvíjí, tvoří se základní orgány', en: 'The embryo develops, basic organs are forming', pl: 'Zarodek się rozwija, tworzą się podstawowe narządy', hu: 'Az embrió fejlődik, kialakulnak az alapvető szervek' },
  'pregnancy.trimDesc2': { sk: 'Plod rastie, začína sa pohybovať', cs: 'Plod roste, začíná se hýbat', en: 'The fetus grows and begins to move', pl: 'Płód rośnie i zaczyna się poruszać', hu: 'A magzat növekszik és mozogni kezd' },
  'pregnancy.trimDesc3': { sk: 'Plod dospeje, pripravuje sa na pôrod', cs: 'Plod dozrává, připravuje se na porod', en: 'The fetus matures and prepares for birth', pl: 'Płód dojrzewa i przygotowuje się do porodu', hu: 'A magzat érik és felkészül a szülésre' },

  'pregnancy.errLmp': { sk: 'Prosím zadajte dátum poslednej menštruácie', cs: 'Zadejte prosím datum poslední menstruace', en: 'Please enter the date of your last menstrual period', pl: 'Podaj datę ostatniej miesiączki', hu: 'Kérjük, adja meg az utolsó menstruáció dátumát' },
  'pregnancy.errConception': { sk: 'Prosím zadajte dátum počatia', cs: 'Zadejte prosím datum početí', en: 'Please enter the date of conception', pl: 'Podaj datę poczęcia', hu: 'Kérjük, adja meg a fogantatás dátumát' },

  'pregnancy.navBmi': { sk: '📊 BMI kalkulačka →', cs: '📊 BMI kalkulačka →', en: '📊 BMI calculator →', pl: '📊 Kalkulator BMI →', hu: '📊 BMI-kalkulátor →' },
  'pregnancy.navParental': { sk: '👶 Rodičovský príspevok →', cs: '👶 Rodičovský příspěvek →', en: '👶 Parental allowance →', pl: '👶 Zasiłek rodzicielski →', hu: '👶 Szülői támogatás →' },
};
