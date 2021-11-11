import sys
import os

from django.core.management import execute_from_command_line
# from comptages.datamodel import config
# from comptages.core.settings import Settings
# from qdmtk import register_datamodel


# if __name__ == "__main__":
#     settings = Settings()
#     DATABASE = {
#         "ENGINE": "django.contrib.gis.db.backends.postgis",
#         "HOST": settings.value("db_host"),
#         "PORT": settings.value("db_port"),
#         "NAME": settings.value("db_name"),
#         "USER": settings.value("db_username"),
#         "PASSWORD": settings.value("db_password"),
#     }
#     try:
#         register_datamodel(config.DATAMODEL_NAME, config.INSTALLED_APPS)
#     except Exception:
#         pass

#     execute_from_command_line(sys.argv)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    execute_from_command_line(sys.argv)
