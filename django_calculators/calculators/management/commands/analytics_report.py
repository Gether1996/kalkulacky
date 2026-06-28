"""
Print a visitor + auth summary for the last N days.

    python manage.py analytics_report            # last 30 days
    python manage.py analytics_report --days 7   # last week
"""
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate
from calculators.models import PageView, AuthEvent


class Command(BaseCommand):
    help = 'Summarise visitor traffic and auth events for the last N days.'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=30, help='Look-back window (default 30).')
        parser.add_argument('--top', type=int, default=15, help='How many top pages to show.')

    def handle(self, *args, **opts):
        days = max(1, opts['days'])
        since = timezone.now() - timedelta(days=days)
        views = PageView.objects.filter(created_at__gte=since)
        auth = AuthEvent.objects.filter(created_at__gte=since)

        total = views.count()
        uniques = views.values('visitor_hash').distinct().count()

        self.stdout.write('=' * 60)
        self.stdout.write(f'  ANALYTICS — last {days} days (since {since:%Y-%m-%d})')
        self.stdout.write('=' * 60)
        self.stdout.write(f'  Page views:       {total}')
        self.stdout.write(f'  Unique visitors:  {uniques}')

        self.stdout.write('\n  Auth events:')
        for row in auth.values('event').annotate(n=Count('id')).order_by('-n'):
            self.stdout.write(f'    {row["event"]:<18} {row["n"]}')
        if not auth.exists():
            self.stdout.write('    (none)')

        self.stdout.write(f'\n  Top {opts["top"]} pages:')
        for row in views.values('path').annotate(n=Count('id')).order_by('-n')[:opts['top']]:
            self.stdout.write(f'    {row["n"]:>6}  {row["path"]}')

        self.stdout.write('\n  Views per day:')
        by_day = (views.annotate(d=TruncDate('created_at')).values('d')
                  .annotate(n=Count('id'), v=Count('visitor_hash', distinct=True))
                  .order_by('d'))
        for row in by_day:
            self.stdout.write(f'    {row["d"]}  views={row["n"]:>5}  visitors={row["v"]:>5}')
        if not by_day:
            self.stdout.write('    (no data)')
        self.stdout.write('=' * 60)
