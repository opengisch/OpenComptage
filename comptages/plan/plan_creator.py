import os
from qgis.core import (
    QgsPrintLayout, QgsProject, QgsReadWriteContext,
    QgsLayoutExporter)
from qgis.PyQt.QtXml import QDomDocument
from qgis.utils import iface
from comptages.core.settings import Settings
from comptages.datamodel import models


class PlanCreator():
    def __init__(self):
        self.settings = Settings()

    def export_pdf(self, count, file_name):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        qpt_file_path = os.path.join(
            current_dir, os.pardir, 'qml', 'plan.qpt')
        self.layout = PlanCreator.create_layout_from_template(
            qpt_file_path)

        self.set_fields(count)

        canvas = iface.mapCanvas()

        map_item = self.layout.itemById('map')
        map_item.setExtent(canvas.extent())

        exporter = QgsLayoutExporter(self.layout)

        exporter.exportToPdf(
            file_name, exporter.PdfExportSettings())

    def set_fields(self, count):
        section = models.Section.objects.filter(lane__id_installation__count=count).distinct()[0]

        self.set_text_item('f_01', count.id_installation.name)
        self.set_text_item('f_03', '')
        self.set_text_item('f_04', section.owner)
        self.set_text_item('f_05', section.road)
        self.set_text_item('f_06', section.way)
        self.set_text_item(
            'f_07',
            '{} + {} m'.format(
                section.start_pr,
                round(section.start_dist, 3)))
        self.set_text_item(
            'f_08',
            '{} + {} m'.format(
                section.end_pr,
                round(section.end_dist, 3)))
        self.set_text_item('f_09', section.place_name)
        self.set_text_item(
            'f_10',
            count.start_process_date.strftime(
                '%d.%m.%Y (%A)'))
        self.set_text_item(
            'f_11',
            count.end_process_date.strftime(
                '%d.%m.%Y (%A)'))
        self.set_text_item('f_14', '')
        self.set_text_item('f_15', '')

        direction_desc = ''
        if models.Lane.objects.filter(id_installation__count=count, direction=1).first():
            direction_desc = models.Lane.objects.filter(id_installation__count=count, direction=1).first().direction_desc
        self.set_text_item(
            'f_30',
            direction_desc)

        direction_desc = ''
        if models.Lane.objects.filter(id_installation__count=count, direction=2).first():
            direction_desc = models.Lane.objects.filter(id_installation__count=count, direction=2).first().direction_desc
        self.set_text_item(
            'f_31',
            direction_desc)

        # Page 2
        self.set_text_item('f_17', 'Campagne de comptage')
        self.set_text_item(
            'f_18',
            'Pose {}'.format(count.start_put_date.strftime(
                '%A %d.%m.%Y')))
        self.set_text_item(
            'f_19',
            'Dépose {}'.format(count.end_put_date.strftime(
                '%A %d.%m.%Y')))
        self.set_text_item('f_20', section.place_name)
        self.set_text_item('f_21', count.id_installation.name)
        self.set_text_item('f_22', '')
        self.set_text_item('f_23', '')

        self.set_picture_item('picture_1', count.id_installation.picture)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.set_picture_item(
            'logo',
            os.path.join(current_dir, os.pardir, 'images', 'logo_ne.png'))

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
