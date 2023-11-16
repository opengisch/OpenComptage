from qgis.PyQt.QtWidgets import QDialog
from comptages.core.utils import get_ui_class

FORM_CLASS = get_ui_class("delete.ui")


class DeleteDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
