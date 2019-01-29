import os
from qgis.core import (
    QgsPrintLayout, QgsProject, QgsReadWriteContext,
    QgsLayoutExporter)
from qgis.PyQt.QtXml import QDomDocument
from comptages.core.settings import Settings


class ReportCreator():
    def __init__(self, layers):
        self.layers = layers
        self.settings = Settings()

    def export_pdf(self, count_id, file_name):

        current_dir = os.path.dirname(os.path.abspath(__file__))
        qpt_file_path = os.path.join(
            current_dir, os.pardir, 'qml', 'report.qpt')
        self.layout = ReportCreator.create_layout_from_template(
            qpt_file_path)

        self.set_fields(count_id)

        exporter = QgsLayoutExporter(self.layout)
        exporter.exportToPdf(
            file_name, exporter.PdfExportSettings())

    def set_fields(self, count_id):
        pass

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
