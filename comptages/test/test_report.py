import decimal
import os
from itertools import chain
from pathlib import Path

from django.core.management import call_command
from django.db.models.manager import Manager
from django.test import TransactionTestCase

from comptages.core import importer, report
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
        year = 2021

        installation = models.Installation.objects.get(name=installation_name)
        count = yearly_count_for(year, installation)
        importer.import_file(utils.test_data_path(file_name), count)

        section_id = installation_name
        report = YearlyReportBike("template_yearly_bike.xlsx", year, section_id)
        report_dir1 = report.values_by_hour_and_direction(1)
        report_dir2 = report.values_by_hour_and_direction(2)

        tjms = []
        if report_dir1.exists():
            report_dir1_values = report_dir1.values_list("tjm", flat=True)
            tjms += [decimal.Decimal(value) for value in report_dir1_values]
        if report_dir2.exists():
            report_dir2_values = report_dir2.values_list("tjm", flat=True)
            tjms += [decimal.Decimal(value) for value in report_dir2_values]
        for value in tjms:
            with self.subTest():
                exponent = value.as_tuple().exponent
                self.assertEqual(exponent, 3)
        print(f"Section {section_id} is GO")
