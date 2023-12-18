import os
from typing import Any

from django.db.models.fields import DateField
from django.db.models.functions import (
    Cast,
    ExtractHour,
    ExtractDay,
    ExtractIsoWeekDay,
    ExtractMonth,
    TruncDate,
)
from django.db.models import Count, Sum, F, Avg
from openpyxl import load_workbook

from comptages.core import definitions
from comptages.datamodel.models import CountDetail, Lane, Section


class YearlyReportBike:
    def __init__(self, file_path, year, section_id):
        # TODO: pass section or section id?

        self.file_path = file_path
        self.year = year
        self.section_id = section_id

    def values_by_direction(self) -> "ValuesQuerySet[CountDetail, Any]":
        # Get all the count details for section and the year
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            # id_category__code__in=[1, 2],
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )

        # Total by day of the week (0->monday, 7->sunday) and by direction
        return (
            qs.annotate(weekday=ExtractIsoWeekDay("timestamp"))
            .values("weekday")
            .annotate(total=Sum("times"))
            .values("weekday", "id_lane__direction", "total")
        )

    def values_by_day_and_hour(self) -> "ValuesQuerySet[CountDetail, dict[str, Any]]":
        # Get all the count details for section and the year
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )

        # TODO: don't divide by 51 but actually aggregate first by the
        # real days (with sum) and then aggregate by weekday (with average)

        # Total by day of the week (0->monday, 6->sunday) and by hour (0->23)
        result = (
            qs.annotate(
                weekday=ExtractIsoWeekDay("timestamp"),
                realday=TruncDate("timestamp"),
                hour=ExtractHour("timestamp"),
            )
            .values("realday")
            .annotate(tjm=Sum("times"))
            .values("weekday")
            .annotate(tjm=Avg("times"))
            .values("weekday", "hour", "tjm")
        )
        return result

    def values_by_hour_and_direction(
        self, direction, weekdays=[0, 1, 2, 3, 4, 5, 6]
    ) -> "ValuesQuerySet[CountDetail, Any]":
        # Get all the count details for section and the year
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            id_lane__direction=direction,
            timestamp__iso_week_day__in=weekdays,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )

        # TODO: don't divide by 365

        # Total by hour (0->23)
        result = (
            qs.annotate(
                hour=ExtractHour("timestamp"),
                realday=TruncDate("timestamp"),
            )
            .values("realday")
            .annotate(tjm=Sum("times"))
            .values("hour", "tjm")
        )

        return result

    def values_by_day_and_month(self) -> "ValuesQuerySet[CountDetail, Any]":
        # Get all the count details for section and the year
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )

        # TODO: don't divide by 12 but actually aggregate first by the
        # real days (with sum) and then aggregate by weekday (with average)

        # Total by day of the week (0->monday, 6->sunday) and by month (1->12)
        result = (
            qs.annotate(
                realday=TruncDate("timestamp"),
                weekday=ExtractIsoWeekDay("timestamp"),
                month=ExtractMonth("timestamp"),
            )
            .values("realday")
            .annotate(tjm=Sum("times"))
            .values("weekday", "tjm")
            .annotate(tjm=Avg("tjm"))
            .values("weekday", "month", "tjm")
        )

        return result

    def values_by_day(self) -> "ValuesQuerySet[CountDetail, Any]":
        # Get all the count details for section and the year
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )

        # Group by date
        result = (
            qs.annotate(date=Cast("timestamp", DateField()))
            .values("date")
            .annotate(tjm=Sum("times"))
            .values("date", "tjm")
        )

        return result

    def values_by_day_of_week(self) -> "ValuesQuerySet[CountDetail, Any]":
        # Get all the count details for section and the year
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )

        # TODO: don't divide by 51 but actually aggregate first by the
        # real days (with sum) and then aggregate by weekday (with average)

        # Group by day of the week (0->monday, 7->sunday)
        result = (
            qs.annotate(
                weekday=ExtractIsoWeekDay("timestamp"), realday=TruncDate("timestamp")
            )
            .values("realday")
            .annotate(tjm=Sum("times"))
            .values("realday", "tjm")
            .annotate(tjm=Avg("times"))
            .values("weekday", "tjm")
        )

        return result

    def values_by_class(self) -> "ValuesQuerySet[CountDetail, Any]":
        # Get all the count details for section and the year
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )

        result = (
            qs.annotate(res=Sum("times"))
            .values("res")
            .values("id_category__code")
            .annotate(tjm=Count("id_category__code"))
        )
        return result

    def tjm_direction_bike(
        self, categories, direction, weekdays=[0, 1, 2, 3, 4, 5, 6]
    ) -> dict:
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            timestamp__iso_week_day__in=weekdays,
            id_category__code__in=categories,
            id_lane__direction=direction,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )

        # TODO: avoid the division?
        return qs.aggregate(res=Sum("times"))["res"] / 365

    def total(self, categories=[1]) -> dict:
        qs = CountDetail.objects.filter(
            timestamp__year=self.year,
            id_category__code__in=categories,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )

        return qs.aggregate(res=Sum("times"))["res"]

    def max_day(self, categories=[1]) -> tuple:
        qs = (
            CountDetail.objects.filter(
                timestamp__year=self.year,
                id_category__code__in=categories,
                import_status=definitions.IMPORT_STATUS_DEFINITIVE,
            )
            .annotate(date=Cast("timestamp", DateField()))
            .values("date")
            .annotate(total=Sum("times"))
            .order_by("-total")
        )

        return qs[0]["total"], qs[0]["date"]

    def max_month(self, categories=[1]) -> tuple:
        qs = (
            CountDetail.objects.filter(
                timestamp__year=self.year,
                id_category__code__in=categories,
                import_status=definitions.IMPORT_STATUS_DEFINITIVE,
            )
            .annotate(month=ExtractMonth("timestamp"))
            .values("month")
            .annotate(total=Sum("times"))
            .order_by("-total")
        )

        return qs[0]["total"], qs[0]["month"]

    def min_month(self, categories=[1]) -> tuple:
        qs = (
            CountDetail.objects.filter(
                timestamp__year=self.year,
                id_category__code__in=categories,
                import_status=definitions.IMPORT_STATUS_DEFINITIVE,
            )
            .annotate(month=ExtractMonth("timestamp"))
            .values("month")
            .annotate(total=Sum("times"))
            .order_by("total")
        )

        return qs[0]["total"], qs[0]["month"]

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template = os.path.join(current_dir, "template_yearly_bike.xlsx")
        workbook = load_workbook(filename=template)

        ws = workbook["Data_count"]

        section = Section.objects.get(id=self.section_id)
        ws["B3"] = (
            "Poste de comptage : {}  Axe : {}:{}{}  " "PR {} + {} m à PR {} + {} m"
        ).format(
            section.id,
            section.owner,
            section.road,
            section.way,
            section.start_pr,
            int(round(section.start_dist)),
            section.end_pr,
            int(round(section.end_dist)),
        )

        ws["B4"] = "Periode de comptage du 01/01/{0} au 31/12/{0}".format(self.year)

        ws["B5"] = "Comptage {}".format(self.year)

        # Get one count for the section and the year to get the base data
        count_detail = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )[0]
        count = count_detail.id_count

        ws["B6"] = "Type de capteur : {}".format(count.id_sensor_type.name)
        ws["B7"] = "Modèle : {}".format(count.id_model.name)
        ws["B8"] = "Classification : {}".format(count.id_class.name)
        ws["B9"] = "Comptage véhicule par véhicule"

        ws["B12"] = "Remarque : {}".format(count.remarks)

        lanes = Lane.objects.filter(id_installation=count.id_installation)

        ws["B13"] = lanes[0].direction_desc
        if len(lanes) > 1:
            ws["B14"] = lanes[1].direction_desc

        ws["B11"] = lanes[0].id_section.place_name

        ws = workbook["AN_TE"]

        row_offset = 14
        column_offset = 1
        data = self.values_by_day_and_hour()
        for i in data:
            ws.cell(
                row=i["hour"] + row_offset,
                column=i["weekday"] + column_offset,
                value=i["tjm"],
            )

        row_offset = 47
        column_offset = 1

        data = self.values_by_day_and_month()
        for i in data:
            ws.cell(
                row=i["month"] + row_offset,
                column=i["weekday"] + column_offset,
                value=i["tjm"],
            )

        ws = workbook["CV_LV"]

        ws["F11"] = self.tjm_direction_bike([1], 1, weekdays=[0, 1, 2, 3, 4])
        ws["G11"] = self.tjm_direction_bike([1], 2, weekdays=[0, 1, 2, 3, 4])
        ws["H11"] = self.tjm_direction_bike([2, 3, 4, 5], 1, weekdays=[0, 1, 2, 3, 4])
        ws["I11"] = self.tjm_direction_bike([2, 3, 4, 5], 2, weekdays=[0, 1, 2, 3, 4])

        ws["F12"] = self.tjm_direction_bike([1], 1)
        ws["G12"] = self.tjm_direction_bike([1], 2)
        ws["H12"] = self.tjm_direction_bike([2, 3, 4, 5], 1)
        ws["I12"] = self.tjm_direction_bike([2, 3, 4, 5], 2)

        ws["J35"] = self.total()
        ws["J39"] = self.max_day()[0]
        ws["K39"] = self.max_day()[1]

        ws["J40"] = self.max_month()[0]
        ws["K40"] = self.max_month()[1]

        ws["J41"] = self.min_month()[0]
        ws["k41"] = self.min_month()[1]

        ws = workbook["Data_year"]
        row_offset = 4
        column_offset = 1

        data = self.values_by_day()
        row = row_offset
        for i in data:
            ws.cell(row=row, column=column_offset, value=i["date"])
            ws.cell(row=row, column=column_offset + 1, value=i["tjm"])
            row += 1

        ws = workbook["Data_week"]
        row_offset = 4
        column_offset = 2

        data = self.values_by_day_of_week()
        row = row_offset
        for i in data:
            ws.cell(row=row, column=column_offset, value=i["tjm"])
            row += 1

        ws = workbook["Data_hour"]
        row_offset = 5
        column_offset = 3

        data = self.values_by_hour_and_direction(1)
        row = row_offset
        for i in data:
            ws.cell(row=row, column=column_offset, value=i["tjm"])
            row += 1

        row_offset = 5
        column_offset = 4

        data = self.values_by_hour_and_direction(2)
        row = row_offset
        for i in data:
            ws.cell(row=row, column=column_offset, value=i["tjm"])
            row += 1

        # Weekend days only
        row_offset = 37
        column_offset = 3

        data = self.values_by_hour_and_direction(1, [5, 6])
        row = row_offset
        for i in data:
            ws.cell(row=row, column=column_offset, value=i["tjm"])
            row += 1

        row_offset = 37
        column_offset = 4

        data = self.values_by_hour_and_direction(2, [5, 6])
        row = row_offset
        for i in data:
            ws.cell(row=row, column=column_offset, value=i["tjm"])
            row += 1

        ws = workbook["Data_class"]
        row_offset = 4
        column_offset = 2

        data = self.values_by_class()
        row = row_offset
        for i in data:
            ws.cell(row=row, column=column_offset, value=i["tjm"])
            row += 1

        ws = workbook["AN_GR"]
        ws.print_area = "A1:Z62"

        ws = workbook["CAT"]
        ws.print_area = "A1:Z62"

        # Save the file
        output = os.path.join(
            self.file_path, "{}_{}_r.xlsx".format(self.section_id, self.year)
        )

        workbook.save(filename=output)
