import os
from builtins import next
from qgis.PyQt.uic import loadUiType, loadUi
from qgis.PyQt.QtCore import QCoreApplication, Qt
from qgis.core import (
    QgsFeatureRequest, QgsMessageLog, QgsProject, QgsDataSourceUri,
    QgsVectorLayer, QgsProject, QgsCoordinateReferenceSystem
)
from comptages.settings import ComptagesSettings


def load_layer_pg(
        schema, layer_name, geometry, sql, display_name, id_col='', epsg=None):

    settings = ComptagesSettings()
    uri = QgsDataSourceUri()
    uri.setConnection(
        settings.value("db_host"),
        str(settings.value("db_port")),
        settings.value("db_name"),
        settings.value("db_username"),
        settings.value("db_password")
    )

    uri.setDataSource(schema, layer_name, geometry, sql, id_col)
    layer = QgsVectorLayer(uri.uri(), display_name, "postgres")
    if epsg is not None:
        crs = QgsCoordinateReferenceSystem(epsg)
        layer.setCrs(crs)

    QgsProject.instance().addMapLayer(layer, addToLegend=False)

    return layer


def get_ui_class(ui_file):
    """Get UI Python class from .ui file.
       Can be filename.ui or subdirectory/filename.ui
    :param ui_file: The file of the ui in svir.ui
    :type ui_file: str
    """
    os.path.sep.join(ui_file.split('/'))
    ui_file_path = os.path.abspath(
            os.path.join(
                    os.path.dirname(__file__),
                    #os.pardir,
                    #os.pardir,
                    'ui',
                    ui_file
            )
    )
    return loadUiType(ui_file_path)[0]
