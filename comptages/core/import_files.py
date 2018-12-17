from qgis.core import QgsMessageLog, Qgis
from qgis.PyQt.QtWidgets import QFileDialog
from comptages.parser.data_parser import (
    DataParser, DataParserVbv1, DataParserInt2)

from comptages.core.utils import push_info


class FileImporter():

    def __init__(self, layers):
        self.layers = layers
        self.ask_for_files()

    def ask_for_files(self):
        file_dialog = QFileDialog()
        title = 'Import data'
        path = '/home/mario/workspace/repos/OpenComptage/comptages/test/test_data/'
        files = QFileDialog.getOpenFileNames(
            file_dialog, title, path, "Data file (*.A?? *.aV? *.I?? *.V??)")[0]

        for file in files:
            QgsMessageLog.logMessage(
                'import file: {}'.format(file), 'Comptages', Qgis.Info)
            self.import_file(file)

    def ask_for_file(self):
        pass

    def import_file(self, file):
        file_format = DataParser.get_file_format(file)

        try:
            if file_format == 'VBV-1':
                data_parser = DataParserVbv1(self.layers, file)
            elif file_format == 'INT-2':
                data_parser = DataParserInt2(self.layers, file)
            else:
                push_info('Format {} not supported'.format(file_format))
                return

            count_id = self.layers.guess_count_id(
                data_parser.get_site(), data_parser.get_start_rec(),
                data_parser.get_stop_rec())

            if not count_id:
                push_info('Could not guess count_id')
                # Exception?
                return

            data_parser.parse_and_import_data(count_id)
        except Exception as e:
            push_info('Error during data parsing: {}'.format(str(e)))
            raise e

    def import_files(self):
        pass

    def show_charts(self):
        pass
