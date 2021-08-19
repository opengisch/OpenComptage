import logging
import os
from decimal import Decimal
from django.contrib.gis.gdal import DataSource
from django.core.management.base import BaseCommand

from ...models import Section, Lane, Brand, Category, Class, ClassCategory

logger = logging.getLogger("main")


class Command(BaseCommand):
    help = "Import initial data from files"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Delete existing data")

    def handle(self, *args, **options):

        if options["clear"]:
            print("Deleting...")
            Lane.objects.all().delete()
            Section.objects.all().delete()
            Brand.objects.all().delete()

        self.import_sections(self.file_path("section.csv"))
        self.import_brands(self.file_path("brand.csv"))
        self.import_categories(self.file_path("category.csv"))
        self.import_classes(self.file_path("class.csv"))
        self.import_class_categories(self.file_path("class_category.csv"))
        print("🚓")

    def file_path(self, filename):
        return os.path.join(os.path.dirname(__file__),'..','..','..','..','db',filename)

    def import_sections(self, csv_file):
        print("Importing sections...")
        ds = DataSource(csv_file)
        sections = []
        for feat in ds[0]:
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

    def import_brands(self, csv_file):
        print("Importing brands...")

        ds = DataSource(csv_file)

        brands = []

        for feat in ds[0]:
            brands.append(
                Brand(
                    id=Decimal(feat["id"].value),
                    name=feat["name"],
                    formatter_name=feat["formatter_name"]
                )
            )
        Brand.objects.bulk_create(brands)
        print(f"Inserted {len(brands)} brands.")

    def import_categories(self, csv_file):
        print("Importing categories...")

        ds = DataSource(csv_file)

        categories = []

        for feat in ds[0]:
            categories.append(
                Category(
                    id=Decimal(feat["id"].value),
                    name=feat["name"],
                    code=Decimal(feat["code"].value),
                    light=bool(feat["light"]),
                    id_category_id=Decimal(feat["id"].value)
                )
            )
        Category.objects.bulk_create(categories)
        print(f"Inserted {len(categories)} categories.")

    def import_classes(self, csv_file):
        print("Importing classes...")

        ds = DataSource(csv_file)

        classes = []

        for feat in ds[0]:
            classes.append(
                Class(
                    id=Decimal(feat["id"].value),
                    name=feat["name"],
                    description=feat["description"],
                )
            )
        Class.objects.bulk_create(classes)
        print(f"Inserted {len(classes)} classes.")

    def import_class_categories(self, csv_file):
        print("Importing class_categories...")

        ds = DataSource(csv_file)

        class_categories = []

        for feat in ds[0]:
            class_categories.append(
                ClassCategory(
                    id_class_id=Decimal(feat["id_class"].value),
                    id_category_id=Decimal(feat["id_category"].value),
                )
            )
        ClassCategory.objects.bulk_create(class_categories)
        print(f"Inserted {len(class_categories)} class categories.")
