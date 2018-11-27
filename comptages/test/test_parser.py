import unittest
import os
from comptages.parser.data_parser import (
    DataParserVbv1, DataParserInt2, DataParser)
from comptages.core.layers import Layers


# run from main repo directory `python -m unittest test/test_parser.py`
class TestDataParser(unittest.TestCase):

    def setUp(self):
        self.layers = Layers()

    def test_parse_data_header(self):
        dp = DataParser(
            self.layers, 0, self.get_test_file_path('13208280.A00'))
        data_header = dp.parse_data_header()
        self.assertEqual(data_header[0], 2)
        self.assertEqual(data_header[1], 12)

    def get_test_file_path(self, file_name):
        return os.path.join(
            os.getcwd(), 'comptages', 'test', 'test_data', file_name)


class TestDataParserInt2(unittest.TestCase):

    def setUp(self):
        self.layers = Layers()

    def test_get_intspec(self):
        dp = DataParserInt2(
            self.layers, 0, self.get_test_file_path('13208280.A00'))
        intespec = dp.get_intspec()
        self.assertEqual(intespec[0], 'DRN')
        self.assertEqual(intespec[1], 'SPD')

    def test_get_bins(self):
        dp = DataParserInt2(
            self.layers, 0, self.get_test_file_path('00056053.A02'))
        self.assertEqual(
            dp.get_bins('LEN'), ['0', '270', '700', '1300', '9999'])
        self.assertEqual(
            dp.get_bins('SPD'),
            ['0', '15', '30', '40', '50', '60', '70', '80', '90', '100',
             '110', '120', '999'])
        self.assertEqual(dp.get_bins('CLS'), 10)

    def get_test_file_path(self, file_name):
        return os.path.join(
            os.getcwd(), 'comptages', 'test', 'test_data', file_name)

    # ***** VBV1 ******
    @unittest.skip('to be fixed')
    def test_parse_data_line(self):
        dp = DataParserVbv1(None)
        data = dp.parse_data_line(
            '024571 121216 1437 55 30 000000  1 1 99.9 27.7  38   594     5  H'
        )

        self.assertEqual(data['numbering'], '024571')
        self.assertEqual(data['timestamp'].day, 12)
        self.assertEqual(data['timestamp'].month, 12)
        self.assertEqual(data['timestamp'].year, 2016)
        self.assertEqual(data['timestamp'].hour, 14)
        self.assertEqual(data['timestamp'].minute, 37)
        self.assertEqual(data['timestamp'].second, 55)
        self.assertEqual(data['timestamp'].microsecond, 300000)
        self.assertEqual(data['reserve_code'], '000000')
        self.assertEqual(data['lane'], 1)
        self.assertEqual(data['direction'], 1)
        self.assertEqual(data['distance_front_front'], 99.9)
        self.assertEqual(data['distance_front_back'], 27.7)
        self.assertEqual(data['speed'], 38)
        self.assertEqual(data['length'], 594)
        self.assertEqual(data['category'], 5)
        self.assertEqual(data['height'], 'H')

    @unittest.skip('to be fixed')
    def test_parse_data_line_with_allowed_missing_int_values(self):
        dp = DataParserVbv1(None)
        data = dp.parse_data_line(
            '043527 191216 1406 43 80 000000  1 2 33.8 33.4       100        M'
        )

        self.assertEqual(data['numbering'], '043527')
        self.assertEqual(data['timestamp'].day, 19)
        self.assertEqual(data['timestamp'].month, 12)
        self.assertEqual(data['timestamp'].year, 2016)
        self.assertEqual(data['timestamp'].hour, 14)
        self.assertEqual(data['timestamp'].minute, 6)
        self.assertEqual(data['timestamp'].second, 43)
        self.assertEqual(data['timestamp'].microsecond, 800000)
        self.assertEqual(data['reserve_code'], '000000')
        self.assertEqual(data['lane'], 1)
        self.assertEqual(data['direction'], 2)
        self.assertEqual(data['distance_front_front'], 33.8)
        self.assertEqual(data['distance_front_back'], 33.4)
        self.assertEqual(data['speed'], 0)
        self.assertEqual(data['length'], 100)
        self.assertEqual(data['category'], 0)
        self.assertEqual(data['height'], 'M')

    @unittest.skip('to be fixed')
    def test_parse_data_line_with_not_allowed_missing_int_values(self):
        dp = DataParserVbv1(None)
        with self.assertRaisesRegex(ValueError, 'lane has an invalid value'):
            dp.parse_data_line(
                '043527 191216 1406 43 80 000000    2 33.8 33.4  27   594     5  M'
            )

    @unittest.skip('to be fixed')
    def test_parse_file_header_line_vith_value(self):
        dp = DataParserVbv1(None)
        data = dp.parse_line('* FORMATTER = GRFORMAT Release = 3.5.47')
        self.assertEqual(data['FORMATTER'], 'GRFORMAT Release = 3.5.47')

    @unittest.skip('to be fixed')
    def test_parse_setting_line_without_value(self):
        dp = DataParserVbv1()
        parsed_line = dp.parse_line('* GRIDREF =')
        line_type = parsed_line[0]
        data = parsed_line[1]
        self.assertEqual(line_type, dp.LINE_TYPE_SETTING)
        self.assertEqual(data['GRIDREF'], '')

    @unittest.skip('to be fixed')        
    def test_parse_begin_line(self):
        dp = DataParserVbv1()
        parsed_line = dp.parse_line('* BEGIN')
        line_type = parsed_line[0]
        data = parsed_line[1]
        self.assertEqual(line_type, dp.LINE_TYPE_BEGIN)
        self.assertDictEqual(data, {})

    @unittest.skip('to be fixed')        
    def test_parse_end_line(self):
        dp = DataParserVbv1()
        parsed_line = dp.parse_line('* END 57448 FFFF')
        line_type = parsed_line[0]
        data = parsed_line[1]
        self.assertEqual(line_type, dp.LINE_TYPE_END)
        self.assertDictEqual(data, {})

    @unittest.skip('to be fixed')        
    def test_parse_header_line(self):
        dp = DataParserVbv1()
        parsed_line = dp.parse_line('* HEAD DDMMYY HHMM SS HH RESCOD  L D HEAD'
                                    'GAP SPD LENTH    CS CH')
        line_type = parsed_line[0]
        data = parsed_line[1]
        self.assertEqual(line_type, dp.LINE_TYPE_HEADER)
        self.assertDictEqual(data, {})
