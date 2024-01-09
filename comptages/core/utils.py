from functools import reduce
import os

from datetime import datetime
from typing import Any

from django.db.models.expressions import F


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


def get_count_details_by_season(count: models.Count) -> dict[str, Any]:
    """Break down count details by season x section x class"""
    output = {}
    # Assuming seasons to run from 20 <month> to 21 <month n + 1>
    seasons = {
        "printemps": [3, 4, 5],
        "été": [6, 7, 8],
        "automne": [9, 10, 11],
        "hiver": [12, 1, 2],
    }

    # Preparing to filter out categories that don't reference the class picked out by `class_name`
    class_name = "SPCH-MD 5C"
    categories_name_to_exclude = ("TRASH", "ELSE")
    _class = models.Class.objects.get(name=class_name)
    categories_ids = (
        _class.classcategory_set.annotate(name=F("id_category__name"))
        .exclude(name__in=categories_name_to_exclude)
        .values_list("id_category", flat=True)
    )

    # Getting data
    count_details = (
        models.CountDetail.objects.filter(
            id_count=count.id, id_category__in=categories_ids
        )
        .annotate(
            section=F("id_lane__id_section"), category_name=F("id_category__name")
        )
        .values("id", "section", "category_name", "times", "timestamp")
    )

    # Preparing to collect data
    def reducer(acc: dict, detail) -> dict:
        timestamp: datetime = detail["timestamp"]

        for season, _range in seasons.items():
            if timestamp.month in _range and (
                timestamp.month != _range[0] or timestamp.day >= 21
            ):
                section_id = detail["section"]
                category_name = detail["category_name"]
                times = detail["times"]

                if season not in acc:
                    acc[season] = {}

                if category_name not in acc[season]:
                    acc[season][category_name] = {}

                if section_id not in acc[season][category_name]:
                    acc[season][category_name][section_id] = 0

                acc[season][category_name][section_id] += times
                break

        return acc

    # Collecting
    return reduce(reducer, count_details, {})
