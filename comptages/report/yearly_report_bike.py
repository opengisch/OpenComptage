from decimal import Decimal
from functools import reduce
import os
from typing import Any, Union

from django.db.models import Sum, Avg, F
from django.db.models.fields import DateField
from django.db.models.functions import (
    Cast,
    ExtractHour,
    ExtractIsoWeekDay,
    ExtractMonth,
    TruncDate,
)
from django.db.models import Sum, Avg
from openpyxl import load_workbook

from comptages.core import definitions
from comptages.datamodel.models import CountDetail, Lane, Section


class YearlyReportBike:
    def __init__(self, path_to_output_dir, year, section_id):
        # TODO: pass section or section id?

        self.path_to_output_dir = path_to_output_dir
        self.year = year
        self.section_id = section_id

    def total_runs_by_directions(self) -> "ValuesQuerySet[CountDetail, dict[str, Any]]":
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

    def tjms_by_weekday_hour(self) -> "ValuesQuerySet[CountDetail, dict[str, Any]]":
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
            qs.annotate(date=TruncDate("timestamp"))
            .values("date")
            .annotate(Sum("times"))
            .annotate(weekday=ExtractIsoWeekDay("date"))
            .values("weekday")
            .annotate(tjm=Avg("times"))
            .annotate(hour=ExtractHour("timestamp"))
            .values("weekday", "hour", "tjm")
        )
        return result

    def total_runs_by_hour_and_direction(
        self, directions=(1, 2), weekdays=(0, 1, 2, 3, 4, 5, 6)
    ) -> dict[int, Any]:
        # Get all the count details for section and the year
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            id_lane__direction__in=directions,
            timestamp__iso_week_day__in=weekdays,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )

        results = (
            qs.annotate(hour=ExtractHour("timestamp"))
            .values("hour")
            .annotate(
                runs=Sum("times"),
                direction=F("id_lane__direction"),
                section=F("id_lane__id_section_id"),
            )
            .values("runs", "hour", "direction", "section")
        )

        def partition(acc: dict, val: dict) -> dict:
            hour = val["hour"]
            direction = val["direction"]

            if hour not in acc:
                acc[hour] = {}

            if direction not in acc[hour]:
                acc[hour][direction] = {}

            acc[hour][direction] = val
            return acc

        return reduce(partition, results, {})

    def total_runs_by_hour_one_direction(self, direction: int) -> dict[int, Any]:
        # Get all the count details for hours and the specific direction
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            id_lane__direction=direction,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )
        results = (
            qs.annotate(hour=ExtractHour("timestamp"))
            .values("hour")
            .annotate(runs=Sum("times"))
            .values("runs", "hour")
            .annotate(day=ExtractIsoWeekDay("timestamp"))
            .order_by("day")
        )

        def reducer(acc: dict, val: dict) -> dict:
            day = val["day"]
            hour = val["hour"]

            if not day in acc:
                acc[day] = {}

            if not hour in acc:
                acc[day][hour] = val["runs"]

            return acc

        return reduce(reducer, results, {})

    def tota_runs_by_hour_weekday_one_direction(
        self, direction: int
    ) -> "ValuesQuerySet[Countdetail, dict[str, Any]]":
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            id_lane__direction=direction,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )
        return (
            qs.annotate(hour=ExtractHour("timestamp"))
            .values("hour")
            .annotate(runs=Sum("times"))
            .values("runs", "hour")
            .annotate(day=ExtractIsoWeekDay("timestamp"))
            .order_by("day")
        )

    def tjms_by_weekday_and_month(
        self,
    ) -> "ValuesQuerySet[CountDetail, dict[str, Any]]":
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
            qs.annotate(date=TruncDate("timestamp"))
            .values("date")
            .annotate(Sum("times"))
            .annotate(weekday=ExtractIsoWeekDay("timestamp"))
            .values("weekday")
            .annotate(tjm=Avg("times"), month=ExtractMonth("timestamp"))
            .values("weekday", "month", "tjm")
        )

        return result

    def tjm_by_day(self) -> "ValuesQuerySet[CountDetail, dict[str, Any]]":
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

    def tjms_total_runs_by_day_of_week(self) -> dict[str, Any]:
        # Get all the count details for section and the year
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )
        result = (
            qs.annotate(date=TruncDate("timestamp"))
            .values("date")
            .annotate(daily_runs=Sum("times"), week_day=ExtractIsoWeekDay("timestamp"))
            .values("week_day", "daily_runs")
            .order_by("week_day")
        )
        # FIXME
        # Aggregation via `values()` into `annotate()` all the way to the end result would be more performant.
        builder = {}
        for item in result:
            if item["week_day"] not in builder:
                builder[item["week_day"]] = {
                    "days": 1,
                    "runs": item["daily_runs"],
                    "tjm": item["daily_runs"],
                    "week_day": item["week_day"],
                }
            else:
                builder[item["week_day"]]["days"] += 1
                builder[item["week_day"]]["runs"] += item["daily_runs"]
                builder[item["week_day"]]["tjm"] = round(
                    builder[item["week_day"]]["runs"]
                    / builder[item["week_day"]]["days"]
                )
        return builder

    def total_runs_by_class(self) -> dict[str, Any]:
        # Get all the count details for section and the year
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )

        results = (
            qs.annotate(day=ExtractIsoWeekDay("timestamp"))
            .values("day")
            .annotate(runs=Sum("times"), code=F("id_category__code"))
            .values("day", "runs", "code")
        )

        def reducer(acc: dict, i: dict):
            code = i["code"]
            day = i["day"]
            runs = i["runs"]

            if code not in acc:
                acc[code] = {}

            acc[code][day] = runs
            return acc

        return reduce(reducer, results, {})

    def tjms_by_direction_bike(
        self, categories, direction, weekdays=[0, 1, 2, 3, 4, 5, 6]
    ) -> float:
        qs = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            timestamp__iso_week_day__in=weekdays,
            id_category__code__in=categories,
            id_lane__direction=direction,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )
        assert qs.exists()

        # TODO: avoid the division?
        return qs.aggregate(res=Sum("times"))["res"] / 365

    def total(self, categories=[1]) -> float:
        qs = CountDetail.objects.filter(
            timestamp__year=self.year,
            id_category__code__in=categories,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )

        return qs.aggregate(res=Sum("times"))["res"]

    def max_day(self, categories=[1]) -> tuple[str, Any]:
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

    def max_month(self, categories=[1]) -> tuple[str, Any]:
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

    def min_month(self, categories=[1]) -> tuple[str, Any]:
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

        def render_section_dist(value: Union[str, Decimal, None]) -> str:
            if value is None or value == "NA":
                return "NA"
            if isinstance(value, str):
                return str(round(int(value)))
            if isinstance(value, Decimal):
                return str(round(value))
            raise ValueError(value)

        section_start_dist = render_section_dist(section.start_dist)
        section_end_dist = render_section_dist(section.end_dist)

        ws[
            "B3"
        ] = f"""
            Poste de comptage : {section.id}  
            Axe : {section.owner}:{section.road}{section.way}
            PR {section.start_pr} + {section_start_dist} m à PR {section.end_pr} + {section_end_dist} m
        """

        ws["B4"] = "Periode de comptage du 01/01/{0} au 31/12/{0}".format(self.year)
        ws["B5"] = "Comptage {}".format(self.year)

        # Get one count for the section and the year to get the base data
        count_detail = CountDetail.objects.filter(
            id_lane__id_section__id=self.section_id,
            timestamp__year=self.year,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        )
        if not count_detail.exists():
            print("Aucun conmptage pour cette année ({}) et cette section ({})".format(self.year,self.section_id))
            return

        count = count_detail[0].id_count

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

        ws = workbook["Data_year"]
        row_offset = 4
        column_offset = 1

        data = self.tjm_by_day()
        row = row_offset
        for i in data:
            ws.cell(row=row, column=column_offset, value=i["date"])
            ws.cell(row=row, column=column_offset + 1, value=i["tjm"])
            row += 1

        ws["F11"] = self.tjms_by_direction_bike([1], 1, weekdays=[0, 1, 2, 3, 4])
        ws["G11"] = self.tjms_by_direction_bike([1], 2, weekdays=[0, 1, 2, 3, 4])
        ws["H11"] = self.tjms_by_direction_bike(
            [2, 3, 4, 5], 1, weekdays=[0, 1, 2, 3, 4]
        )
        ws["I11"] = self.tjms_by_direction_bike(
            [2, 3, 4, 5], 2, weekdays=[0, 1, 2, 3, 4]
        )

        ws["F12"] = self.tjms_by_direction_bike([1], 1)
        ws["G12"] = self.tjms_by_direction_bike([1], 2)
        ws["H12"] = self.tjms_by_direction_bike([2, 3, 4, 5], 1)
        ws["I12"] = self.tjms_by_direction_bike([2, 3, 4, 5], 2)

        ws["J35"] = self.total()
        ws["J39"] = self.max_day()[0]
        ws["K39"] = self.max_day()[1]

        ws["J40"] = self.max_month()[0]
        ws["K40"] = self.max_month()[1]

        ws["J41"] = self.min_month()[0]
        ws["k41"] = self.min_month()[1]

        ws = workbook["Data_week"]
        row_offset = 4
        column_offset = 2

        data = self.tjms_total_runs_by_day_of_week().values()
        row = row_offset
        for i in data:
            ws.cell(row=row, column=column_offset, value=i["runs"])
            ws.cell(row=row, column=column_offset + 3, value=i["tjm"])
            row += 1

        # Data_hour
        ws = workbook["Data_hour"]

        # Data hour > Whole weeks
        print_area = ws["C5:D28"]
        data = self.total_runs_by_hour_and_direction(directions=(1, 2))
        for hour, row in enumerate(print_area, 1):
            if hour == 24:
                hour = 0
            for direction, cell in enumerate(row, 1):
                if not hour in data or not direction in data[hour]:
                    cell.value = 0
                else:
                    cell.value = data[hour][direction]["runs"]

        # Data hour > Weekends only
        print_area = ws["C37:D60"]
        data = self.total_runs_by_hour_and_direction(directions=(1, 2), weekdays=(5, 6))
        for hour, row in enumerate(print_area, 1):
            if hour == 24:
                hour = 0
            for direction, cell in enumerate(row, 1):
                if not hour in data or not direction in data[hour]:
                    cell.value = 0
                else:
                    cell.value = data[hour][direction]["runs"]

        # Data hour > Only dir 1
        print_area = ws["B69:H92"]
        data = self.total_runs_by_hour_one_direction(1)
        for hour, row in enumerate(print_area, 1):
            if hour == 24:
                hour = 0
            for day, cell in enumerate(row, 1):
                if not day in data or not hour in data[day]:
                    cell.value = 0
                else:
                    cell.value = data[day][hour]

        # Data hour > Only dir 2
        print_area = ws["B101:H124"]
        data = self.total_runs_by_hour_one_direction(2)
        for hour, row in enumerate(print_area, 1):
            if hour == 24:
                hour = 0
            for day, cell in enumerate(row, 1):
                if not day in data or not hour in data[day]:
                    cell.value = 0
                else:
                    cell.value = data[day][hour]

        data = self.total_runs_by_class()
        ws = workbook["Data_class"]
        print_area = ws["B4:H18"]
        for code, row in enumerate(print_area, 0):
            for day, cell in enumerate(row, 1):
                if not code in data or not day in data[code]:
                    cell.value = 0
                else:
                    cell.value = data[code][day]

        ws = workbook["AN_GR"]
        ws.print_area = "A1:Z62"

        ws = workbook["CAT"]
        ws.print_area = "A1:Z62"

        # Save the file
        output = os.path.join(
            self.path_to_output_dir, "{}_{}_r.xlsx".format(self.section_id, self.year)
        )

        workbook.save(filename=output)
        print(f"Saved report to {output}")
