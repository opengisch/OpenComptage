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
        cls.test_outputs = Path("/OpenComptage/test_outputs")
        cls.test_data = Path("/OpenComptage/test_data")

        for file in cls.test_outputs.iterdir():
            os.remove(file)

    def setUp(self):
        # With TransactionTestCase the db is reset at every test, so we
        # re-import base data every time.
        call_command("importdata")
        for file in Path(self.test_outputs).iterdir():
            os.remove(file)

    def test_report(self):
        # Create count and import some data
        installation = models.Installation.objects.get(name="00056520")
        count = yearly_count_for(2021, installation)
        importer.import_file(utils.test_data_path("00056520.V01"), count)
        importer.import_file(utils.test_data_path("00056520.V02"), count)
        report.prepare_reports("/tmp/", count)

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

    def test_yearly_bike_report(self):
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

        path_to_file = self.test_data.joinpath("64540060_Latenium_PS2021_ChMixte.txt")
        importer.import_file(str(path_to_file), count)
        print("Imported 1 count files!")

        models.CountDetail.objects.update(import_status=0)
        print("Forced import status to 'definitive' for testing purposes")

        sections_ids = (
            models.Section.objects.filter(lane__id_installation__name=installation_name)
            .distinct()
            .values_list("id", flat=True)
        )
        self.assertTrue(sections_ids.exists())

        report = YearlyReportBike(
            path_to_output_dir=self.test_outputs,
            year=2021,
            section_id=sections_ids.first(),
        )
        report.run()
