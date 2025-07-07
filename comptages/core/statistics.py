from typing import Any
from functools import reduce
from datetime import timedelta, datetime

from pandas import DataFrame, cut
from pytz import timezone
from django.db.models import F, CharField, Value, Sum, QuerySet
from django.db.models.functions import ExtractHour, Trunc, Concat

from comptages.core import definitions
from comptages.core import utils
from comptages.datamodel import models


def get_time_data(
    count,
    section,
    lane=None,
    direction=None,
    start=None,
    end=None,
    exclude_trash=False,
):
    if not start:
        start = count.start_process_date
    if not end:
        end = count.end_process_date + timedelta(days=1)
    start, end = tuple([utils.to_time_aware_utc(d) for d in (start, end)])

    # By lane/direction grouped per hour

    qs = models.CountDetail.objects.filter(
        id_count=count,
        id_lane__id_section=section,
        id_category__isnull=False,
        timestamp__gte=start,
        timestamp__lt=end,
    )

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    if exclude_trash:
        qs = qs.exclude(id_category__trash=True)

    # Vehicles by day and hour
    qs = (
        qs.annotate(date=Trunc("timestamp", "day"), hour=ExtractHour("timestamp"))
        .order_by("hour")
        .values("date", "hour")
        .order_by("-date", "hour")
        .annotate(thm=Sum("times"))
        .values("import_status", "date", "hour", "thm")
    )
    print(f"statistics.py : get_time_data - qs.query={str(qs.query)}")

    df = DataFrame.from_records(qs)
    if not df.empty:
        df["date"] = df["date"].dt.strftime("%a %d.%m.%Y")
        df["import_status"].replace({0: "Existant", 1: "Nouveau"}, inplace=True)

    return df


def get_time_data_yearly(
    year,
    section: models.Section,
    lane=None,
    direction=None,
    exclude_trash=False,
) -> DataFrame:
    """Vehicles by hour and day of the week"""
    start = datetime(year, 1, 1)
    end = datetime(year + 1, 1, 1)
    start, end = tuple([utils.to_time_aware_utc(d) for d in (start, end)])

    # By lane/direction grouped per hour

    qs = models.CountDetail.objects.filter(
        id_lane__id_section=section,
        id_category__isnull=False,
        import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        timestamp__gte=start,
        timestamp__lt=end,
    )

    if exclude_trash:
        qs = qs.exclude(id_category__trash=True)

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    if not qs.exists():
        print(
            f"statistics.py : get_time_data_yearly - Nothing found for Year: {year}, Section: {section}, Lane: {lane}, Direction: {direction}."
        )
        return None

    # Vehicles by day and hour
    qs = (
        qs.annotate(date=Trunc("timestamp", "day"), hour=ExtractHour("timestamp"))
        .order_by("hour")
        .values("date", "hour")
        .order_by("date", "hour")
        .annotate(thm=Sum("times"))
        .values("import_status", "date", "hour", "thm")
    )
    if not qs.exists():
        print(
            f"statistics.py : get_time_data_yearly - Nothing found !!! for Year: {year}. Section: {section}. Lane: {lane}. Direction: {direction}. !!!)"
        )
    print(f"statistics.py : get_time_data_yearly - qsa.query={str(qs.query)}")

    df = DataFrame.from_records(qs)
    if not df.empty:
        df = df.groupby([df["date"].dt.dayofweek, "hour"]).thm.sum()
        df = df.reset_index()

    return df


def get_day_data(
    count: models.Count,
    section=None,
    lane=None,
    direction=None,
    status=None,
    exclude_trash=False,
    start=None,
    end=None,
) -> tuple[DataFrame, int]:
    if not start:
        start = count.start_process_date
    if not end:
        end = count.end_process_date + timedelta(days=1)
    start, end = tuple([utils.to_time_aware_utc(d) for d in (start, end)])

    qs = models.CountDetail.objects.filter(
        id_count=count,
        id_category__isnull=False,
        timestamp__gte=start,
        timestamp__lt=end,
    )

    if exclude_trash:
        qs = qs.exclude(id_category__trash=True)

    # Can be None if we are calculating the total TJM of a special case's count
    if section is not None:
        qs = qs.filter(id_lane__id_section=section)

    if status is not None:
        qs = qs.filter(import_status=status)

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    qs = (
        qs.annotate(date=Trunc("timestamp", "day"))
        .order_by("date")
        .values("date", "import_status")
        .annotate(tj=Sum("times"))
        .values("date", "tj", "import_status")
    )
    print(f"statistics.py : get_day_data - qs.query={str(qs.query)}")

    df = DataFrame.from_records(qs)
    mean = 0
    if not df.empty:
        mean = df["tj"].mean()
        df["import_status"].replace({0: "Existant", 1: "Nouveau"}, inplace=True)

    return df, mean


def get_category_data(
    count: models.Count,
    section: models.Section,
    status=definitions.IMPORT_STATUS_DEFINITIVE,
    start=None,
    end=None,
) -> DataFrame:
    if not start:
        start = count.start_process_date
    if not end:
        end = count.end_process_date + timedelta(days=1)
    start, end = tuple([utils.to_time_aware_utc(d) for d in (start, end)])

    qs = models.CountDetail.objects.filter(
        id_count=count,
        id_lane__id_section=section,
        id_category__isnull=False,
        import_status=status,
        timestamp__gte=start,
        timestamp__lt=end,
    )

    qs = (
        qs.annotate(cat_name=F("id_category__name"))
        .annotate(cat_code=F("id_category__code"))
        .annotate(
            cat_name_code=Concat(
                F("id_category__name"),
                Value(" ("),
                F("id_category__code"),
                Value(")"),
                output_field=CharField(),
            )
        )
        .values("cat_name", "cat_code", "cat_name_code")
        .annotate(value=Sum("times"))
        .order_by("cat_code")
        .values("cat_name", "cat_code", "cat_name_code", "value")
    )
    print(f"statistics.py : get_category_data - qs.query={str(qs.query)}")

    df = DataFrame.from_records(qs)
    return df


def get_speed_data(
    count: models.Count,
    section: models.Section,
    exclude_trash=False,
    start=None,
    end=None,
) -> DataFrame:
    if not start:
        start = count.start_process_date
    if not end:
        end = count.end_process_date + timedelta(days=1)
    start, end = tuple([utils.to_time_aware_utc(d) for d in (start, end)])

    qs = models.CountDetail.objects.filter(
        id_count=count,
        id_lane__id_section=section,
        speed__isnull=False,
        timestamp__gte=start,
        timestamp__lt=end,
    )

    if exclude_trash:
        qs = qs.exclude(id_category__trash=True)

    print(f"statistics.py : get_speed_data - qs.query={str(qs.query)}")

    df = DataFrame.from_records(qs.values("speed", "times", "import_status"))
    if df.empty:
        return df

    df = df.groupby(
        [
            "import_status",
            cut(
                df["speed"],
                bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 999],
                labels=[
                    "0-10",
                    "10-20",
                    "20-30",
                    "30-40",
                    "40-50",
                    "50-60",
                    "60-70",
                    "70-80",
                    "80-90",
                    "90-100",
                    "100-110",
                    "110-120",
                    "120-999",
                ],
                right=False,  # Don't include rightmost edge (e.g. bin 10-20 is actually 10-19.9999999...)
            ),
        ],
        observed=False,
    ).sum("times")

    df = df.rename(columns={"speed": "speedNP"})

    df = df.reset_index(col_fill="NPLA_")
    df["import_status"].replace({0: "Existant", 1: "Nouveau"}, inplace=True)

    return df


def get_light_numbers(
    count: models.Count,
    section: models.Section,
    lane=None,
    direction=None,
    start=None,
    end=None,
    exclude_trash=False,
) -> dict:
    if not start:
        start = count.start_process_date
    if not end:
        end = count.end_process_date + timedelta(days=1)
    start, end = tuple([utils.to_time_aware_utc(d) for d in (start, end)])

    qs = models.CountDetail.objects.filter(
        id_count=count,
        id_lane__id_section=section,
        id_category__isnull=False,
        import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        timestamp__gte=start,
        timestamp__lt=end,
    )

    if exclude_trash:
        qs = qs.exclude(id_category__trash=True)

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    qs = (
        qs.values("id_category__light")
        .annotate(value=Sum("times"))
        .values_list("id_category__light", "value")
    )
    print(f"statistics.py : get_light_numbers - qs.query={str(qs.query)}")

    res = {}
    for r in qs:
        res[r[0]] = r[1]
    return res


def get_light_numbers_yearly(
    section: models.Section,
    lane=None,
    direction=None,
    start=None,
    end=None,
    exclude_trash=False,
) -> DataFrame:
    qs = models.CountDetail.objects.filter(
        id_lane__id_section=section,
        id_category__isnull=False,
        import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        timestamp__gte=start,
        timestamp__lt=end,
    )

    if exclude_trash:
        qs = qs.exclude(id_category__trash=True)

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    qs = qs.annotate(date=Trunc("timestamp", "day"))
    qs = qs.values("date", "id_category__light").annotate(value=Sum("times"))
    print(f"statistics.py : get_light_numbers_yearly - qs.query={str(qs.query)}")

    df = DataFrame.from_records(qs)
    df = df.groupby([df["date"].dt.dayofweek, "id_category__light"]).value.sum()

    return df.reset_index()


def get_speed_data_by_hour(
    count: models.Count,
    section: models.Section,
    lane=None,
    direction=None,
    start=None,
    end=None,
    speed_low=0,
    speed_high=15,
    exclude_trash=False,
) -> "ValuesQuerySet[models.CountDetail, Any]":
    if not start:
        start = count.start_process_date
    if not end:
        end = count.end_process_date + timedelta(days=1)
    start, end = tuple([utils.to_time_aware_utc(d) for d in (start, end)])

    qs = models.CountDetail.objects.filter(
        id_lane__id_section=section,
        speed__gte=speed_low,
        speed__lt=speed_high,
        import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        timestamp__gte=start,
        timestamp__lt=end,
    )

    if exclude_trash:
        qs = qs.exclude(id_category__trash=True)

    if count is not None:
        qs = qs.filter(id_count=count)

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    qs = (
        qs.annotate(hour=ExtractHour("timestamp"))
        .values("hour")
        .annotate(value=Sum("times"))
        .values("hour", "value")
        .values_list("hour", "value")
    )
    print(f"statistics.py : get_speed_data_by_hour - qs.query={str(qs.query)}")

    return qs


def get_characteristic_speed_by_hour(
    count: models.Count,
    section: models.Section,
    lane=None,
    direction=None,
    start=None,
    end=None,
    v=0.15,
    exclude_trash=False,
) -> DataFrame:
    if not start:
        start = count.start_process_date
    if not end:
        end = count.end_process_date + timedelta(days=1)
    start, end = tuple([utils.to_time_aware_utc(d) for d in (start, end)])

    qs = models.CountDetail.objects.filter(
        id_lane__id_section=section,
        speed__isnull=False,
        import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        timestamp__gte=start,
        timestamp__lt=end,
    )

    if exclude_trash:
        qs = qs.exclude(id_category__trash=True)

    if count is not None:
        qs = qs.filter(id_count=count)

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    qs = (
        qs.annotate(hour=ExtractHour("timestamp"))
        .order_by("hour", "speed")
        .values("hour", "speed")
    )
    print(
        f"statistics.py : get_characteristic_speed_by_hour - qs.query={str(qs.query)}"
    )

    df = DataFrame.from_records(qs.values("hour", "speed"))
    if not df.empty:
        df = df.set_index("hour")
        df = df.groupby("hour").quantile(v, interpolation="lower")
    return df


def get_average_speed_by_hour(
    count: models.Count,
    section: models.Section,
    lane=None,
    direction=None,
    start=None,
    end=None,
    v=0.15,
    exclude_trash=False,
) -> DataFrame:
    if not start:
        start = count.start_process_date
    if not end:
        end = count.end_process_date + timedelta(days=1)
    start, end = tuple([utils.to_time_aware_utc(d) for d in (start, end)])

    qs = models.CountDetail.objects.filter(
        id_lane__id_section=section,
        speed__isnull=False,
        import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        timestamp__gte=start,
        timestamp__lt=end,
    )

    if exclude_trash:
        qs = qs.exclude(id_category__trash=True)

    if count is not None:
        qs = qs.filter(id_count=count)

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    qs = (
        qs.annotate(hour=ExtractHour("timestamp"))
        .order_by("hour", "speed")
        .values("hour", "speed")
    )
    print(f"statistics.py : get_average_speed_by_hour - qs.query={str(qs.query)}")

    df = DataFrame.from_records(qs.values("hour", "speed"))
    if not df.empty:
        df = df.set_index("hour")
        df = df.groupby("hour").mean("speed")

    return df


def get_category_data_by_hour(
    count: models.Count,
    section: models.Section,
    category,
    lane=None,
    direction=None,
    start=None,
    end=None,
) -> "ValuesQuerySet[models.CountDetail, Any]":
    if not start:
        start = count.start_process_date
    if not end:
        end = count.end_process_date + timedelta(days=1)
    start, end = tuple([utils.to_time_aware_utc(d) for d in (start, end)])

    qs = models.CountDetail.objects.filter(
        id_lane__id_section=section,
        id_category=category,
        import_status=definitions.IMPORT_STATUS_DEFINITIVE,
        timestamp__gte=start,
        timestamp__lt=end,
    )

    if count is not None:
        qs = qs.filter(id_count=count)

    if lane is not None:
        qs = qs.filter(id_lane=lane)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    qs = (
        qs.annotate(hour=ExtractHour("timestamp"))
        .values("hour", "times")
        .annotate(value=Sum("times"))
        .values("hour", "value")
        .values_list("hour", "value")
    )
    print(f"statistics.py : get_category_data_by_hour - qs.query={str(qs.query)}")

    return qs


def get_special_periods(first_day, last_day) -> QuerySet[models.SpecialPeriod]:
    qs = models.SpecialPeriod.objects.filter(
        start_date__lte=last_day, end_date__gte=first_day
    )
    print(f"statistics.py : get_special_periods - qs.query={str(qs.query)}")

    return qs


def get_month_data(
    section: models.Section,
    start,
    end,
    direction=None,
    exclude_trash=False,
) -> DataFrame:
    qs = models.CountDetail.objects.filter(
        id_lane__id_section=section, timestamp__gte=start, timestamp__lt=end
    )

    qs = (
        qs.annotate(month=Trunc("timestamp", "month"))
        .order_by("month")
        .values("month", "import_status")
        .annotate(tm=Sum("times"))
        .values("month", "tm", "import_status")
    )

    if exclude_trash:
        qs = qs.exclude(id_category__trash=True)

    if direction is not None:
        qs = qs.filter(id_lane__direction=direction)

    print(f"statistics.py : get_month_data - qs.query={str(qs.query)}")

    df = DataFrame.from_records(qs)
    return df


def get_valid_days(year: int, section: models.Section) -> int:
    """
    Count valid days across all counts for `section` and `year`,
    where a day is deemed valid just in case there are at least 14 1-hour blocks
    between 6pm and 4pm with at least 1 vehicle.
    """
    tz = timezone("Europe/Zurich")
    start = tz.localize(datetime(year, 1, 1))
    end = tz.localize(datetime(year + 1, 1, 1))
    iterator = (
        models.CountDetail.objects.filter(
            id_lane__id_section=section,
            id_category__isnull=False,
            import_status=definitions.IMPORT_STATUS_DEFINITIVE,
            timestamp__gte=start,
            timestamp__lt=end,
        )
        .annotate(
            date=F("timestamp__date"), hour=ExtractHour("timestamp"), tj=Sum("times")
        )
        .order_by("date")
        .values("date", "hour", "tj")
    )
    print(f"statistics.py : get_valid_days - iterator.query={str(iterator.query)}")

    def count_valid_blocks(acc: dict, item: dict) -> dict[str, int]:
        date = item["date"]
        if date not in acc:
            acc[date] = 0
        if 6 <= item["hour"] <= 22 and item["tj"] > 0:
            acc[date] += 1
        return acc

    valid_days = reduce(count_valid_blocks, iterator, {})
    has_14_valid_blocks = lambda valid_blocks: valid_blocks >= 14
    return len(list(filter(has_14_valid_blocks, valid_days.values())))
