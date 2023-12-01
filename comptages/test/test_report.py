import decimal
from itertools import chain
import os
from pathlib import Path
from django.test import TransactionTestCase
from django.core.management import call_command
from django.db.models.manager import Manager

from comptages.core import report, importer
from comptages.datamodel import models
from comptages.report.yearly_report_bike import YearlyReportBike
from comptages.test import utils, yearly_count_for


class ImportTest(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        cls.testouputs = "/OpenComptage/testoutputs"

    def setUp(self):
        # With TransactionTestCase the db is reset at every test, so we
        # re-import base data every time.
        call_command("importdata")

    def tearDown(self) -> None:
        for file in Path(self.testouputs).iterdir():
            os.remove(file)

    def test_report(self):
        # Create count and import some data
        installation = models.Installation.objects.get(name="00056520")
        count = yearly_count_for(2021, installation)
        importer.import_file(utils.test_data_path("00056520.V01"), count)
        importer.import_file(utils.test_data_path("00056520.V02"), count)
        report.prepare_reports("/tmp/", count)

    def test_ensure_non_rounded_values(self):
        file_name = "64540060_Latenium_PS2021_ChMixte.txt"
        installation_name = "64540060"
        installation = models.Installation.objects.get(name=installation_name)
        count = yearly_count_for(2021, installation)
        importer.import_file(utils.test_data_path(file_name), count)

        lanes_installation: Manager = installation.lane_set
        section_ids = lanes_installation.values_list("id_section", flat=True)
        self.assertTrue(section_ids.exists())

        report = YearlyReportBike("template_yearly_bike.xlsx", 2021, section_ids[0])
        report_dir1 = report.values_by_hour_and_direction(1).values_list(
            "tjm", flat=True
        )
        report_dir2 = report.values_by_hour_and_direction(2).values_list(
            "tjm", flat=True
        )
        self.assertTrue(report_dir1.exists())
        self.assertTrue(report_dir2.exists())

        tjms_dir1 = (decimal.Decimal(v) for v in report_dir1)
        tjms_dir2 = (decimal.Decimal(v) for v in report_dir2)
        with self.subTest():
            for value in chain(tjms_dir1, tjms_dir2):
                print(value)
                self.assertEqual(value.as_tuple().exponent, 3)
