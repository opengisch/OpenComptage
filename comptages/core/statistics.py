import pandas as pd

from django.db.models import F, CharField, Value
from django.db.models import Count, Sum, Avg, Max
from django.db.models.functions import (
    ExtractIsoWeekDay, ExtractHour, ExtractMonth, ExtractDay, Trunc, Concat)

from comptages.core import definitions
from comptages.datamodel import models

def get_time_data(count, section, lane=None, direction=None):

    start = count.start_process_date
    end = count.end_process_date

    # By lane/direction grouped per hour

    qs = models.CountDetail.objects.filter(
        id_count=count,
        id_lane__id_section=section,
        timestamp__range=(start, end)
    )

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    # Vehicles by day and hour
    qs = qs.annotate(date=Trunc('timestamp', 'day'), hour=ExtractHour('timestamp')) \
           .order_by('hour') \
           .values('date', 'hour', 'times') \
           .order_by('date', 'hour') \
           .annotate(thm=Sum('times')) \
           .values('import_status', 'date', 'hour', 'thm')

    df = pd.DataFrame.from_records(qs)
    df['date'] = df['date'].dt.strftime('%a %d.%m.%Y')
    df['import_status'].replace({0: 'Existant', 1: 'Nouveau'}, inplace=True)
    return df


def get_day_data(count, section, lane=None, direction=None, status=None):

    start = count.start_process_date
    end = count.end_process_date

    qs = models.CountDetail.objects.filter(
        id_count=count,
        timestamp__range=(start, end)
    )

    # Can be None if we are calculating the total TJM of a special case's count
    if section is not None:
        qs = qs.filter(
            id_lane__id_section=section
        )

    if status is not None:
        qs = qs.filter(
            import_status=status
        )

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    qs = qs.annotate(date=Trunc('timestamp', 'day')) \
        .order_by('date') \
        .values('date', 'times', 'import_status') \
        .annotate(tj=Sum('times')) \
        .values('date', 'tj', 'import_status')

    df = pd.DataFrame.from_records(qs)
    mean = df["tj"].mean()
    df['import_status'].replace({0: 'Existant', 1: 'Nouveau'}, inplace=True)
    return df, mean


def get_category_data(count, section, status=definitions.IMPORT_STATUS_DEFINITIVE):

    start = count.start_process_date
    end = count.end_process_date

    qs = models.CountDetail.objects.filter(
        id_count=count,
        id_lane__id_section=section,
        import_status=status,
        timestamp__range=(start, end)
    )

    qs = qs.annotate(cat_name=F('id_category__name')) \
           .annotate(cat_code=F('id_category__code')) \
           .annotate(
               cat_name_code=Concat(
                   F('id_category__name'),
                   Value(' ('),
                   F('id_category__code'),
                   Value(')'),
                   output_field=CharField())) \
           .values('cat_name', 'cat_code', 'cat_name_code', 'times') \
           .annotate(value=Sum('times')) \
           .order_by('cat_code') \
           .values('cat_name', 'cat_code', 'cat_name_code', 'value')

    df = pd.DataFrame.from_records(qs)
    return df


def get_speed_data(count, section):

    start = count.start_process_date
    end = count.end_process_date

    qs = models.CountDetail.objects.filter(
        id_count=count,
        id_lane__id_section=section,
        timestamp__range=(start, end)
    )

    df = pd.DataFrame.from_records(qs.values('speed', 'times', 'import_status'))
    df = df.groupby(
        ['import_status',
         pd.cut(
             df['speed'],
             bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 999],
             labels=[
                 '0-10',
                 '10-20',
                 '20-30',
                 '30-40',
                 '40-50',
                 '50-60',
                 '60-70',
                 '70-80',
                 '80-90',
                 '90-100',
                 '100-110',
                 '110-120',
                 '120-999',
             ],
             right=False,  # Don't include rightmost edge (e.g. bin 10-20 is actually 10-19.9999999...)
         )
         ]).sum('times')

    df = df.rename(columns={'speed': 'speedNP'})

    df = df.reset_index(col_fill='NPLA_')
    df['import_status'].replace({0: 'Existant', 1: 'Nouveau'}, inplace=True)

    return df
