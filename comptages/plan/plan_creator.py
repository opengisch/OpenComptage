import os
from qgis.core import (
    QgsPrintLayout, QgsProject, QgsReadWriteContext,
    QgsLayoutExporter)
from qgis.PyQt.QtXml import QDomDocument
from qgis.utils import iface


class PlanCreator():
    def __init__(self, layers):
        self.layers = layers

    def export_pdf(self, count_id, file_name):
        print('export_pdf: {}, {}'.format(count_id, file_name))

        # FIXME path
        layout = PlanCreator.create_layout_from_template(
            '/home/mario/workspace/repos/OpenComptage/comptages/qml/plan.qpt')

        # layout_manager = QgsProject.instance().layoutManager()
        # layout_manager.addLayout(layout)

        map_item = layout.itemById('map')

        # layout.itemById('field_prova').setText('Uellaaaa')

        self.layers.select_and_zoom_on_section_of_count(count_id)
        canvas = iface.mapCanvas()
        map_item.setExtent(canvas.extent())

        exporter = QgsLayoutExporter(layout)

        exporter.exportToPdf(
            file_name, exporter.PdfExportSettings())

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
