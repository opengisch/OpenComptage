from qgis.PyQt.QtSql import QSqlQuery

from comptages.core.utils import connect_to_db
from comptages.data.count_data import CountData
from comptages.data.day_data import DayData
from comptages.data.hour_data import HourData
from comptages.data.direction_data import DirectionData


class DataLoader():

    def __init__(self, count_id, section_id, status):
        self.db = connect_to_db()
        self.count_id = count_id
        self.section_id = section_id
        self.status = status
        self.categories = []
        self.light_vehicles = []
        self.populate_category_and_light_index()

    def load(self):
        function = self.get_detail_direction_data
        if self.is_data_aggregate():
            function = self.get_aggregate_direction_data

        count_data = CountData()
        dates = self.get_count_dates()
        for date in dates:
            day_data = DayData()
            for hour in range(24):
                hour_data = HourData()
                for direction in range(1, 3):
                    direction_data = DirectionData(self.light_vehicles)
                    direction_data.speed_data, direction_data.category_data = \
                        function(date[0], date[1], date[2], hour, direction)
                    hour_data.direction_data.append(direction_data)
                day_data.hour_data.append(hour_data)
            count_data.day_data.append(day_data)

        self.db.close()
        return count_data

    def get_aggregate_direction_data(self, year, month, day, hour, direction):
        query = QSqlQuery(self.db)

        query_str = (
            "select cou.type, cls.value, cls.id_category, spd.value from "
            "comptages.count_aggregate as cou "
            "join comptages.lane as lan on cou.id_lane = lan.id "
            "left join comptages.count_aggregate_value_cls as cls on "
            "cls.id_count_aggregate = cou.id "
            "left join comptages.count_aggregate_value_spd as spd on "
            "spd.id_count_aggregate = cou.id "
            "where "
            "date_part('year', start) = {} and "
            "date_part('month', start) = {} and "
            " date_part('day', start) = {} and "
            "date_part('hour', start) = {} and "
            "cou.id_count = {} and "
            "direction = {} and "
            "id_section = '{}' and "
            "import_status = {} "
            "order by cls.id_category, spd.low ".format(
                year, month, day, hour, self.count_id, direction,
                self.section_id, self.status))

        query.exec_(query_str)

        speed_data = [0]*12
        category_data = [0]*len(self.categories)

        spd_index = 0
        while query.next():
            if query.value(0) == 'CLS':
                category_data[self.category_index(
                    int(query.value(2)))] += int(query.value(1))
            else:
                speed_data[spd_index] = int(query.value(3))
                spd_index += 1

        return speed_data, category_data

    def get_detail_direction_data(self, year, month, day, hour, direction):
        query = QSqlQuery(self.db)

        query_str = (
            "select cou.speed, cou.id_category from "
            "comptages.count_detail as cou "
            "join comptages.lane as lan on cou.id_lane = lan.id "
            "where date_part('year', timestamp) = {} "
            "and date_part('month', timestamp) = {} "
            "and date_part('day', timestamp) = {} "
            "and date_part('hour', timestamp) = {} "
            "and id_count = {} "
            "and direction = {} "
            "and id_section = '{}' "
            "and import_status = {};".format(
                year, month, day, hour, self.count_id, direction,
                self.section_id, self.status))
        query.exec_(query_str)

        speed_data = [0]*13
        category_data = [0]*len(self.categories)

        while query.next():
            speed = int(query.value(0))
            if speed > 120:
                speed = 121
            speed_data[int((speed - 0.1)/10)] += 1
            category_data[self.category_index(int(query.value(1)))] += 1
        return speed_data, category_data

    def category_index(self, category_id):
        return self.categories.index(category_id)

    def populate_category_and_light_index(self):
        query = QSqlQuery(self.db)

        query_str = (
            "select cat.id, cat.light from comptages.count as cou "
            "join comptages.class_category as cc on "
            "cou.id_class = cc.id_class "
            "join comptages.category as cat on cat.id = cc.id_category "
            "where cou.id = {};".format(self.count_id)
        )
        query.exec_(query_str)

        i = 0
        while query.next():
            self.categories.append(int(query.value(0)))
            if query.value(1):
                self.light_vehicles.append(i)
            i += 1

    def get_count_dates(self):
        query = QSqlQuery(self.db)

        query_str = (
            "select start_process_date, end_process_date "
            "from comptages.count where id = {};".format(self.count_id)
        )
        query.exec_(query_str)

        result = []
        while query.next():
            start_date = query.value(0)
            end_date = query.value(1)

        i = 0
        while True:
            date = start_date.addDays(i)
            if date <= end_date:
                result.append((
                    int(date.toString('yyyy')),
                    int(date.toString('MM')),
                    int(date.toString('dd'))))
                i += 1
            else:
                break

        return result

    def is_data_aggregate(self):
        query = QSqlQuery(self.db)

        query_str = (
            "select id from comptages.count_aggregate "
            "where id_count = {}".format(self.count_id))

        query.exec_(query_str)
        if query.next():
            return True
        return False
