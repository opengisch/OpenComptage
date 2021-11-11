import os
from comptages.core.settings import Settings as PluginSettings


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("NPLAAAAAAAA")
plugin_settings = PluginSettings()

print(plugin_settings.value("db_host"))
print(__name__)
print(plugin_settings.settings_list())

DATABASES = {
    'default': {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": "localhost",
        "PORT": "5432",
        "NAME": "comptages",
        "USER": "postgres",
        "PASSWORD": "postgres",
    }
}

INSTALLED_APPS = (
    'comptages.datamodel.apps.ComptagesConfig',
)

SECRET_KEY = '09n+dhzh+02+_#$!1+8h-&(s-wbda#0*2mrv@lx*y#&fzlv&l)'

USE_TZ = True
TIME_ZONE = 'Europe/Zurich'
