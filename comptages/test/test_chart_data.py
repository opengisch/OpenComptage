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

        self.db = QSqlDatabase.addDatabase("QPSQL")
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

        query_str = (
            "INSERT INTO comptages.count(id, "
            "start_process_date, end_process_date, id_model, id_installation) "
            "VALUES (1, '2018-12-18', '2018-12-20', {}, {});".format(
                model_id, installation_id))
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

        query_str = (
            "INSERT INTO comptages.count(id, "
            "start_process_date, end_process_date, id_model, id_installation) "
            "VALUES (1, '2018-12-18', '2018-12-20', {}, {});".format(
                model_id, installation_id))
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
