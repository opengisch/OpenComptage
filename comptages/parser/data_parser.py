import abc
import os

from datetime import datetime, timedelta

from comptages.core.utils import (
    create_progress_bar, clear_widgets, push_info)


class DataParser(metaclass=abc.ABCMeta):

    def __init__(self, layers, file):
        self.layers = layers
        self.file = file
        self.file_header = self.parse_file_header()
        self.data_header = []

    def parse_file_header(self):
        file_header = dict()
        with open(self.file) as f:
            for line in f:
                if line.startswith('* ') and not line.startswith('* HEAD '):
                    line = line[2:]
                    splitted = line.split('=', 1)
                    if len(splitted) > 1:
                        key = splitted[0].strip()
                        value = splitted[1].strip()
                        if key == 'CLASS' and value == 'SPECIAL10':
                            value = 'SWISS10'
                        file_header[key] = value
        return file_header

    def parse_data_header(self):
        with open(self.file) as f:
            for line in f:
                if line.startswith('* HEAD '):
                    start_char = 20
                    i = 0
                    while True:
                        if line[start_char:start_char+4] != '':
                            i += 1
                            start_char += 5
                        else:
                            self.data_header.append(i)
                            break
        return self.data_header

    def parse_and_import_data(self, count_id, message=''):
        pass

    def get_file_name(self):
        return os.path.basename(self.file)

    def get_number_of_lines(self):
        return sum(1 for line in open(self.file))

    def get_site(self):
        return self.file_header['SITE']

    def get_start_rec(self):
        return datetime.strptime(
            self.file_header['STARTREC'], "%H:%M %d/%m/%y")

    def get_stop_rec(self):
        return datetime.strptime(
            self.file_header['STOPREC'], "%H:%M %d/%m/%y")

    def get_format(self):
        return self.file_header['FORMAT']

    @staticmethod
    def get_file_format(file):
        data_parser = DataParser(None, file)
        return data_parser.get_format()


class DataParserVbv1(DataParser):

    def __init__(self, layers, file):
        DataParser.__init__(self, layers, file)
        self.catbins = self.layers.get_category_bins(self.file_header['CLASS'])

        self.number_of_lines = self.get_number_of_lines()

    def parse_and_import_data(self, count_id, message='Import file'):
        progress_bar = create_progress_bar(message)
        with open(self.file) as f:
            for i, line in enumerate(f):
                progress = int(100 / self.number_of_lines * i)
                progress_bar.setValue(progress)

                if not line.startswith('* '):
                    self.layers.insert_count_detail_row(
                        self.parse_data_line(line),
                        count_id,
                        self.get_file_name())
        clear_widgets()
        self.layers.invalidate_lanes_cache()
        push_info('Imported data from file {}'.format(self.file))

    def parse_data_line(self, line):
        parsed_line = dict()

        parsed_line['numbering'] = line[0:6]
        parsed_line['timestamp'] = datetime.strptime(
            "{}0000".format(line[7:24]), "%d%m%y %H%M %S %f")
        parsed_line['reserve_code'] = line[25:31]
        parsed_line['lane'] = self._cast_data_to_int(line[32:34], 'lane')
        parsed_line['direction'] = self._cast_data_to_int(
            line[35:36], 'direction')
        parsed_line['distance_front_front'] = float(line[37:41])
        parsed_line['distance_front_back'] = float(line[42:46])
        parsed_line['speed'] = self._cast_data_to_int(line[47:50], 'speed')
        parsed_line['length'] = self._cast_data_to_int(
            line[52:56], 'length')
        parsed_line['category'] = self._cast_data_to_int(
            line[60:62].strip(), 'category')
        parsed_line['category_id'] = self.catbins[parsed_line['category']-1]
        parsed_line['height'] = line[63:65].strip()

        return parsed_line

    def _cast_data_to_int(self, data, name):
        try:
            return int(data)
        except ValueError:
            if name == 'speed':
                return 0
            if name == 'length':
                return 0
            # TODO
            if name == 'category':
                return 0

            raise ValueError(
                '{} has an invalid value: {}'.format(name, data))


class DataParserInt2(DataParser):

    def __init__(self, layers, file):
        DataParser.__init__(self, layers, file)
        self.intspec = self.get_intspec()

        self.number_of_lines = self.get_number_of_lines()

    def get_intspec(self):
        self.file_header = self.parse_file_header()
        intspec = []
        for i, code in enumerate(self.file_header['INTSPEC'].split('+')):
            if code.strip() not in ['SPD', 'SDS', 'LEN', 'CLS', 'CNT', 'DRN']:
                raise NotImplementedError('{}'.format(code.strip()))
            # the key corrpespond to the value in the data row
            intspec.append(code.strip())
        return intspec

    def get_bins(self, code):
        """Returns an array with the bins if they exist, or the number of columns
        of this data type"""
        values = []
        if code == 'SPD' or code == 'SDS':
            values = self.file_header['SPDBINS'].split()
        elif code == 'LEN':
            values = self.file_header['LENBINS'].split()
        elif code == 'CLS':
            values = self.layers.get_category_bins(
                self.file_header['CLASS'])
        else:
            data_header = self.parse_data_header()
            values = data_header[self.intspec.index(code)]
        return values

    def parse_and_import_data(self, count_id, message='Import file'):
        progress_bar = create_progress_bar(message)
        with open(self.file) as f:
            for i, line in enumerate(f):
                progress = int(100 / self.number_of_lines * i)
                progress_bar.setValue(progress)

                if not line.startswith('* '):
                    parsed_line = self.parse_data_line(line)
                    row_type = self.intspec[int(parsed_line['info_code'])-1]
                    self.layers.insert_count_aggregate_row(
                        parsed_line,
                        row_type,
                        count_id,
                        self.get_file_name(),
                        self.get_bins(row_type))
        self.layers.invalidate_lanes_cache()
        clear_widgets()

    def parse_data_line(self, line):
        parsed_line = dict()

        # In the data files midnight is 2400 of the current day
        # instead of 0000 of the next day
        if line[7:9] == '24':
            line = line[:7] + '00' + line[9:]
            start = datetime.strptime(
                "{}".format(line[0:11]), "%d%m%y %H%M")
            start += timedelta(days=1)
        else:
            start = datetime.strptime(
                "{}".format(line[0:11]), "%d%m%y %H%M")

        parsed_line['start'] = start
        parsed_line['end'] = parsed_line['start'] + timedelta(
            minutes=int(self.file_header['INTERVAL']))
        parsed_line['channel'] = line[12:13]
        parsed_line['reserve_code'] = line[14:16]
        parsed_line['info_code'] = line[17:19]

        start_char = 20
        i = 1
        while True:
            if line[start_char:start_char+4] != '':
                parsed_line['data_{}'.format(i)] = \
                    line[start_char:start_char+4]
                i += 1
                start_char += 5
            else:
                break

        return parsed_line
