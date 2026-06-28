# Production deployment & hardening guide

## Defence in depth against floods / DDoS

No single layer stops a real DDoS. Stack them — the app is the *last* line, not the first:

| Layer | Stops | Status |
|---|---|---|
| **1. Cloudflare / CDN-WAF** (edge) | Volumetric L3/L4 floods, distributed botnets, most L7 floods; bot rules; caching | **Set up before launch** (free tier is enough to start). Point DNS at Cloudflare, enable "Under Attack" mode when targeted, add a WAF rate-limit rule. |
| **2. nginx reverse proxy** (`limit_req`/`limit_conn`) | Single-IP request/connection floods, slowloris, oversized bodies | Use `deploy/nginx.conf.example`. |
| **3. App throttling** (DRF) | Single-source API abuse, scraping, credential stuffing, accidental hammering | ✅ in code (per-IP `anon`/`user` + scoped login/leads/reports/reset). |
| **4. DB / cache** | Throttle state shared across workers | Set `REDIS_URL` so limits are global, not per-process. |

**Honest limit:** a distributed attack from thousands of IPs ("millions of requests") cannot be absorbed by Django or the Node SSR server — only Cloudflare/CDN scrubbing can. Per-IP throttling and nginx limits stop the *cheap* and *single-source* attacks, which are the common case.

Notes:
- Django only serves `/api/` + `/admin/`. Page HTML is rendered by the **Angular SSR (Node)** server, which has **no app-level throttle** — it relies entirely on nginx/Cloudflare. SSR is CPU-heavy, so cache HTML at the CDN and rate-limit `/` at nginx.
- Auto-calc fires an API request per keystroke/slider tick; nginx `burst=40` and the generous `anon` rate (600/min) absorb that. Tune `THROTTLE_ANON` if needed.
- Add Cloudflare page-rules to **cache** `/`, `/calculator/*`, `/robots.txt`, `/sitemap.xml`, static assets.

## Go-live env checklist (`.env`)

```
SECRET_KEY=<50+ random chars>          # required; dev key triggers a check --deploy warning
DEBUG=False                            # turns on HSTS/SSL-redirect/secure cookies
ALLOWED_HOSTS=kalkulacky.sk,www.kalkulacky.sk
CORS_ALLOWED_ORIGINS=https://kalkulacky.sk,https://www.kalkulacky.sk
CSRF_TRUSTED_ORIGINS=https://kalkulacky.sk,https://www.kalkulacky.sk
FRONTEND_URL=https://kalkulacky.sk

# Database (PostgreSQL recommended; psycopg2 already installed)
DB_ENGINE=postgres
DB_NAME=... DB_USER=... DB_PASSWORD=... DB_HOST=... DB_PORT=5432

# Shared cache (makes throttling global across workers)
REDIS_URL=redis://127.0.0.1:6379/1     # then: pip install redis

# Email (reminders, password reset, data reports)
EMAIL_HOST=... EMAIL_HOST_USER=... EMAIL_HOST_PASSWORD=... DEFAULT_FROM_EMAIL=noreply@kalkulacky.sk
DATA_REPORT_RECIPIENT=pat.kredatus@gmail.com

# Optional throttle overrides: THROTTLE_ANON, THROTTLE_USER, THROTTLE_LOGIN, ...
```

## Deploy steps

1. `pip install -r requirements.txt` (+ `redis` if using `REDIS_URL`).
2. `python manage.py migrate`
3. `python manage.py collectstatic --noinput`  (WhiteNoise serves them)
4. `python manage.py createsuperuser`  (to view analytics / admin)
5. Run Django with gunicorn/uvicorn behind nginx (port 8000).
6. Build + run Angular SSR: `npm run build` then serve `dist/frontend/server` (port 4000).
7. nginx from `deploy/nginx.conf.example`; TLS via certbot.
8. Schedule notification emails — **pick ONE** (running both double-sends):
   - **Cron** (recommended): run every 15 min so daily/weekly/monthly reminders fire near their chosen time, e.g. `*/15 * * * * cd /app && /app/venv/bin/python manage.py send_notifications`.
   - **Always-on worker** (systemd / Docker sidecar): `python manage.py run_notifications_worker --interval 900`.
   Reminders carry a `frequency` (once/daily/weekly/monthly/yearly); recurring ones re-arm to their next occurrence after each send (catch-up safe — a downtime gap sends once, not a backlog). Verify with `python manage.py send_notifications --dry-run`.
9. Fill operator details in the legal pages (`/privacy`, `/terms`, `/cookies`) and have them reviewed.
10. Add 192×192 + 512×512 PNG icons to `frontend/public/` and reference them in `manifest.webmanifest` for full PWA install.
11. Verify: `python manage.py check --deploy` (only the SECRET_KEY warning should remain if env is set).

## Monitoring

- App log: `logs/django.log` (rotating). Audit trail (logins, account deletion): `logs/audit.log`.
- Visitor analytics: Django admin (Page Views / Auth Events, date-filtered) or
  `python manage.py analytics_report --days 30`, or `GET /api/calculators/analytics/stats/?period=month` (staff).
- Consider Sentry (`sentry-sdk`) for error alerting and an uptime monitor hitting `/api/health/`.
