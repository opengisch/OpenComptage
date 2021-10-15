from django.db.models import Count, Avg, Sum
from django.db.models.functions import Extract, Cast
from django.db.models.fields import DateField

from comptages.datamodel import models
from statistics import mean


def calculate_tjm(count_id):

    count = models.Count.objects.get(id=count_id)
    qs = models.CountDetail.objects.filter(
        id_count_id=count_id,
        timestamp__gte=count.start_process_date,
        timestamp__lte=count.end_process_date,
    ).annotate(date=Cast('timestamp', DateField()))

    values = qs.values('date', 'id_lane').order_by('date').annotate(count=Count('times'))

    for i in values:
        models.Tjm.objects.create(
            day=i['date'],
            lane_id=i['id_lane'],
            count_id=count_id,
            value=i['count']
            )

    # We store the total tjm into the count table
    average = models.Tjm.objects.filter(count_id=count_id) \
                                .values('day') \
                                .annotate(part=Sum('value')) \
                                .aggregate(tjm=Avg('part'))

    count.tjm = average['tjm']
    count.save()

def get_tjm_data_by_lane(count_id, lane_id):
    qs = models.Tjm.objects.filter(count_id=count_id, lane_id=lane_id)
    return _get_tjm_data(qs)


def get_tjm_data_by_direction(count_id, direction):
    qs = models.Tjm.objects.filter(count_id=count_id, lane__direction=direction)
    return _get_tjm_data(qs)


def _get_tjm_data(qs):
    """Return a list with the average at position 0 and then the
    average of each day"""
    labels = ['moyenne']
    result = [0]

    # First for each day of the week we store a list with all the values for this day
    for i in qs:
        labels.append(i.day.strftime('%d/%m/%Y'))
        result.append(float(i.value))

    # Then we calculate the first column of the chart with the average of the week
    if len(result) > 1:
        result[0] = mean(result[1:])

    return result, labels


def get_tjm_data_total(count_id):
    qs = models.Tjm.objects.filter(count_id=count_id)

    labels = ['moyenne']
    result = [0]

    # First for each day of the week we store a list with all the values for this day
    for i in qs.values('day').order_by('day').annotate(tot=Sum('value')):
        labels.append(i['day'].strftime('%d/%m/%Y'))
        result.append(float(i['tot']))

    # Then we calculate the first column of the chart with the average of the week
    if len(result) > 1:
        result[0] = mean(result[1:])

    return result, labels
