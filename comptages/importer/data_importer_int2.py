from datetime import datetime, timedelta

from qgis.PyQt.QtSql import QSqlQuery

from comptages.core.layers import Layers
from comptages.importer.data_importer import DataImporter


class DataImporterInt2(DataImporter):
    def __init__(self, file_path, count_id):
        super().__init__(file_path, count_id)
        self.intspec = self.get_intspec()
        self.number_of_lines = self.get_number_of_lines()

    def run(self):
        try:
            with open(self.file_path) as f:
                number_of_lines = sum(1 for _ in f)
                with open(self.file_path) as f:
                    for i, line in enumerate(f):
                        progress = int(100 / number_of_lines * i)
                        self.setProgress(progress)

                        if not line.startswith('* '):
                            self.write_row_into_db(line)
        except Exception as e:
            self.exception = e
            return False
        return True

    def get_intspec(self):
        self.file_header = self.parse_file_header(self.file_path)
        intspec = []
        for i, code in enumerate(self.file_header['INTSPEC'].split('+')):
            if code.strip() not in ['SPD', 'SDS', 'LEN', 'CLS', 'CNT', 'DRN']:
                raise NotImplementedError('{}'.format(code.strip()))
            # the key corrpespond to the value in the data row
            intspec.append(code.strip())
        return intspec

    def get_bins(self, code):
        """Returns an array with the bins if they exist, or the number of
        columns of this data type"""
        values = []
        if code == 'SPD' or code == 'SDS':
            values = self.file_header['SPDBINS'].split()
        elif code == 'LEN':
            values = self.file_header['LENBINS'].split()
        elif code == 'CLS':
            values = list(self.categories.values())
        else:
            values = self.data_header[self.intspec.index(code)]
        return values

    def parse_data_line(self, line):
        parsed_line = dict()

        # In the data files midnight is 2400 of the current day
        # instead of 0000 of the next day
        if line[7:9] == '24':
            line = line[:7] + '00' + line[9:]
            start = datetime.strptime(
                "{}".format(line[0:11]), "%d%m%y %H%M")
            start += timedelta(days=1)
        else:
            start = datetime.strptime(
                "{}".format(line[0:11]), "%d%m%y %H%M")

        parsed_line['start'] = start
        parsed_line['end'] = parsed_line['start'] + timedelta(
            minutes=int(self.file_header['INTERVAL']))
        parsed_line['channel'] = line[12:13]
        parsed_line['reserve_code'] = line[14:16]
        parsed_line['info_code'] = line[17:19]

        start_char = 20
        i = 1
        while True:
            if line[start_char:start_char+4] != '':
                parsed_line['data_{}'.format(i)] = \
                    line[start_char:start_char+4]
                i += 1
                start_char += 5
            else:
                break

        return parsed_line

    def write_row_into_db(self, line):
        row = self.parse_data_line(line)

        row_type = self.intspec[int(row['info_code'])-1]

        query = QSqlQuery(self.db)

        query_str = ("insert into comptages.count_aggregate ("
                     "type, \"start\", \"end\", file_name, import_status, "
                     "id_count, id_lane) "
                     "values ("
                     "'{}', '{}', '{}', '{}', {}, {}, {})".format(
                         row_type,
                         row['start'],
                         row['end'],
                         self.basename,
                         Layers.IMPORT_STATUS_QUARANTINE,
                         self.count_id,
                         self.lanes[int(row['channel'])]))

        query.exec_(query_str)

        bins = self.get_bins(row_type)
        query_str_value = ""
        if row_type == 'SPD':
            query_str_value = self._create_query_str_aggregate_spd(
                row, bins)
        elif row_type == 'LEN':
            query_str_value = self._create_query_str_aggregate_len(
                row, bins)
        elif row_type == 'CLS':
            query_str_value = self._create_query_str_aggregate_cls(
                row, bins)
        elif row_type == 'SDS':
            # Insert the values in the SPD table and only the
            # mean and the deviation in the SDS table
            query_str_value = self._create_query_str_aggregate_spd(
                row, bins)
            query_str_value.append(self._create_query_str_aggregate_sds(
                row, bins))
        elif row_type == 'DRN':
            query_str_value = self._create_query_str_aggregate_drn(
                row, bins)
        elif row_type == 'CNT':
            query_str_value = self._create_query_str_aggregate_cnt(
                row, bins)

        for _ in query_str_value:
            query.exec_(_)

    def _create_query_str_aggregate_spd(self, row, spdbins):
        queries = []
        for i in range(1, len(spdbins)):
            data = row['data_{}'.format(i)]
            if not data == '':
                speed_low = spdbins[i-1]
                speed_high = spdbins[i]
                queries.append(
                    ("insert into comptages.count_aggregate_value_spd ("
                     "value, low, high, "
                     "id_count_aggregate) values ("
                     "{}, {}, {}, "
                     "(select currval('comptages.count_aggregate_id_seq'))"
                     ")".format(
                         data,
                         speed_low,
                         speed_high)))
        return queries

    def _create_query_str_aggregate_sds(self, row, spdbins):
        query = ''
        speed_data_cols = len(spdbins) - 1
        mean = int(row['data_{}'.format(speed_data_cols + 1)]) / 10
        deviation = int(row['data_{}'.format(speed_data_cols + 2)]) / 10
        query = ("insert into comptages.count_aggregate_value_sds ("
                 "mean, deviation, "
                 "id_count_aggregate) values ("
                 "{}, {}, "
                 "(select currval('comptages.count_aggregate_id_seq'))"
                 ")".format(
                     mean,
                     deviation))
        return query

    def _create_query_str_aggregate_len(self, row, lenbins):
        queries = []

        for i in range(1, len(lenbins)):
            data = row['data_{}'.format(i)]
            if not data == '':
                length_low = lenbins[i-1]
                length_high = lenbins[i]
                queries.append(
                    ("insert into comptages.count_aggregate_value_len ("
                     "value, low, high, "
                     "id_count_aggregate) values ("
                     "{}, {}, {}, "
                     "(select currval('comptages.count_aggregate_id_seq'))"
                     ")".format(
                         data,
                         length_low,
                         length_high)))

        return queries

    def _create_query_str_aggregate_cls(self, row, catbins):
        queries = []

        for i in range(1, len(catbins)+1):
            data = row['data_{}'.format(i)]
            if not data == '':
                category = catbins[i-1]
                queries.append(
                    ("insert into comptages.count_aggregate_value_cls ("
                     "value, id_category, "
                     "id_count_aggregate) values ("
                     "{}, {}, "
                     "(select currval('comptages.count_aggregate_id_seq'))"
                     ")".format(
                         data,
                         category)))
        return queries

    def _create_query_str_aggregate_drn(self, row, dirbins):
        queries = []
        for i in range(1, dirbins+1):
            data = row['data_{}'.format(i)]
            if not data == '':
                direction = i
                queries.append(
                    ("insert into comptages.count_aggregate_value_drn ("
                     "value, direction, "
                     "id_count_aggregate) values ("
                     "{}, {}, "
                     "(select currval('comptages.count_aggregate_id_seq'))"
                     ")".format(
                         data,
                         direction)))
        return queries

    def _create_query_str_aggregate_cnt(self, row, countbins):
        queries = []
        for i in range(1, countbins+1):
            data = row['data_{}'.format(i)]
            if not data == '':
                countbin = i
                queries.append(
                    ("insert into comptages.count_aggregate_value_cnt ("
                     "value, interval, "
                     "id_count_aggregate) values ("
                     "{}, {}, "
                     "(select currval('comptages.count_aggregate_id_seq'))"
                     ")".format(
                         data,
                         countbin)))
        return queries
