
import os

from string import ascii_uppercase

from django.db.models import Sum, Avg, Max
from django.db.models.functions import Cast
from django.db.models.fields import DateField
from django.db.models.functions import ExtractIsoWeekDay, ExtractHour, ExtractMonth, ExtractDay

from openpyxl import load_workbook

from comptages.datamodel.models import CountDetail


class YearlyReportBike():
    def __init__(self, file_path, year, section_id):
        # TODO: pass section or section id?

        self.file_path = file_path
        self.year = year
        self.section_id = section_id

    def values_by_direction(self):

        # Get all the count details for section and the year
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            id_category__code__in=[1, 2],
        )

        # Total by day of the week (0->monday, 7->sunday) and by direction
        result = qs.annotate(weekday=ExtractIsoWeekDay('timestamp')) \
                   .values('weekday') \
                   .annotate(total=Sum('times')) \
                   .values('weekday', 'id_lane__direction', 'total')

        print(result)

    def values_by_day_and_hour(self):
        # Get all the count details for section and the year
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
        )

        # TODO: don't divide by 51 but actually aggregate first by the
        # real days (with sum) and then aggregate by weekday (with average)

        # Total by day of the week (0->monday, 7->sunday) and by hour (0->23)
        result = qs.annotate(weekday=ExtractIsoWeekDay('timestamp')) \
                   .annotate(hour=ExtractHour('timestamp')) \
                   .values('weekday', 'hour') \
                   .annotate(tjm=Sum('times') / 51) \
                   .values('weekday', 'hour', 'tjm')

        return result

    def values_by_day_and_month(self):
        # Get all the count details for section and the year
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
        )

        # TODO: don't divide by 12 but actually aggregate first by the
        # real days (with sum) and then aggregate by weekday (with average)

        # Total by day of the week (0->monday, 7->sunday) and by month (1->12)
        result = qs.annotate(weekday=ExtractIsoWeekDay('timestamp')) \
                   .annotate(month=ExtractMonth('timestamp')) \
                   .values('weekday', 'month') \
                   .annotate(tjm=Sum('times') / 12) \
                   .values('weekday', 'month', 'tjm')

        return result

    def tjm_direction_bike(self, categories, direction, weekdays=[0, 1, 2, 3, 4, 5, 6]):

        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            timestamp__iso_week_day__in=weekdays,
            id_category__code__in=categories,
            id_lane__direction=direction,
        )

        # TODO: avoid the division?
        return qs.aggregate(res=Sum('times'))['res'] / 365

    def total(self, categories=[1]):

        qs = CountDetail.objects.filter(
            timestamp__year=self.year,
            id_category__code__in=categories,
        )

        return qs.aggregate(res=Sum('times'))['res']

    def max_day(self, categories=[1]):

        qs = CountDetail.objects.filter(
            timestamp__year=self.year,
            id_category__code__in=categories,
        ).annotate(
            date=Cast('timestamp', DateField())).values('date').annotate(total=Sum('times')).order_by('-total')

        return qs[0]['total'], qs[0]['date']

    def max_month(self, categories=[1]):

        qs = CountDetail.objects.filter(
            timestamp__year=self.year,
            id_category__code__in=categories,
        ).annotate(
            month=ExtractMonth('timestamp')).values('month').annotate(total=Sum('times')).order_by('-total')

        return qs[0]['total'], qs[0]['month']

    def min_month(self, categories=[1]):

        qs = CountDetail.objects.filter(
            timestamp__year=self.year,
            id_category__code__in=categories,
        ).annotate(
            month=ExtractMonth('timestamp')).values('month').annotate(total=Sum('times')).order_by('total')

        return qs[0]['total'], qs[0]['month']

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template = os.path.join(current_dir, 'template_yearly_bike.xlsx')
        workbook = load_workbook(filename=template)

        ws = workbook['AN_TE']

        row_offset = 14
        column_offset = 1
        data = self.values_by_day_and_hour()
        for i in data:
            ws.cell(
                row=i['hour']+row_offset,
                column=i['weekday']+column_offset,
                value=i['tjm'])

        row_offset = 47
        column_offset = 1

        data = self.values_by_day_and_month()
        for i in data:
            ws.cell(
                row=i['month']+row_offset,
                column=i['weekday']+column_offset,
                value=i['tjm'])

        ws = workbook['CV_LV']

        ws['F11'] = self.tjm_direction_bike([1], 1, weekdays=[0, 1, 2, 3, 4])
        ws['G11'] = self.tjm_direction_bike([1], 2, weekdays=[0, 1, 2, 3, 4])
        ws['H11'] = self.tjm_direction_bike([2, 3, 4, 5], 1, weekdays=[0, 1, 2, 3, 4])
        ws['I11'] = self.tjm_direction_bike([2, 3, 4, 5], 2, weekdays=[0, 1, 2, 3, 4])

        ws['F12'] = self.tjm_direction_bike([1], 1)
        ws['G12'] = self.tjm_direction_bike([1], 2)
        ws['H12'] = self.tjm_direction_bike([2, 3, 4, 5], 1)
        ws['I12'] = self.tjm_direction_bike([2, 3, 4, 5], 2)

        ws['J35'] = self.total()
        ws['J39'] = self.max_day()[0]
        ws['K39'] = self.max_day()[1]

        ws['J40'] = self.max_month()[0]
        ws['K40'] = self.max_month()[1]

        ws['J41'] = self.min_month()[0]
        ws['k41'] = self.min_month()[1]

        # Save the file
        output = os.path.join(
            self.file_path, '{}_{}_r.xlsx'.format(self.section_id, self.year))

        workbook.save(filename=output)
