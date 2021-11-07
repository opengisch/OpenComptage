
from comptages.datamodel import config
from comptages.core.settings import Settings

# Register the datamodel
try:

    settings = Settings()
    DATABASE = {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": settings.value("db_host"),
        "PORT": settings.value("db_port"),
        "NAME": settings.value("db_name"),
        "USER": settings.value("db_username"),
        "PASSWORD": settings.value("db_password"),
    }

    from qdmtk import register_datamodel
    register_datamodel(config.DATAMODEL_NAME, config.INSTALLED_APPS, DATABASE)
except Exception as e:
    print(e)
    #    self.iface.messageBar().pushMessage("Could not load QDMTK.", "You must install the QDMTK plugin prior to using Comptages", level=Qgis.Critical)


def classFactory(iface):
    """Load Comptages class from file comptages.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """

    from .comptages import Comptages
    return Comptages(iface)
