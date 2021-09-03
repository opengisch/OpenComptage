from django.db.models import Count, Avg
from django.db.models.functions import Extract
from comptages.datamodel import models


def calculate_tjm(count_id):

    qs = models.CountDetail.objects.filter(id_count_id=count_id).annotate(week_day=Extract('timestamp', 'iso_week_day'))

    for i in qs.values('week_day', 'id_lane').order_by('week_day').annotate(count=Count('times')):
        models.Tjm.objects.create(
            week_day=i['week_day']-1,
            lane_id=i['id_lane'],
            count_id=count_id,
            value=i['count']
            )


def get_tjm_data_by_lane(count_id, lane_id):
    qs = models.Tjm.objects.filter(count_id=count_id, lane_id=lane_id)
    result = [0] * 7

    for i in qs:
        result[i.week_day] += float(i.value)

    return result


def get_tjm_data_by_direction(count_id, direction):
    qs = models.Tjm.objects.filter(count_id=count_id, lane__direction=direction)
    result = [0] * 7

    for i in qs:
        result[i.week_day] += float(i.value)

    return result


def get_tjm_data_total(count_id):
    qs = models.Tjm.objects.filter(count_id=count_id)
    result = [0] * 7

    for i in qs:
        result[i.week_day] += float(i.value)

    return result
