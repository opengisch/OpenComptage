import psycopg2
from datetime import datetime



class DataParserVdv1:

    LINE_TYPE_BEGIN = 0  # * BEGIN
    LINE_TYPE_END = 1  # * END
    LINE_TYPE_HEADER = 2  # * HEAD ...
    LINE_TYPE_SETTING = 3  # * FORMAT = ...
    LINE_TYPE_DATA = 4  # 000001 ...

    def parse_file(self, file):

        conn = psycopg2.connect("dbname=comptages user=postgres password=postgres host=localhost port=5432")
        cur = conn.cursor()

        with open(file) as f:
            for line in f:
                line_type, parsed_line = self.parse_line(line)
                if line_type == self.LINE_TYPE_DATA:
                    cur.execute(f"insert into comptages.count_detail (numbering, timestamp, distance_front_front, distance_front_back, speed, length, height, file_name, id_lane, id_count, id_category)"
                                f" values ({parsed_line['numbering']}, '{parsed_line['timestamp']}', {parsed_line['distance_front_front']}, {parsed_line['distance_front_rear']}, {parsed_line['speed']},"
                                f" {parsed_line['length']}, 1, '00056053.aV0', 1, 2, {parsed_line['category']})"
                    )
        conn.commit()
        cur.close()
        conn.close()

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
            parsed_line['category'] = self._cast_data_to_int(line[60:62].strip(), 'category')
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
            #TODO 
            if name == 'category':
                return 1
            
            raise ValueError(f'{name} has an invalid value: {data}')


if __name__ == '__main__':
    dp = DataParserVdv1()
    dp.parse_file("/home/mario/workspace/tmp/comptages_20180816/Fichiers_Exemples/_Int_VbV/00056053.aV0")
