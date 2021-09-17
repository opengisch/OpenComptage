from qgis.PyQt.QtWidgets import QDialog, QCompleter, QComboBox
from qgis.PyQt.QtCore import Qt
from comptages.core.utils import get_ui_class
from comptages.datamodel import models

FORM_CLASS = get_ui_class('filter.ui')


class FilterDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        # Populate TJM filter
        self.tjm.addItem('Tous', None)
        self.tjm.addItem('0-100', (0, 100))
        self.tjm.addItem('101-1000', (101, 1000))
        self.tjm.addItem('1001-10000', (1001, 10000))
        self.tjm.addItem('10001-...', (10001, 99999999))

        # Populate axe filter
        self.axe.addItem('Tous', None)
        self.axe.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.axe.completer().setFilterMode(Qt.MatchContains)
        self.axe.setInsertPolicy(QComboBox.NoInsert)

        for i in models.Section.objects.all().distinct('owner', 'road').order_by('owner'):
            self.axe.addItem(i.owner + ':' + i.road, (i.owner, i.road))
