from qgis.PyQt.QtSql import QSqlQuery

from comptages.core.utils import connect_to_db
from comptages.data.count_data import CountData
from comptages.data.day_data import DayData
from comptages.data.hour_data import HourData
from comptages.data.direction_data import DirectionData


class DataLoader():

    _monthly_coefficients = [93, 96, 100, 102, 101, 104,
                             98, 98, 104, 103, 102, 98]

    def __init__(self, count_id, section_id, status):
        self.db = connect_to_db()
        self.count_id = count_id
        self.section_id = section_id
        self.status = status
        self.categories = []
        self.light_vehicles = []
        self.populate_category_and_light_index()
        self.attributes = {}
        self.query = QSqlQuery(self.db)

    def load(self):

        function = self.get_detail_direction_data
        self.attributes['aggregate'] = False
        if self.is_data_aggregate():
            function = self.get_aggregate_direction_data
            self.attributes['aggregate'] = True

        self.read_attributes()
        count_data = CountData()
        count_data.attributes = self.attributes
        dates = self.get_count_dates()
        self.attributes['dates'] = dates
        for date in dates:

            if self.is_data_aggregate():
                day_data = DayData()
                for hour in range(24):
                    hour_data = HourData()
                    for direction in range(1, 3):
                        direction_data = DirectionData(self.light_vehicles)
                        direction_data.speed_data, \
                            direction_data.category_data = \
                            function(
                                date[0], date[1], date[2], hour, direction)
                        hour_data.direction_data.append(direction_data)
                    day_data.hour_data.append(hour_data)
                    day_data.monthly_coefficient = self._monthly_coefficients[
                        date[1]-1]
            else:
                day_data = self.get_detail_day_data(
                    date[0], date[1], date[2])

            day_data.monthly_coefficient = self._monthly_coefficients[
                date[1]-1]
            count_data.day_data.append(day_data)

        self.db.close()
        return count_data

    def get_aggregate_direction_data(self, year, month, day, hour, direction):
        query = self.query

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
            elif query.value(0) == 'SPD':
                speed_data[spd_index] = int(query.value(3))
                spd_index += 1

        return speed_data, category_data

    def get_detail_day_data(self, year, month, day):
        day_data = DayData()
        query = self.query

        query_str = (
            "select cou.speed, cou.id_category, "
            "date_part('hour', cou.timestamp), lan.direction from "
            "comptages.count_detail as cou "
            "join comptages.lane as lan on cou.id_lane = lan.id "
            "where date_part('year', timestamp) = {} "
            "and date_part('month', timestamp) = {} "
            "and date_part('day', timestamp) = {} "
            "and id_count = {} "
            "and id_section = '{}' "
            "and import_status = {};".format(
                year, month, day, self.count_id,
                self.section_id, self.status))
        query.exec_(query_str)

        hour_datas = []

        for _ in range(25):
            hour_data = HourData()
            direction_data_1 = DirectionData(self.light_vehicles)
            direction_data_1.speed_data = [0]*13
            direction_data_1.category_data = [0]*len(self.categories)

            direction_data_2 = DirectionData(self.light_vehicles)
            direction_data_2.speed_data = [0]*13
            direction_data_2.category_data = [0]*len(self.categories)

            hour_data.direction_data.append(direction_data_1)
            hour_data.direction_data.append(direction_data_2)
            hour_datas.append(hour_data)

        while query.next():

            hour = int(query.value(2))
            direction = int(query.value(3))-1
            speed = int(query.value(0))

            if speed > 120:
                speed = 121

            hour_datas[hour].direction_data[direction].speed_data[
                int((speed - 0.1)/10)] += 1

            hour_datas[hour].direction_data[direction].category_data[
                self.category_index(int(query.value(1)))] += 1

        day_data.hour_data = hour_datas
        return day_data

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

    def read_attributes(self):
        query = QSqlQuery(self.db)

        query_str = (
            "select cou.remarks, sty.name, mdl.name, cla.name "
            "from comptages.count as cou "
            "join comptages.sensor_type as sty on cou.id_sensor_type = sty.id "
            "join comptages.model as mdl on cou.id_model = mdl.id "
            "join comptages.class as cla on cou.id_class = cla.id "
            "where cou.id = {} ".format(self.count_id))

        query.exec_(query_str)

        query.next()
        self.attributes['remarks'] = query.value(0)
        self.attributes['sensor_type'] = query.value(1)
        self.attributes['model'] = query.value(2)
        self.attributes['class'] = query.value(3)

        query_str = (
            "select sec.owner, sec.road, sec.start_pr, sec.end_pr, "
            "sec.start_dist, sec.end_dist, sec.place_name, "
            "lan.direction, lan.direction_desc "
            "from comptages.section as sec "
            "inner join comptages.lane as lan on sec.id = lan.id_section "
            "where sec.id = '{}' ".format(self.section_id))

        query.exec_(query_str)

        while query.next():
            self.attributes['owner'] = query.value(0)
            self.attributes['road'] = query.value(1)
            self.attributes['start_pr'] = query.value(2)
            self.attributes['end_pr'] = query.value(3)
            self.attributes['start_dist'] = query.value(4)
            self.attributes['end_dist'] = query.value(5)
            self.attributes['place_name'] = query.value(6)
            if int(query.value(7)) == 1:
                self.attributes['dir1'] = query.value(8)
            elif int(query.value(7)) == 2:
                self.attributes['dir2'] = query.value(8)
