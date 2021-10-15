from datetime import datetime

from qgis.core import QgsTask, Qgis, QgsMessageLog
from qgis.PyQt.QtSql import QSqlQuery

from comptages.core.layers import Layers
from comptages.importer.data_importer import DataImporter
from comptages.datamodel import models
from .bulk_create_manager import BulkCreateManager


class DataImporterMC(DataImporter):

    def __init__(self, file_path, count_id):
        super().__init__(file_path, count_id)
        self.numbering = 0
        self.bulk_mgr = BulkCreateManager(chunk_size=1000)

    def run(self):
        try:
            with open(self.file_path, encoding="ISO-8859-1") as f:
                number_of_lines = sum(1 for _ in f)
                with open(self.file_path, encoding="ISO-8859-1") as f:
                    for i, line in enumerate(f):
                        progress = int(100 / number_of_lines * i)
                        self.setProgress(progress)

                        if line.startswith('20'):
                            self.write_row_into_db(line)
        except Exception as e:
            self.exception = f"Error reading line {i+1} ({line}). Value {e}"
            return False

        self.bulk_mgr.done()
        return True

    def write_row_into_db(self, line):
        row = self.parse_data_line(line)
        if not row:
            return

        cat_bins = list(self.categories.values())

        self.bulk_mgr.add(
            models.CountDetail(
                numbering=row['numbering'],
                timestamp=row['timestamp'],
                distance_front_front=row['distance_front_front'],
                distance_front_back=row['distance_front_back'],
                speed=row['speed'],
                length=row['length'],
                height=row['height'],
                file_name=self.basename,
                import_status=Layers.IMPORT_STATUS_QUARANTINE,
                id_lane_id=self.lanes[int(row['lane'])],
                id_count_id=self.count_id,
                id_category_id=cat_bins[row['category']]
            )
        )

    def parse_data_line(self, line):
        parsed_line = None
        try:
            parsed_line = dict()

            self.numbering += 1
            parsed_line['numbering'] = self.numbering
            parsed_line['timestamp'] = datetime.strptime(
                line[0:19], "%Y-%m-%d %H:%M:%S")

            # On MetroCount files, the direction is 0-1 instead of 1-2
            parsed_line['lane'] = int(line[22:23]) + 1
            parsed_line['direction'] = int(line[22:23]) + 1
            parsed_line['distance_front_front'] = float(line[24:31])
            if parsed_line['distance_front_front'] > 99.9:
                parsed_line['distance_front_front'] = 99.9
            parsed_line['distance_front_back'] = float(line[31:38])
            if parsed_line['distance_front_back'] > 99.9:
                parsed_line['distance_front_back'] = 99.9
            parsed_line['speed'] = int(float(line[39:44]))
            parsed_line['length'] = int(float(line[44:50]))
            parsed_line['category'] = int(line[51:54].strip())
            parsed_line['height'] = ''
        except ValueError as e:
            QgsMessageLog.logMessage(
                'ValueError: {}'.format(e),  'Comptages', Qgis.Info)

            # This can happen when some values are missed from a line
            return None

        return parsed_line
