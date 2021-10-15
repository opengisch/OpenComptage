from qgis.PyQt.QtWidgets import QDialog, QCompleter, QComboBox, QSlider, QDialogButtonBox
from qgis.PyQt.QtCore import Qt
from comptages.core.utils import get_ui_class
from comptages.datamodel import models

FORM_CLASS = get_ui_class('filter.ui')


class FilterDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        def update_tjm_labels(min, max):
            self.min_tjm.setNum(min)
            self.max_tjm.setNum(max)
            if max == 30000:
                self.max_tjm.setText("∞")

        # self.tjm_min.setValue(0)
        # self.tjm_max.setValue(30000)
        # self.tjm.setMinimum(0)
        # self.tjm.setMaximum(30000)
        # self.tjm.setSingleStep(100)
        # self.tjm.setTickInterval(5000)
        # self.tjm.setTickPosition(QSlider.TicksBothSides)
        # self.tjm.rangeChanged.connect(update_tjm_labels)

        # Populate axe filter
        self.axe.addItem('Tous', None)
        self.axe.completer().setCompletionMode(QCompleter.PopupCompletion)
        self.axe.completer().setFilterMode(Qt.MatchContains)
        self.axe.setInsertPolicy(QComboBox.NoInsert)

        for i in models.Section.objects.all().distinct('owner', 'road').order_by('owner'):
            self.axe.addItem(i.owner + ':' + i.road, (i.owner, i.road))

        # Populate sector filter
        self.sector.addItem('Tous', None)
        for i in models.Sector.objects.all().order_by('id'):
            self.sector.addItem(str(i.id), i.id)

        def reset_dialog(button):
            self.start_date.clear()
            self.end_date.clear()
            self.installation.setCurrentIndex(0)
            self.sensor.setCurrentIndex(0)
            # self.tjm.setRange(0, 90000)
            self.tjm_min.setValue(0)
            self.tjm_max.setValue(30000)
            self.axe.setCurrentIndex(0)
            self.sector.setCurrentIndex(0)

        self.buttons.button(
            QDialogButtonBox.Reset).clicked.connect(reset_dialog)
