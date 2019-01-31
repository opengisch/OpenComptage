import os
import time
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
from qgis.testing import unittest
from qgis.utils import plugins
from comptages.core.settings import Settings


class TestImportAggregate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.settings = Settings()
        self.layers = plugins['comptages'].layers
        self.layers.load_layers()
        self.comptages = plugins['comptages']

        self.db = QSqlDatabase.addDatabase(
            "QPSQL", "test_import_aggregate_connection")
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
        query.exec_("DELETE FROM comptages.count_aggregate;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_cls;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_cnt;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_drn;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_len;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_spd;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_sds;")
        self.db.close()

    def test_simple_import_aggregate_data_cls(self):
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
                    WHERE id_installation = {} AND number = 1;".format(
                        installation_id))
        query.next()
        lane_id = query.value(0)

        query.exec_("select cat.id from comptages.class as cls \
                     join comptages.class_category as cls_cat \
                     on cls_cat.id_class = cls.id \
                     join comptages.category as cat on \
                     cls_cat.id_category = cat.id \
                     where cls.name = 'SWISS10'")

        categories_id = []
        while query.next():
            categories_id.append(query.value(0))

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

        task = self.comptages.import_file(
            os.path.join(
                self.test_data_path,
                'simple_aggregate_cls.i00'),
            1)

        task.waitForFinished()
        time.sleep(2)

        query.exec_(
            "SELECT type, start, \"end\", file_name, import_status, id_count, \
            id_lane, id FROM comptages.count_aggregate WHERE file_name = \
            'simple_aggregate_cls.i00';")

        self.assertEqual(1, query.size())

        query.next()
        self.assertEqual('CLS', query.value(0))
        self.assertEqual(
            '240918 0800',
            query.value(1).toString('ddMMyy HHmm'))
        self.assertEqual(
            '240918 0900',
            query.value(2).toString('ddMMyy HHmm'))
        self.assertEqual('simple_aggregate_cls.i00', query.value(3))
        self.assertEqual(self.layers.IMPORT_STATUS_QUARANTINE, query.value(4))
        self.assertEqual(1, query.value(5))
        self.assertEqual(lane_id, query.value(6))
        id_count_aggregate = query.value(7)

        query.exec_(
            "SELECT value, id_count_aggregate, id_category \
            FROM comptages.count_aggregate_value_cls ORDER BY id;")

        self.assertEqual(10, query.size())

        query.next()
        self.assertEqual(1, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(categories_id[0], query.value(2))
        query.next()
        self.assertEqual(2, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(categories_id[1], query.value(2))
        query.next()
        self.assertEqual(3, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(categories_id[2], query.value(2))
        query.next()
        self.assertEqual(4, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(categories_id[3], query.value(2))
        query.next()
        self.assertEqual(5, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(categories_id[4], query.value(2))
        query.next()
        self.assertEqual(6, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(categories_id[5], query.value(2))
        query.next()
        self.assertEqual(7, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(categories_id[6], query.value(2))
        query.next()
        self.assertEqual(8, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(categories_id[7], query.value(2))
        query.next()
        self.assertEqual(9, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(categories_id[8], query.value(2))
        query.next()
        self.assertEqual(10, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(categories_id[9], query.value(2))

        self.db.close()

    def test_simple_import_aggregate_data_drn(self):
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
                    WHERE id_installation = {} AND number = 1;".format(
                        installation_id))
        query.next()
        lane_id = query.value(0)

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

        task = self.comptages.import_file(
            os.path.join(
                self.test_data_path,
                'simple_aggregate_drn.i00'),
            1)

        task.waitForFinished()
        # Let the time to the db to finish the writing
        time.sleep(1)

        query.exec_(
            "SELECT type, start, \"end\", file_name, import_status, id_count, \
            id_lane, id FROM comptages.count_aggregate WHERE file_name = \
            'simple_aggregate_drn.i00';")

        self.assertEqual(1, query.size())

        query.next()
        self.assertEqual('DRN', query.value(0))
        self.assertEqual(
            '240918 0800',
            query.value(1).toString('ddMMyy HHmm'))
        self.assertEqual(
            '240918 0900',
            query.value(2).toString('ddMMyy HHmm'))
        self.assertEqual('simple_aggregate_drn.i00', query.value(3))
        self.assertEqual(self.layers.IMPORT_STATUS_QUARANTINE, query.value(4))
        self.assertEqual(1, query.value(5))
        self.assertEqual(lane_id, query.value(6))
        id_count_aggregate = query.value(7)

        query.exec_(
            "SELECT value, id_count_aggregate, direction \
            FROM comptages.count_aggregate_value_drn ORDER BY id;")

        self.assertEqual(2, query.size())

        query.next()
        self.assertEqual(188, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(1, query.value(2))
        query.next()
        self.assertEqual(22, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(2, query.value(2))

        self.db.close()

    def test_simple_import_aggregate_data_len(self):
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
                    WHERE id_installation = {} AND number = 1;".format(
                        installation_id))
        query.next()
        lane_id = query.value(0)

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

        task = self.comptages.import_file(
            os.path.join(
                self.test_data_path,
                'simple_aggregate_len.i00'),
            1)

        task.waitForFinished()
        # Let the time to the db to finish the writing
        time.sleep(1)

        query.exec_(
            "SELECT type, start, \"end\", file_name, import_status, id_count, \
            id_lane, id FROM comptages.count_aggregate WHERE file_name = \
            'simple_aggregate_len.i00';")

        self.assertEqual(1, query.size())

        query.next()
        self.assertEqual('LEN', query.value(0))
        self.assertEqual(
            '240918 0800',
            query.value(1).toString('ddMMyy HHmm'))
        self.assertEqual(
            '240918 0900',
            query.value(2).toString('ddMMyy HHmm'))
        self.assertEqual('simple_aggregate_len.i00', query.value(3))
        self.assertEqual(self.layers.IMPORT_STATUS_QUARANTINE, query.value(4))
        self.assertEqual(1, query.value(5))
        self.assertEqual(lane_id, query.value(6))
        id_count_aggregate = query.value(7)

        query.exec_(
            "SELECT value, id_count_aggregate, low, high \
            FROM comptages.count_aggregate_value_len ORDER BY id;")

        self.assertEqual(4, query.size())

        query.next()
        self.assertEqual(113, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(0, query.value(2))
        self.assertEqual(270, query.value(3))
        query.next()
        self.assertEqual(33, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(270, query.value(2))
        self.assertEqual(700, query.value(3))
        query.next()
        self.assertEqual(6, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(700, query.value(2))
        self.assertEqual(1300, query.value(3))
        query.next()
        self.assertEqual(4, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(1300, query.value(2))
        self.assertEqual(2500, query.value(3))

        self.db.close()

    def test_simple_import_aggregate_data_spd(self):
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
                    WHERE id_installation = {} AND number = 1;".format(
                        installation_id))
        query.next()
        lane_id = query.value(0)

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

        task = self.comptages.import_file(
            os.path.join(
                self.test_data_path,
                'simple_aggregate_spd.i00'),
            1)

        task.waitForFinished()
        # Let the time to the db to finish the writing
        time.sleep(1)

        query.exec_(
            "SELECT type, start, \"end\", file_name, import_status, id_count, \
            id_lane, id FROM comptages.count_aggregate WHERE file_name = \
            'simple_aggregate_spd.i00';")

        self.assertEqual(1, query.size())

        query.next()
        self.assertEqual('SPD', query.value(0))
        self.assertEqual(
            '240918 0800',
            query.value(1).toString('ddMMyy HHmm'))
        self.assertEqual(
            '240918 0900',
            query.value(2).toString('ddMMyy HHmm'))
        self.assertEqual('simple_aggregate_spd.i00', query.value(3))
        self.assertEqual(self.layers.IMPORT_STATUS_QUARANTINE, query.value(4))
        self.assertEqual(1, query.value(5))
        self.assertEqual(lane_id, query.value(6))
        id_count_aggregate = query.value(7)

        query.exec_(
            "SELECT value, id_count_aggregate, low, high \
            FROM comptages.count_aggregate_value_spd ORDER BY id;")

        self.assertEqual(12, query.size())

        query.next()
        self.assertEqual(1, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(0, query.value(2))
        self.assertEqual(15, query.value(3))
        query.next()
        self.assertEqual(2, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(15, query.value(2))
        self.assertEqual(30, query.value(3))
        query.next()
        self.assertEqual(3, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(30, query.value(2))
        self.assertEqual(40, query.value(3))
        query.next()
        self.assertEqual(13, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(40, query.value(2))
        self.assertEqual(50, query.value(3))
        query.next()
        self.assertEqual(14, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(50, query.value(2))
        self.assertEqual(60, query.value(3))
        query.next()
        self.assertEqual(11, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(60, query.value(2))
        self.assertEqual(70, query.value(3))
        query.next()
        self.assertEqual(7, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(70, query.value(2))
        self.assertEqual(80, query.value(3))
        query.next()
        self.assertEqual(6, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(80, query.value(2))
        self.assertEqual(90, query.value(3))
        query.next()
        self.assertEqual(5, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(90, query.value(2))
        self.assertEqual(100, query.value(3))
        query.next()
        self.assertEqual(4, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(100, query.value(2))
        self.assertEqual(110, query.value(3))
        query.next()
        self.assertEqual(9, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(110, query.value(2))
        self.assertEqual(120, query.value(3))
        query.next()
        self.assertEqual(10, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(120, query.value(2))
        self.assertEqual(999, query.value(3))

        self.db.close()

    def test_simple_import_aggregate_data_sds(self):
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
                    WHERE id_installation = {} AND number = 1;".format(
                        installation_id))
        query.next()
        lane_id = query.value(0)

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

        task = self.comptages.import_file(
            os.path.join(
                self.test_data_path,
                'simple_aggregate_sds.i00'),
            1)

        task.waitForFinished()
        # Let the time to the db to finish the writing
        time.sleep(1)

        query.exec_(
            "SELECT type, start, \"end\", file_name, import_status, id_count, \
            id_lane, id FROM comptages.count_aggregate WHERE file_name = \
            'simple_aggregate_sds.i00';")

        self.assertEqual(1, query.size())

        query.next()
        self.assertEqual('SDS', query.value(0))
        self.assertEqual(
            '240918 0800',
            query.value(1).toString('ddMMyy HHmm'))
        self.assertEqual(
            '240918 0900',
            query.value(2).toString('ddMMyy HHmm'))
        self.assertEqual('simple_aggregate_sds.i00', query.value(3))
        self.assertEqual(self.layers.IMPORT_STATUS_QUARANTINE, query.value(4))
        self.assertEqual(1, query.value(5))
        self.assertEqual(lane_id, query.value(6))
        id_count_aggregate = query.value(7)

        query.exec_(
            "SELECT value, id_count_aggregate, low, high \
            FROM comptages.count_aggregate_value_spd ORDER BY id;")

        self.assertEqual(12, query.size())

        query.next()
        self.assertEqual(1, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(0, query.value(2))
        self.assertEqual(15, query.value(3))
        query.next()
        self.assertEqual(2, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(15, query.value(2))
        self.assertEqual(30, query.value(3))
        query.next()
        self.assertEqual(3, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(30, query.value(2))
        self.assertEqual(40, query.value(3))
        query.next()
        self.assertEqual(13, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(40, query.value(2))
        self.assertEqual(50, query.value(3))
        query.next()
        self.assertEqual(14, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(50, query.value(2))
        self.assertEqual(60, query.value(3))
        query.next()
        self.assertEqual(11, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(60, query.value(2))
        self.assertEqual(70, query.value(3))
        query.next()
        self.assertEqual(7, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(70, query.value(2))
        self.assertEqual(80, query.value(3))
        query.next()
        self.assertEqual(6, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(80, query.value(2))
        self.assertEqual(90, query.value(3))
        query.next()
        self.assertEqual(5, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(90, query.value(2))
        self.assertEqual(100, query.value(3))
        query.next()
        self.assertEqual(4, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(100, query.value(2))
        self.assertEqual(110, query.value(3))
        query.next()
        self.assertEqual(9, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(110, query.value(2))
        self.assertEqual(120, query.value(3))
        query.next()
        self.assertEqual(10, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(120, query.value(2))
        self.assertEqual(999, query.value(3))

        query.exec_(
            "SELECT id_count_aggregate, mean, deviation \
            FROM comptages.count_aggregate_value_sds ORDER BY id;")

        self.assertEqual(1, query.size())

        query.next()
        self.assertEqual(id_count_aggregate, query.value(0))
        self.assertEqual(45.0, query.value(1))
        self.assertEqual(2.8, query.value(2))

        self.db.close()

    def test_simple_import_aggregate_data_cnt(self):
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
                    WHERE id_installation = {} AND number = 1;".format(
                        installation_id))
        query.next()
        lane_id = query.value(0)

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

        task = self.comptages.import_file(
            os.path.join(
                self.test_data_path,
                'simple_aggregate_cnt.i00'),
            1)

        task.waitForFinished()
        # Let the time to the db to finish the writing
        time.sleep(1)

        query.exec_(
            "SELECT type, start, \"end\", file_name, import_status, id_count, \
            id_lane, id FROM comptages.count_aggregate WHERE file_name = \
            'simple_aggregate_cnt.i00';")

        self.assertEqual(1, query.size())

        query.next()
        self.assertEqual('CNT', query.value(0))
        self.assertEqual(
            '240918 0100',
            query.value(1).toString('ddMMyy HHmm'))
        self.assertEqual(
            '240918 0200',
            query.value(2).toString('ddMMyy HHmm'))
        self.assertEqual('simple_aggregate_cnt.i00', query.value(3))
        self.assertEqual(self.layers.IMPORT_STATUS_QUARANTINE, query.value(4))
        self.assertEqual(1, query.value(5))
        self.assertEqual(lane_id, query.value(6))
        id_count_aggregate = query.value(7)

        query.exec_(
            "SELECT value, id_count_aggregate, interval \
            FROM comptages.count_aggregate_value_cnt ORDER BY id;")

        self.assertEqual(12, query.size())

        query.next()
        self.assertEqual(13, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(1, query.value(2))
        query.next()
        self.assertEqual(8, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(2, query.value(2))
        query.next()
        self.assertEqual(5, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(3, query.value(2))
        query.next()
        self.assertEqual(3, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(4, query.value(2))
        query.next()
        self.assertEqual(3, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(5, query.value(2))
        query.next()
        self.assertEqual(4, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(6, query.value(2))
        query.next()
        self.assertEqual(6, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(7, query.value(2))
        query.next()
        self.assertEqual(24, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(8, query.value(2))
        query.next()
        self.assertEqual(45, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(9, query.value(2))
        query.next()
        self.assertEqual(78, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(10, query.value(2))
        query.next()
        self.assertEqual(99, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(11, query.value(2))
        query.next()
        self.assertEqual(115, query.value(0))
        self.assertEqual(id_count_aggregate, query.value(1))
        self.assertEqual(12, query.value(2))

        self.db.close()

    def test_simple_import_aggregate_data_multi_channel(self):
        self.db.open()
        query = QSqlQuery(self.db)

        query.exec_("SELECT id FROM comptages.installation \
                    WHERE name = '64080012';")
        query.next()
        installation_id = query.value(0)

        query.exec_("SELECT id FROM comptages.model \
                    WHERE name = 'M660';")
        query.next()
        model_id = query.value(0)

        query.exec_("SELECT id FROM comptages.lane \
                    WHERE id_installation = {} ORDER BY number;".format(
                        installation_id))
        query.next()
        lane_1_id = query.value(0)
        query.next()
        lane_2_id = query.value(0)

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

        task = self.comptages.import_file(
            os.path.join(
                self.test_data_path,
                'simple_aggregate_multi_channel.i00'),
            1)

        task.waitForFinished()
        # Let the time to the db to finish the writing
        time.sleep(1)

        query.exec_(
            "SELECT * FROM comptages.count_aggregate WHERE file_name = \
            'simple_aggregate_multi_channel.i00' ORDER BY id;")

        self.assertEqual(2, query.size())

        query.next()
        self.assertEqual('CLS', query.value(1))
        self.assertEqual(self.layers.IMPORT_STATUS_QUARANTINE, query.value(5))
        self.assertEqual(lane_1_id, query.value(7))

        query.next()
        self.assertEqual('CLS', query.value(1))
        self.assertEqual(self.layers.IMPORT_STATUS_QUARANTINE, query.value(5))
        self.assertEqual(lane_2_id, query.value(7))

        self.db.close()

    def test_simple_import_aggregate_multi_spec(self):
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
                    WHERE id_installation = {} AND number = 1;".format(
                        installation_id))
        query.next()
        lane_id = query.value(0)

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

        task = self.comptages.import_file(
            os.path.join(
                self.test_data_path,
                'simple_aggregate_multi_spec.i00'),
            1)

        task.waitForFinished()
        # Let the time to the db to finish the writing
        time.sleep(1)

        query.exec_(
            "SELECT type, start, \"end\", file_name, import_status, id_count, \
            id_lane, id FROM comptages.count_aggregate WHERE file_name = \
            'simple_aggregate_multi_spec.i00';")

        self.assertEqual(3, query.size())

        query.exec_(
            "SELECT * \
            FROM comptages.count_aggregate_value_len;")
        self.assertEqual(4, query.size())

        query.exec_(
            "SELECT * \
            FROM comptages.count_aggregate_value_cls;")
        self.assertEqual(10, query.size())

        query.exec_(
            "SELECT * \
            FROM comptages.count_aggregate_value_spd;")
        self.assertEqual(12, query.size())

        self.db.close()
