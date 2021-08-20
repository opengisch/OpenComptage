import logging
import os
from decimal import Decimal
from django.contrib.gis.gdal import DataSource
from django.core.management.base import BaseCommand

from ...models import (
    Section, Lane, Brand, Category, Class, ClassCategory, Device, Installation,
    Model, ModelClass, SensorType, SensorTypeClass, SensorTypeInstallation,
    SensorTypeModel)

logger = logging.getLogger("main")


class Command(BaseCommand):
    help = "Import initial data from files"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Delete existing data")

    def handle(self, *args, **options):

        if options["clear"]:
            print("Deleting...")

            ClassCategory.objects.all().delete()
            Category.objects.all().delete()
            SensorTypeClass.objects.all().delete()
            SensorTypeModel.objects.all().delete()
            SensorTypeInstallation.objects.all().delete()
            SensorType.objects.all().delete()
            ModelClass.objects.all().delete()
            Class.objects.all().delete()
            Device.objects.all().delete()
            Model.objects.all().delete()
            Brand.objects.all().delete()
            Installation.objects.all().delete()
            Lane.objects.all().delete()
            Section.objects.all().delete()

        self.import_sections(self.file_path("section.csv"))
        self.import_brands(self.file_path("brand.csv"))
        self.import_categories(self.file_path("category.csv"))
        self.import_classes(self.file_path("class.csv"))
        self.import_class_categories(self.file_path("class_category.csv"))
        self.import_installations(self.file_path("installation.csv"))
        self.import_lanes(self.file_path("lane.csv"))
        self.import_models(self.file_path("model.csv"))
        self.import_model_classes(self.file_path("model_class.csv"))
        self.import_sensor_types(self.file_path("sensor_type.csv"))
        self.import_sensor_type_classes(self.file_path("sensor_type_class.csv"))
        self.import_sensor_type_installations(self.file_path("sensor_type_installation.csv"))
        self.import_sensor_type_models(self.file_path("sensor_type_model.csv"))
        self.import_devices(self.file_path("device.csv"))
        print("🚓")

    def file_path(self, filename):
        return os.path.join(os.path.dirname(__file__),'..','..','..','basedata',filename)

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

    def import_installations(self, csv_file):
        print("Importing installations...")

        ds = DataSource(csv_file)

        objects = []

        for feat in ds[0]:
            objects.append(
                Installation(
                    geometry=feat.geom.wkt,
                    id=Decimal(feat["id"].value),
                    permanent=bool(feat["permanent"]),
                    name=feat["name"],
                    picture=feat["picture"],
                    active=bool(feat["active"]),
                )
            )
        Installation.objects.bulk_create(objects)
        print(f"Inserted {len(objects)} installations.")

    def import_lanes(self, csv_file):
        print("Importing lanes...")

        ds = DataSource(csv_file)

        objects = []

        for feat in ds[0]:
            objects.append(
                Lane(
                    id=Decimal(feat["id"].value),
                    number=Decimal(feat["number"].value),
                    direction=Decimal(feat["direction"].value),
                    direction_desc=feat["direction_desc"],
                    id_installation_id=Decimal(feat["id_installation"].value),
                    id_section_id=feat["id_section"],
                )
            )
        Lane.objects.bulk_create(objects)
        print(f"Inserted {len(objects)} lanes.")

    def import_models(self, csv_file):
        print("Importing models...")

        ds = DataSource(csv_file)

        objects = []

        for feat in ds[0]:
            objects.append(
                Model(
                    id=Decimal(feat["id"].value),
                    name=feat["name"],
                    card_name=feat["card_name"],
                    configuration=feat["configuration"],
                    id_brand_id=Decimal(feat["id_brand"].value),
                )
            )
        Model.objects.bulk_create(objects)
        print(f"Inserted {len(objects)} models.")

    def import_model_classes(self, csv_file):
        print("Importing model classes...")

        ds = DataSource(csv_file)

        objects = []

        for feat in ds[0]:
            objects.append(
                ModelClass(
                    id_model_id=Decimal(feat["id_model"].value),
                    id_class_id=Decimal(feat["id_class"].value),
                )
            )
        ModelClass.objects.bulk_create(objects)
        print(f"Inserted {len(objects)} model classes.")

    def import_sensor_types(self, csv_file):
        print("Importing sensor types...")

        ds = DataSource(csv_file)

        objects = []

        for feat in ds[0]:
            objects.append(
                SensorType(
                    id=Decimal(feat["id"].value),
                    name=feat["name"],
                    permanent=bool(feat["permanent"])
                )
            )
        SensorType.objects.bulk_create(objects)
        print(f"Inserted {len(objects)} sensor types.")

    def import_sensor_type_classes(self, csv_file):
        print("Importing sensor type classes...")

        ds = DataSource(csv_file)

        objects = []

        for feat in ds[0]:
            objects.append(
                SensorTypeClass(
                    id_sensor_type_id=Decimal(feat["id_sensor_type"].value),
                    id_class_id=Decimal(feat["id_class"].value),
                )
            )
        SensorTypeClass.objects.bulk_create(objects)
        print(f"Inserted {len(objects)} sensor type classes.")

    def import_sensor_type_installations(self, csv_file):
        print("Importing sensor type installations...")

        ds = DataSource(csv_file)

        objects = []

        for feat in ds[0]:
            objects.append(
                SensorTypeInstallation(
                    id_sensor_type_id=Decimal(feat["id_sensor_type"].value),
                    id_installation_id=Decimal(feat["id_installation"].value),
                )
            )
        SensorTypeInstallation.objects.bulk_create(objects)
        print(f"Inserted {len(objects)} sensor type installations.")

    def import_sensor_type_models(self, csv_file):
        print("Importing sensor type models...")

        ds = DataSource(csv_file)

        objects = []

        for feat in ds[0]:
            objects.append(
                SensorTypeModel(
                    id_sensor_type_id=Decimal(feat["id_sensor_type"].value),
                    id_model_id=Decimal(feat["id_model"].value),
                )
            )
        SensorTypeModel.objects.bulk_create(objects)
        print(f"Inserted {len(objects)} sensor type models.")

    def import_devices(self, csv_file):
        print("Importing devices...")

        ds = DataSource(csv_file)

        objects = []

        for feat in ds[0]:
            objects.append(
                Device(
                    id=Decimal(feat["id"].value),
                    serial=feat["serial"],
                    purchase_date=feat["purchase_date"].value,
                    name=feat["name"],
                    id_model_id=Decimal(feat["id_model"].value),
                )
            )
        Device.objects.bulk_create(objects)
        print(f"Inserted {len(objects)} devices.")
