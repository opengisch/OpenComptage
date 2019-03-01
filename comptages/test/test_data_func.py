import os
import time
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
from qgis.testing import unittest
from qgis.utils import plugins
from comptages.core.settings import Settings
from comptages.data.data_loader import DataLoader


class TestData(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.settings = Settings()
        self.layers = plugins['comptages'].layers
        self.layers.load_layers()
        self.comptages = plugins['comptages']

        self.db = QSqlDatabase.addDatabase(
            "QPSQL", "test_data_connection")
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

    def test_data_detail(self):
        self.db.open()
        query = QSqlQuery(self.db)

        query.exec_("SELECT id FROM comptages.installation \
                    WHERE name = '64080011';")
        query.next()
        installation_id = query.value(0)

        query.exec_("SELECT id FROM comptages.model \
                    WHERE name = 'M660_LT';")
        query.next()
        model_id = query.value(0)

        query.exec_("select id from comptages.sensor_type \
                    where name = 'Tube'")
        query.next()
        sensor_type_id = query.value(0)

        query.exec_("select id from comptages.class \
                    where name = 'SWISS10'")
        query.next()
        class_id = query.value(0)

        query_str = (
            "INSERT INTO comptages.count(id, "
            "start_process_date, end_process_date, start_service_date, "
            "end_service_date, id_sensor_type, id_model, id_class, "
            "id_installation) "
            "VALUES (1, '2018-12-18', '2018-12-20', '2018-12-18', "
            "'2018-12-20', {}, {}, {}, {});".format(
                sensor_type_id, model_id, class_id, installation_id))
        query.exec_(query_str)

        task = self.comptages.import_file(
            os.path.join(
                self.test_data_path,
                'data_loader_simple_detail.V01'),
            1)

        task.waitForFinished()
        # Let the time to the db to finish the writing
        time.sleep(1)

        data_loader = DataLoader(
            1, '64080011', self.layers.IMPORT_STATUS_QUARANTINE)

        count_data = data_loader.load()
        self.assertEqual(
            [1, 0, 3, 0, 1, 3, 0, 1, 0, 0, 0, 0, 2],
            count_data.day_data[0].hour_data[15].direction_data[0].speed_data)

        self.assertEqual(
            [1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
            count_data.day_data[0].hour_data[15].direction_data[0].category_data)

        self.assertEqual(20, count_data.day_data[0].total())
        self.assertEqual(16, count_data.day_data[0].light_vehicles())
        self.assertEqual(4, count_data.day_data[0].heavy_vehicles())
        self.assertEqual(20.0, count_data.day_data[0].percent_heavy_vehicles())

    def test_data_aggregate(self):
        self.db.open()
        query = QSqlQuery(self.db)

        query.exec_("SELECT id FROM comptages.installation \
                    WHERE name = '64080011';")
        query.next()
        installation_id = query.value(0)

        query.exec_("SELECT id FROM comptages.model \
                    WHERE name = 'M660_LT';")
        query.next()
        model_id = query.value(0)

        query.exec_("select id from comptages.sensor_type \
                    where name = 'Tube'")
        query.next()
        sensor_type_id = query.value(0)

        query.exec_("select id from comptages.class \
                    where name = 'SWISS10'")
        query.next()
        class_id = query.value(0)

        query_str = (
            "INSERT INTO comptages.count(id, "
            "start_process_date, end_process_date, start_service_date, "
            "end_service_date, id_sensor_type, id_model, id_class, "
            "id_installation) "
            "VALUES (1, '2018-12-18', '2018-12-20', '2018-12-18', "
            "'2018-12-20', {}, {}, {}, {});".format(
                sensor_type_id, model_id, class_id, installation_id))
        query.exec_(query_str)

        task = self.comptages.import_file(
            os.path.join(
                self.test_data_path,
                'data_loader_simple_aggregate.i00'),
            1)

        task.waitForFinished()
        # Let the time to the db to finish the writing
        time.sleep(1)

        data_loader = DataLoader(
            1, '64080011', self.layers.IMPORT_STATUS_QUARANTINE)

        count_data = data_loader.load()

        self.assertEqual(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            count_data.day_data[1].hour_data[8].direction_data[0].speed_data)
        self.assertEqual(
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            count_data.day_data[1].hour_data[8].direction_data[0].category_data)
