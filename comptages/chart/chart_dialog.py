import plotly
import plotly.graph_objs as go
import plotly.express as px

from datetime import datetime

from qgis.PyQt.QtWidgets import QDockWidget, QListWidgetItem, QTabWidget
from qgis.core import QgsMessageLog, Qgis
from comptages.core.utils import get_ui_class, push_warning, push_info
from comptages.ui.resources import *
from comptages.core.tjm import calculate_tjm, get_tjm_data_total, get_tjm_data_by_lane, get_tjm_data_by_direction
from comptages.core import statistics, definitions
from comptages.datamodel import models


FORM_CLASS = get_ui_class('chart_dock.ui')


class ChartDock(QDockWidget, FORM_CLASS):

    def __init__(self, iface, layers, parent=None):
        QDockWidget.__init__(self, parent)
        self.setupUi(self)
        self.layers = layers
        self.count_id = None
        self.sensor = None
        self.status = definitions.IMPORT_STATUS_DEFINITIVE

    def set_attributes(self, count_id, approval_process=False):
        try:
            self.tabWidget.currentChanged.disconnect(self.current_tab_changed)
        except Exception:
            pass

        self.count_id = count_id

        self.setWindowTitle("Comptage: {}, installation: {}".format(
             count_id, self.layers.get_installation_name_of_count(count_id)))

        contains_data = self.layers.count_contains_data(count_id)

        # Show message if there are no data to show
        if not contains_data and not approval_process:
            self.hide()
            push_info("Installation {}: Il n'y a pas de données à montrer pour "
                "le comptage {}".format(
                self.layers.get_installation_name_of_count(count_id),count_id))
            return

        self.show()

        # Show message if data for this count already exists in the db
        if contains_data and approval_process:
            push_warning(('La base de données contient déjà des données '
                          'pour ce comptage.'))

        self.tabWidget.clear()
        self.tabWidget.currentChanged.connect(self.current_tab_changed)
        status = definitions.IMPORT_STATUS_DEFINITIVE
        if approval_process:
            status = definitions.IMPORT_STATUS_QUARANTINE

        section_ids = self.layers.get_sections_with_data_of_count(
            count_id, status)

        for section_id in section_ids:
            tab = ChartTab(section_id)
            self.tabWidget.addTab(tab, section_id)
            self.populate_tab(tab, count_id, section_id, approval_process)

    def populate_tab(self, tab, count_id, section_id, approval_process):
        # Remove previous items
        try:
            tab.chartList.currentRowChanged.disconnect(self.chart_list_changed)
        except Exception:
            pass

        for i in range(tab.chartList.count()):
            tab.chartList.takeItem(0)
        tab.chartList.currentRowChanged.connect(self.chart_selection_changed)

        if approval_process:
            tab.buttonValidate.show()
            tab.buttonValidate.clicked.connect(self.validate_count)
            tab.buttonRefuse.clicked.connect(self.refuse_count)
            tab.buttonRefuse.show()
            self.status = definitions.IMPORT_STATUS_QUARANTINE
        else:
            tab.buttonValidate.hide()
            tab.buttonRefuse.hide()
            self.status = definitions.IMPORT_STATUS_DEFINITIVE

        count = models.Count.objects.get(id=count_id)
        sensor_type = count.id_sensor_type
        lanes = models.Lane.objects.filter(id_installation__count=count)
        directions = lanes.values('direction').distinct().values_list('direction', flat=True)

        if(sensor_type.name == 'Boucle'):
            # By lane
            for i, lane in enumerate(lanes):
                tab.chartList.addItem(
                    QListWidgetItem('Par heure, voie {}'.format(
                        lane.number)))
                tab.charts.append(
                    ChartTime(
                        count=count,
                        status=self.status,
                        lane=lane,
                    ).get_div())

        else:
            # By direction
            for i, direction in enumerate(directions):
                tab.chartList.addItem(
                    QListWidgetItem('Par heure, direction {}'.format(
                        direction)))
                tab.charts.append(
                    ChartTime(
                        count=count,
                        status=self.status,
                        direction=direction,
                    ).get_div())

        tab.chartList.addItem(QListWidgetItem('Par catégorie'))
        tab.charts.append(
            ChartCat(
                count=count, status=self.status,
            ).get_div())

        tab.chartList.addItem(QListWidgetItem('Par vitesse'))
        tab.charts.append(
            ChartSpeed(
                count=count, status=self.status,
            ).get_div())

        if(sensor_type.name == 'Boucle'):
            # By lane
            for i, lane in enumerate(lanes):
                tab.chartList.addItem(
                    QListWidgetItem('Par TJM, voie {}'.format(
                        lane.number)))
                tab.charts.append(
                    ChartTjm(
                        count=count,
                        status=self.status,
                        lane=lane,
                    ).get_div())

        else:
            # By direction
            for i, direction in enumerate(directions):
                tab.chartList.addItem(
                    QListWidgetItem('Par TJM, direction {}'.format(
                        direction)))
                tab.charts.append(
                    ChartTjm(
                        count=count,
                        status=self.status,
                        direction=direction,
                    ).get_div())

        tab.chartList.addItem(
            QListWidgetItem('Par TJM total'))
        tab.charts.append(
            ChartTjm(
                count=count,
                status=self.status,
            ).get_div())

        self.layers.select_and_zoom_on_section_of_count(count_id)
        if tab.chartList.currentRow() == 0:
            self.chart_selection_changed(0)
        else:
            tab.chartList.setCurrentRow(0)

    def chart_selection_changed(self, row):
        tab = self.tabWidget.currentWidget()
        tab.webView.setHtml(tab.charts[row])

    def current_tab_changed(self, index):
        tab = self.tabWidget.currentWidget()
        if tab.chartList.currentRow() == 0:
            self.chart_selection_changed(0)

    def validate_count(self):
        QgsMessageLog.logMessage(
            '{} - Accept data started'.format(datetime.now()),
            'Comptages', Qgis.Info)

        tab = self.tabWidget.currentWidget()
        self.layers.change_status_of_count_data(
            self.count_id, tab.section_id,
            definitions.IMPORT_STATUS_DEFINITIVE)
        calculate_tjm(self.count_id)
        self.show_next_quarantined_chart()

        QgsMessageLog.logMessage(
            '{} - Accept data ended'.format(datetime.now()),
            'Comptages', Qgis.Info)

    def refuse_count(self):
        QgsMessageLog.logMessage(
            '{} - Reject data started'.format(datetime.now()),
            'Comptages', Qgis.Info)

        tab = self.tabWidget.currentWidget()
        self.layers.delete_count_data(
            self.count_id, tab.section_id,
            definitions.IMPORT_STATUS_QUARANTINE)
        self.show_next_quarantined_chart()

        QgsMessageLog.logMessage(
            '{} - Reject data ended'.format(datetime.now()),
            'Comptages', Qgis.Info)

    def show_next_quarantined_chart(self):
        QgsMessageLog.logMessage(
            '{} - Generate validation chart started'.format(datetime.now()),
            'Comptages', Qgis.Info)

        quarantined_counts = self.layers.get_quarantined_counts()
        if not quarantined_counts:
            self.hide()
            push_info("Il n'y a pas de données à valider")
            return

        self.set_attributes(quarantined_counts[0], True)
        self.show()

        QgsMessageLog.logMessage(
            '{} - Generate validation chart ended'.format(datetime.now()),
            'Comptages', Qgis.Info)

TAB_CLASS = get_ui_class('chart_tab.ui')


class ChartTab(QTabWidget, TAB_CLASS):

    def __init__(self, section_id, parent=None):
        QTabWidget.__init__(self, parent)
        self.setupUi(self)
        self.charts = []
        self.section_id = section_id


class Chart():

    def __init__(self, count, status, lane=None, direction=None):
        self.count = count
        self.status = status
        self.lane = lane
        self.direction = direction

    def get_div(self):
        pass

class ChartTjm(Chart):
    def get_div(self):

        df = statistics.get_day_data(
            self.count,
            self.status,
            self.lane,
            self.direction,
        )

        if df.empty:
            return

        fig = px.bar(
            df,
            x='date',
            y='tj',
            title="Véhicules ...")

        return plotly.offline.plot(fig, output_type='div')


class ChartTime(Chart):

    def get_div(self):

        df = statistics.get_time_data(
            self.count,
            self.status,
            self.lane,
            self.direction,
        )
        if df.empty:
            return

        title = 'Véhicules par heure'
        if self.lane is not None:
            title = 'Véhicules par heure, voie {}'.format(self.lane.number)
        elif self.direction is not None:
            title = 'Véhicules par heure, direction {}'.format(self.direction)

        fig = px.line(
            df,
            x='hour',
            y='thm',
            color='date',
            render_mode='svg',
            title=title)

        return plotly.offline.plot(fig, output_type='div')


class ChartCat(Chart):

    def get_div(self):

        df = statistics.get_category_data(self.count, self.status)

        if df.empty:
            return

        fig = px.pie(
            df,
            values='value',
            names='cat_name',
            title="Véhicules groupés par catégorie")

        return plotly.offline.plot(fig, output_type='div')


class ChartSpeed(Chart):

    def get_div(self):

        df = statistics.get_speed_data(self.count, self.status)
        if df.empty:
            return

        fig = px.bar(
            df,
            x='bins',
            y='times',
            title="Véhicules groupés par vitesse")

        return plotly.offline.plot(fig, output_type='div')
