import pytz

from django.test import TransactionTestCase, override_settings
from datetime import datetime
from comptages.test import utils
from comptages.importer import importer
from comptages.datamodel import models


# run from main repo directory `python -m unittest comptages/test/unit/test_importer.py`

@override_settings(MY_SETTING='NPIWTLYA')
class TestData(TransactionTestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_encoding(self):
        encoding = importer.get_file_encoding(
            utils.test_data_path("encoding_utf8.i00"))
        self.assertEqual(encoding, "utf-8")

        encoding = importer.get_file_encoding(
            utils.test_data_path("encoding_iso_8859_1.i00"))
        self.assertEqual(encoding, "ISO-8859-1")

    def test_format(self):
        format = importer.get_file_format(
            utils.test_data_path("format_int_2.txt"))
        self.assertEqual(format, "INT-2")

        format = importer.get_file_format(
            utils.test_data_path("format_vbv_1.txt"))
        self.assertEqual(format, "VBV-1")

        format = importer.get_file_format(
            utils.test_data_path("format_mc.txt"))
        self.assertEqual(format, "MC")

        with self.assertRaises(NotImplementedError):
            importer.get_file_format(
                utils.test_data_path("format_unknown.txt"))

    def test_get_header(self):
        header = importer.get_file_header(
            utils.test_data_path("format_int_2.txt"))

        self.assertEqual(len(header), 24)

        header = importer.get_file_header(
            utils.test_data_path("format_vbv_1.txt"))

        self.assertEqual(len(header), 18)

        header = importer.get_file_header(
            utils.test_data_path("format_mc.txt"))

        self.assertEqual(len(header), 32)

    def test_parse_header(self):
        header = importer.get_file_header(
            utils.test_data_path("format_int_2.txt"))

        parsed_header = importer.parse_file_header(
            header, "INT-2")

        self.assertEqual(parsed_header['SITE'], '64080011')
        self.assertEqual(parsed_header['STARTREC'], '07:00 19/12/18')
        self.assertEqual(parsed_header['STOPREC'], '08:00 19/12/18')
        self.assertEqual(parsed_header['SPDBINS'], '0 15 30 40 50 60 70 80 90 100 110 120 999')
        self.assertEqual(parsed_header['CLASS'], 'SWISS10')
        self.assertEqual(parsed_header['INTSPEC'], 'CLS')

        header = importer.get_file_header(
            utils.test_data_path("format_mc.txt"))

        parsed_header = importer.parse_file_header(
            header, "MC")

        self.assertEqual(parsed_header['SITE'], '00056270')
        self.assertEqual(parsed_header['CLASS'], 'FHWA13')

    def test_first_record_date(self):
        tz = pytz.timezone('Europe/Zurich')

        date = importer.get_first_record_date(
            utils.test_data_path("format_int_2.txt"))

        self.assertEqual(
            date,
            datetime(2018, 9, 24, 8, 0, tzinfo=tz)
        )

        date = importer.get_first_record_date(
            utils.test_data_path("format_mc.txt"))

        self.assertEqual(
            date,
            datetime(2018, 11, 13, 14, 8, 11, tzinfo=tz)
        )

    def test_last_record_date(self):
        tz = pytz.timezone('Europe/Zurich')

        date = importer.get_last_record_date(
            utils.test_data_path("format_int_2.txt"))

        self.assertEqual(
            date,
            datetime(2018, 9, 24, 9, 2, tzinfo=tz)
        )

        date = importer.get_last_record_date(
            utils.test_data_path("format_mc.txt"))

        self.assertEqual(
            date,
            datetime(2018, 12, 11, 14, 7, 39, tzinfo=tz)
        )

    def test_guess_count(self):

        count = utils.create_test_count(
            '00208495',
            'SWISS7',
            datetime(2020, 1, 1),
            datetime(2020, 1, 14),
        )

        self.assertEqual(
            importer.guess_count(
                '00208495',
                'SWISS7',
                datetime(2020, 1, 1),
                datetime(2020, 1, 14),
            )[0],
            count
        )

    def test_lane_dict(self):

        count = utils.create_test_count(
            '00056130',
            'SWISS7',
            datetime(2020, 1, 1),
            datetime(2020, 1, 14),
            lanes=2,
        )

        lane_dict = importer.get_lane_dict(count)

        self.assertEqual(len(lane_dict), 2)
        # TODO: implement better test

    def test_category_dict(self):
        count = utils.create_test_count(
            '00056132',
            'MB1',
            datetime(2020, 1, 1),
            datetime(2020, 1, 14),
            lanes=2,
        )

        cat_dict = importer.get_category_dict(count)
        self.assertEqual(len(cat_dict), 3)
        # TODO: implement better test

    def test_file_lines(self):
        self.assertEqual(
            importer.get_file_lines(utils.test_data_path("format_int_2.txt")),
            28
        )
