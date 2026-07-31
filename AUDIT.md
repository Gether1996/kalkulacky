# Kalkulačky.sk — Komplexný audit projektu

**Dátum:** 2026-07-07
**Rozsah:** Django 5 + DRF backend (`django_calculators/`) + Angular 21 SSR frontend (`frontend/`)
**Metóda:** 6 paralelných statických auditov (i18n/preklady, FE↔BE API kompatibilita, mobil/responzivita + dark mode, funkcionalita/kompletnosť, backend korektnosť/bezpečnosť, legal/GDPR + embed/blog). Python ani Node nie sú na tomto stroji nainštalované → statická revízia; testy/build sa nedali spustiť.

Legenda stavu: ✅ opravené v tejto session · 🔜 odporúčané (nezmenené) · ⚠️ vyžaduje manuálny vstup (dáta prevádzkovateľa).

---

## Pass 4 — 2026-07-31 (6-agentový audit + opravy Set A/B/C)

6 paralelných read-only agentov (kalkulačná správnosť, backend bezpečnosť, FE↔BE kontrakt, FE runtime, build/a11y/i18n, config/deploy/GDPR). Najzávažnejšie nálezy **overené proti kódu aj proti oficiálnym zdrojom 2026** (nemenil som daňové hodnoty naslepo — a dobre tak: jeden agent nesprávne označil SZČO min. základ €914,40 za bug, pritom je pre 2026 správny, lebo sa pravidlo zmenilo z 50 % na 60 % priemernej mzdy).

**Opravené a otestované (105 backend testov · FE build + unit · deploy check 0 · SSR overené):**

*Set A — jasné bugy/config:*
- **i18n KRITICKÉ:** `calc/*.ts` (495 kľúčov, 5 jazykov) neboli importované → vacation/freelancer/hours-worked zobrazovali surové kľúče aj v SK. Zapojené do `translations.calc.ts`.
- **Payment:** `first_payment.principal` = úrok → opravené na `splátka − úrok`.
- **FE leaky:** rating widget (`router.events`) + navbar/dashboard (`currentUser$`) → `takeUntilDestroyed`.
- **Docker prod:** Postgres heslo split-brain (interpolácia vs env_file) → jednotný zdroj + `:?` guard; porty na loopback; DB/Redis wiring; `redis` do requirements.
- Stale `<head>` SEO na account routách → default; VAT default 20→23; mŕtve `SeoService` importy (12); date-picker `aria-label`.
- **Bezpečnosť:** neautentifikované odosielanie e-mailu na ľubovoľnú adresu (tracking) → e-maily len overenému majiteľovi účtu; register throttle; LogoutView generická hláška; split-bill list `max_length=100`; anonymné saved-calc podľa e-mailu sa mažú pri delete účtu.

*Set B — daňová logika (overené oficiálne 2026 hodnoty, zdroje nižšie):*
- **Priemerná mzda** 1400 → **1524** €; **max. vymeriavací základ** 8862 → **16764** € (11× pre 2026); **nemocenská max. DVZ** €241,64 → **€100,21/deň** (2×VŠVZ/365).
- **Freelancer:** doplnený **max. vymeriavací základ** (predtým chýbal → prepočet vysokopríjmových SZČO); **NČZD taper** (nad €26 083 klesá, €0 pri €43 983).
- **Daňový bonus:** teraz **refundovateľný** + strop **% zo základu** (1 dieťa 29 % … 6+ 64 %). Príklad: hrubá €900, 1 dieťa → čistá €770,40 → **€818,50** (bonus €100 vyplatený). SZČO min. základ €914,40 **ponechaný** (správny pre 2026).

*Set C — SEO:* obnovené **FAQ rich-results + keywords** pre 12 kalkulačiek (SK), lokalizovane cez centrálny builder (`seo-faq.ts`); ostatné jazyky čisté kým nie sú preložené FAQ.

**Zdroje 2026:** [Sociálna poisťovňa — vymeriavacie základy](https://www.socpoist.sk/news/nove-vymeriavacie-zaklady-pre-platenie-poistneho-od-1-januara-2026) · [Podnikajte — max. nemocenské dávky 2026](https://www.podnikajte.sk/socialne-a-zdravotne-odvody/maximalne-nemocenske-davky-2026-pn-ocr-materske-tehotenske) · [Financná správa — daňový bonus 2026](https://podpora.financnasprava.sk/215354) · [Podnikajte — NČZD 2026](https://www.podnikajte.sk/dan-z-prijmov/nezdanitelne-casti-zakladu-dane-2026)

**Zostáva (nižšia priorita / dáta):** child-bonus sumy €100/€50 + prípadný high-income strop dodatočne overiť; NČZD taper aj do mesačnej mzdy (teraz plná mesačná NČZD = payroll preddavky, taper v ročnom zúčtovaní); non-SK mzda vynecháva polia o deťoch; ~17 kalkulačiek má telo hardkódované po SK (kľúče už čakajú v `calc/*.ts`); og:image; PWA ikony; legal `[DOPLŇTE]`.

---

## Pass 2 — 2026-07-31 (dynamický audit: testy + build + živý Docker)

Na rozdiel od Pass 1 (statická revízia) boli Python 3.11 + Node 24 + Docker dostupné, takže sa **reálne spustilo**:

- ✅ **Backend testy: 101/101 OK** (`python manage.py test calculators users`) — pribudlo 7 nových regresných testov (`calculators/tests/test_hardening.py`).
- ✅ **Frontend build OK** (`npm run build`, SSR bundle) · **FE unit testy 2/2 OK** (predtým padal scaffold `app.spec.ts` — opravené).
- ✅ **`manage.py check --deploy` = 0 issues** pri prod-env (DEBUG=False). Bezpečnostné nastavenia sú správne env-gated.
- ✅ **Živý stack cez `docker compose up`** — backend aj SSR frontend vracajú HTTP 200; mzda 1500 € → net 1134,51 € (2026 sadzby OK).
- ✅ **Žiadne chýbajúce migrácie** (`makemigrations --check`).

### Opravené v tomto passe (✅)
| # | Oblasť | Nález | Fix |
|---|--------|-------|-----|
| P1 | GDPR | Zrušenie účtu nemazalo PII bez FK (`Lead`, `DataReport`, `AuthEvent` podľa e-mailu/IP) | `DeleteAccountView` teraz maže Lead/DataReport a anonymizuje AuthEvent |
| P2 | Bezpečnosť | Log injection — e-mail útočníka logovaný bez orezania CR/LF | `log_auth_event` striháva CR/LF, limit 200 zn. |
| P3 | Backend | **Split-bill `by_items` 500-oval na KAŽDOM requeste** (`validated_data['total_amount']` KeyError) | číta sa cez `.get()`; overené živé (200 + korektný breakdown) |
| P4 | Validácia | Split-bill položky bez schémy (KeyError→500 na `[{}]`) | `SplitBillItemSerializer` (person+amount) → 400 |
| P5 | DoS | Savings-goal tracker: neohraničené vstupy + `target_date` rok 9999 → ~95k-iteračná projekcia na každý dashboard GET | min/max validátory + cap horizontu 1200 mes. |
| P6 | Hygiena | `.env` (reálna cesta `django_calculators/.env`) **nebol v .gitignore**; 47 `.pyc` + `django.log` verzionované | `.gitignore` rozšírený na `.env`/`*.env`; junk `git rm --cached` |
| P7 | SSR | 6 služieb natvrdo `http://backend:8000` (compose alias) → SSR fetch zlyhá mimo Dockera | `ssrApiBase()` číta `SSR_API_URL`, fallback = compose alias |

### Implementácia „urob, čo je najlepšie" (druhá vlna, ✅ + overené živým Dockerom)
| # | Oblasť | Nález | Fix / overenie |
|---|--------|-------|-----|
| P8 | **KRITICKÉ — FE** | `angular.json` **nemal `fileReplacements`** → prod build zapiekol `environment.ts` (`apiUrl: http://localhost:8000/api`); `environment.prod.ts` sa NIKDY nepoužil. V prode by zlyhali VŠETKY API volania z prehliadača. | pridané `fileReplacements` → bundle teraz obsahuje `https://kalkulacky.sk/api` (overené `grep` v dist) |
| P9 | **KRITICKÉ — SSR/SEO** | Angular 21 SSR blokuje request, ktorého Host nie je v `NG_ALLOWED_HOSTS` (prázdne = VŠETKO padá na client-side render → žiadne SSR, žiadne SEO). | `NG_ALLOWED_HOSTS` v prod compose; overené živo: `/calculator/salary` 3 158 B (CSR shell) → **67 KB server-rendered** (`ng-server-context`), 0 fallbackov |
| P10 | Bezpečnosť | `str(e)` v 26 (calculators) + 1 (users, Google auth) 500-handleroch → leak interných chýb | `server_error()` helper: loguje traceback server-side, klientovi generická hláška; 400 `ValueError` hlášky ponechané (kontrolované) |
| P11 | Deploy | Docker/compose boli len dev (`runserver`, `ng serve`, `DEBUG=True`) | **prod stack**: `Dockerfile.prod` (gunicorn + collectstatic), `frontend/Dockerfile.prod` (multi-stage → SSR bundle), `docker-compose.prod.yml` (gunicorn + SSR + Postgres + Redis + notif. worker) + gunicorn v requirements + `.dockerignore`/`.gitattributes`. Overené: `docker compose -f docker-compose.prod.yml up` beží, gunicorn 22 servíruje, SSR renderuje |
| P12 | Hardening | `DEBUG` default `True` (fail-open) · `DATA_REPORT_RECIPIENT` osobný Gmail | `DEBUG` default `False`; recipient default = `DEFAULT_FROM_EMAIL` |

**Test suite po druhej vlne: backend 101/101 OK · FE build OK · FE unit 2/2 OK.**

### Zostáva pred go-live (vyžaduje rozhodnutie / dáta prevádzkovateľa)
- ⚠️ **Legal placeholders** `[DOPLŇTE: obchodné meno, IČO, sídlo, e-mail]` v `privacy-policy.component.ts` a `terms.component.ts` — reálna identita prevádzkovateľa. **Jediný tvrdý právny blocker.**
- 🔜 **`environment.prod.ts`**: `googleClientId` prázdny (OAuth login mŕtvy), `adsensePublisherId` prázdny (ads off) — doplniť reálne ID.
- 🔜 **Affiliate URL** `example.com` v `monetization.config.ts` — reálne partnerské linky (inak „affiliate" vedie na example.com).
- 🔜 **PWA ikony** 192/512/maskable chýbajú (len favicon) · **sitemap.xml** statický (bez blog URL a bez cs/en/pl/hu).
- 🔜 Menšie: savings-goal peňažná matematika vo `float` (doménová zmena, treba upraviť testy) · XFF dôvera pri IP (nastavenie proxy).

---

## Pass 3 — 2026-07-31 (SEO audit + implementácia, overené SSR/živým Dockerom)

Stav pred: SSR funguje (P9), ale per-page SEO malo len ~20 z ~37 indexovateľných stránok.

| # | Oblasť | Nález | Fix / overenie |
|---|--------|-------|-----|
| S1 | **SEO pokrytie** | Domovská stránka + 17 kalkulačiek nemali žiadne per-page SEO (generický `<title>`, bez canonical/OG/JSON-LD) | centrálny `ROUTE_SEO` register + aplikácia v `App` na `NavigationEnd`; overené SSR: `/calculator/vat` má teraz vlastný title, canonical, description, WebApplication + BreadcrumbList |
| S2 | **Domovská SEO** | `/` bez štruktúrovaných dát | `WebSite` + `Organization` + `SearchAction` (sitelinks searchbox) JSON-LD; overené v SSR výstupe |
| S3 | i18n SEO | `og:locale` natvrdo `sk_SK`, `inLanguage` natvrdo `sk` | čítajú sa z `LocaleService` (locale-aware); `<html lang>` sa nastavuje podľa jazyka |
| S4 | Štruktúra | Chýbal BreadcrumbList a `publisher` prepojenie | pridané pre kalkulačky (breadcrumbs + Organization publisher) |
| S5 | **Sitemap** | Statický `sitemap.xml` — bez blog článkov, bez `lastmod`, ručná údržba | **dynamický** `/sitemap.xml` route v SSR serveri: generuje sa z registra kalkulačiek + živých blog článkov; overené živo (36 URL vrátane blog článku); statický súbor odstránený |
| S6 | **BEZPEČNOSŤ** | Vnorený `django_calculators/django_calculators/.env` (číta ho decouple ako prvý) obsahuje **reálny Google OAuth secret** + placeholder `SECRET_KEY` + `ALLOWED_HOSTS` bez `backend` → (a) secret sa **zapiekol do Docker image**, (b) SSR→backend fetch padal na `DisallowedHost` 400. Súbor NIE JE v git histórii (nikdy necommitnutý). | `.dockerignore` (backend aj FE) rozšírený na `**/.env` → image už secret neobsahuje; kód-default `ALLOWED_HOSTS` (obsahuje `backend`) sa uplatní → SSR→backend teraz 200. **⚠️ ODPORÚČANIE: rotovať Google OAuth client secret** (bol v dev súbore + v lokálnom image). |

**Overené:** FE build OK · FE unit 2/2 OK · SSR renderuje SEO tagy server-side · dynamický sitemap 36 URL (kalkulačky + blog) · SSR→backend 200. Sebe-spravujúce stránky (salary/mortgage/…) SEO neprepísané.

### Pass 3b — Viacjazyčné SEO (SEO pre všetkých 5 jazykov)

Analýza odhalila, že hoci obsah je preložený (i18n, 5 jazykov), **SSR bol locale-slepý** — server renderoval SK pre KAŽDÝ jazyk, takže hreflang alternatívy (`?lang=en/cs/pl/hu`) servírovali SK HTML. Meta boli SK-only. Reálne viacjazyčné SEO teda NEEXISTOVALO.

| # | Nález | Fix / overenie |
|---|-------|-----|
| M1 | **SSR locale-slepé** — `LocaleService` čítal jazyk len v prehliadači; SSR vždy `sk` | SSR číta `?lang=` z `REQUEST` tokenu → server renderuje v požadovanom jazyku (obsah + meta + `<html lang>`); overené: `?lang=en` → `lang="en"`, `?lang=cs` → `lang="cs"` |
| M2 | **Meta SK-only** pre všetky kalkulačky (12 komponentov malo natvrdo SK title/description) | odstránené natvrdo-SK `seo.apply` z 12 komponentov; centrálny lokalizovaný builder stavia title/description z existujúcich `calc.<id>.name`/`.desc` (5 jazykov) → overené: salary = Čistá mzda / Net salary / Wynagrodzenie netto / Nettó bér |
| M3 | **Canonical mieril na SK URL** aj pre `?lang=en` → Google by zahodil cudzojazyčné verzie | každá jazyková verzia je self-canonical (`…?lang=xx`); `sk` hreflang aj canonical bez parametra (konzistentné) |
| M4 | `og:locale`/`inLanguage`/`<html lang>` natvrdo SK | čítajú sa z locale (5 jazykov) |

**Overené SSR pre všetkých 5 jazykov** (salary + mortgage + home): lokalizovaný title, description, canonical, og:locale, hreflang, `<html lang>`. FE build + unit testy zelené.

### SEO — čo ešte zlepšiť (nižšia priorita / vyžaduje asset alebo väčšiu zmenu)
- 🔜 **`og:image`** — chýba (zdieľania na sociálnych sieťach bez náhľadu). Treba 1200×630 PNG asset.
- 🔜 **Bespoke meta / FAQ rich-results per jazyk** — meta sa teraz stavajú z `calc.name/.desc` (dobré, jednotné). Pôvodné bohaté SK titulky + FAQ JSON-LD boli odstránené kvôli konzistentnej lokalizácii; dajú sa vrátiť ako per-lokálne override + preložené FAQ.
- 🔜 **Locale-prefixované URL** (`/en/...`) namiesto `?lang=` — čistejšie oddelené SEO povrchy (väčšia zmena: routing).
- 🔜 **PWA ikony** 192/512/maskable (viac nižšie).

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
