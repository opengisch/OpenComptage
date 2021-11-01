import pytz
from datetime import datetime, timezone


def get_file_format(file_path):
    """Return the file format on None if not identified."""
    with open(file_path, encoding=get_file_encoding(file_path)) as f:
        for line in f:
            line = f.readline()
            if line.startswith("* FORMAT"):
                return line.split("=", 1)[1].strip()
            elif line.startswith("MetroCount"):
                return "MC"

        return None


def get_file_encoding(file_path):
    """Guess the right file encoding."""
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            for line in f:
                pass
        except UnicodeDecodeError:
            return 'ISO-8859-1'
        else:
            return 'utf-8'


def get_file_header(file_path):
    """Return the file header lines in a list."""

    file_format = get_file_format(file_path)

    result = []
    if file_format == "INT-2" or file_format == "VBV-1":
        with open(file_path, encoding=get_file_encoding(file_path)) as f:
            for line in f:
                if not line.startswith("* "):
                    break

                result.append(line)
        return result

    elif file_format == "MC":
        with open(file_path, encoding=get_file_encoding(file_path)) as f:
            for line in f:
                if line.startswith(""):
                    break

                result.append(line)
        return result

    else:
        return None


def get_first_record_date(file_path):
    """Get the date of the first record in the file as a timedate."""

    tz = pytz.timezone('Europe/Zurich')
    result = None
    file_format = get_file_format(file_path)

    if file_format == "INT-2" or file_format == "VBV-1":
        with open(file_path, encoding=get_file_encoding(file_path)) as f:
            for line in f:
                if not line.startswith("* "):
                    # In the data files midnight is 2400 of the current day
                    # instead of 0000 of the next day
                    if line[7:9] == '24':
                        line = line[:7] + '00' + line[9:]
                        result = datetime.strptime(
                            "{}".format(line[0:11]), "%d%m%y %H%M").replace(
                                tzinfo=tz)
                        result += timedelta(days=1)
                    else:
                        result = datetime.strptime(
                            "{}".format(line[0:11]), "%d%m%y %H%M").replace(
                                tzinfo=tz)

                    return result
    elif file_format == "MC":
        with open(file_path, encoding=get_file_encoding(file_path)) as f:
            for line in f:
                if line.startswith('20'):
                    result = datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S").replace(
                        tzinfo=tz)
                    return result
    else:
        return None


def get_last_record_date(file_path):
    """Get the date of the last record in the file as a timedate.

    It scans until the end of the file looking for the last date."""

    tz = pytz.timezone('Europe/Zurich')
    result = None
    file_format = get_file_format(file_path)

    if file_format == "INT-2" or file_format == "VBV-1":
        with open(file_path, encoding=get_file_encoding(file_path)) as f:
            for line in f:
                if not line.startswith("* "):
                    # In the data files midnight is 2400 of the current day
                    # instead of 0000 of the next day
                    if line[7:9] == '24':
                        line = line[:7] + '00' + line[9:]
                        result = datetime.strptime(
                            "{}".format(line[0:11]), "%d%m%y %H%M").replace(
                                tzinfo=tz)
                        result += timedelta(days=1)
                    else:
                        result = datetime.strptime(
                            "{}".format(line[0:11]), "%d%m%y %H%M").replace(
                                tzinfo=tz)

            return result
    elif file_format == "MC":
        with open(file_path, encoding=get_file_encoding(file_path)) as f:
            for line in f:
                if line.startswith('20'):
                    result = datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S").replace(
                        tzinfo=tz)
            return result
    else:
        return None


def parse_file_header(file_header, file_format):
    """Return the header important items in a dict."""
    result = {}
    if file_format == "INT-2" or file_format == "VBV-1":
        for line in file_header:
            line = line[2:]
            splitted = line.split('=', 1)
            if len(splitted) > 1:
                key = splitted[0].strip()
                value = splitted[1].strip()
                if key == 'CLASS' and value == 'SPECIAL10':
                    value = 'SWISS10'
                result[key] = value
        return result

    elif file_format == "MC":
        result['FORMAT'] = 'MC'
        for line in file_header:
            if line.startswith('Place'):
                result['SITE'] = line[
                    line.find('[') + 1:line.find(']')].replace('-', '')
            elif line.startswith('20'):
                result['STARTREC'] = datetime.strftime(
                    datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S"),
                    "%H:%M %d/%m/%y")
            elif line.startswith('20'):
                result['STOPREC'] = datetime.strftime(
                    datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S"),
                    "%H:%M %d/%m/%y")
            elif line.startswith('Type de Cat'):
                class_ = line[line.find('(') + 1:line.find(')')]
                if class_ == 'Euro13':
                    result['CLASS'] = 'EUR13'
                elif class_ == 'NZTA2011':
                    result['CLASS'] = 'NZ13'
                elif class_[:5] == 'FHWA ':
                    result['CLASS'] = 'FHWA13'
                elif class_ == 'CAT-Cycle_dist-empat':
                    result['CLASS'] = 'SPCH-MD 5C'
        return result

    else:
        return None
