from datetime import datetime

import pytz
from django.core.management import call_command
from django.test import TransactionTestCase

from comptages.core import importer, report
from comptages.datamodel import models
from comptages.test import utils


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
