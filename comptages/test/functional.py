"""Comptages functional tests"""

from qgis.PyQt.QtWidgets import QToolBar

import sys
import os
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery
from qgis.testing import unittest
from qgis.core import QgsProject
from qgis.utils import iface, active_plugins, plugins
from comptages.core.settings import Settings
from comptages.parser.data_parser import DataParserInt2


def run_all():
    """Default function that is called by the runner if nothing else is
    specified"""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestFunc, 'test'))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)


class TestFunc(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.settings = Settings()
        self.layers = plugins['comptages'].layers

        self.db = QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName(self.settings.value("db_host"))
        self.db.setPort(self.settings.value("db_port"))
        self.db.setDatabaseName(self.settings.value("db_name"))
        self.db.setUserName(self.settings.value("db_username"))
        self.db.setPassword(self.settings.value("db_password"))

        self.test_data_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'test_data/')

    def test_plugin_is_active(self):
        self.assertIn('comptages', active_plugins)

    def test_functional(self):

        # Julie sees the plugin toolbar with the "connect_db" and the
        # "settings" buttons enabled and the other disabled
        self.assertTrue(TestFunc.get_comptages_toolbar())
        self.assertTrue(TestFunc.is_action_enabled("Connection DB"))
        self.assertTrue(TestFunc.is_action_enabled("Réglages"))
        self.assertFalse(
            TestFunc.is_action_enabled("Créer un nouveau comptage"))
        self.assertFalse(TestFunc.is_action_enabled("Modifier comptage"))
        self.assertFalse(TestFunc.is_action_enabled("Importation"))
        self.assertFalse(TestFunc.is_action_enabled("Validation"))
        self.assertFalse(TestFunc.is_action_enabled("Filtrer"))

        # Julie presses on the start button of the plugin
        TestFunc.trigger_action("Connection DB")

        # She sees that the layers are loaded
        self.assertTrue(
            TestFunc.layer_is_loaded("installation"))
        self.assertTrue(
            TestFunc.layer_is_loaded("troncon"))

        # And all the buttons are enabled
        self.assertTrue(TestFunc.is_action_enabled("Connection DB"))
        self.assertTrue(TestFunc.is_action_enabled("Réglages"))
        self.assertTrue(
            TestFunc.is_action_enabled("Créer un nouveau comptage"))
        self.assertTrue(TestFunc.is_action_enabled("Modifier comptage"))
        self.assertTrue(TestFunc.is_action_enabled("Importation"))
        self.assertTrue(TestFunc.is_action_enabled("Validation"))
        self.assertTrue(TestFunc.is_action_enabled("Filtrer"))

        # The features of the section layer are around 8800
        self.assertGreater(TestFunc.get_layer("troncon").featureCount(), 8000)
        self.assertLess(TestFunc.get_layer("troncon").featureCount(), 9000)

    def test_simple_import_aggregate_data(self):
        TestFunc.trigger_action("Connection DB")

        self.db.open()
        query = QSqlQuery(self.db)
        query_str = (
            "INSERT INTO comptages.count(id, "
            "start_process_date, end_process_date, id_model, id_installation) "
            "VALUES (1, '2018-12-18', '2018-12-20', 1, 2468);")
        # 2468 -> 64080011

        query.exec_(query_str)

        data_parser = DataParserInt2(
            self.layers,
            os.path.join(
                self.test_data_path,
                'simple_aggregate.i00'))
        data_parser.parse_and_import_data(3)

        query.exec_(
            "SELECT * FROM comptages.count_aggregate WHERE file_name = \
            'simple_aggregate.i00'")

        self.assertEqual(1, query.size())

        query.next()

        self.assertEqual('CLS', query.value(1))
        self.assertEqual(self.layers.IMPORT_STATUS_QUARANTINE, query.value(5))

        # FIXME
        # self.assertEqual(4911, query.value(7))  # lane_id

        self.db.close()

    @staticmethod
    def trigger_action(text):
        if(not TestFunc.is_action_enabled(text)):
            return False

        toolbar = TestFunc.get_comptages_toolbar()
        for action in toolbar.actions():
            if action.text() == text:
                action.trigger()

    @staticmethod
    def is_action_enabled(text):
        toolbar = TestFunc.get_comptages_toolbar()
        for action in toolbar.actions():
            if action.text() == text:
                return action.isEnabled()

    @staticmethod
    def get_comptages_toolbar():
        for toolbar in iface.mainWindow().findChildren(QToolBar):
            if toolbar.objectName() == "Comptages":
                return toolbar

    @staticmethod
    def layer_is_loaded(name):
        for layer in QgsProject.instance().mapLayersByName(name):
            return True
        return False

    @staticmethod
    def get_layer(name):
        for layer in QgsProject.instance().mapLayersByName(name):
            return layer
        return None
