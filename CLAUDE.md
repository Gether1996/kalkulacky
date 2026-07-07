# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Kalkulačky.sk — a Slovak-market portal of online calculators (net salary, mortgage, VAT, freelancer tax, pension, energy/solar subsidies, …) with blog, user accounts, saved calculations, reminders/notifications, favorites, ratings, first-party analytics and monetization (leads/affiliate). Expanding to V4 markets (CZ/PL/HU + EN).

Two independent apps in one repo:

- `django_calculators/` — Django 5 + DRF JSON API (serves only `/api/` + `/admin/`)
- `frontend/` — Angular 21 standalone-components app with SSR (Node/Express), all UI and page HTML

## Commands

### Backend (run from `django_calculators/`)

```bash
python manage.py runserver              # dev server on :8000
python manage.py migrate
python manage.py test calculators users # real test suite (calculators/tests/, users/tests/)
python manage.py test calculators.tests.test_security          # one module
python manage.py test calculators.tests.test_calculators.SalaryCalculatorTests  # one class
python manage.py send_notifications --dry-run   # verify reminder emails
python manage.py check --deploy
```

- **`.env` is required**: `SECRET_KEY` has no default (`python-decouple`), so `manage.py` dies without `django_calculators/.env` containing at least `SECRET_KEY=...`. All deploy config is env-driven (see `deploy/PRODUCTION.md` for the full checklist).
- The loose `test_*.py` scripts in `django_calculators/` root (test_calc.py, test_odvody.py, …) are **manual print-scripts**, not part of the test suite. The maintained suite lives in `calculators/tests/` and `users/tests/`.
- Tests inherit from `calculators/tests/base.py`, which disables DRF throttling for functional tests (throttle behaviour is tested explicitly in `test_security.py` with tiny override rates + `cache.clear()`). Don't assert rate limits in functional tests.

### Frontend (run from `frontend/`)

```bash
npm start                # ng serve on :4200 (proxies nothing — calls http://localhost:8000/api directly)
npm run build            # production build incl. SSR
npm test                 # ng test (vitest)
npm run serve:ssr:frontend   # serve built SSR bundle (dist/frontend/server/server.mjs)
```

`docker-compose up` starts both (backend :8000, frontend :4200) for dev.

## Architecture

### Backend

- **Two Django apps**: `users` (JWT auth via simplejwt — `USER_ID_FIELD` is **email**, custom `users.User` model, Google OAuth, password reset) mounted at `/api/auth/`; `calculators` (everything else) at `/api/calculators/`.
- **Service layer**: every calculator is a class in `calculators/services/<name>_calculator.py`; views in `calculators/views.py` (~2600 lines, all endpoints) are thin wrappers that validate via `serializers.py` and call the service. New calculator = service + serializer + view + `urls.py` path + entry in `CalculatorListView`.
- **`calculators/services/config_variables.py`** is the single source of truth for Slovak tax rates/thresholds (2026 figures: 4-bracket progressive tax, odvody, NČZD, child bonus…). Updated annually — calculators must read constants from here, never hardcode rates.
- **Throttling**: DRF anon/user global rates + scoped throttles (`leads`, `login`, `forgot_password`, `rating`, `analytics`, `data_report`) — all env-overridable. Abuse-prone endpoints get a scope; see `settings.py` REST_FRAMEWORK block.
- **Notifications/reminders**: models + `calculators/services/notification_*.py`, sent by `manage.py send_notifications` (cron) **or** `run_notifications_worker` (daemon) — production must run only ONE of the two or emails double-send.
- **Email** backend is env-driven: console in dev, SMTP automatically when `EMAIL_HOST` is set.
- DB is SQLite in dev, PostgreSQL via `DB_ENGINE=postgres` env. `USE_TZ = False`, timezone Europe/Bratislava.

### Frontend

- **Standalone components, lazy routes**: each calculator is a component under `src/app/components/<name>-calculator/` lazy-loaded at `/calculator/<name>` in `app.routes.ts`. Some calculators are frontend-only (heat-pump, renovation, car-insurance, basic) with no backend endpoint.
- **Custom i18n (not Angular built-in i18n)**: `src/app/i18n/` — 5 locales (`sk` default, `cs`, `en`, `pl`, `hu`), dictionaries in `translations.ts`/`translations.app.ts`/`translations.calc.ts`, rendered via `translate.pipe` + `LocaleService`. Every user-facing string needs keys in all 5 locales.
- **Country params vs. tax logic** (`i18n/country-params.ts`): per-locale numbers (VAT rates, currency, salary presets) are localized, but tax-system calculators all implement `taxLogic: 'SK'` — non-SK locales show a "uses Slovak rules" banner until a country gets its own engine. Don't fake localization by only swapping numbers where the system differs structurally.
- **Services** (`src/app/services/`) wrap the API (auth with JWT refresh, calculator calls, favorites, ratings, analytics, consent, theme, SEO). API base URL comes from `src/environments/`.
- **SSR caveat**: code runs on the server too — guard direct `window`/`localStorage`/`document` access (platform checks) as done in existing services.

## Conventions

- Prettier config in `frontend/package.json`: 100-char width, single quotes, Angular parser for HTML.
- Monetary math on the backend uses `Decimal` (see services), never float.
- Domain language is Slovak (mzda, odvody, NČZD…); code/comments are English with Slovak domain terms where they aid precision.
- Legal/GDPR surface exists (`/privacy`, `/terms`, `/cookies`, consent service, account deletion, audit log) — features touching personal data must keep this consistent.
