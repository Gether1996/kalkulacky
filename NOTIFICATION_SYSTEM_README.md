# Notification & Tracking System - Implementation Guide

## Prehľad systému

Tento implementačný balík pridáva komplexný systém notifikácií a trackingu pre kalkulačky Tehotenstvo, Dovolenka a Hypotéka/Úver.

## Implementované featury

### 1. **Tehotenstvo (Pregnancy) Tracking** ⭐⭐⭐⭐⭐

#### Notifikácie:
- ✅ **Týždenné updaty**: Každý týždeň informácie o vývoji bábätka
- ✅ **Míľniky**: Dôležité míľniky (týždne 8, 12, 20, 28, 36, 38, 40)
- ✅ **Trimester prechody**: Notifikácie pri prechode do 2. a 3. trimestra (týždne 13, 27)
- ✅ **Prenatálne kontroly**: Pripomienky na lekárske vyšetrenia
- ✅ **Blížiaci sa termín**: Pripomienky 30, 14, 7, 3, 1 deň pred termínom pôrodu

#### Príklad použitia:
```python
# Uloženie výpočtu s trackingom
POST /api/saved-calculations/
{
    "session_key": "abc123xyz",
    "email": "user@example.com",
    "calculator_type": "pregnancy",
    "name": "Moje tehotenstvo - júl 2026",
    "params": {
        "calculation_method": "lmp",
        "lmp_date": "2025-11-01",
        "current_date": "2026-03-06"
    },
    "result": { ... },
    "is_tracking": true,
    "notification_enabled": true
}
```

Po uložení výpočtu sa automaticky vygenerujú všetky naplánované notifikácie na nasledujúcich 40 týždňov.

### 2. **Dovolenka (Vacation) Tracking** ⭐⭐⭐⭐⭐

#### Notifikácie:
- ✅ **Štvrťročné pripomienky**: Každý kvartál kontrola zostávajúcej dovolenky
- ✅ **Birthday reminder (33 rokov)**: Pripomienka 2 a 1 mesiac pred 33. narodeninami (+5 dní dovolenky)
- ✅ **Expiration warnings**: Varovania 60, 30, 14, 7 dní pred vypršaním dovolenky

#### Príklad použitia:
```python
POST /api/saved-calculations/
{
    "session_key": "abc123xyz",
    "email": "user@example.com",
    "calculator_type": "vacation",
    "name": "Moja dovolenka 2026",
    "params": {
        "total_days": 25,
        "used_days": 5,
        "birth_date": "1993-08-15",
        "expiry_date": "2026-12-31"
    },
    "result": {
        "remaining_days": 20,
        "used_days": 5,
        "total_days": 25
    },
    "is_tracking": true,
    "notification_enabled": true
}
```

### 3. **Hypotéka/Úver (Mortgage/Loan) Tracking** ⭐⭐⭐⭐

#### Notifikácie:
- ✅ **Mesačné splátky**: Pripomienky 5 dní pred splatnosťou (12 mesiacov vopred)
- ✅ **Míľniky splatenia**: Pri dosiahnutí 25%, 50%, 75% splatenia
- ✅ **Extra payment tips**: Štvrťročné tipy na nadplatenie a úsporu úrokov

#### Príklad použitia:
```python
POST /api/saved-calculations/
{
    "session_key": "abc123xyz",
    "email": "user@example.com",
    "calculator_type": "mortgage",
    "name": "Hypotéka VUB",
    "params": {
        "principal": 150000,
        "interest_rate": 4.5,
        "months": 360,
        "payment_day": 15
    },
    "result": {
        "monthly_payment": 760.03,
        "total_payment": 273610.80,
        "total_interest": 123610.80
    },
    "is_tracking": true,
    "notification_enabled": true
}
```

## Architektúra

### Modely (models.py)
- **SavedCalculation**: Uložený výpočet s parametrami a výsledkom
- **ScheduledNotification**: Naplánovaná notifikácia s dátumom a časom odoslania

### Services
- **NotificationService**: Odosielanie emailov (plain text + HTML templates)
- **NotificationGenerator**: Orchestrátor pre vytváranie notifikácií
- **TrackingHelpers**: Špecifické helpery pre každý typ kalkulačky
  - PregnancyTrackingHelper
  - VacationTrackingHelper
  - MortgageLoanTrackingHelper

### Management Commands
- **send_notifications**: Odošle všetky naplánované notifikácie (spustiť cez cron)

## Setup a konfigurácia

### 1. Migrácie databázy

```bash
cd django_calculators
python manage.py makemigrations
python manage.py migrate
```

### 2. Email konfigurácia

Pre development (console output):
```python
# settings.py (už nastavené)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

Pre production (SMTP):
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@kalkulacky.sk'
```

### 3. Cron job setup

Pridajte do crontab (Linux/Mac):
```bash
# Odosielať notifikácie každý deň o 9:00
0 9 * * * cd /path/to/django_calculators && python manage.py send_notifications
```

Windows Task Scheduler:
```powershell
# Vytvorte scheduled task
cd C:\path\to\django_calculators
python manage.py send_notifications
```

### 4. Testovanie

Manuálny test (dry-run):
```bash
python manage.py send_notifications --dry-run
```

Force send (pre testing):
```bash
python manage.py send_notifications --force
```

## API Endpoints

### Uloženie výpočtu s trackingom
```http
POST /api/saved-calculations/
Content-Type: application/json

{
    "session_key": "string",
    "email": "string (optional)",
    "calculator_type": "pregnancy|vacation|mortgage|loan",
    "name": "string",
    "params": {},
    "result": {},
    "is_tracking": true,
    "notification_enabled": true
}
```

### Získanie uložených výpočtov
```http
GET /api/saved-calculations/?session_key=abc123
```

### Získanie detailov výpočtu
```http
GET /api/saved-calculations/{id}/
```

### Aktualizácia výpočtu
```http
PUT /api/saved-calculations/{id}/
Content-Type: application/json

{
    "name": "Updated name",
    "is_tracking": false
}
```

### Vymazanie výpočtu
```http
DELETE /api/saved-calculations/{id}/
```

### Zapnutie trackingu pre existujúci výpočet
```http
POST /api/saved-calculations/{id}/enable-tracking/
Content-Type: application/json

{
    "email": "user@example.com"
}
```

## Databázová štruktúra

### SavedCalculation
| Pole | Typ | Popis |
|------|-----|-------|
| id | Integer | Primary key |
| session_key | String | Session identifier |
| email | Email | Email pre notifikácie (optional) |
| calculator_type | String | Typ kalkulačky |
| name | String | Názov výpočtu |
| params | JSON | Vstupné parametre |
| result | JSON | Výsledok výpočtu |
| is_tracking | Boolean | Zapnutý tracking |
| notification_enabled | Boolean | Povolené notifikácie |
| created_at | DateTime | Dátum vytvorenia |
| last_accessed | DateTime | Posledný prístup |

### ScheduledNotification
| Pole | Typ | Popis |
|------|-----|-------|
| id | Integer | Primary key |
| calculation | ForeignKey | Odkaz na SavedCalculation |
| notification_type | String | Typ notifikácie |
| priority | String | Priorita (low/medium/high/urgent) |
| scheduled_date | Date | Dátum odoslania |
| scheduled_time | Time | Čas odoslania |
| title | String | Predmet emailu |
| message | Text | Obsah emailu |
| action_url | String | URL na detail |
| sent | Boolean | Odoslané |
| sent_at | DateTime | Dátum odoslania |

## Email šablóny

Všetky email šablóny sú definované v `notification_service.py` v metóde `_get_template_config()`.

### Príklad pregnancy email:
```
Subject: 🤰 Týždeň 12 tehotenstva - Moje tehotenstvo

Ahoj!

Vitaj v týždni 12 tehotenstva! 🎉

Vaše bábätko sa neustále vyvíja a rastie.

Bábätko: slivka
Trimester: 1
Zostáva: 196 dní do termínu (2026-07-20)

⭐ MÍĽNIK: Koniec 1. trimestra

Zobraziť detail: https://kalkulacky.sk/calculator/pregnancy?id=123

S pozdravom,
Tím Kalkulačky.sk
```

## Troubleshooting

### Notifikácie sa neposielajú
1. Skontrolujte EMAIL_BACKEND v settings.py
2. Skontrolujte cron job
3. Spustite manuálne: `python manage.py send_notifications --dry-run`
4. Skontrolujte logy: `django_calculators/logs/django.log`

### Notifikácie sa generujú duplicitne
- Pri aktualizácii výpočtu sa staré notifikácie automaticky vymažú a vygenerujú nové

### Email má nesprávne údaje
- Skontrolujte metódu `_prepare_context()` v `send_notifications.py`
- Skontrolujte template v `notification_service.py`

## Ďalšie rozšírenia

### Plánované featury:
- [ ] HTML email šablóny (aktuálne len plain text)
- [ ] SMS notifikácie (Twilio integrácia)
- [ ] Push notifikácie (Firebase)
- [ ] In-app notifikácie
- [ ] Vlastné notifikačné frekvencie (weekly/monthly)
- [ ] Notifikačné preferencie pre každého usera
- [ ] A/B testing emailov

## Performance optimalizácie

### Indexy databázy
```sql
-- Už vytvorené v models.py
CREATE INDEX ON scheduled_notification (scheduled_date, sent);
CREATE INDEX ON saved_calculation (session_key, calculator_type);
CREATE INDEX ON saved_calculation (email);
```

### Batch processing
Management command podporuje batch processing notifikácií pre lepšiu performance.

## Bezpečnosť

- Email adresy sú optional (podporujeme anonymous tracking)
- Session keys sú použité pre identifikáciu anonymných userov
- SQL injection protection cez Django ORM
- XSS protection v email templates

## Záver

Tento systém poskytuje komplexné riešenie pre tracking a notifikácie na kalkulacky.sk. Je škálovateľný, bezpečný a jednoducho rozšíriteľný o nové typy kalkulačiek.

Pre otázky a support kontaktujte development team.
