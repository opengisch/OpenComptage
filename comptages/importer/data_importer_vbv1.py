from datetime import datetime

from qgis.PyQt.QtSql import QSqlQuery

from comptages.core.layers import Layers
from comptages.importer.data_importer import DataImporter


class DataImporterVbv1(DataImporter):

    def __init__(self, file_path, count_id):
        super().__init__(file_path, count_id)

    def run(self):
        try:
            with open(self.file_path) as f:
                number_of_lines = sum(1 for _ in f)
                with open(self.file_path) as f:
                    for i, line in enumerate(f):
                        progress = int(100 / number_of_lines * i)
                        self.setProgress(progress)

                        if not line.startswith('* '):
                            self.write_row_into_db(line)
        except Exception as e:
            self.exception = e
            return False
        return True

    def write_row_into_db(self, line):
        row = self.parse_data_line(line)
        if not row:
            return

        cat_bins = list(self.categories.values())
        query = QSqlQuery(self.db)

        query_str = ("insert into comptages.count_detail ("
                     "numbering, timestamp, "
                     "distance_front_front, distance_front_back, "
                     "speed, length, height, "
                     "file_name, import_status, "
                     "id_lane, id_count, id_category) values ("
                     "{}, '{}', {}, {}, {}, {}, '{}', '{}', {}, {}, "
                     "{}, {})".format(
                         row['numbering'],
                         row['timestamp'],
                         row['distance_front_front'],
                         row['distance_front_back'],
                         row['speed'],
                         row['length'],
                         row['height'],
                         self.basename,
                         Layers.IMPORT_STATUS_QUARANTINE,
                         self.lanes[int(row['lane'])],
                         self.count_id,
                         cat_bins[row['category']-1]))
        query.exec_(query_str)

    def parse_data_line(self, line):
        parsed_line = None
        try:
            parsed_line = dict()

            parsed_line['numbering'] = line[0:6]
            parsed_line['timestamp'] = datetime.strptime(
                "{}0000".format(line[7:24]), "%d%m%y %H%M %S %f")
            parsed_line['reserve_code'] = line[25:31]
            parsed_line['lane'] = int(line[32:34])
            parsed_line['direction'] = int(line[35:36])
            parsed_line['distance_front_front'] = float(line[37:41])
            parsed_line['distance_front_back'] = float(line[42:46])
            parsed_line['speed'] = int(line[47:50])
            parsed_line['length'] = int(line[52:56])
            parsed_line['category'] = int(line[60:62].strip())
            parsed_line['height'] = line[63:65].strip()
        except ValueError:
            # This can happen when some values are missed from a line
            return None

        return parsed_line
