from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from home.models import Reservation  # adjust if your model name/path is different

class Command(BaseCommand):
    help = "Deletes old unconfirmed reservations (e.g., older than 24 hours)"

    def add_arguments(self, parser):
        # Optional: allow custom threshold in hours
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Delete reservations older than this many hours'
        )

    def handle(self, *args, **options):
        hours = options['hours']
        threshold = timezone.now() - timedelta(hours=hours)

        # Filter unconfirmed/pending reservations older than threshold
        old_reservations = Reservation.objects.filter(
            status__in=['pending', 'unconfirmed'],  # adjust status field values
            start_time__lt=threshold
        )

        count = old_reservations.count()
        old_reservations.delete()

        self.stdout.write(self.style.SUCCESS(
            f"Deleted {count} unconfirmed reservations older than {hours} hours."
        ))
