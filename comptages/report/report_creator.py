import os
import datetime
from openpyxl import load_workbook
from qgis.PyQt.QtCore import QDate
from comptages.core.settings import Settings
from comptages.data.data_loader import DataLoader
from comptages.core.layers import Layers


class ReportCreator():
    def __init__(self, count_id, file_path, layers):
        self.count_id = count_id
        self.file_path = file_path
        self.settings = Settings()
        self.layers = layers

    def run(self):
        # TODO: Evaluate special cases

        # FIXME: section_id
        self.section_id = '01743230'

        data_loader = DataLoader(
            self.count_id, self.section_id, Layers.IMPORT_STATUS_DEFINITIVE)

        count_data = data_loader.load()

        for i in range(int(len(count_data.day_data)/7)):
            self._export_report(count_data, i*7, i*7+6)

    def _export_report(self, count_data, start_day, end_day):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template = os.path.join(current_dir, 'template.xlsx')
        wb = load_workbook(filename=template)

        self._set_data_count(wb, count_data, start_day, end_day)
        self._set_data_day(wb, count_data, start_day, end_day)
        self._set_data_speed(wb, count_data, start_day, end_day)
        self._set_data_category(wb, count_data, start_day, end_day)

        # Save the file
        week_num = datetime.date(
            count_data.attributes['dates'][start_day][0],
            count_data.attributes['dates'][start_day][1],
            count_data.attributes['dates'][start_day][2]).strftime('%V')
        output = '{}_S{}.xlsx'.format(self.file_path[0:-5], week_num)
        wb.save(filename=output)

    def _set_data_count(self, workbook, count_data, start_day, end_day):
        ws = workbook['Data_count']

        ws['B3'] = ('Poste de comptage : {}  Axe : {}:{}:  '
                    'PR {} + {} m à PR {} + {} m').format(
                        self.section_id,
                        count_data.attributes['owner'],
                        count_data.attributes['road'],
                        count_data.attributes['start_pr'],
                        count_data.attributes['start_dist'],
                        count_data.attributes['end_pr'],
                        count_data.attributes['end_dist'])

        ws['B4'] = 'Periode de comptage du {}/{}/{} au {}/{}/{}'.format(
            count_data.attributes['dates'][start_day][2],
            count_data.attributes['dates'][start_day][1],
            count_data.attributes['dates'][start_day][0],
            count_data.attributes['dates'][end_day][2],
            count_data.attributes['dates'][end_day][1],
            count_data.attributes['dates'][end_day][0],)

        ws['B5'] = 'Comptage {}'.format(
            count_data.attributes['dates'][start_day][0])

        ws['B6'] = 'Type de capteur : {}'.format(
            count_data.attributes['sensor_type'])
        ws['B7'] = 'Modèle : {}'.format(
            count_data.attributes['model'])
        ws['B8'] = 'Classification : {}'.format(
            count_data.attributes['class'])

        ws['B9'] = 'Comptage véhicule par véhicule'
        if count_data.attributes['aggregate']:
            ws['K5'] = 'Comptage par interval'

        ws['B10'] = 'Periode speciales : {}'.format(
            self.layers.check_dates(
                QDate(
                    count_data.attributes['dates'][start_day][0],
                    count_data.attributes['dates'][start_day][1],
                    count_data.attributes['dates'][start_day][2]),
                QDate(
                    count_data.attributes['dates'][end_day][0],
                    count_data.attributes['dates'][end_day][1],
                    count_data.attributes['dates'][end_day][2])))

        ws['B11'] = count_data.attributes['place_name']

        ws['B12'] = 'Remarque : {}'.format(
            count_data.attributes['remarks']
            if type(count_data.attributes['remarks']) == str else '')

        ws['B13'] = count_data.attributes['dir1']
        ws['B14'] = count_data.attributes['dir2']

    def _set_data_day(self, workbook, count_data, start_day, end_day):
        ws = workbook['Data_day']
        days = count_data.day_data[start_day:end_day+1]

        day_cols_tot = ['B', 'C', 'D', 'E', 'F', 'G', 'H']
        section_start_cell = 5
        coefficient_cell = 31
        dir1_start_cell = 35
        dir1_light_cell = 61
        dir1_heavy_cell = 62
        dir2_start_cell = 66
        dir2_light_cell = 92
        dir2_heavy_cell = 93
        for i, day_data in enumerate(days):
            for j in range(24):
                ws['{}{}'.format(day_cols_tot[i], j+section_start_cell)] = \
                    day_data.hour_data[j].total()
                ws['{}{}'.format(day_cols_tot[i], j+dir1_start_cell)] = \
                    day_data.hour_data[j].total(0)
                ws['{}{}'.format(day_cols_tot[i], j+dir2_start_cell)] = \
                    day_data.hour_data[j].total(1)

            ws['{}{}'.format(day_cols_tot[i], coefficient_cell)] = \
                '{}%'.format(day_data.monthly_coefficient)
            ws['{}{}'.format(day_cols_tot[i], dir1_light_cell)] = \
                day_data.light_vehicles(0)
            ws['{}{}'.format(day_cols_tot[i], dir2_light_cell)] = \
                day_data.light_vehicles(1)
            ws['{}{}'.format(day_cols_tot[i], dir1_heavy_cell)] = \
                day_data.heavy_vehicles(0)
            ws['{}{}'.format(day_cols_tot[i], dir2_heavy_cell)] = \
                day_data.heavy_vehicles(1)

    def _set_data_speed(self, workbook, count_data, start_day, end_day):
        ws = workbook['Data_speed']

        speed_cols = ['B', 'C', 'D', 'E', 'F', 'G', 'H',
                      'I', 'J', 'K', 'L', 'M', 'N']
        dir1_start_cell = 5
        dir2_start_cell = 33

        days_idx = [x for x in range(start_day, end_day+1)]
        dir1 = count_data.speed_cumulus(0, days=days_idx)
        dir2 = count_data.speed_cumulus(1, days=days_idx)

        for i, hour in enumerate(dir1):
            for j, speed in enumerate(hour):
                ws['{}{}'.format(speed_cols[j], i+dir1_start_cell)] = speed

        for i, hour in enumerate(dir2):
            for j, speed in enumerate(hour):
                ws['{}{}'.format(speed_cols[j], i+dir2_start_cell)] = speed

    def _set_data_category(self, workbook, count_data, start_day, end_day):
        ws = workbook['Data_category']

        cat_cols = ['B', 'C', 'D', 'E', 'F', 'G', 'H',
                    'I', 'J', 'K']

        dir1_start_cell = 5
        dir2_start_cell = 33

        days_idx = [x for x in range(start_day, end_day+1)]
        dir1 = count_data.category_cumulus(0, days=days_idx)
        dir2 = count_data.category_cumulus(1, days=days_idx)

        for i, hour in enumerate(dir1):
            for j, cat in enumerate(hour):
                ws['{}{}'.format(cat_cols[j], i+dir1_start_cell)] = cat

        for i, hour in enumerate(dir2):
            for j, cat in enumerate(hour):
                ws['{}{}'.format(cat_cols[j], i+dir2_start_cell)] = cat
