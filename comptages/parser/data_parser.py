import abc
import os

from datetime import datetime


class DataParser(metaclass=abc.ABCMeta):

    def __init__(self, layers, count_id, file):
        self.layers = layers
        self.count_id = count_id
        self.file = file
        self.file_header = dict()

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
                    print(line)

    @abc.abstractmethod
    def parse_data(self):
        pass


class DataParserVbv1(DataParser):

    def parse_data(self):
        with open(self.file) as f:
            for line in f:
                if not line.startswith('* '):
                    #print(self.parse_data_line(line))
                    self.layers.insert_count_detail_row(self.parse_data_line(line),
                                                        self.count_id,
                                                        self.get_file_name())

    def parse_data_line(self, line):
        parsed_line = dict()

        parsed_line['numbering'] = line[0:6]
        parsed_line['timestamp'] = datetime.strptime(
            f"{line[7:24]}0000", "%d%m%y %H%M %S %f")
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

            raise ValueError(f'{name} has an invalid value: {data}')

    def get_file_name(self):
        return os.path.basename(self.file)
