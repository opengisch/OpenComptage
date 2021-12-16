import pandas as pd

from datetime import timedelta, datetime

from django.db.models import F, CharField, Value, Q
from django.db.models import Sum
from django.db.models.functions import (
    ExtractHour, Trunc, Concat)

from comptages.core import definitions
from comptages.datamodel import models


def get_time_data(count, section, lane=None, direction=None, start=None, end=None):

    if not start:
        start = count.start_process_date
    if not end:
        end = count.end_process_date + timedelta(days=1)

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
    if not df.empty:
        df['date'] = df['date'].dt.strftime('%a %d.%m.%Y')
        df['import_status'].replace({0: 'Existant', 1: 'Nouveau'}, inplace=True)
    return df


def get_time_data_yearly(year, section, lane=None, direction=None):
    """Vehicles by hour and day of the week"""
    start = datetime(year, 1, 1)
    end = datetime(year + 1, 1, 1)

    # By lane/direction grouped per hour

    qs = models.CountDetail.objects.filter(
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
    df = df.groupby([df['date'].dt.dayofweek, 'hour']).thm.sum()
    df = df.reset_index()

    return df


def get_day_data(count, section=None, lane=None, direction=None, status=None):

    start = count.start_process_date
    end = count.end_process_date + timedelta(days=1)

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

    mean = 0
    if not df.empty:
        mean = df["tj"].mean()
        df['import_status'].replace({0: 'Existant', 1: 'Nouveau'}, inplace=True)

    return df, int(mean)


def get_category_data(count, section, status=definitions.IMPORT_STATUS_DEFINITIVE):

    start = count.start_process_date
    end = count.end_process_date + timedelta(days=1)

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
    end = count.end_process_date + timedelta(days=1)

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


def get_light_numbers(count, section, lane=None, direction=None, start=None, end=None):

    if not start:
        start = count.start_process_date
    if not end:
        end = count.end_process_date + timedelta(days=1)

    qs = models.CountDetail.objects.filter(
        id_count=count,
        id_lane__id_section=section,
        timestamp__range=(start, end)
    )

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    qs = qs.values('id_category__light') \
           .annotate(value=Sum('times')) \
           .values_list('id_category__light', 'value')

    res = {}
    for r in qs:
        res[r[0]] = r[1]
    return res


def get_light_numbers_yearly(section, lane=None, direction=None, start=None, end=None):

    qs = models.CountDetail.objects.filter(
        id_lane__id_section=section,
        timestamp__range=(start, end)
    )

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    qs = qs.annotate(date=Trunc('timestamp', 'day'))
    qs = qs.values('date', 'id_category__light').annotate(value=Sum('times'))

    df = pd.DataFrame.from_records(qs)
    df = df.groupby([df['date'].dt.dayofweek, 'id_category__light']).value.sum()

    return df.reset_index()


def get_speed_data_by_hour(count, section, lane=None, direction=None, start=None, end=None, speed_low=0, speed_high=15):

    if not start:
        start = count.start_process_date
    if not end:
        end = count.end_process_date + timedelta(days=1)

    qs = models.CountDetail.objects.filter(
        id_lane__id_section=section,
        timestamp__range=(start, end),
        speed__gte=speed_low,
        speed__lt=speed_high,
    )

    if count is not None:
        qs = qs.filter(id_count=count)

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    qs = qs.annotate(hour=ExtractHour('timestamp')) \
           .values('hour', 'times') \
           .annotate(value=Sum('times')) \
           .values('hour', 'value') \
           .values_list('hour', 'value')

    return qs


def get_characteristic_speed_by_hour(count, section, lane=None, direction=None, start=None, end=None, v=0.15):
    if not start:
        start = count.start_process_date
    if not end:
        end = count.end_process_date + timedelta(days=1)

    qs = models.CountDetail.objects.filter(
        id_lane__id_section=section,
        timestamp__range=(start, end))

    if count is not None:
        qs = qs.filter(id_count=count)

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    qs = qs.annotate(hour=ExtractHour('timestamp')) \
           .order_by('hour', 'speed') \
           .values('hour', 'speed')

    df = pd.DataFrame.from_records(qs.values('hour', 'speed'))
    if not df.empty:
        df = df.set_index('hour')
        df = df.groupby('hour').quantile(v, interpolation='lower')
    return df


def get_average_speed_by_hour(count, section, lane=None, direction=None, start=None, end=None, v=0.15):
    if not start:
        start = count.start_process_date
    if not end:
        end = count.end_process_date + timedelta(days=1)

    qs = models.CountDetail.objects.filter(
        id_lane__id_section=section,
        timestamp__range=(start, end))

    if count is not None:
        qs = qs.filter(id_count=count)

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    qs = qs.annotate(hour=ExtractHour('timestamp')) \
           .order_by('hour', 'speed') \
           .values('hour', 'speed')

    df = pd.DataFrame.from_records(qs.values('hour', 'speed'))
    if not df.empty:
        df = df.set_index('hour')
        df = df.groupby('hour').mean('speed')

    return df


def get_category_data_by_hour(count, section, category, lane=None, direction=None, start=None, end=None):

    if not start:
        start = count.start_process_date
    if not end:
        end = count.end_process_date + timedelta(days=1)

    qs = models.CountDetail.objects.filter(
        id_lane__id_section=section,
        timestamp__range=(start, end),
        id_category=category,
    )

    if count is not None:
        qs = qs.filter(id_count=count)

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    qs = qs.annotate(hour=ExtractHour('timestamp')) \
           .values('hour', 'times') \
           .annotate(value=Sum('times')) \
           .values('hour', 'value') \
           .values_list('hour', 'value')

    return qs


def get_special_periods(first_day, last_day):
    qs = models.SpecialPeriod.objects.filter(
        Q(
            (Q(start_date__lte=first_day) & \
             Q(end_date__gte=last_day))) | \
            (Q(start_date__lte=last_day) & \
             Q(end_date__gte=first_day)))
    return qs


def get_month_data(section, start, end):
    qs = models.CountDetail.objects.filter(
        id_lane__id_section=section,
        timestamp__range=(start, end))

    qs = qs.annotate(month=Trunc('timestamp', 'month')) \
           .order_by('month') \
           .values('month', 'times', 'import_status') \
           .annotate(tm=Sum('times')) \
           .values('month', 'tm', 'import_status')

    df = pd.DataFrame.from_records(qs)
    return df
