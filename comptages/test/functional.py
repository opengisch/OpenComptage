"""Comptages functional tests"""

import unittest
from qgis.utils import (
    iface, active_plugins, plugins, available_plugins, startPlugin, loadPlugin)


class TestComptagesFunctionalities(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        loadPlugin('comptages')
        startPlugin('comptages')

    def test_plugin_is_active(self):
        self.assertIn('comptages', active_plugins)

    def test_true(self):
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main(exit=False)
