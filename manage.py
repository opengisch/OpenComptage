import os
import sys
from django.core.management import execute_from_command_line
from comptages.datamodel import config
from qdmtk import register_datamodel


if __name__ == "__main__":
    register_datamodel(config.DATAMODEL_NAME, config.INSTALLED_APPS, config.DATABASE)
    execute_from_command_line(sys.argv)
