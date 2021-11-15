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
    workbook = load_workbook(filename=template_path)

    # We do by section and not by count because of special cases.
    sections = models.Section.objects.filter(lane__id_installation__count=count).distinct()

    for section in sections:
        for monday in _mondays_of_count(count):
            _data_count(count, section, monday, workbook)
            _data_day(count, section, monday, workbook)
            _data_speed(count, section, monday, workbook)

    output = os.path.join(
        file_path, '{}_{}_r.xlsx'.format(section.id, "NPLA"))

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


# TODO: Data_speed
# TODO: Data_category

def _data_count(count, section, monday, workbook):
    ws = workbook['Data_count']
    pass

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
            print(row)
            ws.cell(
                row=row_offset + row[0],
                column=col_offset + i,
                value=row[1]
            )

    # Direction 2
    row_offset = 33
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
            print(row)
            ws.cell(
                row=row_offset + row[0],
                column=col_offset + i,
                value=row[1]
            )
