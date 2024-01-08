from functools import reduce
import os

from datetime import datetime
from typing import Any


from qgis.core import Qgis
from qgis.PyQt.uic import loadUiType
from qgis.PyQt.QtWidgets import QProgressBar
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtSql import QSqlDatabase
from qgis.utils import iface

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
    from comptages.core.settings import Settings

    settings = Settings()
    db = QSqlDatabase.addDatabase("QPSQL", str(datetime.now()))
    db.setHostName(settings.value("db_host"))
    db.setPort(settings.value("db_port"))
    db.setDatabaseName(settings.value("db_name"))
    db.setUserName(settings.value("db_username"))
    db.setPassword(settings.value("db_password"))
    db.open()

    return db


def partition_by_season(count: models.Count) -> dict[str, Any]:
    """Break down count details by season"""
    seasons = {
        "spring": [3, 4, 5],
        "summer": [6, 7, 8],
        "fall": [9, 10, 11],
        "winter": [12, 1, 2],
    }
    accumulator = {k: {"_range": v, "times": 0} for k, v in seasons.items()}

    def reducer(acc: dict, detail: models.CountDetail) -> dict:
        d = detail.timestamp
        for name, season in acc.items():
            if d.month in season["_range"]:
                acc[name]["times"] += detail.times
                break
        return acc

    count_details = models.CountDetail.objects.filter(id_count=count.id)
    return reduce(reducer, count_details, accumulator)
