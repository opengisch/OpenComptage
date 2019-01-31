import os

from datetime import datetime

from qgis.core import QgsTask, Qgis, QgsMessageLog
from qgis.PyQt.QtSql import QSqlDatabase, QSqlQuery

from comptages.core.settings import Settings


class DataImporter(QgsTask):

    def __init__(self, file_path, count_id):
        self.basename = os.path.basename(file_path)
        super().__init__(
            'Importation fichier {}'.format(self.basename))
        self.file_path = file_path
        self.count_id = count_id
        self.connect_to_db()
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

    def connect_to_db(self):
        settings = Settings()
        self.db = QSqlDatabase.addDatabase("QPSQL", str(datetime.now()))
        self.db.setHostName(settings.value("db_host"))
        self.db.setPort(settings.value("db_port"))
        self.db.setDatabaseName(settings.value("db_name"))
        self.db.setUserName(settings.value("db_username"))
        self.db.setPassword(settings.value("db_password"))
        self.db.open()

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
        with open(file_path) as f:
            for line in f:
                if line.startswith('* ') and not line.startswith('* HEAD '):
                    line = line[2:]
                    splitted = line.split('=', 1)
                    if len(splitted) > 1:
                        key = splitted[0].strip()
                        value = splitted[1].strip()
                        if key == 'CLASS' and value == 'SPECIAL10':
                            value = 'SWISS10'
                        file_header[key] = value
        return file_header

    def parse_data_header(self):
        data_header = []
        with open(self.file_path) as f:
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
