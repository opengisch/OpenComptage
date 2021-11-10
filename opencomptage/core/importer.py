import pytz
import os
from datetime import datetime

from opencomptage.datamodel import models
from opencomptage.core.bulk_create_manager import BulkCreateManager

IMPORT_STATUS_QUARANTINE = 1
IMPORT_STATUS_DEFINITIVE = 0


def import_file(file_path, count):

    # TODO: check format
    # TODO: all formats

    _parse_and_write(file_path, count)


def simple_print_callback(progress):
    print(f"Importing... {progress}%")


def _parse_and_write(file_path, count, callback_progress=simple_print_callback):

    basename = os.path.basename(file_path)
    bulk_mgr = BulkCreateManager(chunk_size=1000)
    lanes = _populate_lane_dict(count)
    cat_bins = _populate_category_dict(count)
    previous_progress = 0
    try:
        with open(file_path) as f:
            number_of_lines = sum(1 for _ in f)
            with open(file_path) as f:
                for i, line in enumerate(f):
                    progress = int(100 / number_of_lines * i)

                    if not progress == previous_progress:
                        callback_progress(progress)
                        previous_progress = progress

                    if not line.startswith('* '):
                        row = _parse_line(line)
                        if not row:
                            return

                        bulk_mgr.add(
                            models.CountDetail(
                                numbering=row['numbering'],
                                timestamp=row['timestamp'],
                                distance_front_front=row['distance_front_front'],
                                distance_front_back=row['distance_front_back'],
                                speed=row['speed'],
                                length=row['length'],
                                height=row['height'],
                                file_name=basename,
                                import_status=IMPORT_STATUS_QUARANTINE,
                                id_lane_id=lanes[int(row['lane'])],
                                id_count_id=count.id,
                                id_category_id=cat_bins[row['category']]
                            )
                        )

    except Exception as e:
        raise e

    bulk_mgr.done()


def _parse_line(line):
    parsed_line = None
    try:
        tz = pytz.timezone('Europe/Zurich')
        parsed_line = dict()

        parsed_line['numbering'] = line[0:6]
        parsed_line['timestamp'] = tz.localize(datetime.strptime(
            "{}0000".format(line[7:24]), "%d%m%y %H%M %S %f"))
        parsed_line['reserve_code'] = line[25:31]
        parsed_line['lane'] = int(line[32:34])
        parsed_line['direction'] = int(line[35:36])
        parsed_line['distance_front_front'] = float(line[37:41])
        parsed_line['distance_front_back'] = float(line[42:46])
        parsed_line['speed'] = int(line[47:50])
        parsed_line['length'] = int(line[52:56])
        parsed_line['category'] = int(line[60:62].strip())
        parsed_line['height'] = line[63:65].strip()

        # If the speed of a vehicle is 0, we put it in the category 0
        if parsed_line['speed'] == 0:
            parsed_line['category'] = 0

        # If the speed of a vehicle is greater than 3*max_speed or 150km/h
        # TODO: get actual speed limit of the section
        if parsed_line['speed'] > 150:
            parsed_line['category'] = 0

    except ValueError:
        # This can happen when some values are missed from a line

        if 'lane' not in parsed_line:
            return None
        if 'direction' not in parsed_line:
            return None
        if 'distance_front_front' not in parsed_line:
            parsed_line['distance_front_front'] = 0
        if 'distance_front_back' not in parsed_line:
            parsed_line['distance_front_back'] = 0
        if 'speed' not in parsed_line:
            parsed_line['speed'] = -1
        if 'length' not in parsed_line:
            parsed_line['length'] = 0
        if 'category' not in parsed_line:
            parsed_line['category'] = 0
        if 'height ' not in parsed_line:
            parsed_line['height'] = 'NA'

    return parsed_line


def _populate_lane_dict(count):
    # e.g. lanes = {1: 435, 2: 436}

    count = models.Count.objects.get(id=count.id)
    lanes = models.Lane.objects.filter(
        id_installation__count=count,
    ).order_by("number")

    return {x.number: x.id for x in lanes}


def _populate_category_dict(count):
    # if 'CLASS' not in self.file_header:
    #     return
    # class_name = self.file_header['CLASS']

    class_name = count.id_class.name

    # Use customized SWISS7 class for Marksmann devices
    # because they manage this class in a wrong way
    # if self.file_header['FORMAT'] in ['INT-2', 'VBV-1'] and class_name == 'SWISS7':
    #     class_name = 'SWISS7-MM'

    # e.g. categories = {0: 922, 1: 22, 2: 23, 3: 24, 4: 25, 5: 26, 6: 27, 7: 28, 8: 29, 9: 30, 10: 31}
    categories = models.Category.objects.filter(
        classcategory__id_class__name=class_name
    ).order_by('code')

    return {x.code: x.id for x in categories}
