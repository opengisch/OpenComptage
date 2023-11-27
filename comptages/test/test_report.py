from pathlib import Path
import pytz
from datetime import datetime
from django.test import TransactionTestCase
from django.core.management import call_command
import os

from comptages.test import utils
from comptages.datamodel import models
from comptages.core import report, importer


class ImportTest(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        cls.testoutputs = "/OpenComptage/testoutputs"

    def setUp(self):
        # With TransactionTestCase the db is reset at every test, so we
        # re-import base data every time.
        call_command("importdata")

    def tearDown(self):
        for file in Path(self.testoutputs).iterdir():
            os.remove(file)

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

    def test_report_ensure_first_sections(self):
        # Create count and import some data pertaining to
        # a specific special case
        section_id = "53526896"
        test_data_folder = "5350_1_4"

        model = models.Model.objects.all()[0]
        device = models.Device.objects.all()[0]
        sensor_type = models.SensorType.objects.all()[0]
        class_ = models.Class.objects.get(name="SWISS10")
        installation = models.Installation.objects.get(lane__id_section_id=section_id)
        tz = pytz.timezone("Europe/Zurich")

        count = models.Count.objects.create(
            start_service_date=tz.localize(datetime(2021, 3, 1)),
            end_service_date=tz.localize(datetime(2021, 3, 2)),
            start_process_date=tz.localize(datetime(2021, 3, 15)),
            end_process_date=tz.localize(datetime(2021, 3, 28)),
            start_put_date=tz.localize(datetime(2021, 2, 20)),
            end_put_date=tz.localize(datetime(2021, 4, 1)),
            id_model=model,
            id_device=device,
            id_sensor_type=sensor_type,
            id_class=class_,
            id_installation=installation,
        )

        for file in Path(utils.test_data_path(test_data_folder)).iterdir():
            importer.import_file(utils.test_data_path(str(file)), count)

        report.prepare_reports(self.testoutputs, count)
        self.assertEqual(len(list(Path(self.testoutputs).iterdir())), 4)
