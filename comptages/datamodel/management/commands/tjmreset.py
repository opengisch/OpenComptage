import logging
from django.core.management.base import BaseCommand

from comptages.datamodel import models
from comptages.core import statistics

logger = logging.getLogger("main")


class Command(BaseCommand):
    help = "Recalculate TJM of all counts"

    def add_arguments(self, parser):
        parser.add_argument("--min_id", help="Minimum count id considered (included)")
        parser.add_argument("--max_id", help="Maximum count id considered (included)")

    def handle(self, *args, **options):
        counts = models.Count.objects.all()

        if options['min_id']:
            counts = counts.filter(id__gte=options['min_id'])

        if options['max_id']:
            counts = counts.filter(id__lte=options['max_id'])

        for i, count in enumerate(counts):
            print(f"{i+1} of {len(counts)} - Calculate TJM of count {count.id}")

            df, tjm = statistics.get_day_data(count)

            count.tjm = tjm
            count.save(update_fields=['tjm'])
