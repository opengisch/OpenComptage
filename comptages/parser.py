import pytz
from datetime import datetime, timedelta, timezone


class Parser():
    """Data file parser."""

    def __init__(self, file_path):
        """Create a parser object from a data file."""
        self.file_path = file_path
        self.encoding = self._file_encoding()
        self.file_format = self._file_format()
        self.header = self._parse_file_header()

    def lines(self):
        """Generate the next line to be written into the db.

        It returns a dict with the attributes of CountDetail (without the
        foreign keys values that are added after for performace reasons)
        and the percent of the file already parsed.
        """

        with open(self.file_path, encoding=self.encoding) as f:
            for line in f:
                if self.file_format == "MC":
                    yield self._parse_data_line_metrocount(line)
                
                # result = {
                #     "np": "la",
                #     "tf": "la",
                #     "dj": "la",
                #     }
                # yield result

        # {
        #     # numbering:  # TODO: still needed?
        #     # timestamp
        #     # distance_front_front
        #     # distance_front_back
        #     # speed
        #     # length
        #     # height
        #     # file_name # needed here?
        #     # import_status
        #     # id_lane_id
        #     # id_count_id
        #     # id_category_id
        # }

    def _parse_data_line_goldenriver(self, line):
        parsed_line = None
        try:
            parsed_line = dict()

            parsed_line['numbering'] = line[0:6]
            parsed_line['timestamp'] = datetime.strptime(
                "{}0000".format(line[7:24]), "%d%m%y %H%M %S %f").replace(
                    tzinfo=timezone.utc)
            parsed_line['reserve_code'] = line[25:31]
            parsed_line['lane'] = int(line[32:34])
            parsed_line['direction'] = int(line[35:36])
            parsed_line['distance_front_front'] = float(line[37:41])
            parsed_line['distance_front_back'] = float(line[42:46])
            parsed_line['speed'] = int(line[47:50])
            parsed_line['length'] = int(line[52:56])
            parsed_line['category'] = int(line[60:62].strip())
            parsed_line['height'] = line[63:65].strip()

            # If the speed of a vehicle is 0, we put it in the category 0
            if parsed_line['speed'] == 0:
                parsed_line['category'] = 0

            # If the speed of a vehicle is greater than 3*max_speed or 150km/h
            # TODO: get actual speed limit of the section
            if parsed_line['speed'] > 150:
                parsed_line['category'] = 0

        except ValueError:
            # This can happen when some values are missed from a line

            if 'lane' not in parsed_line:
                return None
            if 'direction' not in parsed_line:
                return None
            if 'distance_front_front' not in parsed_line:
                parsed_line['distance_front_front'] = 0
            if 'distance_front_back' not in parsed_line:
                parsed_line['distance_front_back'] = 0
            if 'speed' not in parsed_line:
                parsed_line['speed'] = -1
            if 'length' not in parsed_line:
                parsed_line['length'] = 0
            if 'category' not in parsed_line:
                parsed_line['category'] = 0
            if 'height ' not in parsed_line:
                parsed_line['height'] = 'NA'

        return parsed_line

    def _parse_data_line_metrocount(self, line):
        parsed_line = None
        try:
            parsed_line = dict()

            # self.numbering += 1
            # parsed_line['numbering'] = self.numbering
            parsed_line['timestamp'] = datetime.strptime(
                line[0:19], "%Y-%m-%d %H:%M:%S").replace(
                    tzinfo=timezone.utc)

            # On MetroCount files, the direction is 0-1 instead of 1-2
            parsed_line['lane'] = int(line[22:23]) + 1
            parsed_line['direction'] = int(line[22:23]) + 1
            parsed_line['distance_front_front'] = float(line[24:31])
            if parsed_line['distance_front_front'] > 99.9:
                parsed_line['distance_front_front'] = 99.9
            parsed_line['distance_front_back'] = float(line[31:38])
            if parsed_line['distance_front_back'] > 99.9:
                parsed_line['distance_front_back'] = 99.9
            parsed_line['speed'] = int(float(line[39:44]))
            parsed_line['length'] = int(float(line[44:50]))
            parsed_line['category'] = int(line[51:54].strip())
            parsed_line['height'] = ''
        except ValueError as e:
            # QgsMessageLog.logMessage(
            #     'ValueError: {}'.format(e),  'Comptages', Qgis.Info)

            # This can happen when some values are missed from a line
            return None

        return parsed_line

    def _file_format(self):
        """Return the file format."""
        with open(self.file_path, encoding=self.encoding) as f:
            for line in f:
                line = f.readline()
                if line.startswith("* FORMAT"):
                    return line.split("=", 1)[1].strip()
                elif line.startswith("MetroCount"):
                    return "MC"

        raise NotImplementedError()

    def _file_encoding(self):
        """Guess the right file encoding."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            try:
                for line in f:
                    pass
            except UnicodeDecodeError:
                return 'ISO-8859-1'
            else:
                return 'utf-8'

    def _first_record_date(self):
        """Get the date of the first record in the file as a timedate."""
        tz = pytz.timezone('Europe/Zurich')
        result = None

        if self.file_format == "INT-2" or self.file_format == "VBV-1":
            with open(self.file_path, encoding=self.encoding) as f:
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
        elif self.file_format == "MC":
            with open(self.file_path, encoding=self.encoding) as f:
                for line in f:
                    if line.startswith('20'):
                        result = datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S").replace(
                            tzinfo=tz)
                        return result

    def get_last_record_date(self):
        """Get the date of the last record in the file as a timedate.

        It scans until the end of the file looking for the last date.
        """
        tz = pytz.timezone('Europe/Zurich')
        result = None

        if self.file_format == "INT-2" or self.file_format == "VBV-1":
            with open(self.file_path, encoding=self.encoding) as f:
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
        elif self.file_format == "MC":
            with open(self.file_path, encoding=self.encoding) as f:
                for line in f:
                    if line.startswith('20'):
                        result = datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S").replace(
                            tzinfo=tz)
                return result

    def _file_lines(self):
        """Return the lines of a file.

        Store the result in a variable and avoid to call it multiple times
        because it will read all the file every time.
        """
        return sum(1 for line in open(
            self.file_path, "r", encoding=self.encoding))

    def _parse_file_header(self):
        if self.file_format == "INT-2" or self.file_format == "VBV-1":
            return self._parse_file_header_goldenriver()
        elif self.file_format == "MC":
            return self._parse_file_header_metrocount()

    def _parse_file_header_goldenriver(self):
        result = {}
        with open(self.file_path, encoding=self.encoding) as f:
            for line in f:
                if not line.startswith("* "):
                    break
                line = line[2:]
                splitted = line.split('=', 1)
                if len(splitted) > 1:
                    key = splitted[0].strip()
                    value = splitted[1].strip()
                    if key == 'CLASS' and value == 'SPECIAL10':
                        value = 'SWISS10'
                    result[key] = value
        return result

    def _parse_file_header_metrocount(self):
        result = {}
        with open(self.file_path, encoding=self.encoding) as f:
            for line in f:
                if line.startswith(""):
                    break

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
