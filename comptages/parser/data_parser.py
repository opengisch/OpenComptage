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

    def parse_data(self):
        pass

    def get_file_name(self):
        return os.path.basename(self.file)

    @staticmethod
    def get_format(file):
        data_parser = DataParser(None, None, file)
        return data_parser.parse_file_header()['FORMAT']


class DataParserVbv1(DataParser):

    def __init__(self, layers, count_id, file):
        DataParser.__init__(self, layers, count_id, file)
        file_header = self.parse_file_header()
        self.catbins = self.layers.get_category_bins(file_header['CLASS'])

    def parse_data(self):
        with open(self.file) as f:
            for line in f:
                if not line.startswith('* '):
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

            raise ValueError(f'{name} has an invalid value: {data}')


class DataParserInt2(DataParser):


    def __init__(self, layers, count_id, file):
        DataParser.__init__(self, layers, count_id, file)
        
        file_header = self.parse_file_header()
        self.intspec = dict()
        for i, code in enumerate(file_header['INTSPEC'].split('+')):
            self.intspec['0'+str(i+1)] = code.strip()

        # Speed and length bins. min-max n goes from spdbins[n-1] to spdbins[n]
        self.spdbins = file_header['SPDBINS'].split()
        self.lenbins = file_header['LENBINS'].split()

        # Category bins. CS n is catbins[n-1]
        self.catbins = self.layers.get_category_bins(file_header['CLASS'])

    def parse_data(self):
        with open(self.file) as f:
            for line in f:
                if not line.startswith('* '):

                    parsed_line = self.parse_data_line(line)
                    
                    self.layers.insert_count_aggregate_row(parsed_line,
                                                           self.intspec[parsed_line['info_code']],
                                                           self.count_id,
                                                           self.get_file_name(),
                                                           self.spdbins,
                                                           self.lenbins,
                                                           self.catbins)

    def parse_data_line(self, line):
        parsed_line = dict()

        # In the data files midnight is 2400 instead of 0000
        if line[7:9] == '24':
            line = line[:7] + '00' + line[9:] 

        parsed_line['start'] = datetime.strptime(
            f"{line[0:11]}", "%d%m%y %H%M")
        parsed_line['channel'] = line[12:13]
        parsed_line['reserve_code'] = line[14:16]
        parsed_line['info_code'] = line[17:19]
        parsed_line['data_1'] = line[20:24]
        parsed_line['data_2'] = line[25:29]
        parsed_line['data_3'] = line[30:34]
        parsed_line['data_4'] = line[35:39]
        parsed_line['data_5'] = line[40:44]
        parsed_line['data_6'] = line[45:49]
        parsed_line['data_7'] = line[50:54]
        parsed_line['data_8'] = line[55:59]
        parsed_line['data_9'] = line[60:64]
        parsed_line['data_10'] = line[65:69]
        parsed_line['data_11'] = line[70:74]
        parsed_line['data_12'] = line[75:79]                                                                                       
        return parsed_line

if __name__ == '__main__':
    # data_parser = DataParserInt2(
    #     None, 1, '/home/mario/workspace/repos/OpenComptage/comptages/test/test_data/_Int_VbV/00056214.A02')

    # data_parser.parse_data()

    # file_header = data_parser.parse_file_header()
    # intspec = dict()
    # for i, code in enumerate(file_header['INTSPEC'].split('+')):
    #     intspec['0'+str(i+1)] = code.strip()

    
    
    # print(intspec)

    print(DataParser.get_format('/home/mario/workspace/repos/OpenComptage/comptages/test/test_data/_Int_VbV/00056214.A02'))
    
