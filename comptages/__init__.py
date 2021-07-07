from comptages.datamodel import config

# Register the datamodel
try:
    from qdmtk import register_datamodel
    register_datamodel(config.DATAMODEL_NAME, config.INSTALLED_APPS, config.DATABASE)
except ImportError:
    pass
    #    self.iface.messageBar().pushMessage("Could not load QDMTK.", "You must install the QDMTK plugin prior to using Comptages", level=Qgis.Critical)


def classFactory(iface):
    """Load Comptages class from file comptages.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """

    from .comptages import Comptages
    return Comptages(iface)
