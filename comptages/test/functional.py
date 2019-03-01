"""Comptages functional tests entry point"""

import sys
from qgis.testing import unittest
from comptages.test.test_interface import TestInterface
from comptages.test.test_import_aggregate import TestImportAggregate
from comptages.test.test_import_detail import TestImportDetail
from comptages.test.test_chart_data import TestChartData
from comptages.test.test_data_func import TestData


def run_all():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestInterface, 'test'))
    suite.addTests(unittest.makeSuite(TestImportAggregate, 'test'))
    suite.addTests(unittest.makeSuite(TestImportDetail, 'test'))
    suite.addTests(unittest.makeSuite(TestChartData, 'test'))
    suite.addTests(unittest.makeSuite(TestData, 'test'))
    unittest.TextTestRunner(verbosity=3, stream=sys.stdout).run(suite)
