import pytz
from datetime import datetime
from django.test import TransactionTestCase
from django.core.management import call_command

from comptages.test import utils
from comptages.datamodel import models
from comptages.core import report, importer, statistics


class ImportTest(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        # With TransactionTestCase the db is reset at every test, so we
        # re-import base data every time.
        call_command("importdata")

    def test_report(self):
        # Create count and import some data
        model = models.Model.objects.all()[0]
        device = models.Device.objects.all()[0]
        sensor_type = models.SensorType.objects.all()[0]
        class_ = models.Class.objects.get(name="SWISS10")
        installation = models.Installation.objects.get(name="00056520")
        tz = pytz.timezone("Europe/Zurich")

        count = models.Count.objects.create(
            start_service_date=tz.localize(datetime(2021, 10, 11)),
            end_service_date=tz.localize(datetime(2021, 10, 17)),
            start_process_date=tz.localize(datetime(2021, 10, 11)),
            end_process_date=tz.localize(datetime(2021, 10, 17)),
            start_put_date=tz.localize(datetime(2021, 10, 11)),
            end_put_date=tz.localize(datetime(2021, 10, 17)),
            id_model=model,
            id_device=device,
            id_sensor_type=sensor_type,
            id_class=class_,
            id_installation=installation,
        )

        importer.import_file(utils.test_data_path("00056520.V01"), count)
        importer.import_file(utils.test_data_path("00056520.V02"), count)

        report.prepare_reports("/tmp/", count)

    def test_no_missing_items_from_count_details(self):
        file_name = "64540060_Latenium_PS2021_ChMixte.txt"
        installation_name = "64540060"

        model = models.Model.objects.all()[0]
        device = models.Device.objects.all()[0]
        sensor_type = models.SensorType.objects.all()[0]
        class_ = models.Class.objects.get(name="SPCH13")
        installation = models.Installation.objects.get(name=installation_name)

        count = models.Count.objects.create(
            start_service_date=datetime(2021, 1, 5),
            end_service_date=datetime(2021, 12, 1),
            start_process_date=datetime(2021, 1, 10),
            end_process_date=datetime(2021, 11, 1),
            start_put_date=datetime(2021, 1, 1),
            end_put_date=datetime(2021, 12, 31),
            id_model=model,
            id_device=device,
            id_sensor_type=sensor_type,
            id_class=class_,
            id_installation=installation,
        )

        importer.import_file(utils.test_data_path(file_name), count)
        items = models.CountDetail.objects.filter(
            id_count=count.id, timestamp__gt="2021-03-02", timestamp__lt="2021-03-03"
        )
        self.assertEqual(items.count(), 360)
