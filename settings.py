
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
    'opencomptage.datamodel.apps.OpenComptageConfig',
)

SECRET_KEY = '09n+dhzh+02+_#$!1+8h-&(s-wbda#0*2mrv@lx*y#&fzlv&l)'

USE_TZ = True
TIME_ZONE = 'Europe/Zurich'
