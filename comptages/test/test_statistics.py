import pytz
from datetime import datetime
from django.test import TransactionTestCase
from django.core.management import call_command

from comptages.test import utils
from comptages.datamodel import models
from comptages.core import importer, statistics, definitions


class StatisticsTest(TransactionTestCase):

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        # With TransactionTestCase the db is reset at every test, so we
        # re-import base data every time.
        call_command("importdata")

    def test_time_data(self):
        # Create count and import some data
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

        # self.assertEqual(models.CountDetail.objects.count(), 18114)

        # print(statistics.get_time_data(count))
        print(statistics.get_category_data(count, status=definitions.IMPORT_STATUS_QUARANTINE))

