import pytz
from datetime import datetime
from django.test import TransactionTestCase
from django.core.management import call_command

from comptages.test import utils
from comptages.datamodel import models
from comptages.core import importer


class ImportTest(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        # With TransactionTestCase the db is reset at every test, so we
        # re-import base data every time.
        call_command("importdata")

    def test_import_vbv1(self):
        model = models.Model.objects.all()[0]
        device = models.Device.objects.all()[0]
        sensor_type = models.SensorType.objects.all()[0]
        class_ = models.Class.objects.get(name="SWISS10")
        installation = models.Installation.objects.get(name="00056520")

        count = models.Count.objects.create(
            start_service_date=datetime(2021, 10, 15),
            end_service_date=datetime(2021, 10, 16),
            start_process_date=datetime(2021, 10, 15),
            end_process_date=datetime(2021, 10, 16),
            start_put_date=datetime(2021, 10, 15),
            end_put_date=datetime(2021, 10, 16),
            id_model=model,
            id_device=device,
            id_sensor_type=sensor_type,
            id_class=class_,
            id_installation=installation,
        )

        importer.import_file(
            utils.test_data_path("00056520.V01"),
            count)

        self.assertEqual(models.CountDetail.objects.count(), 18114)

        tz = pytz.timezone("Europe/Zurich")

        first = tz.normalize(models.CountDetail.objects.first().timestamp)
        last = tz.normalize(models.CountDetail.objects.last().timestamp)

        self.assertEqual(first, tz.localize(datetime(2021, 10, 15, 9, 46, 43, 500000)))
        self.assertEqual(last, tz.localize(datetime(2021, 10, 15, 23, 59, 54, 600000)))

    def test_import_mc(self):
        model = models.Model.objects.all()[0]
        device = models.Device.objects.all()[0]
        sensor_type = models.SensorType.objects.all()[0]
        class_ = models.Class.objects.get(name="SPCH13")
        installation = models.Installation.objects.get(name="64210836")

        count = models.Count.objects.create(
            start_service_date=datetime(2021, 9, 10),
            end_service_date=datetime(2021, 9, 21),
            start_process_date=datetime(2021, 9, 10),
            end_process_date=datetime(2021, 9, 21),
            start_put_date=datetime(2021, 9, 10),
            end_put_date=datetime(2021, 9, 21),
            id_model=model,
            id_device=device,
            id_sensor_type=sensor_type,
            id_class=class_,
            id_installation=installation,
        )

        importer.import_file(
            utils.test_data_path("64210836_TCHO-Capitaine.txt"),
            count)

        self.assertEqual(models.CountDetail.objects.count(), 25867)

        tz = pytz.timezone("Europe/Zurich")

        first = tz.normalize(models.CountDetail.objects.first().timestamp)
        last = tz.normalize(models.CountDetail.objects.last().timestamp)

        self.assertEqual(first, tz.localize(datetime(2021, 9, 10, 4, 16, 16)))
        self.assertEqual(last, tz.localize(datetime(2021, 9, 21, 8, 2, 15)))

    def test_import_int2(self):
        model = models.Model.objects.all()[0]
        device = models.Device.objects.all()[0]
        sensor_type = models.SensorType.objects.all()[0]
        class_ = models.Class.objects.get(name="SWISS10")
        installation = models.Installation.objects.get(name="10020260")

        count = models.Count.objects.create(
            start_service_date=datetime(2018, 4, 13),
            end_service_date=datetime(2018, 5, 1),
            start_process_date=datetime(2018, 4, 13),
            end_process_date=datetime(2018, 5, 1),
            start_put_date=datetime(2018, 4, 13),
            end_put_date=datetime(2018, 5, 1),
            id_model=model,
            id_device=device,
            id_sensor_type=sensor_type,
            id_class=class_,
            id_installation=installation,
        )

        importer.import_file(
            utils.test_data_path("10020260.A01"),
            count)

        tz = pytz.timezone("Europe/Zurich")

        first = tz.normalize(models.CountDetail.objects.first().timestamp)
        last = tz.normalize(models.CountDetail.objects.last().timestamp)

        self.assertEqual(first, tz.localize(datetime(2018, 4, 13, 12, 0)))
        self.assertEqual(last, tz.localize(datetime(2018, 5, 1, 13, 0)))

    def test_import_simple_int2(self):
        model = models.Model.objects.all()[0]
        device = models.Device.objects.all()[0]
        sensor_type = models.SensorType.objects.all()[0]
        class_ = models.Class.objects.get(name="SWISS10")
        installation = models.Installation.objects.get(name="64080011")

        count = models.Count.objects.create(
            start_service_date=datetime(2018, 9, 24),
            end_service_date=datetime(2018, 9, 24),
            start_process_date=datetime(2018, 9, 24),
            end_process_date=datetime(2018, 9, 24),
            start_put_date=datetime(2018, 9, 24),
            end_put_date=datetime(2018, 9, 24),
            id_model=model,
            id_device=device,
            id_sensor_type=sensor_type,
            id_class=class_,
            id_installation=installation,
        )

        importer.import_file(
            utils.test_data_path("simple_aggregate_multi_spec.i00"),
            count)

        self.assertEqual(models.CountDetail.objects.count(), 52)

        tz = pytz.timezone("Europe/Zurich")

        first = tz.normalize(models.CountDetail.objects.first().timestamp)
        last = tz.normalize(models.CountDetail.objects.last().timestamp)

        self.assertEqual(first, tz.localize(datetime(2018, 9, 24, 0, 0)))
        self.assertEqual(last, tz.localize(datetime(2018, 9, 24, 1, 0)))

        speed20 = models.CountDetail.objects.filter(speed=20)
        self.assertEqual(speed20[0].times, 3)
        self.assertEqual(speed20[1].times, 4)

    def test_cat_bin(self):
        model = models.Model.objects.all()[0]
        device = models.Device.objects.all()[0]
        sensor_type = models.SensorType.objects.all()[0]
        class_ = models.Class.objects.get(name="SWISS10")
        installation = models.Installation.objects.get(name="64080011")

        count = models.Count.objects.create(
            start_service_date=datetime(2018, 9, 24),
            end_service_date=datetime(2018, 9, 24),
            start_process_date=datetime(2018, 9, 24),
            end_process_date=datetime(2018, 9, 24),
            start_put_date=datetime(2018, 9, 24),
            end_put_date=datetime(2018, 9, 24),
            id_model=model,
            id_device=device,
            id_sensor_type=sensor_type,
            id_class=class_,
            id_installation=installation,
        )

        self.assertEqual(
            importer._populate_category_dict(count),
            {0: 922, 1: 22, 2: 23, 3: 24, 4: 25, 5: 26, 6: 27, 7: 28, 8: 29, 9: 30, 10: 31}
        )

    def test_lane_dict(self):
        pass
