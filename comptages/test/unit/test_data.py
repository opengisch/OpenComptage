import unittest

from comptages.data.direction_data import DirectionData
from comptages.data.hour_data import HourData
from comptages.data.day_data import DayData
from comptages.data.count_data import CountData


# run from main repo directory `python -m unittest comptages/test/unit/test_data.py`
class TestData(unittest.TestCase):

    def test_direction_data_speed_total(self):
        directionData = DirectionData()
        directionData.speed_data.append(0)
        directionData.speed_data.append(2)
        directionData.speed_data.append(1)
        directionData.speed_data.append(151)
        directionData.speed_data.append(197)
        directionData.speed_data.append(23)
        directionData.speed_data.append(2)
        directionData.speed_data.append(2)
        directionData.speed_data.append(0)
        directionData.speed_data.append(0)
        directionData.speed_data.append(0)
        directionData.speed_data.append(0)

        self.assertEqual(378, directionData.total())

    def test_direction_data_category_total(self):
        directionData = DirectionData()
        directionData.category_data.append(0)
        directionData.category_data.append(5)
        directionData.category_data.append(358)
        directionData.category_data.append(0)
        directionData.category_data.append(12)
        directionData.category_data.append(1)
        directionData.category_data.append(0)
        directionData.category_data.append(2)
        directionData.category_data.append(0)
        directionData.category_data.append(0)

        self.assertEqual(378, directionData.total())

    def test_direction_data_weight(self):
        directionData = DirectionData([1, 2, 3, 4, 5, 6])
        directionData.category_data.append(0)
        directionData.category_data.append(5)
        directionData.category_data.append(358)
        directionData.category_data.append(0)
        directionData.category_data.append(12)
        directionData.category_data.append(1)
        directionData.category_data.append(0)
        directionData.category_data.append(2)
        directionData.category_data.append(0)
        directionData.category_data.append(0)

        self.assertEqual(376, directionData.light_vehicles())
        self.assertEqual(2, directionData.heavy_vehicles())
        self.assertEqual(0.53, directionData.percent_heavy_vehicles())

    def test_hour_data(self):
        directionData1 = DirectionData([1, 2, 3, 4, 5, 6])
        directionData1.category_data.append(0)
        directionData1.category_data.append(5)
        directionData1.category_data.append(358)
        directionData1.category_data.append(0)
        directionData1.category_data.append(12)
        directionData1.category_data.append(1)
        directionData1.category_data.append(0)
        directionData1.category_data.append(2)
        directionData1.category_data.append(0)
        directionData1.category_data.append(0)

        directionData2 = DirectionData([1, 2, 3, 4, 5, 6])
        directionData2.category_data.append(0)
        directionData2.category_data.append(3)
        directionData2.category_data.append(268)
        directionData2.category_data.append(0)
        directionData2.category_data.append(8)
        directionData2.category_data.append(0)
        directionData2.category_data.append(0)
        directionData2.category_data.append(2)
        directionData2.category_data.append(0)
        directionData2.category_data.append(1)

        hourData = HourData()
        hourData.direction_data.append(directionData1)
        hourData.direction_data.append(directionData2)

        self.assertEqual(660, hourData.total())
        self.assertEqual(655, hourData.light_vehicles())
        self.assertEqual(5, hourData.heavy_vehicles())
        self.assertEqual(0.76, hourData.percent_heavy_vehicles())

        self.assertEqual(378, hourData.total(0))
        self.assertEqual(376, hourData.light_vehicles(0))
        self.assertEqual(2, hourData.heavy_vehicles(0))
        self.assertEqual(0.53, hourData.percent_heavy_vehicles(0))
        self.assertEqual(282, hourData.total(1))
        self.assertEqual(279, hourData.light_vehicles(1))
        self.assertEqual(3, hourData.heavy_vehicles(1))
        self.assertEqual(1.06, hourData.percent_heavy_vehicles(1))

    def test_day_data(self):
        directionData1 = DirectionData([1, 2, 3, 4, 5, 6])
        directionData1.category_data.append(0)
        directionData1.category_data.append(5)
        directionData1.category_data.append(358)
        directionData1.category_data.append(0)
        directionData1.category_data.append(12)
        directionData1.category_data.append(1)
        directionData1.category_data.append(0)
        directionData1.category_data.append(2)
        directionData1.category_data.append(0)
        directionData1.category_data.append(0)

        directionData2 = DirectionData([1, 2, 3, 4, 5, 6])
        directionData2.category_data.append(0)
        directionData2.category_data.append(3)
        directionData2.category_data.append(268)
        directionData2.category_data.append(0)
        directionData2.category_data.append(8)
        directionData2.category_data.append(0)
        directionData2.category_data.append(0)
        directionData2.category_data.append(2)
        directionData2.category_data.append(0)
        directionData2.category_data.append(1)

        hourData = HourData()
        hourData.direction_data.append(directionData1)
        hourData.direction_data.append(directionData2)

        dayData = DayData()
        dayData.hour_data.append(hourData)
        dayData.hour_data.append(hourData)

        self.assertEqual(1320, dayData.total())
        self.assertEqual(1310, dayData.light_vehicles())
        self.assertEqual(10, dayData.heavy_vehicles())
        self.assertEqual(0.76, hourData.percent_heavy_vehicles())

    def test_count_data(self):
        directionData1 = DirectionData([1, 2, 3, 4, 5, 6])
        directionData1.category_data.append(0)
        directionData1.category_data.append(5)
        directionData1.category_data.append(358)
        directionData1.category_data.append(0)
        directionData1.category_data.append(12)
        directionData1.category_data.append(1)
        directionData1.category_data.append(0)
        directionData1.category_data.append(2)
        directionData1.category_data.append(0)
        directionData1.category_data.append(0)

        directionData2 = DirectionData([1, 2, 3, 4, 5, 6])
        directionData2.category_data.append(0)
        directionData2.category_data.append(3)
        directionData2.category_data.append(268)
        directionData2.category_data.append(0)
        directionData2.category_data.append(8)
        directionData2.category_data.append(0)
        directionData2.category_data.append(0)
        directionData2.category_data.append(2)
        directionData2.category_data.append(0)
        directionData2.category_data.append(1)

        hourData = HourData()
        hourData.direction_data.append(directionData1)
        hourData.direction_data.append(directionData2)

        dayData = DayData()
        dayData.hour_data.append(hourData)
        dayData.hour_data.append(hourData)

        countData = CountData()
        countData.day_data.append(dayData)
        countData.day_data.append(dayData)
        countData.day_data.append(dayData)

        self.assertEqual(1320, countData.average_total())
        self.assertEqual(1320, countData.average_total(days=[1, 2]))

        self.assertEqual(378*2, countData.average_total(direction=0))
        self.assertEqual(282*2, countData.average_total(direction=1))

        self.assertEqual(1310, countData.average_light_vehicles())
        self.assertEqual(376*2, countData.average_light_vehicles(direction=0))
        self.assertEqual(279*2, countData.average_light_vehicles(direction=1))

        self.assertEqual(10, countData.average_heavy_vehicles())
        self.assertEqual(2*2, countData.average_heavy_vehicles(direction=0))
        self.assertEqual(3*2, countData.average_heavy_vehicles(direction=1))

        self.assertEqual(0.76, countData.average_percent_heavy_vehicles())
        self.assertEqual(0.53, countData.average_percent_heavy_vehicles(0))
        self.assertEqual(1.06, countData.average_percent_heavy_vehicles(1))
