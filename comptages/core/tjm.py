from django.db.models import Count
from django.db.models.functions import TruncDay
from comptages.datamodel import models


def calculate_tjm(count_id):

    qs = models.CountDetail.objects.filter(id_count_id=1).annotate(day=TruncDay('timestamp'))

    for i in qs.values('day', 'id_lane').order_by('day').annotate(count=Count('day')):
        models.Tjm.objects.create(
            day=i['day'],
            lane_id=i['id_lane'],
            count_id=count_id,
            value=i['count']
            )
