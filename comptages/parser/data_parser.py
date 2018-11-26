import abc
import os

from datetime import datetime, timedelta

from comptages.core.utils import (
    create_progress_bar, clear_widgets, push_info)


class DataParser(metaclass=abc.ABCMeta):

    def __init__(self, layers, count_id, file):
        self.layers = layers
        self.count_id = count_id
        self.file = file
        self.file_header = dict()
        self.data_header = []

    def parse_file_header(self):
        with open(self.file) as f:
            for line in f:
                if line.startswith('* ') and not line.startswith('* HEAD '):
                    line = line[2:]
                    splitted = line.split('=', 1)
                    if len(splitted) > 1:
                        self.file_header[
                            splitted[0].strip()] = splitted[1].strip()
        return self.file_header

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

    def parse_data(self):
        pass

    def get_file_name(self):
        return os.path.basename(self.file)

    def get_number_of_lines(self):
        return sum(1 for line in open(self.file))

    @staticmethod
    def get_format(file):
        data_parser = DataParser(None, None, file)
        return data_parser.parse_file_header()['FORMAT']


class DataParserVbv1(DataParser):

    def __init__(self, layers, count_id, file):
        DataParser.__init__(self, layers, count_id, file)
        file_header = self.parse_file_header()
        self.catbins = self.layers.get_category_bins(file_header['CLASS'])

        self.number_of_lines = self.get_number_of_lines()

    def parse_data(self):
        progress_bar = create_progress_bar("Import data")
        with open(self.file) as f:
            for i, line in enumerate(f):
                progress = int(100 / self.number_of_lines * i)
                progress_bar.setValue(progress)

                if not line.startswith('* '):
                    self.layers.insert_count_detail_row(
                        self.parse_data_line(line),
                        self.count_id,
                        self.get_file_name())
        clear_widgets()
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

    def __init__(self, layers, count_id, file):
        DataParser.__init__(self, layers, count_id, file)

        self.file_header = self.parse_file_header()
        self.intspec = self.get_intspec()

        self.number_of_lines = self.get_number_of_lines()

    def get_intspec(self):
        self.file_header = self.parse_file_header()
        intspec = []
        for i, code in enumerate(self.file_header['INTSPEC'].split('+')):
            # the key corrpespond to the value in the data row
            intspec.append(code.strip())
        return intspec

    def get_bins(self, code):
        """Returns an array with the bins if they exist, or the number of columns
        of this data type"""
        values = []
        if code == 'SPD':
            values = self.file_header['SPDBINS'].split()
        elif code == 'LEN':
            values = self.file_header['LENBINS'].split()
        else:
            data_header = self.parse_data_header()
            values = data_header[self.intspec.index(code)]
        return values

    def parse_data(self):
        progress_bar = create_progress_bar("Import data")
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
                        self.count_id,
                        self.get_file_name(),
                        self.get_bins(row_type))
        clear_widgets()
        push_info(
            'Imported data from file {}'.format(self.file))

    def parse_data_line(self, line):
        parsed_line = dict()

        # In the data files midnight is 2400 instead of 0000
        if line[7:9] == '24':
            line = line[:7] + '00' + line[9:]

        parsed_line['start'] = datetime.strptime(
            "{}".format(line[0:11]), "%d%m%y %H%M")
        parsed_line['end'] = parsed_line['start'] + timedelta(
            minutes=int(self.file_header['INTERVAL']))
        parsed_line['channel'] = line[12:13]
        parsed_line['reserve_code'] = line[14:16]
        parsed_line['info_code'] = line[17:19]

        start_char = 20
        i = 1
        while True:
            print(start_char)
            if line[start_char:start_char+4] != '':
                print(start_char)
                parsed_line['data_{}'.format(i)] = \
                    line[start_char:start_char+4]
                i += 1
                start_char += 5
            else:
                break

        return parsed_line
