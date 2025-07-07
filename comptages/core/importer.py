from typing import Callable, Iterator, Optional
from pytz import timezone
from os import path
from datetime import datetime, timedelta
from django.db.models import Q

from comptages.core import definitions
from comptages.datamodel import models
from comptages.core.bulk_create_manager import BulkCreateManager

TZ = timezone("Europe/Zurich")


def simple_print_callback(progress: int):
    if progress % 10 == 0:
        print(f"Importing... {progress}%")


def import_file(file_path: str, count, callback_progress=simple_print_callback):
    file_format = get_file_format(file_path)
    file_header = _parse_file_header(file_path)

    if file_format == "VBV-1":
        _parse_and_write(file_path, count, _parse_line_vbv1, callback_progress)
    elif file_format == "INT-2":
        interval = int(file_header["INTERVAL"])
        intspec = get_intspec(file_header)
        data_header = _parse_data_header(file_path)
        cat_bins = _populate_category_dict(count)
        _parse_and_write(
            file_path,
            count,
            _parse_line_int2,
            callback_progress,
            interval=interval,
            intspec=intspec,
            data_header=data_header,
            file_header=file_header,
            categories=cat_bins,
            from_aggregate=True,
        )
    elif file_format == "MC":
        _parse_and_write(file_path, count, _parse_line_mc, callback_progress)
    else:
        raise NotImplementedError("file format not recognized")


def _parse_and_write(
    file_path: str,
    count: models.Count,
    line_parser: Callable,
    callback_progress,
    from_aggregate: bool = False,
    **kwargs,
):
    basename = path.basename(file_path)
    bulk_mgr = BulkCreateManager(chunk_size=500)
    lanes = _populate_lane_dict(count)
    directions = _populate_direction_dict(count)
    cat_bins = _populate_category_dict(count)
    line_count = get_line_count(file_path)
    previous_progress = 0
    try:
        with open(file_path, encoding=get_file_encoding(file_path)) as f:
            for i, line in enumerate(f):
                rows = line_parser(line, **kwargs)
                if not rows:
                    continue

                progress = int(100 / line_count * i)

                if not progress == previous_progress:
                    callback_progress(progress)
                    previous_progress = progress

                for row in rows:
                    category = (
                        cat_bins[row["category"]]
                        if row["category"] is not None
                        else None
                    )
                    id_lane = (
                        lanes[int(row["lane"])]
                        if row["lane"]
                        else directions[int(row["direction"])]
                    )
                    bulk_mgr.add(
                        models.CountDetail(
                            numbering=row["numbering"],
                            timestamp=row["timestamp"],
                            distance_front_front=row["distance_front_front"],
                            distance_front_back=row["distance_front_back"],
                            speed=row["speed"],
                            length=row["length"],
                            height=row["height"],
                            file_name=basename,
                            import_status=definitions.IMPORT_STATUS_QUARANTINE,
                            id_lane_id=id_lane,
                            id_count_id=count.id,
                            id_category_id=category,
                            times=row["times"],
                            from_aggregate=from_aggregate,
                        )
                    )

    except Exception as e:
        print(f"_parse_and_write - Une erreur est survenue, la categorie {row['category']} n'est probablement pas disponible"
              " dans la classification utilisée par ce comptage !")
        raise e

    bulk_mgr.done()


def _parse_line_vbv1(line: str, **kwargs) -> Optional[list[dict]]:
    if line.startswith("* "):
        return None

    parsed_line = {}
    try:
        parsed_line["numbering"] = line[0:6]
        parsed_line["timestamp"] = TZ.localize(
            datetime.strptime("{}0000".format(line[7:24]), "%d%m%y %H%M %S %f")
        )
        parsed_line["reserve_code"] = line[25:31]
        parsed_line["lane"] = int(line[32:34])
        parsed_line["direction"] = int(line[35:36])

        # Default values that are used in case some values are missed from a line
        parsed_line["distance_front_front"] = 0
        parsed_line["distance_front_back"] = 0
        parsed_line["speed"] = -1
        parsed_line["length"] = 0
        parsed_line["category"] = 0
        parsed_line["height"] = "NA"
        parsed_line["times"] = 1

        parsed_line["distance_front_front"] = float(line[37:41])
        parsed_line["distance_front_back"] = float(line[42:46])
        parsed_line["speed"] = int(line[47:50])
        parsed_line["length"] = int(line[52:56])
        parsed_line["category"] = int(line[60:62])
        parsed_line["height"] = line[63:65].strip()

        # If the speed of a vehicle is 0, we put it in the category 0
        if parsed_line["speed"] == 0:
            print('_parse_line_vbv1 - "speed" est égal à 0 km/h !  -> véhicule passé en TRASH')
            parsed_line["category"] = 0

        # If the speed of a vehicle is greater than 3*max_speed or 150km/h
        # TODO: get actual speed limit of the section
        if parsed_line["speed"] > 150:
            print(f'_parse_line_vbv1 - "speed={parsed_line["speed"]}" est supérieur à 150 kmh !  -> véhicule passé en TRASH')
            parsed_line["category"] = 0

    except ValueError:
        if "lane" not in parsed_line:
            print(f'_parse_line_vbv1 - Erreur: véhicule sans voie ({line})')
            return None
        if "direction" not in parsed_line:
            print(f'_parse_line_vbv1 - Erreur: véhicule sans direction ({line})')
            return None
        print(f'_parse_line_vbv1 - parsed_line(!exception!): {parsed_line}')

    return [parsed_line]


def _parse_line_mc(line: str, **kwargs) -> Optional[list[dict]]:
    if not line.startswith("20"):
        return None

    parsed_line = {}
    try:
        # TODO: numbering
        numbering = 1
        parsed_line["numbering"] = numbering
        parsed_line["timestamp"] = TZ.localize(
            datetime.strptime(line[0:19], "%Y-%m-%d %H:%M:%S")
        )
        # On MetroCount files, the direction is 0-1 instead of 1-2
        parsed_line["lane"] = None
        parsed_line["direction"] = int(line[22:23]) + 1
        parsed_line["distance_front_front"] = float(line[24:31])
        if parsed_line["distance_front_front"] > 99.9:
            parsed_line["distance_front_front"] = 99.9
        parsed_line["distance_front_back"] = float(line[31:38])
        if parsed_line["distance_front_back"] > 99.9:
            parsed_line["distance_front_back"] = 99.9
        parsed_line["speed"] = int(float(line[39:44]))
        parsed_line["length"] = int(float(line[44:50]))
        parsed_line["category"] = int(line[51:54].strip())
        parsed_line["height"] = ""
        parsed_line["times"] = 1
    except ValueError:
        # QgsMessageLog.logMessage(
        #     'ValueError: {}'.format(e),  'Comptages', Qgis.Info)

        # This can happen when some values are missed from a line
        return None

    return [parsed_line]


def _parse_line_int2(line, **kwargs) -> Iterator[Optional[dict]]:
    if line.startswith("* "):
        return None

    parsed_line = {}
    # TODO: numbering
    numbering = 1
    parsed_line["numbering"] = numbering
    # In the data files midnight is 2400 of the current day
    # instead of 0000 of the next day
    if line[7:9] == "24":
        line = line[:7] + "00" + line[9:]
        end = TZ.localize(datetime.strptime("{}".format(line[0:11]), "%d%m%y %H%M"))
        end += timedelta(days=1)
    else:
        end = TZ.localize(datetime.strptime("{}".format(line[0:11]), "%d%m%y %H%M"))

    parsed_line["end"] = end
    parsed_line["start"] = parsed_line["end"] - timedelta(minutes=kwargs["interval"])
    parsed_line["channel"] = line[12:13]
    parsed_line["reserve_code"] = line[14:16]
    parsed_line["info_code"] = line[17:19]

    parsed_line["timestamp"] = parsed_line["start"]

    parsed_line["distance_front_front"] = None
    parsed_line["distance_front_back"] = None
    parsed_line["speed"] = None
    parsed_line["length"] = None
    parsed_line["height"] = None
    parsed_line["category"] = None
    parsed_line["lane"] = parsed_line["channel"]
    parsed_line["times"] = 1

    intspec = kwargs["intspec"]
    row_type = intspec[int(parsed_line["info_code"]) - 1]
    bins = _get_int_bins(
        kwargs["file_header"],
        kwargs["data_header"],
        kwargs["intspec"],
        kwargs["categories"],
        row_type,
    )
    if row_type == "SPD":
        for i, data in enumerate(line[20:].split()):
            if int(data) == 0:
                continue
            speed_low = bins[i]
            speed = int(int(speed_low) + 5)
            parsed_line["speed"] = speed
            parsed_line["times"] = int(data)
            yield parsed_line
    elif row_type == "LEN":
        for i, data in enumerate(line[20:].split()):
            if int(data) == 0:
                continue
            lenght_low = bins[i]
            lenght_high = bins[i + 1]
            lenght = int(int(lenght_low) + int(lenght_high) / 2)
            parsed_line["lenght"] = lenght
            parsed_line["times"] = int(data)
            yield parsed_line
    elif row_type == "CLS":
        for i, data in enumerate(line[20:].split()):
            if int(data) == 0:
                continue
            parsed_line["category"] = i + 1
            parsed_line["times"] = int(data)
            yield parsed_line
    elif row_type == "SDS":
        # Insert the values in the SPD table and only the
        # mean and the deviation in the SDS table
        pass
    elif row_type == "DRN":
        pass
    elif row_type == "CNT":
        pass

    return None


def _get_int_bins(
    file_header, data_header, intspec, categories: dict, code: str
) -> list:
    """Returns an array with the bins if they exist, or the number of
    columns of this data type"""
    values = []
    if code == "SPD" or code == "SDS":
        values = file_header["SPDBINS"].split()
    elif code == "LEN":
        values = file_header["LENBINS"].split()
    elif code == "CLS":
        values = list(categories.values())[1:]  # [1:] is because 0 is trash
    else:
        values = data_header[intspec.index(code)]
    return values


def _parse_file_header(file_path: str):
    file_header = dict()

    with open(file_path, encoding=get_file_encoding(file_path)) as f:
        for line in f:
            # Marksmann
            if line.startswith("* ") and not line.startswith("* HEAD "):
                line = line[2:]
                splitted = line.split("=", 1)
                if len(splitted) > 1:
                    key = splitted[0].strip()
                    value = splitted[1].strip()
                    if key == "CLASS" and value == "SPECIAL10":
                        value = "SWISS10"
                    if key in ["STARTREC", "STOPREC"]:
                        value = TZ.localize(datetime.strptime(value, "%H:%M %d/%m/%y"))
                    file_header[key] = value
            # MetroCount
            elif line.startswith("MetroCount"):
                file_header["FORMAT"] = "MC"
            elif line.startswith("Place") and "SITE" not in file_header:
                file_header["SITE"] = line[line.find("[") + 1 : line.find("]")].replace(
                    "-", ""
                )
            elif (
                line.startswith("20")
                and file_header["FORMAT"] == "MC"
                and "STARTREC" not in file_header
            ):
                file_header["STARTREC"] = TZ.localize(
                    datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S")
                )
            elif line.startswith("20") and file_header["FORMAT"] == "MC":
                file_header["STOPREC"] = TZ.localize(
                    datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S")
                )
            elif line.startswith("Type de Cat") and file_header["FORMAT"] == "MC":
                file_header["CLASS"] = line[line.find("(") + 1 : line.find(")")]
                if file_header["CLASS"] == "Euro13":
                    file_header["CLASS"] = "EUR13"
                elif file_header["CLASS"] == "NZTA2011":
                    file_header["CLASS"] = "NZ13"
                elif file_header["CLASS"][:5] == "FHWA ":
                    file_header["CLASS"] = "FHWA13"
                elif file_header["CLASS"] in (
                    "CAT-Cycle_dist-empat",
                    "SPCH-MD5C",
                    "SPCH-MD 5C",
                ):
                    file_header["CLASS"] = "SPCH-MD_5C"

    return file_header


def _parse_data_header(file_path: str) -> list:
    data_header = []

    with open(file_path, encoding=get_file_encoding(file_path)) as f:
        for line in f:
            if line.startswith("* HEAD "):
                start_char = 20
                i = 0
                while True:
                    if not line[start_char : start_char + 4] == "":
                        i += 1
                        start_char += 5
                    else:
                        data_header.append(i)
                        break
    return data_header


def _populate_lane_dict(count: models.Count) -> dict[int, int]:
    # e.g. lanes = {1: 435, 2: 436}

    lanes = models.Lane.objects.filter(id_installation__count=count).order_by("number")

    return {x.number: x.id for x in lanes}


def _populate_direction_dict(count: models.Count):
    # e.g. lanes = {1: 406, 2: 408}
    # It will return only one lane per direction

    directions = models.Lane.objects.filter(id_installation__count=count).order_by(
        "-number"
    )

    return {x.direction: x.id for x in directions}


def _populate_category_dict(count: models.Count):
    # if 'CLASS' not in self.file_header:
    #     return
    # class_name = self.file_header['CLASS']

    class_name = count.id_class.name

    # Use customized SWISS7 class for Marksmann devices
    # because they manage this class in a wrong way
    # if self.file_header['FORMAT'] in ['INT-2', 'VBV-1'] and class_name == 'SWISS7':
    #     class_name = 'SWISS7-MM'

    # e.g. categories = {0: 922, 1: 22, 2: 23, 3: 24, 4: 25, 5: 26, 6: 27, 7: 28, 8: 29, 9: 30, 10: 31}
    categories = models.Category.objects.filter(
        classcategory__id_class__name=class_name
    ).order_by("code")

    return {x.code: x.id for x in categories}


def get_file_format(file_path: str) -> Optional[str]:
    """Return the file format on None if not identified."""
    with open(file_path, encoding=get_file_encoding(file_path)) as f:
        for line in f:
            line = f.readline()
            if line.startswith("* FORMAT"):
                return line.split("=", 1)[1].strip()
            elif line.startswith("MetroCount"):
                return "MC"

        return None


def get_file_encoding(file_path: str) -> str:
    """Guess the right file encoding."""
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            for line in f:
                pass
        except UnicodeDecodeError:
            return "ISO-8859-1"
        else:
            return "utf-8"


def get_line_count(file_path) -> int:
    with open(file_path, encoding=get_file_encoding(file_path)) as f:
        number_of_lines = sum(1 for _ in f)
    return number_of_lines


def get_intspec(file_header):
    intspec = []
    for i, code in enumerate(file_header["INTSPEC"].split("+")):
        if code.strip() not in ["SPD", "SDS", "LEN", "CLS", "CNT", "DRN"]:
            raise NotImplementedError("{}".format(code.strip()))
        # the key corrpespond to the value in the data row
        intspec.append(code.strip())
    return intspec


def guess_count(file_path: str) -> Optional[models.Count]:
    """Try to identify the count related to an imported file."""

    header = _parse_file_header(file_path)

    result = models.Count.objects.filter(
        Q(id_installation__name=header["SITE"])
        | Q(id_installation__alias=header["SITE"])
    )
    result = result.filter(
        id_installation__active=True,
        id_class__name=header["CLASS"],
        start_service_date__lte=header["STARTREC"],
        end_service_date__gte=header["STOPREC"]
        - timedelta(
            seconds=1
        ),  # To manage datetimes like 01.01.2022 00.00 that should be equal to 31.12.2021
    )

    if len(result) > 0:
        return result[0]
    else:
        return None
