from datetime import datetime, timedelta

import pytz
from django.core.management import call_command
from django.test import TransactionTestCase

from comptages.core import definitions, importer, statistics
from comptages.datamodel import models
from comptages.test import utils


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
        tz = pytz.timezone("Europe/Zurich")

        count = models.Count.objects.create(
            start_service_date=tz.localize(datetime(2021, 10, 15)),
            end_service_date=tz.localize(datetime(2021, 10, 16)),
            start_process_date=tz.localize(datetime(2021, 10, 15)),
            end_process_date=tz.localize(datetime(2021, 10, 16)),
            start_put_date=tz.localize(datetime(2021, 10, 15)),
            end_put_date=tz.localize(datetime(2021, 10, 16)),
            id_model=model,
            id_device=device,
            id_sensor_type=sensor_type,
            id_class=class_,
            id_installation=installation,
        )

        importer.import_file(utils.test_data_path("00056520.V01"), count)

        self.assertEqual(models.CountDetail.objects.count(), 18114)

        section = models.Section.objects.filter(
            lane__id_installation__count=count
        ).distinct()[0]

        df = statistics.get_time_data(count, section)

        self.assertEqual(df["thm"][0], 305)
        self.assertEqual(df["thm"][1], 1306)

        df, mean = statistics.get_day_data(count, section, direction=1)
        self.assertEqual(df["tj"][0], 9871)
        df, mean = statistics.get_day_data(count, section, direction=2)
        self.assertEqual(mean, 8243)

        df = statistics.get_category_data(
            count, section, status=definitions.IMPORT_STATUS_QUARANTINE
        )
        self.assertEqual(df["value"][0], 1)
        self.assertEqual(df["value"][1], 93)
        self.assertEqual(df["value"][2], 1)
        self.assertEqual(df["value"][3], 17315)
        self.assertEqual(df["value"][4], 16)
        self.assertEqual(df["value"][5], 570)
        self.assertEqual(df["value"][6], 15)
        self.assertEqual(df["value"][7], 4)
        self.assertEqual(df["value"][8], 70)
        self.assertEqual(df["value"][9], 12)
        self.assertEqual(df["value"][10], 17)

        df = statistics.get_speed_data(count, section)
        self.assertEqual(df["times"][0], 0)
        self.assertEqual(df["times"][1], 1)
        self.assertEqual(df["times"][2], 13)
        self.assertEqual(df["times"][3], 638)
        self.assertEqual(df["times"][4], 11331)
        self.assertEqual(df["times"][5], 5792)
        self.assertEqual(df["times"][6], 304)
        self.assertEqual(df["times"][7], 29)
        self.assertEqual(df["times"][8], 5)
        self.assertEqual(df["times"][9], 0)
        self.assertEqual(df["times"][10], 0)
        self.assertEqual(df["times"][11], 0)
        self.assertEqual(df["times"][12], 1)

    def test_special_period(self):
        # Add a special period
        models.SpecialPeriod.objects.create(
            start_date=datetime(2020, 1, 1), end_date=datetime(2020, 1, 31)
        )

        self.assertEqual(
            len(
                statistics.get_special_periods(
                    datetime(2020, 1, 1), datetime(2020, 1, 1)
                )
            ),
            1,
        )

        self.assertEqual(
            len(
                statistics.get_special_periods(
                    datetime(2020, 1, 1), datetime(2020, 1, 31)
                )
            ),
            1,
        )

        self.assertEqual(
            len(
                statistics.get_special_periods(
                    datetime(2020, 1, 31), datetime(2020, 1, 31)
                )
            ),
            1,
        )

        self.assertEqual(
            len(
                statistics.get_special_periods(
                    datetime(2019, 12, 25), datetime(2020, 1, 1)
                )
            ),
            1,
        )

        self.assertEqual(
            len(
                statistics.get_special_periods(
                    datetime(2019, 12, 25), datetime(2020, 1, 10)
                )
            ),
            1,
        )

        self.assertEqual(
            len(
                statistics.get_special_periods(
                    datetime(2019, 12, 25), datetime(2019, 12, 26)
                )
            ),
            0,
        )

        self.assertEqual(
            len(
                statistics.get_special_periods(
                    datetime(2021, 12, 25), datetime(2021, 12, 26)
                )
            ),
            0,
        )

        self.assertEqual(
            len(
                statistics.get_special_periods(
                    datetime(2020, 1, 10), datetime(2020, 1, 15)
                )
            ),
            1,
        )

        self.assertEqual(
            len(
                statistics.get_special_periods(
                    datetime(2020, 1, 10), datetime(2020, 2, 15)
                )
            ),
            1,
        )

    def test_light_numbers(self):
        # Create count and import some data
        model = models.Model.objects.all()[0]
        device = models.Device.objects.all()[0]
        sensor_type = models.SensorType.objects.all()[0]
        class_ = models.Class.objects.get(name="SWISS10")
        installation = models.Installation.objects.get(name="00056365")
        tz = pytz.timezone("Europe/Zurich")

        count = models.Count.objects.create(
            start_service_date=tz.localize(datetime(2017, 3, 27)),
            end_service_date=tz.localize(datetime(2017, 4, 4)),
            start_process_date=tz.localize(datetime(2017, 3, 27)),
            end_process_date=tz.localize(datetime(2017, 4, 4)),
            start_put_date=tz.localize(datetime(2017, 3, 27)),
            end_put_date=tz.localize(datetime(2017, 4, 4)),
            id_model=model,
            id_device=device,
            id_sensor_type=sensor_type,
            id_class=class_,
            id_installation=installation,
        )

        importer.import_file(utils.test_data_path("00056365.A00"), count)

        section = models.Section.objects.filter(
            lane__id_installation__count=count
        ).distinct()[0]
        res = statistics.get_light_numbers(
            count,
            section,
            start=tz.localize(datetime(2017, 3, 27)),
            end=tz.localize(datetime(2017, 3, 28)),
        )

        self.assertEqual(res, {False: 15, True: 492})

        res = statistics.get_time_data(
            count,
            section,
            start=tz.localize(datetime(2017, 3, 27)),
            end=tz.localize(datetime(2017, 3, 28)),
        )

        self.assertEqual(res["thm"][0], 252)
        self.assertEqual(res["thm"][1], 255)

        monday = tz.localize(datetime(2017, 3, 27))

        res = statistics.get_speed_data_by_hour(
            count,
            section,
            start=monday,
            end=monday + timedelta(days=7),
            speed_low=0,
            speed_high=30,
        )

        self.assertEqual((10, 5), res[0])
        self.assertEqual((11, 1), res[1])

    def test_get_speed_data_empty(self):
        # Create count and import some data
        model = models.Model.objects.all()[0]
        device = models.Device.objects.all()[0]
        sensor_type = models.SensorType.objects.all()[0]
        class_ = models.Class.objects.get(name="SWISS10")
        installation = models.Installation.objects.get(name="53409999")
        tz = pytz.timezone("Europe/Zurich")

        count = models.Count.objects.create(
            start_service_date=tz.localize(datetime(2022, 4, 25)),
            end_service_date=tz.localize(datetime(2022, 4, 27)),
            start_process_date=tz.localize(datetime(2022, 4, 25)),
            end_process_date=tz.localize(datetime(2022, 4, 27)),
            start_put_date=tz.localize(datetime(2022, 4, 25)),
            end_put_date=tz.localize(datetime(2022, 4, 27)),
            id_model=model,
            id_device=device,
            id_sensor_type=sensor_type,
            id_class=class_,
            id_installation=installation,
        )

        importer.import_file(utils.test_data_path("53409999.V04"), count)

        # This is a special case and there are no data for the first 2 sections
        sections = models.Section.objects.filter(
            lane__id_installation__count=count
        ).distinct()
        self.assertTrue(statistics.get_speed_data(count, sections[0]).empty)

        self.assertFalse(statistics.get_speed_data(count, sections[2]).empty)
