import os
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
from qgis.testing import unittest
from qgis.utils import plugins
from comptages.core.settings import Settings
from comptages.parser.data_parser import DataParserVbv1, DataParserInt2


class TestChartData(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.settings = Settings()
        self.layers = plugins['comptages'].layers
        self.layers.load_layers()

        self.db = QSqlDatabase.addDatabase(
            "QPSQL", "test_chart_data_connection")
        self.db.setHostName(self.settings.value("db_host"))
        self.db.setPort(self.settings.value("db_port"))
        self.db.setDatabaseName(self.settings.value("db_name"))
        self.db.setUserName(self.settings.value("db_username"))
        self.db.setPassword(self.settings.value("db_password"))

        self.test_data_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_data/')

    def setUp(self):
        self.db.open()
        query = QSqlQuery(self.db)

        query.exec_("DELETE FROM comptages.count;")
        query.exec_("DELETE FROM comptages.count_detail;")
        query.exec_("DELETE FROM comptages.count_aggregate;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_cls;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_cnt;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_drn;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_len;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_spd;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_sds;")
        self.db.close()

    def test_speed_chart_aggregate(self):
        self.db.open()
        query = QSqlQuery(self.db)

        query.exec_("SELECT id FROM comptages.installation \
                    WHERE name = '64080011';")
        query.next()
        installation_id = query.value(0)

        query.exec_("SELECT id FROM comptages.model \
                    WHERE name = 'M660';")
        query.next()
        model_id = query.value(0)

        query.exec_("select id from comptages.sensor_type \
                    where name = 'Tube'")
        query.next()
        sensor_type_id = query.value(0)

        query_str = (
            "INSERT INTO comptages.count(id, "
            "start_process_date, end_process_date, start_service_date, "
            "end_service_date, id_sensor_type, id_model, id_installation) "
            "VALUES (1, '2018-12-18', '2018-12-20', '2018-12-18', "
            "'2018-12-20', {}, {}, {});".format(
                sensor_type_id, model_id, installation_id))
        query.exec_(query_str)

        data_parser = DataParserInt2(
            self.layers,
            os.path.join(
                self.test_data_path,
                'speed_chart_aggregate.i00'))
        data_parser.parse_and_import_data(1)

        x, y = self.layers.get_aggregate_speed_chart_data(
            1, self.layers.IMPORT_STATUS_QUARANTINE)

        self.assertEqual(['0-15 km/h', '15-30 km/h', '30-40 km/h',
                          '40-50 km/h', '50-60 km/h', '60-70 km/h',
                          '70-80 km/h', '80-90 km/h', '90-100 km/h',
                          '100-110 km/h', '110-120 km/h', '120-999 km/h'], x)

        self.assertEqual([10, 55, 55, 130, 140, 110, 70, 60, 50, 40, 90, 100],
                         y)

    def test_speed_chart_detail(self):
        self.db.open()
        query = QSqlQuery(self.db)

        query.exec_("SELECT id FROM comptages.installation \
                    WHERE name = '64080011';")
        query.next()
        installation_id = query.value(0)

        query.exec_("SELECT id FROM comptages.model \
                    WHERE name = 'M660';")
        query.next()
        model_id = query.value(0)

        query.exec_("select id from comptages.sensor_type \
                    where name = 'Tube'")
        query.next()
        sensor_type_id = query.value(0)

        query_str = (
            "INSERT INTO comptages.count(id, "
            "start_process_date, end_process_date, start_service_date, "
            "end_service_date, id_sensor_type, id_model, id_installation) "
            "VALUES (1, '2018-12-18', '2018-12-20', '2018-12-18', "
            "'2018-12-20', {}, {}, {});".format(
                sensor_type_id, model_id, installation_id))
        query.exec_(query_str)

        data_parser = DataParserVbv1(
            self.layers,
            os.path.join(
                self.test_data_path,
                'speed_chart_detail.V01'))
        data_parser.parse_and_import_data(1)

        x, y = self.layers.get_detail_speed_chart_data(
            1, self.layers.IMPORT_STATUS_QUARANTINE)

        self.assertEqual(['0-10 km/h', '10-20 km/h', '20-30 km/h',
                          '30-40 km/h', '40-50 km/h', '50-60 km/h',
                          '60-70 km/h', '70-80 km/h', '80-90 km/h',
                          '90-100 km/h', '100-110 km/h', '110-120 km/h',
                          '120-999 km/h'], x)

        self.assertEqual([1, 0, 3, 0, 0, 4, 0, 0, 1, 0, 0, 0, 2], y)

    def test_category_chart_aggregate(self):
        self.db.open()
        query = QSqlQuery(self.db)

        query.exec_("SELECT id FROM comptages.installation \
                    WHERE name = '64080011';")
        query.next()
        installation_id = query.value(0)

        query.exec_("SELECT id FROM comptages.model \
                    WHERE name = 'M660';")
        query.next()
        model_id = query.value(0)

        query.exec_("select id from comptages.sensor_type \
                    where name = 'Tube'")
        query.next()
        sensor_type_id = query.value(0)

        query_str = (
            "INSERT INTO comptages.count(id, "
            "start_process_date, end_process_date, start_service_date, "
            "end_service_date, id_sensor_type, id_model, id_installation) "
            "VALUES (1, '2018-12-18', '2018-12-20', '2018-12-18', "
            "'2018-12-20', {}, {}, {});".format(
                sensor_type_id, model_id, installation_id))
        query.exec_(query_str)

        data_parser = DataParserInt2(
            self.layers,
            os.path.join(
                self.test_data_path,
                'category_chart_aggregate.i00'))
        data_parser.parse_and_import_data(1)

        label, values = self.layers.get_aggregate_category_chart_data(
            1, self.layers.IMPORT_STATUS_QUARANTINE)

        self.assertEqual(label.index('CAR (1)'), values.index(10))
        self.assertEqual(label.index('MR (2)'), values.index(20))
        self.assertEqual(label.index('PW (3)'), values.index(30))
        self.assertEqual(label.index('PW+ANH (4)'), values.index(40))
        self.assertEqual(label.index('LIE (5)'), values.index(50))
        self.assertEqual(label.index('LIE+ANH (6)'), values.index(60))
        self.assertEqual(label.index('LIE+AUFL (7)'), values.index(70))
        self.assertEqual(label.index('LW (8)'), values.index(80))
        self.assertEqual(label.index('LZ (9)'), values.index(90))
        self.assertEqual(label.index('SZ (10)'), values.index(100))

    def test_category_chart_detail(self):
        self.db.open()
        query = QSqlQuery(self.db)

        query.exec_("SELECT id FROM comptages.installation \
                    WHERE name = '64080011';")
        query.next()
        installation_id = query.value(0)

        query.exec_("SELECT id FROM comptages.model \
                    WHERE name = 'M660';")
        query.next()
        model_id = query.value(0)

        query.exec_("select id from comptages.sensor_type \
                    where name = 'Tube'")
        query.next()
        sensor_type_id = query.value(0)

        query_str = (
            "INSERT INTO comptages.count(id, "
            "start_process_date, end_process_date, start_service_date, "
            "end_service_date, id_sensor_type, id_model, id_installation) "
            "VALUES (1, '2018-12-18', '2018-12-20', '2018-12-18', "
            "'2018-12-20', {}, {}, {});".format(
                sensor_type_id, model_id, installation_id))
        query.exec_(query_str)

        data_parser = DataParserVbv1(
            self.layers,
            os.path.join(
                self.test_data_path,
                'category_chart_detail.V01'))
        data_parser.parse_and_import_data(1)

        label, values = self.layers.get_detail_category_chart_data(
            1, self.layers.IMPORT_STATUS_QUARANTINE)

        self.assertEqual(label.index('CAR (1)'), values.index(3))
        self.assertEqual(label.index('MR (2)'), values.index(2))
        self.assertEqual(label.index('PW (3)'), values.index(5))
        self.assertEqual(label.index('SZ (10)'), values.index(1))

    def test_time_chart_by_lane_aggregate(self):
        self.db.open()
        query = QSqlQuery(self.db)

        query.exec_("SELECT id FROM comptages.installation \
                    WHERE name = '64080011';")
        query.next()
        installation_id = query.value(0)

        query.exec_("SELECT id FROM comptages.model \
                    WHERE name = 'M660';")
        query.next()
        model_id = query.value(0)

        query.exec_("SELECT id FROM comptages.lane \
                    WHERE id_installation = {};".format(
                        installation_id))
        lanes_id = []

        while query.next():
            lanes_id.append(query.value(0))

        query.exec_("select id from comptages.sensor_type \
                    where name = 'Boucle'")
        query.next()
        sensor_type_id = query.value(0)

        query_str = (
            "INSERT INTO comptages.count(id, "
            "start_process_date, end_process_date, start_service_date, "
            "end_service_date, id_sensor_type, id_model, id_installation) "
            "VALUES (1, '2018-12-18', '2018-12-20', '2018-12-18', "
            "'2018-12-20', {}, {}, {});".format(
                sensor_type_id, model_id, installation_id))
        query.exec_(query_str)

        data_parser = DataParserInt2(
            self.layers,
            os.path.join(
                self.test_data_path,
                'time_chart_aggregate.i00'))
        data_parser.parse_and_import_data(1)

        xs, ys, days = self.layers.get_aggregate_time_chart_data_by_lane(
            1, self.layers.IMPORT_STATUS_QUARANTINE, lanes_id[0])

        self.assertTrue(2, len(days))
        self.assertEqual(
            ['00h-01h', '01h-02h', '02h-03h', '03h-04h', '04h-05h', '05h-06h',
             '06h-07h', '07h-08h', '08h-09h', '09h-10h', '10h-11h', '11h-12h',
             '12h-13h', '13h-14h', '14h-15h', '15h-16h', '16h-17h', '17h-18h',
             '18h-19h', '19h-20h', '20h-21h', '21h-22h', '22h-23h', '23h-00h'],
            xs[0])
        self.assertEqual(
            ['00h-01h', '01h-02h', '02h-03h', '03h-04h', '04h-05h', '05h-06h',
             '06h-07h', '07h-08h', '08h-09h', '09h-10h', '10h-11h', '11h-12h',
             '12h-13h', '13h-14h', '14h-15h', '15h-16h', '16h-17h', '17h-18h',
             '18h-19h', '19h-20h', '20h-21h', '21h-22h', '22h-23h', '23h-00h'],
            xs[1])
        self.assertEqual(
            [None, None, None, None, None, None, None, None,
             55, 55, 55, 55, 55, 55, 55, 55, 55, 55,
             None, None, None, None, None, None],
            ys[0])
        self.assertEqual(
            [None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None,
             None, 55, None, None, None, None, None, None],
            ys[1])

        xs, ys, days = self.layers.get_aggregate_time_chart_data_by_lane(
            1, self.layers.IMPORT_STATUS_QUARANTINE, lanes_id[1])

        self.assertTrue(2, len(days))
        self.assertEqual(
            ['00h-01h', '01h-02h', '02h-03h', '03h-04h', '04h-05h', '05h-06h',
             '06h-07h', '07h-08h', '08h-09h', '09h-10h', '10h-11h', '11h-12h',
             '12h-13h', '13h-14h', '14h-15h', '15h-16h', '16h-17h', '17h-18h',
             '18h-19h', '19h-20h', '20h-21h', '21h-22h', '22h-23h', '23h-00h'],
            xs[0])
        self.assertEqual(
            ['00h-01h', '01h-02h', '02h-03h', '03h-04h', '04h-05h', '05h-06h',
             '06h-07h', '07h-08h', '08h-09h', '09h-10h', '10h-11h', '11h-12h',
             '12h-13h', '13h-14h', '14h-15h', '15h-16h', '16h-17h', '17h-18h',
             '18h-19h', '19h-20h', '20h-21h', '21h-22h', '22h-23h', '23h-00h'],
            xs[1])
        self.assertEqual(
            [None, None, None, None, None, None, None, None,
             10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
             None, None, None, None, None, None],
            ys[0])
        self.assertEqual(
            [None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None,
             None, 10, None, None, None, None, None, None],
            ys[1])

    def test_time_chart_by_direction_aggregate(self):
        self.db.open()
        query = QSqlQuery(self.db)

        query.exec_("SELECT id FROM comptages.installation \
                    WHERE name = '00056520';")
        query.next()
        installation_id = query.value(0)

        query.exec_("SELECT id FROM comptages.model \
                    WHERE name = 'M660';")
        query.next()
        model_id = query.value(0)

        query.exec_("select id from comptages.sensor_type \
                    where name = 'Tube'")
        query.next()
        sensor_type_id = query.value(0)

        query_str = (
            "INSERT INTO comptages.count(id, "
            "start_process_date, end_process_date, start_service_date, "
            "end_service_date, id_sensor_type, id_model, id_installation) "
            "VALUES (1, '2018-12-18', '2018-12-20', '2018-12-18', "
            "'2018-12-20', {}, {}, {});".format(
                sensor_type_id, model_id, installation_id))
        query.exec_(query_str)

        data_parser = DataParserInt2(
            self.layers,
            os.path.join(
                self.test_data_path,
                'time_chart_aggregate_direction.i00'))
        data_parser.parse_and_import_data(1)

        xs, ys, days = self.layers.get_aggregate_time_chart_data_by_direction(
            1, self.layers.IMPORT_STATUS_QUARANTINE, 1)

        self.assertTrue(1, len(days))
        self.assertEqual(
            ['00h-01h', '01h-02h', '02h-03h', '03h-04h', '04h-05h', '05h-06h',
             '06h-07h', '07h-08h', '08h-09h', '09h-10h', '10h-11h', '11h-12h',
             '12h-13h', '13h-14h', '14h-15h', '15h-16h', '16h-17h', '17h-18h',
             '18h-19h', '19h-20h', '20h-21h', '21h-22h', '22h-23h', '23h-00h'],
            xs[0])
        self.assertEqual(
            [None, None, None, None, None, None,
             None, None, 66, 66, 66, 66,
             66, None, None, None, None, None,
             None, None, None, None, None, None],
            ys[0])

        xs, ys, days = self.layers.get_aggregate_time_chart_data_by_direction(
            1, self.layers.IMPORT_STATUS_QUARANTINE, 2)

        self.assertTrue(1, len(days))
        self.assertEqual(
            ['00h-01h', '01h-02h', '02h-03h', '03h-04h', '04h-05h', '05h-06h',
             '06h-07h', '07h-08h', '08h-09h', '09h-10h', '10h-11h', '11h-12h',
             '12h-13h', '13h-14h', '14h-15h', '15h-16h', '16h-17h', '17h-18h',
             '18h-19h', '19h-20h', '20h-21h', '21h-22h', '22h-23h', '23h-00h'],
            xs[0])
        self.assertEqual(
            [None, None, None, None, None, None,
             None, None, 70, 70, 70, 70,
             70, None, None, None, None, None,
             None, None, None, None, None, None],
            ys[0])

    def test_time_chart_by_lane_detail(self):
        self.db.open()
        query = QSqlQuery(self.db)

        query.exec_("SELECT id FROM comptages.installation \
                    WHERE name = '00056520';")
        query.next()
        installation_id = query.value(0)

        query.exec_("SELECT id FROM comptages.model \
                    WHERE name = 'M660';")
        query.next()
        model_id = query.value(0)

        query.exec_("SELECT id FROM comptages.lane \
                    WHERE id_installation = {};".format(
                        installation_id))
        lanes_id = []
        while query.next():
            lanes_id.append(query.value(0))

        query.exec_("select id from comptages.sensor_type \
                    where name = 'Boucle'")
        query.next()
        sensor_type_id = query.value(0)
        query_str = (
            "INSERT INTO comptages.count(id, "
            "start_process_date, end_process_date, start_service_date, "
            "end_service_date, id_sensor_type, id_model, id_installation) "
            "VALUES (1, '2018-09-23', '2018-09-29', '2018-09-23', "
            "'2018-09-29', {}, {}, {});".format(
                sensor_type_id, model_id, installation_id))
        query.exec_(query_str)

        data_parser = DataParserVbv1(
            self.layers,
            os.path.join(
                self.test_data_path,
                'time_chart_detail.V01'))
        data_parser.parse_and_import_data(1)

        xs, ys, days = self.layers.get_detail_time_chart_data_by_lane(
            1, self.layers.IMPORT_STATUS_QUARANTINE, lanes_id[0])

        self.assertTrue(1, len(days))
        self.assertEqual(
            ['00h-01h', '01h-02h', '02h-03h', '03h-04h', '04h-05h', '05h-06h',
             '06h-07h', '07h-08h', '08h-09h', '09h-10h', '10h-11h', '11h-12h',
             '12h-13h', '13h-14h', '14h-15h', '15h-16h', '16h-17h', '17h-18h',
             '18h-19h', '19h-20h', '20h-21h', '21h-22h', '22h-23h', '23h-00h'],
            xs[0])
        self.assertEqual(
            [None, None, None, None, None, None,
             None, None, None, None, None, 1,
             1, 1, None, None, 1, 1,
             1, None, None, 1, None, None],
            ys[0])

        xs, ys, days = self.layers.get_detail_time_chart_data_by_lane(
            1, self.layers.IMPORT_STATUS_QUARANTINE, lanes_id[1])

        self.assertTrue(1, len(days))
        self.assertEqual(
            ['00h-01h', '01h-02h', '02h-03h', '03h-04h', '04h-05h', '05h-06h',
             '06h-07h', '07h-08h', '08h-09h', '09h-10h', '10h-11h', '11h-12h',
             '12h-13h', '13h-14h', '14h-15h', '15h-16h', '16h-17h', '17h-18h',
             '18h-19h', '19h-20h', '20h-21h', '21h-22h', '22h-23h', '23h-00h'],
            xs[0])
        self.assertEqual(
            [None, None, None, None, None, None,
             None, None, None, None, None, None,
             None, None, 1, 1, None, None,
             None, 1, 1, None, None, None],
            ys[0])

    def test_time_chart_by_direction_detail(self):
        self.db.open()
        query = QSqlQuery(self.db)

        query.exec_("SELECT id FROM comptages.installation \
                    WHERE name = '00056520';")
        query.next()
        installation_id = query.value(0)

        query.exec_("SELECT id FROM comptages.model \
                    WHERE name = 'M660';")
        query.next()
        model_id = query.value(0)

        query.exec_("select id from comptages.sensor_type \
                    where name = 'Tube'")
        query.next()
        sensor_type_id = query.value(0)

        query_str = (
            "INSERT INTO comptages.count(id, "
            "start_process_date, end_process_date, start_service_date, "
            "end_service_date, id_sensor_type, id_model, id_installation) "
            "VALUES (1, '2018-12-18', '2018-12-20', '2018-12-18', "
            "'2018-12-20', {}, {}, {});".format(
                sensor_type_id, model_id, installation_id))
        query.exec_(query_str)

        data_parser = DataParserVbv1(
            self.layers,
            os.path.join(
                self.test_data_path,
                'time_chart_detail_direction.V01'))
        data_parser.parse_and_import_data(1)

        xs, ys, days = self.layers.get_detail_time_chart_data_by_direction(
            1, self.layers.IMPORT_STATUS_QUARANTINE, 1)

        self.assertTrue(1, len(days))
        self.assertEqual(
            ['00h-01h', '01h-02h', '02h-03h', '03h-04h', '04h-05h', '05h-06h',
             '06h-07h', '07h-08h', '08h-09h', '09h-10h', '10h-11h', '11h-12h',
             '12h-13h', '13h-14h', '14h-15h', '15h-16h', '16h-17h', '17h-18h',
             '18h-19h', '19h-20h', '20h-21h', '21h-22h', '22h-23h', '23h-00h'],
            xs[0])
        self.assertEqual(
            [None, None, None, None, None, None,
             None, None, None, None, None, 8,
             None, None, None, None, None, None,
             None, None, None, None, None, None],
            ys[0])

        xs, ys, days = self.layers.get_detail_time_chart_data_by_direction(
            1, self.layers.IMPORT_STATUS_QUARANTINE, 2)

        self.assertTrue(1, len(days))
        self.assertEqual(
            ['00h-01h', '01h-02h', '02h-03h', '03h-04h', '04h-05h', '05h-06h',
             '06h-07h', '07h-08h', '08h-09h', '09h-10h', '10h-11h', '11h-12h',
             '12h-13h', '13h-14h', '14h-15h', '15h-16h', '16h-17h', '17h-18h',
             '18h-19h', '19h-20h', '20h-21h', '21h-22h', '22h-23h', '23h-00h'],
            xs[0])
        self.assertEqual(
            [None, None, None, None, None, None,
             None, None, None, None, None, 3,
             None, None, None, None, None, None,
             None, None, None, None, None, None],
            ys[0])
