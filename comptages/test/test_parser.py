import unittest
from parser.data_parser import DataParserVdv1


# run from plugin directory `python -m unittest test/test_parser.py`
class TestDataParserVDV1(unittest.TestCase):
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

    def test_parse_data_line_with_not_allowed_missing_int_values(self):
        dp = DataParserVbv1(None)
        with self.assertRaisesRegex(ValueError, 'lane has an invalid value'):
            dp.parse_data_line(
                '043527 191216 1406 43 80 000000    2 33.8 33.4  27   594     5  M'
            )

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
