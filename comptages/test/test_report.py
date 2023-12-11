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
from comptages.core import report, importer


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
        year = 2021

        installation = models.Installation.objects.get(name=installation_name)
        count = yearly_count_for(year, installation)
        importer.import_file(utils.test_data_path(file_name), count)

        lanes_installation: Manager = installation.lane_set
        section_ids = lanes_installation.values_list("id_section", flat=True)
        self.assertTrue(section_ids.exists())

        for section_id in section_ids:
            with self.subTest():
                report = YearlyReportBike("template_yearly_bike.xlsx", year, section_id)
                report_dir1 = report.values_by_hour_and_direction(1)
                report_dir2 = report.values_by_hour_and_direction(2)
                report_dir1_values = report_dir1.values_list("tjm", flat=True)
                report_dir2_values = report_dir2.values_list("tjm", flat=True)
                self.assertTrue(report_dir1_values.exists())
                self.assertTrue(report_dir2_values.exists())

                tjms = (
                    decimal.Decimal(v)
                    for v in chain(report_dir1_values, report_dir2_values)
                )
                for value in tjms:
                    with self.subTest():
                        exponent = value.as_tuple().exponent
                        self.assertEqual(exponent, 3)
                print(f"Section {section_id} is GO")
