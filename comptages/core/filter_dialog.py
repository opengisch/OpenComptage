from qgis.PyQt.QtWidgets import QDialog
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
        self.axe.addItem('Tous')
        self.axe.addItems(
            list(models.Section.objects.all().distinct().order_by('road').values_list('road', flat=True)))
