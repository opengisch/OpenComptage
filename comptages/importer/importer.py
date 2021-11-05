import os
import pytz
from datetime import datetime, timezone

from qgis.core import QgsTask, Qgis, QgsMessageLog

from comptages.datamodel import models
from comptages.importer.bulk_create_manager import BulkCreateManager
from comptages.core.layers import Layers



def guess_count(site, class_, start, end):
    """Try to identify the count related to an imported file."""

    result = models.Count.objects.filter(
        id_installation__name=site,
        id_installation__active=True,
        id_class__name=class_,
        start_service_date__lte=start,
        end_service_date__gte=end,
        )

    return result


def get_lane_dict(count):
    """Return a dictionary with the id of the lanes of a count.

    e.g. {1: 435, 2: 436}"""

    lanes = models.Lane.objects.filter(
        id_installation__count=count,
    ).order_by("number")

    return {x.number: x.id for x in lanes}


def get_category_dict(count):
    """Return a dictionary with the id of the categories of a count.

    e.g. self.categories = {0: 922, 1: 22, 2: 23, 3: 24, 4: 25}"""

    categories = models.Category.objects.filter(
        id_class=count.id_class,
        ).order_by('code')

    return {x.code: x.id for x in categories}



class ImporterTask(QgsTask):

    def __init__(self, file_path):
        self.file_path = file_path
        self.format = get_file_format(self.file_path)
        file_basename = os.path.basename(self.file_path)
        super().__init__(f"Importation fichier {file_basename}")
        self.bulk_mgr = BulkCreateManager(chunk_size=1000)
        self.header = parse_file_header(get_file_header(file_path), self.format)
        self.count = guess_count(
            self.header['SITE'],
            self.header['CLASS'],
            self.header['STARTREC'],
            self.header['STOPREC'])
        self.lanes = get_lane_dict(self.count)

    def run(self):
        try:
            with open(self.file_path, encoding=get_file_encoding(self.file_path)) as f:
                total_lines = get_file_lines(self.file_path)
                for i, line in enumerate(f):
                    progress = int(100 / total_lines * i)
                    self.setProgress(progress)

                    self.parse_line(line)
        except Exception as e:
            print(e)
            return False

        self.bulk_mgr.done()
        return True

    def parse_line(self, line):

        # Different formats
        if self.format == "MC":
            if line.startswith("20"):
                row = self.parse_data_line_mc(line)
                self.bulk_mgr.add(
                    models.CountDetail(
                        numbering=row['numbering'],
                        timestamp=row['timestamp'],
                        distance_front_front=row['distance_front_front'],
                        distance_front_back=row['distance_front_back'],
                        speed=row['speed'],
                        length=row['length'],
                        height=row['height'],
                        file_name="NPLA",  # TODO: # self.basename,
                        import_status=Layers.IMPORT_STATUS_QUARANTINE,
                        id_lane_id=self.lanes[int(row['lane'])],
                        id_count_id=self.count_id,
                        id_category_id=cat_bins[row['category']]
                    ))

    def parse_data_line_mc(self, line):
        parsed_line = None
        try:
            parsed_line = dict()

            # self.numbering += 1
            parsed_line['numbering'] = 1 # TODO: numbering
            parsed_line['timestamp'] = datetime.strptime(
                line[0:19], "%Y-%m-%d %H:%M:%S").replace(
                    tzinfo=timezone.utc)

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


    def finished(self, result):
        print("finished")
        pass

    def cancel(self):
        pass

