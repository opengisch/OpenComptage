import logging
import os
from decimal import Decimal
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal.error import GDALException
from django.core.management.base import BaseCommand

from ...models import Section, Lane

logger = logging.getLogger("main")


class Command(BaseCommand):
    help = "Import sections from file"

    def add_arguments(self, parser):
        parser.add_argument('--sections_file', default=os.path.join(os.path.dirname(__file__),'..','..','..','..','..','db','sections_clean.csv'))
        parser.add_argument("--clear", action="store_true", help="Delete existing data")

    def handle(self, *args, **options):

        ds_sections = DataSource(options["sections_file"])

        layer_sections = ds_sections[0]

        if options["clear"]:
            print("Deleting...")
            Lane.objects.all().delete()
            Section.objects.all().delete()

        print("Importing sections...")
        sections = []
        for feat in layer_sections:
            sections.append(
                Section(
                    geometry=feat.geom.wkt,
                    id=feat["id"],
                    name=feat["name"],
                    owner=feat["owner"],
                    road=feat["road"],
                    way=feat["way"],
                    start_pr=feat["start_pr"],
                    end_pr=feat["end_pr"],
                    start_dist=Decimal(feat["start_dist"].value),
                    end_dist=Decimal(feat["end_dist"].value),
                    place_name=feat["place_name"],
                    start_validity=feat["start_validity"].value,  # TODO : probably needs cast do datetime
                    end_validity=feat["end_validity"].value,  # TODO : probably needs cast do datetime
                )
            )
        Section.objects.bulk_create(sections)
        print(f"Inserted {len(sections)} sections.")

        print("🚓")
