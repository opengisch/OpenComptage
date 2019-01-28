from qgis.PyQt.QtWidgets import QToolBar


import os
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
from qgis.testing import unittest
from qgis.utils import plugins
from comptages.core.settings import Settings
from comptages.parser.data_parser import DataParserInt2


class TestImportAggregate(unittest.TestCase):

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
        query.exec_("DELETE FROM comptages.count_aggregate;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_cls;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_cnt;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_drn;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_len;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_spd;")
        query.exec_("DELETE FROM comptages.count_aggregate_value_sds;")
        self.db.close()

    def test_simple_import_aggregate_data(self):
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
                'simple_aggregate.i00'))
        data_parser.parse_and_import_data(1)

        query.exec_(
            "SELECT * FROM comptages.count_aggregate WHERE file_name = \
            'simple_aggregate.i00';")

        self.assertEqual(1, query.size())

        query.next()

        self.assertEqual('CLS', query.value(1))
        self.assertEqual(self.layers.IMPORT_STATUS_QUARANTINE, query.value(5))
        self.assertEqual(lane_id, query.value(7))

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
                'simple_aggregate_multi_channel.i00'))
        data_parser.parse_and_import_data(1)

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
