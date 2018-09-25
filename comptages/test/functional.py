"""Comptages functional tests"""

from qgis.PyQt.QtWidgets import QToolBar

import unittest
from qgis.utils import iface, active_plugins, startPlugin, loadPlugin


class TestFunc(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        loadPlugin('comptages')
        startPlugin('comptages')

    def test_plugin_is_active(self):
        self.assertIn('comptages', active_plugins)

    def test_functional(self):

        # Julie sees the plugin toolbar with the "connect_db" and the
        # "settings" buttons enabled and the other disabled
        self.assertTrue(TestFunc.get_comptages_toolbar())
        self.assertTrue(TestFunc.is_action_enabled("Connect DB"))
        self.assertTrue(TestFunc.is_action_enabled("Settings"))
        self.assertFalse(TestFunc.is_action_enabled("Create new campaign"))
        self.assertFalse(TestFunc.is_action_enabled("Select/edit campaign"))
        self.assertFalse(TestFunc.is_action_enabled("Import special periods"))

        # Julie presses on the start button of the plugin
        TestFunc.trigger_action("Connect DB")

        # She sees that the layers are loaded
        self.assertTrue(
            TestFunc.layer_is_loaded("installation"))
        self.assertTrue(
            TestFunc.layer_is_loaded("troncon"))

        # And all the buttons are enabled
        self.assertTrue(TestFunc.is_action_enabled("Connect DB"))
        self.assertTrue(TestFunc.is_action_enabled("Settings"))
        self.assertTrue(TestFunc.is_action_enabled("Create new campaign"))
        self.assertTrue(TestFunc.is_action_enabled("Select/edit campaign"))
        self.assertTrue(TestFunc.is_action_enabled("Import special periods"))

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


if __name__ == "__main__":
    unittest.main(exit=False)
