from datetime import datetime

from qgis.PyQt.QtSql import QSqlQuery
from qgis.core import QgsMessageLog, Qgis

from comptages.core.layers import Layers
from comptages.data.data_importer import DataImporter


class DataImporterVbv1(DataImporter):

    def __init__(self, file_path, count_id):
        super().__init__(file_path, count_id)
        self.exception = None

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

    def finished(self, result):
        if result:
            QgsMessageLog.logMessage(
                'Importation terminée {}'.format(self.basename),
                'Comptages', Qgis.Info)
        else:
            pass
        # TODO: Print errors to the QgsMessageLog

        self.db.close()
        del self.db

    def cancel(self):
        QgsMessageLog.logMessage(
            'Importation terminée', 'Comptages', Qgis.Info)

    def write_row_into_db(self, line):
        row = self.parse_data_line(line)

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
                         row['category_id']))

        query.exec_(query_str)

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
        parsed_line['category_id'] = int(
            self.categories[int(parsed_line['category'])])
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
            if name == 'category':
                return 0
