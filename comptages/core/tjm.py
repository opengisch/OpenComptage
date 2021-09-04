from django.db.models import Count, Avg
from django.db.models.functions import Extract
from comptages.datamodel import models
from statistics import mean


def calculate_tjm(count_id):

    qs = models.CountDetail.objects.filter(id_count_id=count_id).annotate(week_day=Extract('timestamp', 'iso_week_day'))

    # FIXME: wrong on multiple weeks, should be average instead of sum of same days
    for i in qs.values('week_day', 'id_lane').order_by('week_day').annotate(count=Count('times')):
        models.Tjm.objects.create(
            week_day=i['week_day']-1,
            lane_id=i['id_lane'],
            count_id=count_id,
            value=i['count']
            )


def get_tjm_data_by_lane(count_id, lane_id):
    qs = models.Tjm.objects.filter(count_id=count_id, lane_id=lane_id)
    return _get_tjm_data(qs)


def get_tjm_data_by_direction(count_id, direction):
    qs = models.Tjm.objects.filter(count_id=count_id, lane__direction=direction)
    return _get_tjm_data(qs)


def _get_tjm_data(qs):
    """Return a list with the week's average at position 0 and then the
    average of each week day"""
    result = [[], [], [], [], [], [], [], []]

    # First for each day of the week we store a list with all the values for this day
    for i in qs:
        result[i.week_day + 1].append(float(i.value))

    # Then we calculate the mean of the day or zero if there are no values
    for count, value in enumerate(result):
        if not value:
            result[count] = 0
        else:
            result[count] = mean(value)

    # Then we calculate the first column of the chart with the average of the week
    result[0] = mean(result[1:])

    return result


def get_tjm_data_total(count_id):

    qs = models.Tjm.objects.filter(count_id=count_id)
    result = [0] * 8

    for i in qs:
        result[i.week_day + 1] += float(i.value)

    result[0] = mean(result[1:])
    return result
