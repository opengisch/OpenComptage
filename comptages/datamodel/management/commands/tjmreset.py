import logging
from django.core.management.base import BaseCommand

from comptages.datamodel import models
from comptages.core import statistics

logger = logging.getLogger("main")


class Command(BaseCommand):
    help = "Recalculate TJM of all counts"

    def handle(self, *args, **options):
        counts = models.Count.objects.all()

        for i, count in enumerate(counts):
            print(f"{i+1} of {len(counts)} - Calculate TJM of count {count.id}")

            df, tjm = statistics.get_day_data(count)

            count.tjm = tjm
            count.save(update_fields=['tjm'])
