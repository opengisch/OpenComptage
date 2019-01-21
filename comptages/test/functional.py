"""Comptages functional tests"""

from qgis.PyQt.QtWidgets import QToolBar

import os
import sys
from qgis.testing import unittest
from qgis.core import QgsProject
from qgis.utils import iface, active_plugins, startPlugin, loadPlugin


def run_all():
    """Default function that is called by the runner if nothing else is
    specified"""
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestFunc, 'test'))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)


class TestFunc(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     loadPlugin('comptages')
    #     startPlugin('comptages')

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
        TestFunc.trigger_action("Connect DB")

        # She sees that the layers are loaded
        self.assertTrue(
            TestFunc.layer_is_loaded("installation"))
    #     self.assertTrue(
    #         TestFunc.layer_is_loaded("troncon"))

    #     # And all the buttons are enabled
    #     self.assertTrue(TestFunc.is_action_enabled("Connect DB"))
    #     self.assertTrue(TestFunc.is_action_enabled("Settings"))
    #     self.assertTrue(TestFunc.is_action_enabled("Create new measure"))
    #     self.assertTrue(TestFunc.is_action_enabled("Edit measure"))
    #     self.assertTrue(TestFunc.is_action_enabled("Filter"))

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
