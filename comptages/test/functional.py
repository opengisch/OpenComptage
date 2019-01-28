"""Comptages functional tests entry point"""

import sys
from qgis.testing import unittest
from comptages.test.test_interface import TestInterface
from comptages.test.test_import_aggregate import TestImportAggregate
from comptages.test.test_import_detail import TestImportDetail


def run_all():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestInterface, 'test'))
    suite.addTests(unittest.makeSuite(TestImportAggregate, 'test'))
    suite.addTests(unittest.makeSuite(TestImportDetail, 'test'))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
