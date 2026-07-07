# Kalkulačky.sk — Komplexný audit projektu

**Dátum:** 2026-07-07
**Rozsah:** Django 5 + DRF backend (`django_calculators/`) + Angular 21 SSR frontend (`frontend/`)
**Metóda:** 6 paralelných statických auditov (i18n/preklady, FE↔BE API kompatibilita, mobil/responzivita + dark mode, funkcionalita/kompletnosť, backend korektnosť/bezpečnosť, legal/GDPR + embed/blog). Python ani Node nie sú na tomto stroji nainštalované → statická revízia; testy/build sa nedali spustiť.

Legenda stavu: ✅ opravené v tejto session · 🔜 odporúčané (nezmenené) · ⚠️ vyžaduje manuálny vstup (dáta prevádzkovateľa).

---

## 0. Zhrnutie — kritické (HIGH) nálezy

| # | Oblasť | Nález | Stav |
|---|--------|-------|------|
| 1 | Auth | Odhlásenie pri KAŽDOM načítaní stránky (`/auth/check/` volané bez tokenu → vyčistí tokeny) | ✅ |
| 2 | Auth | Súbežné 401 → paralelný refresh → blacklist rotácie → nútené odhlásenie | ✅ (single-flight) |
| 3 | Bezpečnosť | IDOR: ktokoľvek číta/mení/maže anonymné uložené výpočty podľa `pk` | ✅ |
| 4 | Backend | Blog detail 500-uje na každý request (`increment_views()` neexistuje) | ✅ |
| 5 | Backend | CPU DoS: neohraničený `loan_term_years` v payment kalkulačke → obrovská Decimal mocnina | ✅ |
| 6 | Bezpečnosť | Password validátory nakonfigurované, ale nikdy nevolané (akceptuje `12345678`) | ✅ |
| 7 | API | Split-bill zobrazuje 0.00 € (FE číta `original_amount`/`subtotal`, BE vracia `total_amount`/`amount_before_tip`) | ✅ |
| 8 | API | CZ hypotéka 400-uje (loan_amount > 1 000 000 cap, chýba `country`) | ✅ |
| 9 | Config | `environment.prod.ts` má placeholder `yourdomain.com/api` | ✅ |
| 10 | i18n | `common.loading` kolízia → všetky kalkulačky zobrazujú "Loading" namiesto "Počítam…" | ✅ |
| 11 | Mobil/Dark | Systémová chyba dark módu: globálny prepínač farieb nepozná ~30 komponentov → neviditeľné nadpisy/hodnoty | ✅ (globálny patch) |
| 12 | Mobil | 3 stránky rozbité na mobile (parental-benefit, pregnancy, vacation) | ✅ |
| 13 | UX | Login return-URL nesúlad (`redirect` vs `returnUrl`) → používateľ sa nevráti | ✅ |
| 14 | Ops | Notifikácie: overdue z minulých dní preskočené (porovnanie iba času dňa) | ✅ |
| 15 | SEO | Blog sa nerenderuje v SSR + blog-detail bez SEO meta | ✅ |
| 16 | Legal | Placeholders `[DOPLŇTE]` v privacy/terms (identita prevádzkovateľa) | ⚠️ |

---

## 1. i18n / Preklady

**Pokrytie kľúčov: 100 %** — žiadne chýbajúce kľúče v žiadnom z 5 jazykov (sk/cs/en/pl/hu). Žiadne "SK text v EN" hodnoty. Problém i18n nie je kvalita prekladu, ale **pokrytie UI** (veľa hardkódovaných reťazcov).

- ✅ **[HIGH]** `common.loading` kolízia — `translations.calc.ts` predefinoval kľúč na "Načítavam/Loading" a vyhral merge → spinnery kalkulačiek. Rozdelené na `common.loading` (Počítam…/Calculating…) a `common.loadingData` (Načítavam/Loading); dátové načítania (dashboard, salary-value-page, forgot/reset-password) presmerované na nový kľúč.
- 🔜 **[HIGH]** ~22 šablón kalkulačiek má takmer celé UI hardkódované po slovensky (labels, buttons, selecty, výsledky) — pod cs/en/pl/hu sa mení len "chrome". Najhoršie: vacation, hours-worked, freelancer-tax, inflation, payment, unit-converter, energy, percentage, split-bill, sick-leave. Vzor localizácie existuje v salary/mortgage/solar. **Odporúčanie:** migrovať UI reťazce do `translations.calc.ts`.
- 🔜 **[HIGH]** Auth/účet stránky (login, register, user-profile) majú **nula** i18n — 0 použití pipe. Rozšíriť namespace `auth.*`.
- 🔜 **[MED]** SSR je locale-slepé — nečíta `?lang=` na serveri → SSR vždy renderuje sk; hreflang alternatívy servírujú SK HTML; `<html lang>` ostáva sk. Riešiť cez `REQUEST` token v `app.config.server.ts`.
- 🔜 **[MED]** `seo.service.ts:50` `og:locale` natvrdo `sk_SK`; `:99` JSON-LD `inLanguage: 'sk'`; canonical vs hreflang nesúlad; 18× `seo.apply()` posiela SK titulky aj pre `?lang=en`.
- 🔜 **[MED]** Mena/čísla: natvrdo `€` v 22 šablónach a `'sk-SK'` formátovanie na viacerých miestach — potrebný zdieľaný `formatCurrency/formatDate` čítajúci `getCountryParams(locale).numberLocale`.
- 🔜 **[MED/HIGH]** API chyby zobrazené natvrdo (backend SK hlášky + DRF EN built-ins → jazykový mix). Riešiť stabilnými error-kódmi + FE mapou, alebo `Accept-Language` + `LocaleMiddleware`.
- 🔜 **[LOW]** date-picker natvrdo SK (mesiace/dni); mŕtve SK dáta polia v navbar/home; chýba CI test na pokrytie kľúčov.

## 2. Frontend ↔ Backend API kompatibilita

**Endpoint mapa: bez 404 nesúladov.** Payloady kalkulačiek verifikované ako zhodné okrem nižšie.

- ✅ **[HIGH]** Auto-logout (viď §0/#1) — interceptor prepísaný: Bearer sa pripája na všetky autentifikované requesty (vrátane `/auth/check/`), verejné auth cesty na explicitnom zozname.
- ✅ **[HIGH]** Refresh race (#2) — `refreshToken()` je teraz single-flight (`shareReplay`); zlyhaný refresh → `forceLogout()` bez HTTP volania.
- ✅ **[HIGH]** Split-bill 0.00 € (#7) — model + šablóna zosúladené na `total_amount`/`amount_before_tip`.
- ✅ **[HIGH]** CZ hypotéka (#8) — cap zdvihnutý (mena-agnostická matematika), pridané voliteľné `country`, view ho vyfiltruje pred volaním služby.
- ✅ **[HIGH]** `environment.prod.ts` apiUrl → `https://kalkulacky.sk/api`.
- ✅ **[MED]** car-leasing `term_months` — serializer zosúladený s UI (max 120).
- 🔜 **[MED]** SSR base URL natvrdo `http://backend:8000/api` v 6 službách — mimo Dockera SSR fetch zlyhá; spraviť env-driven.
- 🔜 **[LOW]** Fantómové polia v TS interface (VAT `reduced`, area-volume, parental-benefit, mŕtvy `BlogListResponse`) — vyčistené split-bill; zvyšok 🔜.
- 🔜 **[MED]** Osirelý endpoint `saved-calculations/<id>/notifications/` (nevolaný). `GET /api/calculators/` nevolaný.
- ✅ **Error handling (čiastočne):** tiché delete operácie v dashboarde (výpočet, pripomienka, sporiaci cieľ) majú teraz error vetvu + lokalizovaný banner (`common.actionError`). 🔜 zostáva: globálny 429-aware `parseDrfError()` a error vetvy inde (favorites.add, login 429 hláška).

## 3. Mobil / Responzivita + Dark mode

**Dominantný defekt = dark mode** (nie layout). Globálny prepínač (`styles.css`) prepínal fixný zoznam tried + všetky h1–h5 na svetlé `!important`, ale nepoznal ~30 komponentov → (a) svetlé nadpisy na bielych kartách, (b) tmavé labels na tmavých kartách (chýbalo globálne pravidlo pre `label`/`td`).

- ✅ **[HIGH] G1** — `styles.css` rozšírený: +~45 tried kariet, globálne `label`/`td`/`strong` dark pravidlá, tmavé inset pozadia pre vnútorné riadky, opravy nadpisov na pastelových callout kartách.
- ✅ **[HIGH] G2** — "biele" tlačidlá (preset/toggle/method/benchmark…) dostali explicitnú dark plochu + text; aktívny stav re-asertovaný akcentom.
- ✅ **[HIGH]** blog-detail: telo článku (`.blog-html-content`, `[innerHTML]`) štýlované z globálneho CSS (dark text, scrollovateľné tabuľky, `overflow-wrap`).
- ✅ **[HIGH]** 3 rozbité layouty: parental-benefit (grid `1fr` ≤640px), pregnancy (trimester segmenty 56px, wrap), vacation (nav-links wrap, reálny ≤640px breakpoint).
- ✅ **[MED] G3** — globálne `input,select,textarea { font-size:16px }` ≤700px (iOS zoom).
- ✅ **[MED]** navbar `.mobile-overlay` nemal ŽIADNE CSS → pridaný backdrop (`.visible`); dark farby mobilných odkazov.
- ✅ **[MED] G5** — `.blog-html-content table` pridané do mobilnej scroll-siete.
- 🔜 **[MED] G4** — tap-targety < 44px (hviezdičky ratingu, date-picker, steppers, hamburger) — plošný sweep zostáva.
- 🔜 **[LOW]** kozmetika: svetlé chips/pills v dark, `100dvh` mobilné menu, date-picker `max-height`, mŕtve `html[data-theme=dark]` selektory vo vnútri komponentov (encapsulation) → `:host-context()`.

## 4. Funkcionalita / Kompletnosť

- ✅ **[MED]** `car-insurance` chýbal na home mriežke (bol v route + navbar) — pridaný.
- ✅ **[HIGH]** Login return-URL nesúlad — login teraz akceptuje `returnUrl` aj `redirect`.
- ✅ **[HIGH]** Blog SSR + SEO (viď §6).
- 🔜 **[HIGH]** ~16 kalkulačiek + home bez per-page SEO meta — aplikovať existujúci `SeoService` vzor plošne.
- 🔜 **[HIGH]** Statický `sitemap.xml` bez blog URL, bez hreflang/lastmod — generovať dynamicky z registry + blog API.
- 🔜 **[HIGH]** PWA neinštalovateľné — chýbajú 192/512/maskable ikony (len favicon.ico). *(vyžaduje binárne assety)*
- 🔜 **[MED]** backend `CalculatorListView` rozsync (mŕtve `fees`/`travel-cost`, chýba ~15 kalkulačiek, stale `implemented:False`) — regenerovať z jedného registra.
- 🔜 **[MED]** footer bez odkazov na kalkulačky (stratený SEO interný linking); `/energia` hub mimo hlavnej navigácie.
- 🔜 **[MED]** chýba "načítať uložený výpočet späť do kalkulačky" (URL-state) a GDPR export dát.

### Odporúčané nové funkcie (najvyššia hodnota / malý-stredný effort)
1. Reverzná mzda net→gross ("chcem X € čistého").
2. Kalkulačka zloženého úročenia / rast investície.
3. Zdieľanie/tlač/PDF výsledku s URL-state vstupov.
4. Porovnanie hypoték/úverov (2–3 ponuky) + "poplatky pri kúpe nehnuteľnosti".

## 5. Backend — korektnosť / bezpečnosť

- ✅ **[HIGH]** IDOR na anonymné `SavedCalculation` (#3) — nový helper `check_calculation_access()`: vlastnené → len majiteľ; anonymné → vyžaduje zhodný `session_key`. Použité v GET/PUT/DELETE detail + notifications.
- ✅ **[HIGH]** Blog detail 500 (#4) — pridaná `BlogPost.increment_views()` (atomický `F()` update).
- ✅ **[HIGH]** Payment DoS (#5) — `loan_term_years max=100`, `annual_interest_rate max=1000`.
- ✅ **[MED]** Password validátory (#6) — `validate_password()` zapojené do register/change/reset serializerov.
- ✅ **[MED]** Notifikácie #2 (#14) — dátumové porovnanie opravené: `date<today OR (date=today AND time<=now)`.
- ✅ **[LOW]** `DataReport.message` cap 5000 znakov; `print()` → `logger.error()` v generovaní notifikácií.
- 🔜 **[MED]** NČZD phase-out (`salary_calculator.py:127`) — chýba taper pre vysoké príjmy (net nadhodnotený). *Doménová zmena — implementovať s aktualizáciou testov.*
- 🔜 **[LOW]** SZČO vymeriavací základ (`freelancer_tax_calculator.py:140`) — overiť voči SK pravidlám (možné nadhodnotenie odvodov). *Overiť pred zmenou.*
- 🔜 **[LOW]** stale komentáre v `config_variables.py:196` a `freelancer_tax_calculator.py:39`; fantómové 30/35% brackety vo `rates` output salary.
- 🔜 **[MED]** validácia: `ScheduledNotification.message`/`SavedCalculation.params` bez limitu; split-bill items bez schémy (KeyError→500); vacation dni bez `min_value=0`.
- 🔜 **[MED]** GDPR: `Lead`/`DataReport`/`AffiliateClick` (email/IP) sa nemazú pri zrušení účtu; `PageView` rastie bez limitu (retention job).
- 🔜 **[MED]** `MyDashboardView` 3× extra COUNT query (N+1).
- 🔜 **[LOW]** `log_auth_event` loguje útočníkom dodaný email bez orezania (log injection); 500 body vracia `str(e)`; `settings.py:307` osobný Gmail default.

## 6. Legal / GDPR + Embed + Blog

- ✅ **[HIGH]** Blog SSR — odstránené `isPlatformBrowser` guardy v blog-list/blog-detail → renderuje sa na serveri.
- ✅ **[HIGH]** blog-detail SEO — zapojený `SeoService` (title/description/canonical/OG/hreflang z `post`); blog-list má tiež SEO.
- ⚠️ **[HIGH]** Placeholders `[DOPLŇTE: obchodné meno, IČO, sídlo]` + viditeľné ⚠️ bannery v `privacy-policy.component.ts` a `terms.component.ts` — **vyžaduje reálne údaje prevádzkovateľa** (nemôžem doplniť).
- 🔜 **[MED]** Granulárny consent: `consent.service.save(analytics, ads)` existuje, ale žiadne UI ho nevolá (len všetko-alebo-nič).
- 🔜 **[MED]** Affiliate URL placeholders `example.com` (`monetization.config.ts`).
- 🔜 **[MED]** Chýba GDPR export endpoint, hoci privacy policy sľubuje prenosnosť.
- 🔜 **[MED]** Embed: len 7 kalkulačiek embeddable; snippet UI len na 3 stránkach; `server.ts` bez security headerov (clickjacking celého webu).
- 🔜 **[MED]** Blog SK-only (BlogPost bez `language` poľa).

## Konsenzus + duplicity naprieč auditmi (potvrdené 2+ agentmi)
- Auto-logout / auth flow (API audit).
- `environment.prod.ts` placeholder (API + legal + funkcionalita).
- blog-detail bez SEO + nie SSR (funkcionalita + legal + mobil).
- Legal placeholders (legal + funkcionalita).
- Embed obmedzenia (legal + funkcionalita).

---

## Poznámka k overeniu
Python ani Node nie sú na stroji dostupné, takže `python manage.py test` ani `npm run build`/`npm test` sa nedali spustiť. Backendové zmeny sú konzervatívne a zosúladené s existujúcimi testami (heslá v testoch sú silné → validátory neprepadnú). Po nainštalovaní toolingu spustiť:
```
cd django_calculators && python manage.py test calculators users
cd frontend && npm run build && npm test
```
