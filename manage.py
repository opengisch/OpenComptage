import os
import sys
from comptages import prepare_django

from django.core.management import execute_from_command_line

if __name__ == "__main__":

    default_db = {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": "db" if os.environ.get("LOCAL_TEST") == "1" else "localhost",
        "PORT": "5432",
        "NAME": "comptages",
        "USER": "postgres",
        "PASSWORD": "postgres",
    }

    prepare_django(default_db=default_db, DEBUG=True)
    execute_from_command_line(sys.argv)
