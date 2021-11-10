
import pytz
from datetime import datetime
from django.test import TransactionTestCase
from django.core.management import call_command

from opencomptage.test import utils
from opencomptage.datamodel import models
from opencomptage.core import importer


class OpenComptageTest(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        # Import basedata
        call_command("importdata")

    def setUp(self):
        # TODO: delete all count, countDetail and tjm
        pass

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

        importer._parse_and_write(
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
        class_ = models.Class.objects.get(name="SPCH-13")
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

        importer._parse_and_write(
            utils.test_data_path("64210836_TCHO-Capitaine.txt"),
            count)

        self.assertEqual(models.CountDetail.objects.count(), 25867)
