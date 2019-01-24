import os
from qgis.core import (
    QgsPrintLayout, QgsProject, QgsReadWriteContext,
    QgsLayoutExporter)
from qgis.PyQt.QtXml import QDomDocument
from qgis.utils import iface
from comptages.core.settings import Settings


class PlanCreator():
    def __init__(self, layers):
        self.layers = layers
        self.settings = Settings()

    def export_pdf(self, count_id, file_name):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        qpt_file_path = os.path.join(
            current_dir, os.pardir, 'qml', 'plan.qpt')
        self.layout = PlanCreator.create_layout_from_template(
            qpt_file_path)

        self.set_fields(count_id)

        # self.layers.select_and_zoom_on_section_of_count(count_id)
        canvas = iface.mapCanvas()

        map_item = self.layout.itemById('map')
        map_item.setExtent(canvas.extent())

        exporter = QgsLayoutExporter(self.layout)

        exporter.exportToPdf(
            file_name, exporter.PdfExportSettings())

    def set_fields(self, count_id):
        count = self.layers.get_count(count_id)
        installation = self.layers.get_installation_of_count(count_id)
        sections = self.layers.get_sections_of_count(count_id)

        self.set_text_item('f_01', installation.attribute('name'))
        self.set_text_item('f_02', '')
        self.set_text_item('f_03', '')
        self.set_text_item('f_04', sections[0].attribute('owner'))
        self.set_text_item('f_05', sections[0].attribute('road'))
        self.set_text_item('f_06', sections[0].attribute('way'))
        self.set_text_item(
            'f_07',
            '{} + {} m'.format(
                sections[0].attribute('start_pr'),
                sections[0].attribute('start_dist')))
        self.set_text_item(
            'f_08',
            '{} + {} m'.format(
                sections[0].attribute('end_pr'),
                sections[0].attribute('end_dist')))
        self.set_text_item('f_09', sections[0].attribute('place_name'))
        self.set_text_item(
            'f_10',
            count.attribute('start_process_date').toString(
                'dd.MM.yyyy (dddd)'))
        self.set_text_item(
            'f_11',
            count.attribute('end_process_date').toString(
                'dd.MM.yyyy (dddd)'))
        self.set_text_item('f_12', '')
        self.set_text_item('f_13', '')
        self.set_text_item('f_14', '')
        self.set_text_item('f_15', '')
        self.set_text_item('f_16', '')
        self.set_text_item('f_17', '')
        self.set_text_item('f_18', '')
        self.set_text_item('f_19', '')
        self.set_text_item('f_20', '')
        self.set_text_item('f_21', '')
        self.set_text_item('f_22', '')
        self.set_text_item('f_23', '')

        self.set_picture_item('picture_1', installation.attribute('picture'))

    def set_text_item(self, name, text):
        self.layout.itemById(name).setText(text)

    def set_picture_item(self, name, file_name):
        if not file_name:
            return

        picture_path = os.path.join(
            self.settings.value('picture_directory'), file_name)
        self.layout.itemById(name).setPicturePath(picture_path)

    @staticmethod
    def create_layout_from_template(template_filename):
        layout = QgsPrintLayout(QgsProject().instance())
        document = QDomDocument()
        with open(os.path.join('data', 'general',
                               template_filename)) as template_file:
            template_content = template_file.read()
        document.setContent(template_content)
        layout.loadFromTemplate(document, QgsReadWriteContext())
        return layout
