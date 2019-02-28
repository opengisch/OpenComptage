import os
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
        # TODO: Evaluate if more than a report file are to be created i.e. more
        # weeks or special cases

        # FIXME: section_id
        self.section_id = '01743230'
        print(self.count_id)
        print(self.section_id)
        data_loader = DataLoader(
            self.count_id, self.section_id, Layers.IMPORT_STATUS_DEFINITIVE)

        self.count_data = data_loader.load()
        self._export_report()

    def _export_report(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template = os.path.join(current_dir, 'template.xlsx')
        self.wb = load_workbook(filename=template)

        self._set_data_count()
        self._set_data_day()
        self._set_data_speed()
        self._set_data_category()

        # Save the file
        output = os.path.join(current_dir, self.file_path)
        self.wb.save(filename=output)

    def _set_data_count(self):
        ws = self.wb['Data_count']

        ws['B3'] = ('Poste de comptage : {}  Axe : {}:{}:  '
                    'PR {} + {} m à PR {} + {} m').format(
                        self.section_id,
                        self.count_data.attributes['owner'],
                        self.count_data.attributes['road'],
                        self.count_data.attributes['start_pr'],
                        self.count_data.attributes['start_dist'],
                        self.count_data.attributes['end_pr'],
                        self.count_data.attributes['end_dist'])

        ws['B4'] = 'Periode de comptage du {}/{}/{} au {}/{}/{}'.format(
            self.count_data.attributes['dates'][0][2],
            self.count_data.attributes['dates'][0][1],
            self.count_data.attributes['dates'][0][0],
            self.count_data.attributes['dates'][6][2],
            self.count_data.attributes['dates'][6][1],
            self.count_data.attributes['dates'][6][0],)

        ws['B5'] = 'Comptage {}'.format(
            self.count_data.attributes['dates'][0][0])

        ws['B6'] = 'Type de capteur : {}'.format(
            self.count_data.attributes['sensor_type'])
        ws['B7'] = 'Modèle : {}'.format(
            self.count_data.attributes['model'])
        ws['B8'] = 'Classification : {}'.format(
            self.count_data.attributes['class'])

        ws['B9'] = 'Comptage véhicule par véhicule'
        if self.count_data.attributes['aggregate']:
            ws['K5'] = 'Comptage par interval'

        ws['B10'] = 'Periode speciales : {}'.format(
            self.layers.check_dates(
                QDate(
                    self.count_data.attributes['dates'][0][0],
                    self.count_data.attributes['dates'][0][1],
                    self.count_data.attributes['dates'][0][2]),
                QDate(
                    self.count_data.attributes['dates'][6][0],
                    self.count_data.attributes['dates'][0][1],
                    self.count_data.attributes['dates'][0][2])))

        ws['B11'] = self.count_data.attributes['place_name']

        ws['B12'] = 'Remarque : {}'.format(
            self.count_data.attributes['remarks']
            if type(self.count_data.attributes['remarks']) == str else '')

        ws['B13'] = self.count_data.attributes['dir1']
        ws['B14'] = self.count_data.attributes['dir2']

    def _set_data_day(self):
        ws = self.wb['Data_day']

        days = self.count_data.day_data[0:7]

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

    def _set_data_speed(self):
        ws = self.wb['Data_speed']

        speed_cols = ['B', 'C', 'D', 'E', 'F', 'G', 'H',
                      'I', 'J', 'K', 'L', 'M', 'N']
        dir1_start_cell = 5
        dir2_start_cell = 33

        dir1 = self.count_data.speed_cumulus(0, days=[0, 1, 2, 3, 4, 5, 6])
        dir2 = self.count_data.speed_cumulus(1, days=[0, 1, 2, 3, 4, 5, 6])

        for i, hour in enumerate(dir1):
            for j, speed in enumerate(hour):
                ws['{}{}'.format(speed_cols[j], i+dir1_start_cell)] = speed

        for i, hour in enumerate(dir2):
            for j, speed in enumerate(hour):
                ws['{}{}'.format(speed_cols[j], i+dir2_start_cell)] = speed

    def _set_data_category(self):
        ws = self.wb['Data_category']

        cat_cols = ['B', 'C', 'D', 'E', 'F', 'G', 'H',
                    'I', 'J', 'K']

        dir1_start_cell = 5
        dir2_start_cell = 33

        dir1 = self.count_data.category_cumulus(0, days=[0, 1, 2, 3, 4, 5, 6])
        dir2 = self.count_data.category_cumulus(1, days=[0, 1, 2, 3, 4, 5, 6])

        for i, hour in enumerate(dir1):
            for j, cat in enumerate(hour):
                ws['{}{}'.format(cat_cols[j], i+dir1_start_cell)] = cat

        for i, hour in enumerate(dir2):
            for j, cat in enumerate(hour):
                ws['{}{}'.format(cat_cols[j], i+dir2_start_cell)] = cat
