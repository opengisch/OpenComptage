from datetime import datetime


class DataParserVdv1:

    LINE_TYPE_BEGIN = 0  # * BEGIN
    LINE_TYPE_END = 1  # * END
    LINE_TYPE_HEADER = 2  # * HEAD ...
    LINE_TYPE_SETTING = 3  # * FORMAT = ...
    LINE_TYPE_DATA = 4  # 000001 ...

    def parse_file(self, file):
        with open(file) as f:
            for line in f:
                self.parse_line(line)

    def parse_line(self, line):

        line_type = self._line_type(line)

        parsed_line = {}
        if not line_type == self.LINE_TYPE_DATA:
            line = line[2:]
            splitted = line.split('=', 1)
            if len(splitted) > 1:
                parsed_line[splitted[0].strip()] = splitted[1].strip()
        else:
            parsed_line['numbering'] = line[0:6]
            parsed_line['timestamp'] = datetime.strptime(
                f"{line[7:24]}0000", "%d%m%y %H%M %S %f")
            parsed_line['reserve_code'] = line[25:31]
            parsed_line['lane'] = self._cast_data_to_int(line[32:34], 'lane')
            parsed_line['direction'] = self._cast_data_to_int(
                line[35:36], 'direction')
            parsed_line['distance_front_front'] = float(line[37:41])
            parsed_line['distance_front_rear'] = float(line[42:46])
            parsed_line['speed'] = self._cast_data_to_int(line[47:50], 'speed')
            parsed_line['length'] = self._cast_data_to_int(
                line[52:56], 'length')
            parsed_line['category'] = line[60:62].strip()
            parsed_line['height'] = line[63:65].strip()

        return line_type, parsed_line

    def _line_type(self, line):
        if line.startswith('* BEGIN'):
            return self.LINE_TYPE_BEGIN
        elif line.startswith('* END'):
            return self.LINE_TYPE_END
        elif line.startswith('* HEAD'):
            return self.LINE_TYPE_HEADER
        elif line.startswith('*') and '=' in line:
            return self.LINE_TYPE_SETTING
        else:
            return self.LINE_TYPE_DATA

    def _cast_data_to_int(self, data, name):
        try:
            return int(data)
        except ValueError:
            if name == 'speed':
                return 0
            if name == 'length':
                return 0

            raise ValueError(f'{name} has an invalid value: {data}')


if __name__ == '__main__':
    dp = DataParserVdv1()
    dp.parse_file("/home/mario/workspace/tmp/comptages_20180816/Fichiers_Exemples/_Int_VbV/00056053.aV0")
