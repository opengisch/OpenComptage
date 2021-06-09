DATAMODEL_NAME = "comptages"
DATABASE = {
    "ENGINE": "django.contrib.gis.db.backends.postgis",
    "NAME": "comptages",
    "USER": "postgres",
    "PASSWORD": "postgres",
    "OPTIONS": {"options": "-c search_path=comptages,transfer,public"},
}
INSTALLED_APPS = ["comptages.datamodel"]
