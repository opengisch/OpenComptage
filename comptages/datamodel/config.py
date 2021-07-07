DATAMODEL_NAME = "comptages"
DATABASE = {
    "ENGINE": "django.contrib.gis.db.backends.postgis",
    "HOST": "127.0.0.1",
    "PORT": "5432",
    "NAME": "comptages",
    "USER": "postgres",
    "PASSWORD": "postgres",
}
INSTALLED_APPS = ["comptages.datamodel"]
