from django.db.models import Count
from django.db.models.functions import Extract
from comptages.datamodel import models


def calculate_tjm(count_id):

    qs = models.CountDetail.objects.filter(id_count_id=1).annotate(week_day=Extract('timestamp', 'week_day'))

    for i in qs.values('week_day', 'id_lane').order_by('week_day').annotate(count=Count('week_day')):
        models.Tjm.objects.create(
            week_day=i['week_day'],
            lane_id=i['id_lane'],
            count_id=count_id,
            value=i['count']
            )
