"""
Reimplementation of data_importer_vbv1.py as a Django management command
"""


import functools
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from ...models import Category, Count, CountDetail, Installation, Lane, Model, Brand, Section, SensorType

IMPORT_STATUS_QUARANTINE = 1


class Command(BaseCommand):
    help = 'Import comptages files'

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):
        with open(options['file']) as f:

            # Parse headers
            headers = {}
            for line in f:
                if not line.startswith('* '):
                    continue
                try:
                    key, val = line[2:].split('=', 1)
                    headers[key.strip()] = val.strip()
                except ValueError:
                    pass

            # Get the count instance
            installation_instance, _ = Installation.objects.get_or_create(
                name=headers["SITE"],
                defaults={
                    "permanent": True,
                    "active": True,
                },
            )

            start = datetime.strptime(headers['STARTREC'], "%H:%M %d/%m/%y")
            stop = datetime.strptime(headers['STOPREC'], "%H:%M %d/%m/%y")
            count_instance = Count.objects.create(
                id_installation=installation_instance,
                start_service_date=start,
                end_service_date=stop,
                start_process_date=start,
                end_process_date=start,
                id_model=Model.objects.create(name="Unknown", id_brand=Brand.objects.create(name="Unknown")),
                id_sensor_type=SensorType.objects.create(name="Unknown"),
            )

            if count_instance is None:
                site_instance, _ = Installation.objects.get_or_create(
                    name=headers["SITE"],
                    active=True,
                )
                count_instance = Count.objects.create(
                    id_installation=site_instance,
                    start_service_date=headers["STARTREC"],
                    end_service_date=headers["STOPREC"],
                )


            # Import lines
            f.seek(0)
            instances = []
            for line in f:
                if line.startswith('* '):
                    continue

                # Parse the line
                parsed_line = {}
                try:
                    parsed_line['numbering'] = line[0:6]
                    parsed_line['timestamp'] = datetime.strptime("{}0000".format(line[7:24]), "%d%m%y %H%M %S %f")
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
                        print("Could not parse line")
                        continue
                    if 'direction' not in parsed_line:
                        print("Could not parse line")
                        continue
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

                row = parsed_line

                instances.append(
                    CountDetail(
                        numbering=row['numbering'],
                        timestamp=row['timestamp'],
                        distance_front_front=row['distance_front_front'],
                        distance_front_back=row['distance_front_back'],
                        speed=row['speed'],
                        length=row['length'],
                        height=row['height'],
                        file_name=options['file'],
                        import_status=IMPORT_STATUS_QUARANTINE,
                        id_lane=_get_lane(count_instance, row['lane']),
                        id_count=count_instance,
                        id_category=Category(id=row['category']),
                    )
                )

            CountDetail.objects.bulk_create(instances)
            self.stdout.write(self.style.SUCCESS(f'Successfully created {len(instances)} comptages'))


@functools.lru_cache(maxsize=None)
def _get_lane(count_instance, lane_number):
    # TODO : replace this by actual lane creation/retrieval logic
    section = Section.objects.get_or_create(name="Unknown", defaults={
        "geometry": "LINESTRING(0 0, 10 10)"
    })[0]
    return Lane.objects.get_or_create(number=lane_number, direction=0, id_section=section)[0]
