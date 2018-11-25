"""Comptages functional tests"""

from qgis.PyQt.QtWidgets import QToolBar

import unittest
import os
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
        #self.assertFalse(TestFunc.is_action_enabled("Create new measure"))
        #self.assertFalse(TestFunc.is_action_enabled("Edit measure"))
        #self.assertFalse(TestFunc.is_action_enabled("Filter"))

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
        self.assertTrue(TestFunc.is_action_enabled("Create new measure"))
        self.assertTrue(TestFunc.is_action_enabled("Edit measure"))
        self.assertTrue(TestFunc.is_action_enabled("Filter"))

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


if __name__ == "__main__" or __name__ == "__console__":
    print("--- Functional tests ---")
    iface.openMessageLog()
    result = unittest.result.TestResult()
    test_loader = unittest.TestLoader()
    test_loader.loadTestsFromTestCase(TestFunc).run(result)
    print(result)
    exit_code = 0
    for _ in result.failures:
        exit_code = 1
        print(_)

    for _ in result.errors:
        exit_code = 1
        print(_)

    os._exit(exit_code)
