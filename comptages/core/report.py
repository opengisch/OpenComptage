import os
import pytz

from datetime import datetime, timedelta
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import load_workbook

from comptages.datamodel import models
from comptages.core import statistics, definitions


def prepare_reports(count, file_path, template='default'):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if template == 'default':
        template_name = 'template.xlsx'
    elif template == 'yearly':
        pass
    elif template == 'yearly_bike':
        pass

    template_path = os.path.join(
        current_dir,
        os.pardir,
        'report',
        template_name)

    # We do by section and not by count because of special cases.
    sections = models.Section.objects.filter(lane__id_installation__count=count).distinct()

    for section in sections:
        for monday in _mondays_of_count(count):
            workbook = load_workbook(filename=template_path)
            _data_count(count, section, monday, workbook)
            _data_day(count, section, monday, workbook)
            _data_speed(count, section, monday, workbook)
            _data_category(count, section, monday, workbook)

            output = os.path.join(
                file_path, '{}_{}_r.xlsx'.format(
                    section.id,
                    monday.strftime("%Y%m%d")))

            workbook.save(filename=output)


def _mondays_of_count(count):
    """Generator that return the Mondays of the count"""

    start = count.start_process_date
    end = count.end_process_date

    # Monday of first week
    monday = (start - timedelta(days=start.weekday()))
    yield monday

    while True:
        monday = monday + timedelta(days=7)
        if monday > end:
            return
        yield monday


def _data_count(count, section, monday, workbook):
    ws = workbook['Data_count']
    ws['B3'] = (
        'Poste de comptage : {}  Axe : {}:{}{}  '
        'PR {} + {} m à PR {} + {} m').format(
            section.id,
            section.owner,
            section.road,
            section.way,
            section.start_pr,
            int(section.start_dist),
            section.end_pr,
            int(section.end_dist)
    )

    ws['B4'] = 'Periode de comptage du {} au {}'.format(
        monday.strftime("%d/%m/%Y"),
        (monday + timedelta(days=7)).strftime("%d/%m/%Y"),
    )

    ws['B5'] = 'Comptage {}'.format(
        monday.strftime("%Y")
    )
    ws['B6'] = 'Type de capteur : {}'.format(
        count.id_sensor_type.name
    )
    ws['B7'] = 'Modèle : {}'.format(
        count.id_model.name)
    ws['B8'] = 'Classification : {}'.format(
        count.id_class.name)

    from_aggregate = models. \
        CountDetail.objects. \
        filter(id_count=count) \
        .distinct('from_aggregate') \
        .values('from_aggregate')[0]['from_aggregate']

    ws['B9'] = 'Comptage véhicule par véhicule'
    if from_aggregate:
        ws['B9'] = 'Comptage par interval'

    special_periods = statistics.get_special_periods(
        monday,
        monday + timedelta(days=6))
    texts = []
    for i in special_periods:
        texts.append(f"{i.start_date} - {i.end_date}: {i.description}")
    ws['B10'] = 'Periode speciales : {}'.format(
        ", ".join(texts)
    )

    ws['B11'] = section.place_name

    if count.remarks:
        ws['B12'] = 'Remarque : {}'.format(count.remarks)

    lanes = models.Lane.objects.filter(id_section=section).order_by('direction')
    if lanes:
        ws['B13'] = lanes[0].direction_desc
    if len(lanes) > 1:
        ws['B14'] = lanes[1].direction_desc


def _data_day(count, section, monday, workbook):
    ws = workbook['Data_day']

    # Total
    row_offset = 5
    col_offset = 2
    for i in range(7):
        df = statistics.get_time_data(
            count,
            section,
            start=monday + timedelta(days=i),
            end=monday + timedelta(days=i + 1)
        )

        for row in df.itertuples():
            ws.cell(
                row=row_offset + row.hour,
                column=col_offset + i,
                value=row.thm
            )

    # Monthly coefficients
    row_offset = 31
    col_offset = 2
    monthly_coefficients = [93, 96, 100, 102, 101, 104, 98, 98, 104, 103, 102, 98]

    for i in range(7):
        day = monday + timedelta(days=i)
        ws.cell(
            row=row_offset,
            column=col_offset + i,
            value=monthly_coefficients[day.month]
        )

    # Direction 1
    row_offset = 35
    col_offset = 2
    for i in range(7):
        df = statistics.get_time_data(
            count,
            section,
            start=monday + timedelta(days=i),
            end=monday + timedelta(days=i + 1),
            direction=1
        )

        for row in df.itertuples():
            ws.cell(
                row=row_offset + row.hour,
                column=col_offset + i,
                value=row.thm
            )

    # Light heavy direction 1
    row_offset = 61
    col_offset = 2
    for i in range(7):
        light = statistics.get_light_numbers(
            count,
            section,
            start=monday + timedelta(days=i),
            end=monday + timedelta(days=i + 1),
            direction=1
        )
        ws.cell(
            row=row_offset,
            column=col_offset + i,
            value=light.get(True, 0)
        )
        ws.cell(
            row=row_offset + 1,
            column=col_offset + i,
            value=light.get(False, 0)
        )

    # Direction 2
    row_offset = 66
    col_offset = 2
    for i in range(7):
        df = statistics.get_time_data(
            count,
            section,
            start=monday + timedelta(days=i),
            end=monday + timedelta(days=i + 1),
            direction=2
        )

        for row in df.itertuples():
            ws.cell(
                row=row_offset + row.hour,
                column=col_offset + i,
                value=row.thm
            )

    # Light heavy direction 2
    row_offset = 92
    col_offset = 2
    for i in range(7):
        light = statistics.get_light_numbers(
            count,
            section,
            start=monday + timedelta(days=i),
            end=monday + timedelta(days=i + 1),
            direction=2
        )
        ws.cell(
            row=row_offset,
            column=col_offset + i,
            value=light.get(True, 0)
        )
        ws.cell(
            row=row_offset + 1,
            column=col_offset + i,
            value=light.get(False, 0)
        )


def _data_speed(count, section, monday, workbook):
    ws = workbook['Data_speed']

    from_aggregate = models. \
        CountDetail.objects. \
        filter(id_count=count) \
        .distinct('from_aggregate') \
        .values('from_aggregate')[0]['from_aggregate']

    speed_ranges = [
        (0, 10),
        (10, 20),
        (20, 30),
        (30, 40),
        (40, 50),
        (50, 60),
        (60, 70),
        (70, 80),
        (80, 90),
        (90, 100),
        (100, 110),
        (110, 120),
        (120, 999),
    ]

    if from_aggregate:
        speed_ranges = [
            (0, 30),
            (30, 40),
            (40, 50),
            (50, 60),
            (60, 70),
            (70, 80),
            (80, 90),
            (90, 100),
            (100, 110),
            (110, 120),
            (120, 130),
            (130, 999),
        ]

    characteristic_speeds = [0.15, 0.5, 0.85]

    # Direction 1
    row_offset = 5
    col_offset = 2
    for i, range_ in enumerate(speed_ranges):
        res = statistics.get_speed_data_by_hour(
            count,
            section,
            direction=1,
            start=monday,
            end=monday + timedelta(days=7),
            speed_low=range_[0],
            speed_high=range_[1],
        )

        for row in res:
            ws.cell(
                row=row_offset + row[0],
                column=col_offset + i,
                value=row[1]
            )

    if not from_aggregate:
        # Characteristic speed direction 1
        row_offset = 5
        col_offset = 16
        for i, v in enumerate(characteristic_speeds):
            df = statistics.get_characteristic_speed_by_hour(
                count,
                section,
                direction=1,
                start=monday,
                end=monday + timedelta(days=7),
                v=v
            )
            for row in df.itertuples():
                ws.cell(
                    row=row_offset + row.Index,
                    column=col_offset + i,
                    value=row.speed
                )

        # Average speed direction 1
        row_offset = 5
        col_offset = 19

        df = statistics.get_average_speed_by_hour(
            count,
            section,
            direction=1,
            start=monday,
            end=monday + timedelta(days=7))
        for row in df.itertuples():
            ws.cell(
                row=row_offset + row.Index,
                column=col_offset,
                value=row.speed
            )

    # Direction 2
    row_offset = 33
    col_offset = 2
    for i, range_ in enumerate(speed_ranges):
        res = statistics.get_speed_data_by_hour(
            count,
            section,
            direction=2,
            start=monday,
            end=monday + timedelta(days=7),
            speed_low=range_[0],
            speed_high=range_[1],
        )

        for row in res:
            ws.cell(
                row=row_offset + row[0],
                column=col_offset + i,
                value=row[1]
            )

    if not from_aggregate:
        # Characteristic speed direction 2
        row_offset = 33
        col_offset = 16
        for i, v in enumerate(characteristic_speeds):
            df = statistics.get_characteristic_speed_by_hour(
                count,
                section,
                direction=2,
                start=monday,
                end=monday + timedelta(days=7),
                v=v
            )
            for row in df.itertuples():
                ws.cell(
                    row=row_offset + row.Index,
                    column=col_offset + i,
                    value=row.speed
                )

        # Average speed direction 1
        row_offset = 33
        col_offset = 19

        df = statistics.get_average_speed_by_hour(
            count,
            section,
            direction=2,
            start=monday,
            end=monday + timedelta(days=7))
        for row in df.itertuples():
            ws.cell(
                row=row_offset + row.Index,
                column=col_offset,
                value=row.speed
            )


def _data_category(count, section, monday, workbook):
    ws = workbook['Data_category']

    categories = models.Category.objects.filter(countdetail__id_count=count).distinct().order_by('code')

    # Direction 1
    row_offset = 5
    col_offset = 2
    for category in categories:
        if category.code == 0:
            continue  # We don't put TRASH category in report
        res = statistics.get_category_data_by_hour(
            count,
            section,
            category=category,
            direction=1,
            start=monday,
            end=monday + timedelta(days=7),
        )

        for row in res:
            ws.cell(
                row=row_offset + row[0],
                column=col_offset + category.code -1,
                value=row[1]
            )

    # Direction 2
    row_offset = 33
    col_offset = 2
    for category in categories:
        if category.code == 0:
            continue  # We don't put TRASH category in report
        res = statistics.get_category_data_by_hour(
            count,
            section,
            category=category,
            direction=2,
            start=monday,
            end=monday + timedelta(days=7),
        )

        for row in res:
            ws.cell(
                row=row_offset + row[0],
                column=col_offset + category.code -1,
                value=row[1]
            )
