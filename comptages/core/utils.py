import os

from datetime import datetime
from comptages.core.statistics import get_time_data_yearly

from qgis.core import Qgis
from qgis.PyQt.uic import loadUiType
from qgis.PyQt.QtWidgets import QProgressBar
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtSql import QSqlDatabase
from qgis.utils import iface

from django.db.models.functions import Trunc

from comptages.core.settings import Settings
from comptages.datamodel import models


def get_ui_class(ui_file):
    """Get UI Python class from .ui file.
       Can be filename.ui or subdirectory/filename.ui
    :param ui_file: The file of the ui in svir.ui
    :type ui_file: str
    """
    os.path.sep.join(ui_file.split("/"))
    ui_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, "ui", ui_file)
    )
    return loadUiType(ui_file_path)[0]


def push_info(message: str):
    iface.messageBar().pushInfo("Comptages", message)


def push_warning(message: str):
    iface.messageBar().pushMessage("Comptages", message, Qgis.Warning, 0)


def push_error(message: str):
    # iface.messageBar().pushCritical('Comptages', message)
    iface.messageBar().pushMessage("Comptages", message, Qgis.Critical, 0)


def create_progress_bar(message: str):
    progress_widget = QProgressBar()
    progress_widget.setMaximum(100)
    progress_widget.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    message_bar = iface.messageBar().createMessage(message)
    message_bar.setWidget(progress_widget)
    iface.messageBar().pushMessage("")
    iface.messageBar().pushWidget(message_bar)

    return progress_widget


def clear_widgets():
    iface.messageBar().clearWidgets()


def connect_to_db():
    settings = Settings()
    db = QSqlDatabase.addDatabase("QPSQL", str(datetime.now()))
    db.setHostName(settings.value("db_host"))
    db.setPort(settings.value("db_port"))
    db.setDatabaseName(settings.value("db_name"))
    db.setUserName(settings.value("db_username"))
    db.setPassword(settings.value("db_password"))
    db.open()

    return db


def count_valid_days(section_id: str, year: int) -> int:
    """Count valid days across all counts for `section` and `year`."""
    section = models.Section.objects.get(id=section_id)
    df = get_time_data_yearly(year, section)
    df.reset_index()

    valid_days_in_year = set()
    valid_hours_in_day = set()
    prev_day = None
    for _, row in df.iterrows():
        if row["date"] != prev_day:
            if len(valid_hours_in_day) >= 14:
                valid_days_in_year.add(prev_day)
            valid_hours_in_day.clear()
        if 6 <= row["hour"] <= 22 and row["thm"] > 0:
            valid_hours_in_day.add(row["hour"])
        prev_day = row["date"]
    return len(valid_days_in_year)
