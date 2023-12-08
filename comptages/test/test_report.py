from pathlib import Path
import pytz
from datetime import datetime
from django.test import TransactionTestCase
from django.db.models import Count
from django.core.management import call_command
import os

from comptages.test import utils
from comptages.datamodel import models
from comptages.core import report, importer


class ImportTest(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        cls.testoutputs = "/testoutputs"

    def setUp(self):
        for file in Path(self.testoutputs).iterdir():
            os.remove(file)
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

    def test_generate_yearly_reports(self):
        call_command("importdata", "--only-swiss10year", "--limit", 100)
        # year and section id come from --add-swiss10year`
        year = 2021
        section_id = "00107695"
        installations = models.Installation.objects.filter(lane__id_section=section_id)
        installation = installations.first()

        count = models.Count.objects.filter(id_installation=installation.id).first()
        report.prepare_reports(
            self.testoutputs, count, year, "yearly", section_id=section_id
        )

        self.assertTrue(list(Path(self.testoutputs).iterdir()))

    def test_generate_yearly_reports_special_case(self):
        call_command("importdata", "--only-swiss10year", "--limit", 100)

        special_case_installations = models.Installation.objects.annotate(
            sections=Count("lane__id_section")
        ).filter(sections__lte=3)
        self.assertTrue(special_case_installations.exists())

        count = models.Count.objects.filter(
            id_installation__in=special_case_installations
        ).first()

        year = count.start_process_date.year
        section_id = special_case_installations.values_list(
            "lane__id_section", flat=True
        ).first()

        print(
            f"Preparing reports for count = {count}, year = {year}, section_id = {section_id}"
        )
        report.prepare_reports(
            self.testoutputs, count, year, "yearly", section_id=section_id
        )
        self.assertTrue(list(Path(self.testoutputs).iterdir()))
