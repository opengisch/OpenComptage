import decimal
import os
from pathlib import Path
from itertools import islice
from pathlib import Path
import pytz
from datetime import datetime

from django.test import TransactionTestCase
from django.core.management import call_command

from comptages.core import importer, report
from comptages.datamodel import models
from comptages.report.yearly_report_bike import YearlyReportBike
from comptages.test import utils, yearly_count_for


class ImportTest(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_outputs = "/test_outputs"

    def setUp(self):
        # With TransactionTestCase the db is reset at every test, so we
        # re-import base data every time.
        call_command("importdata")
        for file in Path(self.test_outputs).iterdir():
            os.remove(file)

    def tearDown(self) -> None:
        for file in Path(self.test_outputs).iterdir():
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

    def test_ensure_more_accurate_details(self):
        file_name = "64540060_Latenium_PS2021_ChMixte.txt"
        installation_name = "64540060"
        year = 2021

        installation = models.Installation.objects.get(name=installation_name)
        count = yearly_count_for(year, installation)
        importer.import_file(utils.test_data_path(file_name), count)

        section_id = installation_name
        report = YearlyReportBike("template_yearly_bike.xlsx", year, section_id)
        day_and_hour = report.values_by_day_and_hour()
        hour_and_direction1 = report.values_by_hour_and_direction(1)
        hour_and_direction2 = report.values_by_hour_and_direction(2)
        day_and_month = report.values_by_day_and_month()
        day_of_week = report.values_by_day_of_week()

        for qs_name, qs in zip(
            [
                "day and hour",
                "hour and direction 1",
                "hour and direction 2",
                "day and month",
                "day of week",
            ],
            [
                day_and_hour,
                hour_and_direction1,
                hour_and_direction2,
                day_and_month,
                day_of_week,
            ],
        ):
            print(f"{qs_name}:")
            for value in qs:
                print(value)

    def test_all_sections_default(self):
        # Test if default report features all sections for special case
        test_data_folder = "5350_1_4"
        section_id = "53526896"

        installation = models.Installation.objects.get(lane__id_section_id=section_id)
        n_sections = (
            models.Lane.objects.filter(id_installation=installation.id)
            .values("id_section")
            .count()
        )
        self.assertGreater(n_sections, 0)

        model = models.Model.objects.all().first()
        device = models.Device.objects.all().first()
        sensor_type = models.SensorType.objects.all().first()
        class_ = models.Class.objects.get(name="SWISS10")
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

        report.prepare_reports(self.test_outputs, count)
        found_files = len(list(Path(self.test_outputs).iterdir()))
        # The number of files generated is expected to be: weeks measured x sections
        # so let's make sure all sections are considered in the files generation
        self.assertGreater(found_files, 0)
        self.assertEqual(found_files % n_sections, 0)

    def test_all_sections_yearly(self):
        # Test if yearly report features all sections for special case
        test_data_folder = "ASC"
        installation_name = "53309999"

        installation = models.Installation.objects.get(name=installation_name)

        model = models.Model.objects.all().first()
        device = models.Device.objects.all().first()
        sensor_type = models.SensorType.objects.all().first()
        class_ = models.Class.objects.get(name="SWISS10")
        tz = pytz.timezone("Europe/Zurich")

        count = models.Count.objects.create(
            start_put_date=tz.localize(datetime(2021, 1, 1)),
            start_service_date=tz.localize(datetime(2021, 1, 8)),
            end_service_date=tz.localize(datetime(2021, 12, 15)),
            start_process_date=tz.localize(datetime(2021, 1, 15)),
            end_process_date=tz.localize(datetime(2021, 12, 28)),
            end_put_date=tz.localize(datetime(2021, 12, 31)),
            id_model=model,
            id_device=device,
            id_sensor_type=sensor_type,
            id_class=class_,
            id_installation=installation,
        )

        gen = Path(utils.test_data_path(test_data_folder)).iterdir()
        to_import = 100
        imported = 0
        for file in islice(gen, to_import):
            importer.import_file(utils.test_data_path(str(file)), count)
            imported += 1
            print(f"Remaining: {to_import - imported}")

        sections = models.Section.objects.filter(
            lane__id_installation=installation.id, lane__countdetail__id_count=count.id
        ).distinct()
        self.assertTrue(sections.exists())

        sections_ids = list(sections.values_list("id", flat=True))
        report.prepare_reports(
            file_path=self.test_outputs,
            count=count,
            year=count.start_process_date.year,
            template="yearly",
            sections_ids=sections_ids,
        )
        found_files = len(list(Path(self.test_outputs).iterdir()))
        self.assertEqual(found_files, sections.count())

    def test_report_md(self):
        # Import test data pertaining to "mobilité douce"
        installation_name = "64540060"
        installation = models.Installation.objects.get(name=installation_name)
        model = models.Model.objects.all().first()
        device = models.Device.objects.all().first()
        sensor_type = models.SensorType.objects.all().first()
        class_ = models.Class.objects.get(name="SPCH-MD 5C")
        tz = pytz.timezone("Europe/Zurich")

        count = models.Count.objects.create(
            start_service_date=tz.localize(datetime(2021, 2, 1)),
            end_service_date=tz.localize(datetime(2021, 12, 10)),
            start_process_date=tz.localize(datetime(2021, 2, 10)),
            end_process_date=tz.localize(datetime(2021, 12, 15)),
            start_put_date=tz.localize(datetime(2021, 1, 1)),
            end_put_date=tz.localize(datetime(2021, 1, 5)),
            id_model=model,
            id_device=device,
            id_sensor_type=sensor_type,
            id_class=class_,
            id_installation=installation,
        )

        path_to_file = Path("/OpenComptage/comptages/test/test_data").joinpath(
            "64540060_Latenium_PS2021_ChMixte.txt"
        )
        importer.import_file(str(path_to_file), count)
        print("Imported 1 count files!")

        sections_ids = (
            models.Section.objects.filter(lane__id_installation__name=installation_name)
            .distinct()
            .values_list("id", flat=True)
        )
        self.assertTrue(sections_ids.exists())

        report.prepare_reports(
            file_path=self.test_outputs,
            count=count,
            year=2021,
            sections_ids=list(sections_ids),
            template="yearly",
        )
