from qgis.PyQt.QtWidgets import QToolBar

from qgis.testing import unittest
from qgis.core import QgsProject
from qgis.utils import iface, active_plugins


class TestInterface(unittest.TestCase):

    def test_plugin_is_active(self):
        self.assertIn('comptages', active_plugins)

    def test_menu(self):

        self.assertTrue(TestInterface.get_comptages_toolbar())
        self.assertTrue(TestInterface.is_action_enabled("Connection DB"))
        self.assertTrue(TestInterface.is_action_enabled("Réglages"))
        self.assertFalse(
            TestInterface.is_action_enabled("Créer un nouveau comptage"))
        self.assertFalse(TestInterface.is_action_enabled("Modifier comptage"))
        self.assertFalse(TestInterface.is_action_enabled("Importation"))
        self.assertFalse(TestInterface.is_action_enabled("Validation"))
        self.assertFalse(TestInterface.is_action_enabled("Filtrer"))

        TestInterface.trigger_action("Connection DB")

        self.assertTrue(
            TestInterface.layer_is_loaded("installation"))
        self.assertTrue(
            TestInterface.layer_is_loaded("troncon"))

        self.assertTrue(TestInterface.is_action_enabled("Connection DB"))
        self.assertTrue(TestInterface.is_action_enabled("Réglages"))
        self.assertTrue(
            TestInterface.is_action_enabled("Créer un nouveau comptage"))
        self.assertTrue(TestInterface.is_action_enabled("Modifier comptage"))
        self.assertTrue(TestInterface.is_action_enabled("Importation"))
        self.assertTrue(TestInterface.is_action_enabled("Validation"))
        self.assertTrue(TestInterface.is_action_enabled("Filtrer"))

        # The features of the section layer are around 8800
        self.assertGreater(
            TestInterface.get_layer("troncon").featureCount(), 8000)
        self.assertLess(
            TestInterface.get_layer("troncon").featureCount(), 9000)

    @staticmethod
    def trigger_action(text):
        if(not TestInterface.is_action_enabled(text)):
            return False

        toolbar = TestInterface.get_comptages_toolbar()
        for action in toolbar.actions():
            if action.text() == text:
                action.trigger()

    @staticmethod
    def is_action_enabled(text):
        toolbar = TestInterface.get_comptages_toolbar()
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
