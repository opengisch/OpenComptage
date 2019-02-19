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

        self._set_cv_h()
        self._set_cv_lv()
        self._set_cv_c()

        # FIXME: set vit_h or vit_hd depending if is aggregate
        self._set_vit_hd()
        self._set_swiss10_h()

        # Save the file
        output = os.path.join(current_dir, self.file_path)
        self.wb.save(filename=output)

    def _set_cv_h(self):
        ws = self.wb['CV_H']

        ws['A1'] = ('Poste de comptage : {}  Axe : {}:{}:  '
                    'PR {} + {} m à PR {} + {} m').format(
                        self.section_id,
                        self.count_data.attributes['owner'],
                        self.count_data.attributes['road'],
                        self.count_data.attributes['start_pr'],
                        self.count_data.attributes['start_dist'],
                        self.count_data.attributes['end_pr'],
                        self.count_data.attributes['end_dist'])

        ws['A2'] = 'Periode de comptage du {}/{}/{} au {}/{}/{}'.format(
            self.count_data.attributes['dates'][0][2],
            self.count_data.attributes['dates'][0][1],
            self.count_data.attributes['dates'][0][0],
            self.count_data.attributes['dates'][6][2],
            self.count_data.attributes['dates'][6][1],
            self.count_data.attributes['dates'][6][0],)

        ws['G2'] = 'Comptage {}'.format(
            self.count_data.attributes['dates'][0][0])

        ws['K2'] = 'Type de capteur : {}'.format(
            self.count_data.attributes['sensor_type'])
        ws['K3'] = 'Modèle : {}'.format(
            self.count_data.attributes['model'])
        ws['K4'] = 'Classification : {}'.format(
            self.count_data.attributes['class'])

        ws['K5'] = 'Comptage véhicule par véhicule'
        if self.count_data.attributes['aggregate']:
            ws['K5'] = 'Comptage par interval'

        ws['A5'] = 'Periode speciales : {}'.format(
            self.layers.check_dates(
                QDate(
                    self.count_data.attributes['dates'][0][0],
                    self.count_data.attributes['dates'][0][1],
                    self.count_data.attributes['dates'][0][2]),
                QDate(
                    self.count_data.attributes['dates'][6][0],
                    self.count_data.attributes['dates'][0][1],
                    self.count_data.attributes['dates'][0][2])))

        ws['F6'] = self.count_data.attributes['place_name']

        ws['B22'] = 'Remarque : {}'.format(
            self.count_data.attributes['remarks']
            if type(self.count_data.attributes['remarks']) == str else '')

        mo_fr = self.count_data.day_data[0:5]
        sa_su = self.count_data.day_data[5:7]

        for i, day_data in enumerate(mo_fr):
            ws['C{}'.format(i+11)] = day_data.total()
            ws['D{}'.format(i+11)] = day_data.total(0)
            ws['E{}'.format(i+11)] = day_data.total(1)
            ws['F{}'.format(i+11)] = day_data.light_vehicles(0)
            ws['G{}'.format(i+11)] = day_data.light_vehicles(1)
            ws['H{}'.format(i+11)] = day_data.heavy_vehicles(0)
            ws['I{}'.format(i+11)] = day_data.heavy_vehicles(1)
            ws['J{}'.format(i+11)] = day_data.percent_heavy_vehicles(0)
            ws['K{}'.format(i+11)] = day_data.percent_heavy_vehicles(1)
            ws['E{}'.format(i+28)] = '{}%'.format(day_data.monthly_coefficient)

        for i, day_data in enumerate(sa_su):
            ws['C{}'.format(i+17)] = day_data.total()
            ws['D{}'.format(i+17)] = day_data.total(0)
            ws['E{}'.format(i+17)] = day_data.total(1)
            ws['F{}'.format(i+17)] = day_data.light_vehicles(0)
            ws['G{}'.format(i+17)] = day_data.light_vehicles(1)
            ws['H{}'.format(i+17)] = day_data.heavy_vehicles(0)
            ws['I{}'.format(i+17)] = day_data.heavy_vehicles(1)
            ws['J{}'.format(i+17)] = day_data.percent_heavy_vehicles(0)
            ws['K{}'.format(i+17)] = day_data.percent_heavy_vehicles(1)
            ws['E{}'.format(i+34)] = '{}%'.format(day_data.monthly_coefficient)

        ws['C20'] = self.count_data.average_total(days=[0, 1, 2, 3, 4])
        ws['D20'] = self.count_data.average_total(0, days=[0, 1, 2, 3, 4])
        ws['E20'] = self.count_data.average_total(1, days=[0, 1, 2, 3, 4])
        ws['F20'] = self.count_data.average_light_vehicles(0, days=[0, 1, 2, 3, 4])
        ws['G20'] = self.count_data.average_light_vehicles(1, days=[0, 1, 2, 3, 4])
        ws['H20'] = self.count_data.average_heavy_vehicles(0, days=[0, 1, 2, 3, 4])
        ws['I20'] = self.count_data.average_heavy_vehicles(1, days=[0, 1, 2, 3, 4])
        ws['J20'] = self.count_data.average_percent_heavy_vehicles(0, days=[0, 1, 2, 3, 4])
        ws['K20'] = self.count_data.average_percent_heavy_vehicles(1, days=[0, 1, 2, 3, 4])

        ws['C21'] = self.count_data.average_total(days=[5, 6])
        ws['D21'] = self.count_data.average_total(0, days=[5, 6])
        ws['E21'] = self.count_data.average_total(1, days=[5, 6])
        ws['F21'] = self.count_data.average_light_vehicles(0, days=[5, 6])
        ws['G21'] = self.count_data.average_light_vehicles(1, days=[5, 6])
        ws['H21'] = self.count_data.average_heavy_vehicles(0, days=[5, 6])
        ws['I21'] = self.count_data.average_heavy_vehicles(1, days=[5, 6])
        ws['J21'] = self.count_data.average_percent_heavy_vehicles(0, days=[5, 6])
        ws['K21'] = self.count_data.average_percent_heavy_vehicles(1, days=[5, 6])

    def _set_cv_c(self):
        ws = self.wb['CV_C']

        ws['A1'] = ('Poste de comptage : {}  Axe : {}:{}:  '
                    'PR {} + {} m à PR {} + {} m').format(
                        self.section_id,
                        self.count_data.attributes['owner'],
                        self.count_data.attributes['road'],
                        self.count_data.attributes['start_pr'],
                        self.count_data.attributes['start_dist'],
                        self.count_data.attributes['end_pr'],
                        self.count_data.attributes['end_dist'])

        ws['A2'] = 'Periode de comptage du {}/{}/{} au {}/{}/{}'.format(
            self.count_data.attributes['dates'][0][2],
            self.count_data.attributes['dates'][0][1],
            self.count_data.attributes['dates'][0][0],
            self.count_data.attributes['dates'][6][2],
            self.count_data.attributes['dates'][6][1],
            self.count_data.attributes['dates'][6][0],)

        ws['P2'] = 'Comptage {}'.format(
            self.count_data.attributes['dates'][0][0])

        ws['AE2'] = 'Type de capteur : {}'.format(
            self.count_data.attributes['sensor_type'])
        ws['AE3'] = 'Modèle : {}'.format(
            self.count_data.attributes['model'])
        ws['AE4'] = 'Classification : {}'.format(
            self.count_data.attributes['class'])

        ws['AE5'] = 'Comptage véhicule par véhicule'
        if self.count_data.attributes['aggregate']:
            ws['AE5'] = 'Comptage par interval'

        ws['A5'] = 'Periode speciales : {}'.format(
            self.layers.check_dates(
                QDate(
                    self.count_data.attributes['dates'][0][0],
                    self.count_data.attributes['dates'][0][1],
                    self.count_data.attributes['dates'][0][2]),
                QDate(
                    self.count_data.attributes['dates'][6][0],
                    self.count_data.attributes['dates'][0][1],
                    self.count_data.attributes['dates'][0][2])))

        ws['P6'] = self.count_data.attributes['place_name']

        ws['B9'] = 'Remarque : {}'.format(
            self.count_data.attributes['remarks']
            if type(self.count_data.attributes['remarks']) == str else '')

        days = self.count_data.day_data[0:7]

        day_cols_tot = ['C', 'D', 'E', 'F', 'G', 'H', 'I']
        day_cols_d1 = ['M', 'N', 'O', 'P', 'Q', 'R', 'S']
        day_cols_d2 = ['W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC']
        for i, day_data in enumerate(days):
            for j in range(24):
                ws['{}{}'.format(day_cols_tot[i], j+14)] = day_data.hour_data[j].total()
                ws['{}{}'.format(day_cols_d1[i], j+14)] = day_data.hour_data[j].total(0)
                ws['{}{}'.format(day_cols_d2[i], j+14)] = day_data.hour_data[j].total(1)

    def _set_vit_hd(self):
        ws = self.wb['Vit_Hd']

        speed_cols = ['B', 'C', 'D', 'E', 'F', 'G', 'H',
                      'I', 'J', 'K', 'L', 'M', 'N']

        dir1 = self.count_data.speed_cumulus(0, days=[0, 1, 2, 3, 4, 5, 6])
        dir2 = self.count_data.speed_cumulus(1, days=[0, 1, 2, 3, 4, 5, 6])

        for i, hour in enumerate(dir1):
            for j, speed in enumerate(hour):
                ws['{}{}'.format(speed_cols[j], i+14)] = speed

        for i, hour in enumerate(dir2):
            for j, speed in enumerate(hour):
                ws['{}{}'.format(speed_cols[j], i+50)] = speed

    def _set_swiss10_h(self):
        ws = self.wb['SWISS10_H']

        ws['A1'] = ('Poste de comptage : {}  Axe : {}:{}:  '
                    'PR {} + {} m à PR {} + {} m').format(
                        self.section_id,
                        self.count_data.attributes['owner'],
                        self.count_data.attributes['road'],
                        self.count_data.attributes['start_pr'],
                        self.count_data.attributes['start_dist'],
                        self.count_data.attributes['end_pr'],
                        self.count_data.attributes['end_dist'])

        ws['A2'] = 'Periode de comptage du {}/{}/{} au {}/{}/{}'.format(
            self.count_data.attributes['dates'][0][2],
            self.count_data.attributes['dates'][0][1],
            self.count_data.attributes['dates'][0][0],
            self.count_data.attributes['dates'][6][2],
            self.count_data.attributes['dates'][6][1],
            self.count_data.attributes['dates'][6][0],)

        ws['A6'] = self.count_data.attributes['place_name']

        cat_cols = ['B', 'C', 'D', 'E', 'F', 'G', 'H',
                    'I', 'J', 'K']

        dir1 = self.count_data.category_cumulus(0, days=[0, 1, 2, 3, 4, 5, 6])
        dir2 = self.count_data.category_cumulus(1, days=[0, 1, 2, 3, 4, 5, 6])

        for i, hour in enumerate(dir1):
            for j, cat in enumerate(hour):
                ws['{}{}'.format(cat_cols[j], i+12)] = cat

        for i, hour in enumerate(dir2):
            for j, cat in enumerate(hour):
                ws['{}{}'.format(cat_cols[j], i+45)] = cat

        for i, col in enumerate(cat_cols):
            ws['{}37'.format(col)] = \
                '=SUM({0}12:{0}35)/{1}'.format(
                    col, self.count_data.total(0, [0, 1, 2, 3, 4, 5, 6]))
            ws['{}38'.format(col)] = \
                '=SUM({0}18:{0}33)/{1}'.format(
                    col, self.count_data.total(0, [0, 1, 2, 3, 4, 5, 6]))
            ws['{}70'.format(col)] = \
                '=SUM({0}45:{0}68)/{1}'.format(
                    col, self.count_data.total(0, [0, 1, 2, 3, 4, 5, 6]))
            ws['{}71'.format(col)] = \
                '=SUM({0}51:{0}66)/{1}'.format(
                    col, self.count_data.total(0, [0, 1, 2, 3, 4, 5, 6]))

        for i in range(24):
            ws['N{}'.format(i+12)] = '=M{}/{}*7'.format(
                i+12, self.count_data.total(0, [0, 1, 2, 3, 4, 5, 6]))

        for i in range(24):
            ws['N{}'.format(i+45)] = '=M{}/{}*7'.format(
                i+45, self.count_data.total(1, [0, 1, 2, 3, 4, 5, 6]))

    def _set_cv_lv(self):
        ws = self.wb['CV_LV']

        ws['A1'] = ('Poste de comptage : {}  Axe : {}:{}:  '
                    'PR {} + {} m à PR {} + {} m').format(
                        self.section_id,
                        self.count_data.attributes['owner'],
                        self.count_data.attributes['road'],
                        self.count_data.attributes['start_pr'],
                        self.count_data.attributes['start_dist'],
                        self.count_data.attributes['end_pr'],
                        self.count_data.attributes['end_dist'])

        ws['A2'] = 'Periode de comptage du {}/{}/{} au {}/{}/{}'.format(
            self.count_data.attributes['dates'][0][2],
            self.count_data.attributes['dates'][0][1],
            self.count_data.attributes['dates'][0][0],
            self.count_data.attributes['dates'][6][2],
            self.count_data.attributes['dates'][6][1],
            self.count_data.attributes['dates'][6][0],)

        ws['G2'] = 'Comptage {}'.format(
            self.count_data.attributes['dates'][0][0])

        ws['K2'] = 'Type de capteur : {}'.format(
            self.count_data.attributes['sensor_type'])
        ws['K3'] = 'Modèle : {}'.format(
            self.count_data.attributes['model'])
        ws['K4'] = 'Classification : {}'.format(
            self.count_data.attributes['class'])

        ws['K5'] = 'Comptage véhicule par véhicule'
        if self.count_data.attributes['aggregate']:
            ws['K5'] = 'Comptage par interval'

        ws['A5'] = 'Periode speciales : {}'.format(
            self.layers.check_dates(
                QDate(
                    self.count_data.attributes['dates'][0][0],
                    self.count_data.attributes['dates'][0][1],
                    self.count_data.attributes['dates'][0][2]),
                QDate(
                    self.count_data.attributes['dates'][6][0],
                    self.count_data.attributes['dates'][0][1],
                    self.count_data.attributes['dates'][0][2])))

        ws['F6'] = self.count_data.attributes['place_name']
