import os

from qgis.PyQt.uic import loadUiType
from qgis.PyQt.QtWidgets import QProgressBar
from qgis.PyQt.QtCore import Qt
from qgis.utils import iface


def get_ui_class(ui_file):
    """Get UI Python class from .ui file.
       Can be filename.ui or subdirectory/filename.ui
    :param ui_file: The file of the ui in svir.ui
    :type ui_file: str
    """
    os.path.sep.join(ui_file.split('/'))
    ui_file_path = os.path.abspath(
            os.path.join(
                    os.path.dirname(__file__),
                    os.pardir,
                    'ui',
                    ui_file
            )
    )
    return loadUiType(ui_file_path)[0]


def push_info(message):
    iface.messageBar().pushInfo('Comptages', message)


def create_progress_bar(message):

    progress_widget = QProgressBar()
    progress_widget.setMaximum(100)
    progress_widget.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    message_bar = iface.messageBar().createMessage(message)
    message_bar.setWidget(progress_widget)
    iface.messageBar().pushMessage('')
    iface.messageBar().pushWidget(message_bar)

    return progress_widget


def clear_widgets():
    iface.messageBar().clearWidgets()
