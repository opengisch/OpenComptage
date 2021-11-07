import os

from datetime import datetime

from qgis.core import QgsTask, Qgis, QgsMessageLog
from qgis.PyQt.QtSql import QSqlQuery

from comptages.datamodel import models


class DataImporter(QgsTask):

    def __init__(self, file_path, count_id):
        self.basename = os.path.basename(file_path)
        super().__init__(
            'Importation fichier {}'.format(self.basename))
        self.file_path = file_path
        self.count_id = count_id
        self.file_header = self.parse_file_header(self.file_path)
        self.lanes = dict()
        self.populate_lane_dict()
        self.categories = dict()
        self.populate_category_dict()
        self.data_header = self.parse_data_header()
        self.exception = None

    def run(self):
        """To be implemented in the subclasses"""
        pass

    def finished(self, result):
        if result:
            QgsMessageLog.logMessage(
                '{} - Import file {} ended'.format(
                    datetime.now(), self.basename),
                'Comptages', Qgis.Info)

        else:
            QgsMessageLog.logMessage(
                '{} - Import file {} ended with errors: {}'.format(
                    datetime.now(), self.basename, self.exception),
                'Comptages', Qgis.Info)


    def cancel(self):
        # TODO: Cancel needed?
        pass

    def get_number_of_lines(self):
        return sum(1 for line in open(self.file_path))

    def populate_lane_dict(self):
        # e.g. self.lanes = {1: 435, 2: 436}

        count = models.Count.objects.get(id=self.count_id)
        lanes = models.Lane.objects.filter(
            id_installation__count=count,
        ).order_by("number")

        self.lanes = {x.number: x.id for x in lanes}

    def populate_category_dict(self):
        if 'CLASS' not in self.file_header:
            return
        class_name = self.file_header['CLASS']

        # Use customized SWISS7 class for Marksmann devices
        # because they manage this class in a wrong way
        if self.file_header['FORMAT'] in ['INT-2', 'VBV-1'] and class_name == 'SWISS7':
            class_name = 'SWISS7-MM'

        # e.g. self.categories = {0: 922, 1: 22, 2: 23, 3: 24, 4: 25, 5: 26, 6: 27, 7: 28, 8: 29, 9: 30, 10: 31}
        categories = models.Category.objects.filter(
            classcategory__id_class__name=class_name
        ).order_by('code')

        self.categories = {x.code: x.id for x in categories}

    @staticmethod
    def parse_file_header(file_path):
        file_header = dict()

        # Guess the right file encoding
        f = open(file_path, 'r', encoding='utf8')
        while True:
            try:
                line = f.readline()
            except UnicodeDecodeError:
                f.close()
                encoding = 'ISO-8859-1'
                break
            if not line:
                f.close()
                encoding = 'utf8'
                break

        with open(file_path, encoding=encoding) as f:
            for line in f:
                # Marksmann
                if line.startswith('* ') and not line.startswith('* HEAD '):
                    line = line[2:]
                    splitted = line.split('=', 1)
                    if len(splitted) > 1:
                        key = splitted[0].strip()
                        value = splitted[1].strip()
                        if key == 'CLASS' and value == 'SPECIAL10':
                            value = 'SWISS10'
                        file_header[key] = value
                # MetroCount
                elif line.startswith('MetroCount'):
                    file_header['FORMAT'] = 'MC'
                elif line.startswith('Place'):
                    file_header['SITE'] = line[
                        line.find('[') + 1:line.find(']')].replace('-', '')
                elif line.startswith('20') and file_header['FORMAT'] == 'MC' and 'STARTREC' not in file_header:
                    file_header['STARTREC'] = datetime.strftime(
                        datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S"),
                        "%H:%M %d/%m/%y")
                elif line.startswith('20') and file_header['FORMAT'] == 'MC':
                    file_header['STOPREC'] = datetime.strftime(
                        datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S"),
                        "%H:%M %d/%m/%y")
                elif line.startswith('Type de Cat') and file_header['FORMAT'] == 'MC':
                    file_header['CLASS'] = line[line.find('(') + 1:line.find(')')]
                    if file_header['CLASS'] == 'Euro13':
                        file_header['CLASS'] = 'EUR13'
                    elif file_header['CLASS'] == 'NZTA2011':
                        file_header['CLASS'] = 'NZ13'
                    elif file_header['CLASS'][:5] == 'FHWA ':
                        file_header['CLASS'] = 'FHWA13'
                    elif file_header['CLASS'] == 'CAT-Cycle_dist-empat':
                        file_header['CLASS'] = 'SPCH-MD 5C'
        return file_header

    def parse_data_header(self):
        data_header = []

        # Guess the right file encoding
        f = open(self.file_path, 'r', encoding='utf8')
        while True:
            try:
                line = f.readline()
            except UnicodeDecodeError:
                f.close()
                encoding = 'ISO-8859-1'
                break
            if not line:
                f.close()
                encoding = 'utf8'
                break

        with open(self.file_path, encoding=encoding) as f:
            for line in f:
                if line.startswith('* HEAD '):
                    start_char = 20
                    i = 0
                    while True:
                        if line[start_char:start_char+4] != '':
                            i += 1
                            start_char += 5
                        else:
                            data_header.append(i)
                            break
        return data_header
