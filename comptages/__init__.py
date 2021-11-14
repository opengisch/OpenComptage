import os
import django

from django.conf import settings as django_settings


def prepare_django(default_db=None, **additional_settings):
    if django_settings.configured:
        return

    if not additional_settings:
        additional_settings = {}

    # If the default db doesn't arrives from the manage.py script
    # (i.e. the command is lauched from the QGIS python console), we
    # use the one in the plugin settings
    if not default_db:

        from comptages.core.settings import Settings as PluginSettings
        plugin_settings = PluginSettings()
        default_db = {
            "ENGINE": "django.contrib.gis.db.backends.postgis",
            "HOST": plugin_settings.value("db_host"),
            "PORT": plugin_settings.value("db_port"),
            "NAME": plugin_settings.value("db_name"),
            "USER": plugin_settings.value("db_username"),
            "PASSWORD": plugin_settings.value("db_password"),
        }

    # Allow to configure GDAL/GEOS/Spatialite libraries from env vars
    # see https://docs.djangoproject.com/en/3.2/ref/contrib/gis/install/geolibs/#geos-library-path
    GDAL_LIBRARY_PATH_ENV = os.getenv("GDAL_LIBRARY_PATH")
    GEOS_LIBRARY_PATH_ENV = os.getenv("GEOS_LIBRARY_PATH")
    SPATIALITE_LIBRARY_PATH_ENV = os.getenv("SPATIALITE_LIBRARY_PATH")
    if GDAL_LIBRARY_PATH_ENV:
        additional_settings["GDAL_LIBRARY_PATH"] = GDAL_LIBRARY_PATH_ENV
    if GEOS_LIBRARY_PATH_ENV:
        additional_settings["GEOS_LIBRARY_PATH"] = GEOS_LIBRARY_PATH_ENV
    if SPATIALITE_LIBRARY_PATH_ENV:
        additional_settings["SPATIALITE_LIBRARY_PATH"] = SPATIALITE_LIBRARY_PATH_ENV

    django_settings.configure(
        BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir),
        DATABASES={"default": default_db},
        INSTALLED_APPS=('comptages.datamodel.apps.ComptagesConfig',),
        USE_TZ=True,
        TIME_ZONE='Europe/Zurich',
        SECRET_KEY='09n+dhzh+02+_#$!1+8h-&(s-wbda#0*2mrv@lx*y#&fzlv&l)',
        **additional_settings
    )
    django.setup()


def classFactory(iface):
    """Load Comptages class from file comptages.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    prepare_django()
    from .comptages import Comptages
    return Comptages(iface)
