from comptages.core.settings import Settings

settings = Settings()
DATAMODEL_NAME = "comptages"
DATABASE = {
    "ENGINE": "django.contrib.gis.db.backends.postgis",
    "HOST": settings.value("db_host"),
    "PORT": settings.value("db_port"),
    "NAME": settings.value("db_name"),
    "USER": settings.value("db_username"),
    "PASSWORD": settings.value("db_password"),
}
INSTALLED_APPS = ["comptages.datamodel"]
