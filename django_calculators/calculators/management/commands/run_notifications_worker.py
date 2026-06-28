"""
Long-running notifications worker.

A dependency-free periodic scheduler: it calls `send_notifications` on a fixed
interval, forever. Use this when you want a simple always-on worker (a systemd
service or a Docker sidecar) instead of an OS cron entry.

    python manage.py run_notifications_worker                # every 15 min
    python manage.py run_notifications_worker --interval 300 # every 5 min
    python manage.py run_notifications_worker --once         # one pass, then exit

For production, EITHER run this as a managed service OR schedule
`send_notifications` via cron / Celery beat — not both (you'd double-send).
See deploy/PRODUCTION.md.
"""

import time
import logging
from django.core.management import call_command
from django.core.management.base import BaseCommand

logger = logging.getLogger('calculators')


class Command(BaseCommand):
    help = 'Run an always-on worker that sends due notifications on an interval.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval', type=int, default=900,
            help='Seconds between passes (default 900 = 15 min).',
        )
        parser.add_argument(
            '--once', action='store_true',
            help='Run a single pass and exit (useful for cron / testing).',
        )
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Pass --dry-run through to send_notifications (no emails sent).',
        )

    def handle(self, *args, **options):
        interval = max(30, int(options['interval']))
        once = options['once']
        dry_run = options['dry_run']

        self.stdout.write(self.style.SUCCESS(
            f"Notifications worker started (interval={interval}s, once={once}, dry_run={dry_run})."
        ))

        while True:
            try:
                call_command('send_notifications', dry_run=dry_run)
            except Exception as e:  # never let one failed pass kill the worker
                logger.exception('notifications worker pass failed: %s', e)
                self.stderr.write(self.style.ERROR(f"Pass failed: {e}"))

            if once:
                break

            try:
                time.sleep(interval)
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING('Worker stopped (KeyboardInterrupt).'))
                break
