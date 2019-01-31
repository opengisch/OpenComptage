import os
import time
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
from qgis.testing import unittest
from qgis.utils import plugins
from comptages.core.settings import Settings
from comptages.data.data_importer_vbv1 import DataImporterVbv1


class TestImportDetail(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.settings = Settings()
        self.layers = plugins['comptages'].layers
        self.layers.load_layers()
        self.comptages = plugins['comptages']

        self.db = QSqlDatabase.addDatabase(
            "QPSQL", "test_import_detail_connection")
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
        self.db.close()

    def test_simple_import_detail_data_multi_lane(self):
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
                    WHERE id_installation = {} ORDER BY number;".format(
                        installation_id))
        query.next()
        lane_1_id = query.value(0)
        query.next()
        lane_2_id = query.value(0)

        query.exec_("SELECT id FROM comptages.category \
                    WHERE code = '3'")
        query.next()
        category_id_1 = query.value(0)

        query.exec_("SELECT id FROM comptages.category \
                    WHERE code = '4'")
        query.next()
        category_id_2 = query.value(0)

        query.exec_("select id from comptages.sensor_type \
                    where name = 'Tube'")
        query.next()
        sensor_type_id = query.value(0)

        query_str = (
            "INSERT INTO comptages.count(id, "
            "start_process_date, end_process_date, start_service_date, "
            "end_service_date, id_sensor_type, id_model, id_installation, "
            "id_class) "
            "VALUES (1, '2018-09-23', '2018-09-26', '2018-09-23', "
            "'2018-09-26', {}, {}, {}, 6);".format(  # FIXME: id_class
                sensor_type_id, model_id, installation_id))
        query.exec_(query_str)

        task = self.comptages.import_file(
            os.path.join(
                self.test_data_path,
                'simple_detail_multi_lane.V01'),
            1)

        task.waitForFinished()
        # Let the time to the db to finish the writing
        time.sleep(1)

        query.exec_(
            "SELECT numbering, timestamp, distance_front_front, \
            distance_front_back, speed, length, height, fixed, wrong_way, \
            file_name, import_status, id_lane, id_count, id_category \
            FROM comptages.count_detail \
            WHERE file_name = 'simple_detail_multi_lane.V01' ORDER BY id;")

        self.assertEqual(2, query.size())

        query.next()
        self.assertEqual(1, query.value(0))
        self.assertEqual(
            '240918 1545 49 800',
            query.value(1).toString('ddMMyy HHmm ss zzz'))
        self.assertEqual(12.3, query.value(2))
        self.assertEqual(99.9, query.value(3))
        self.assertEqual(50, query.value(4))
        self.assertEqual(428, query.value(5))
        self.assertEqual('L', query.value(6).strip())
        self.assertNotEqual(True, query.value(7))
        self.assertNotEqual(True, query.value(8))
        self.assertEqual('simple_detail_multi_lane.V01', query.value(9))
        self.assertEqual(self.layers.IMPORT_STATUS_QUARANTINE, query.value(10))
        self.assertEqual(lane_1_id, query.value(11))
        self.assertEqual(1, query.value(12))
        self.assertEqual(category_id_1, query.value(13))

        query.next()
        self.assertEqual(2, query.value(0))
        self.assertEqual(
            '240918 1545 50 900',
            query.value(1).toString('ddMMyy HHmm ss zzz'))
        self.assertEqual(3.8, query.value(2))
        self.assertEqual(1.4, query.value(3))
        self.assertEqual(51, query.value(4))
        self.assertEqual(416, query.value(5))
        self.assertEqual('VL', query.value(6).strip())
        self.assertNotEqual(True, query.value(7))
        self.assertNotEqual(True, query.value(8))
        self.assertEqual('simple_detail_multi_lane.V01', query.value(9))
        self.assertEqual(self.layers.IMPORT_STATUS_QUARANTINE, query.value(10))
        self.assertEqual(lane_2_id, query.value(11))
        self.assertEqual(1, query.value(12))
        self.assertEqual(category_id_2, query.value(13))

        self.db.close()
