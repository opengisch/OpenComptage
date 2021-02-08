import os

from datetime import datetime

from qgis.core import QgsTask, Qgis, QgsMessageLog
from qgis.PyQt.QtSql import QSqlQuery

from comptages.core.utils import connect_to_db


class DataImporter(QgsTask):

    def __init__(self, file_path, count_id):
        self.basename = os.path.basename(file_path)
        super().__init__(
            'Importation fichier {}'.format(self.basename))
        self.file_path = file_path
        self.count_id = count_id
        self.db = connect_to_db()
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
                'Importation terminée {}'.format(self.basename),
                'Comptages', Qgis.Info)
        else:
            QgsMessageLog.logMessage(
                'Importation terminée avec des erreurs {}: {}'.format(
                    self.basename, self.exception),
                'Comptages', Qgis.Critical)

        self.db.close()
        del self.db

    def cancel(self):
        # TODO: Cancel needed?
        pass

    def get_number_of_lines(self):
        return sum(1 for line in open(self.file_path))

    def populate_lane_dict(self):
        query = QSqlQuery(self.db)

        query_str = (
            "select l.number, l.id from comptages.count as c "
            "join comptages.installation as i on i.id = c.id_installation "
            "join comptages.lane as l on l.id_installation = i.id "
            "where c.id = {};".format(self.count_id))

        query.exec_(query_str)
        while query.next():
            self.lanes[int(query.value(0))] = int(query.value(1))

    def populate_category_dict(self):
        if 'CLASS' not in self.file_header:
            return
        class_name = self.file_header['CLASS']
        query = QSqlQuery(self.db)

        # Use customized SWISS7 class for Marksmann devices
        # because they manage this class in a wrong way
        if self.file_header['FORMAT'] in ['INT-2', 'VBV-1'] and class_name == 'SWISS7':
            class_name = 'SWISS7-MM'

        query_str = (
            "select cat.code, cc.id_category from "
            "comptages.class_category as cc "
            "join comptages.category as cat on cc.id_category = cat.id "
            "join comptages.class as cl on cl.id = cc.id_class "
            "where cl.name = '{}';".format(class_name))

        query.exec_(query_str)
        while query.next():
            self.categories[int(query.value(0))] = int(query.value(1))

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
                        file_header['CLASS'] = 'ARX Cycle'
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
