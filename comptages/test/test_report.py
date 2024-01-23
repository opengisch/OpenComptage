from pathlib import Path
import pytz
from datetime import datetime
from django.test import TransactionTestCase
from django.core.management import call_command
from openpyxl import load_workbook

from comptages.test import utils as test_utils
from comptages.datamodel import models
from comptages.report.yearly_report_bike import YearlyReportBike
from comptages.core import report, importer


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

        importer.import_file(test_utils.test_data_path("00056520.V01"), count)
        importer.import_file(test_utils.test_data_path("00056520.V02"), count)

        report.prepare_reports("/tmp/", count)

    def test_busiest_by_season(self):
        # Import test data pertaining to "mobilité douce"
        installation = models.Installation.objects.get(name="00107695")
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

        # Collect count details
        details = YearlyReportBike.count_details_by_season(count)

        def inspect_leaves(d, res) -> list[int]:
            for v in d.values():
                if isinstance(v, int):
                    res.append(v)
                elif isinstance(v, dict):
                    inspect_leaves(v, res)
            return res

        self.assertTrue(all(value > 0 for value in inspect_leaves(details, [])))

        # Prepare workbook
        path_to_inputs = Path("comptages/report").joinpath("template_yearly_bike.xlsx")
        path_to_outputs = Path("/OpenComptage/testoutputs").joinpath("yearly_bike.xlsx")
        wb = load_workbook(path_to_inputs)

        # Write data & save
        ws = wb["Data_yearly_stats"]
        window = ws["B22:F25"]

        for row, season in zip(window, ("printemps", "été", "automne", "hiver")):
            for cell, category in zip(
                row, ("VELO", "MONO", "SHORT", "SPECIAL", "MULTI")
            ):
                cell.value = sum(details[season][category].values())

        wb.save(path_to_outputs)

    def test_busiest_by_day_month(self):
        # Import test data pertaining to "mobilité douce"
        installation = models.Installation.objects.get(name="00107695")
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

        # Collecting count details
        data = YearlyReportBike.count_details_by_day_month(count)

        # Prepare workbook
        path_to_inputs = Path("comptages/report").joinpath("template_yearly_bike.xlsx")
        path_to_outputs = Path("/OpenComptage/testoutputs").joinpath("yearly_bike.xlsx")
        wb = load_workbook(path_to_inputs)

        # Write data & save
        ws = wb["Data_yearly_stats"]
        print_area = ws["B31:H42"]
        for row_idx, row in enumerate(print_area, 1):
            for column_idx, cell in enumerate(row, 1):
                cell.value = data[row_idx][column_idx]

        wb.save(path_to_outputs)

    def test_busiest_by_various_criteria(self):
        # Import test data pertaining to "mobilité douce"
        installation = models.Installation.objects.get(name="00107695")
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

        # Collecting count details
        data = YearlyReportBike.count_details_by_various_criteria(count)
        print(data)
        return

        # Prepare workbook
        path_to_inputs = Path("comptages/report").joinpath("template_yearly_bike.xlsx")
        path_to_outputs = Path("/OpenComptage/testoutputs").joinpath("yearly_bike.xlsx")
        wb = load_workbook(path_to_inputs)

        # Write data & save
        print(data)
        ws = wb["Data_yearly_stats"]
        print_area = ws["B2:G8"]
        row_names = data.keys()
        column_names = ("VELO", "MONO", "SHORT", "SPECIAL", "MULTI")
        for row_name, row in zip(row_names, print_area):
            for column_name, cell in zip(column_names, row):
                print(row_name, column_name)
                print(data[row_name])
                if value := next(
                    filter(lambda item: column_name in item, data[row_name]), None
                ):
                    cell.value = value
        wb.save(path_to_outputs)
