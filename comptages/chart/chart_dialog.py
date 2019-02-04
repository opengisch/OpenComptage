import plotly
import plotly.graph_objs as go
from datetime import datetime

from qgis.PyQt.QtWidgets import QDockWidget, QListWidgetItem, QTabWidget
from comptages.core.utils import get_ui_class, push_warning
from comptages.ui.resources import *


FORM_CLASS = get_ui_class('chart_dock.ui')


class ChartDock(QDockWidget, FORM_CLASS):

    def __init__(self, iface, layers, parent=None):
        QDockWidget.__init__(self, parent)
        self.setupUi(self)
        self.layers = layers
        self.count_id = None
        self.sensor = None
        self.status = self.layers.IMPORT_STATUS_DEFINITIVE

    def set_attributes(self, count_id, approval_process=False):
        try:
            self.tabWidget.currentChanged.disconnect(self.current_tab_changed)
        except Exception:
            pass

        self.count_id = count_id

        self.setWindowTitle("Comptage: {}, installation: {}".format(
             count_id, self.layers.get_installation_name_of_count(count_id)))

        # Show message if data for this count already exists in the db
        if self.layers.count_contains_data(count_id) and approval_process:
            push_warning(('La base de données contient déjà des données '
                          'pour ce comptage.'))

        self.tabWidget.clear()
        self.tabWidget.currentChanged.connect(self.current_tab_changed)
        status = self.layers.IMPORT_STATUS_DEFINITIVE
        if approval_process:
            status = self.layers.IMPORT_STATUS_QUARANTINE

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
            self.status = self.layers.IMPORT_STATUS_QUARANTINE
        else:
            tab.buttonValidate.hide()
            tab.buttonRefuse.hide()
            self.status = self.layers.IMPORT_STATUS_DEFINITIVE

        sensor_type = self.layers.get_sensor_type_of_count(count_id)
        sensor = sensor_type.attribute('name')

        if(sensor == 'Boucle'):
            # By lane
            lanes = self.layers.get_lanes_of_section(section_id)
            for i, lane in enumerate(lanes):
                tab.chartList.addItem(
                    QListWidgetItem('Par heure, voie {}'.format(
                        lane.attribute('number'))))
                tab.charts.append(
                    ChartTime(self.layers, count_id, section_id,
                              self.status,
                              (lane.attribute('number'),
                               lane.attribute('id')),
                              None).get_div())
        else:
            # By direction
            # TODO: better get_directions_of_section or doesnt matter
            # i.e. special cases are always 'Boucle'?
            directions = self.layers.get_directions_of_count(count_id)
            for direction in directions:
                tab.chartList.addItem(
                    QListWidgetItem('Par heure, direction {}'.format(
                        direction)))
                tab.charts.append(
                    ChartTime(self.layers, count_id, section_id, self.status,
                              None, direction).get_div())

        tab.chartList.addItem(QListWidgetItem('Par catégorie'))
        tab.charts.append(
            ChartCategory(
                self.layers, count_id, section_id, self.status).get_div())

        tab.chartList.addItem(QListWidgetItem('Par vitesse'))
        tab.charts.append(
            ChartSpeed(
                self.layers, count_id, section_id, self.status).get_div())

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
        tab = self.tabWidget.currentWidget()
        self.layers.change_status_of_count_data(
            self.count_id, tab.section_id,
            self.layers.IMPORT_STATUS_DEFINITIVE)
        self.show_next_quarantined_chart()

    def refuse_count(self):
        tab = self.tabWidget.currentWidget()
        self.layers.delete_count_data(
            self.count_id, tab.section_id,
            self.layers.IMPORT_STATUS_QUARANTINE)
        self.show_next_quarantined_chart()

    def show_next_quarantined_chart(self):
        quarantined_counts = self.layers.get_quarantined_counts()
        if not quarantined_counts:
            self.hide()
            return

        self.set_attributes(quarantined_counts[0], True)
        self.show()


TAB_CLASS = get_ui_class('chart_tab.ui')


class ChartTab(QTabWidget, TAB_CLASS):

    def __init__(self, section_id, parent=None):
        QTabWidget.__init__(self, parent)
        self.setupUi(self)
        self.charts = []
        self.section_id = section_id


class Chart():

    def __init__(self, layers, count_id, section_id, status):
        self.layers = layers
        self.count_id = count_id
        self.section_id = section_id
        self.status = status

    def get_div(self):
        pass


class ChartSpeed(Chart):

    def get_div(self):

        x = []
        y = []

        is_aggregate = self.layers.is_data_aggregate(self.count_id)

        if is_aggregate:
            x, y = self.get_aggregate_data()
        else:
            x, y = self.get_detail_data()

        total_y = sum(y)
        percent_y = 0
        if not total_y == 0:
            percent_y = ['{}%'.format(
                round((i / total_y) * 100, 2)) for i in y]

        bar = go.Bar(
            x=x,
            y=y,
            text=percent_y,
            textposition='auto'
        )

        layout = go.Layout(
            title='Véhicules groupés par vitesse')
        fig = go.Figure(data=[bar], layout=layout)
        return plotly.offline.plot(fig, output_type='div')

    def get_aggregate_data(self):
        x, y = self.layers.get_aggregate_speed_chart_data(
            self.count_id, self.status, self.section_id)
        return x, y

    def get_detail_data(self):
        x, y = self.layers.get_detail_speed_chart_data(
            self.count_id, self.status, self.section_id)
        return x, y


class ChartCategory(Chart):

    def get_div(self):

        labels = []
        values = []

        is_aggregate = self.layers.is_data_aggregate(self.count_id)

        if is_aggregate:
            labels, values = self.get_aggregate_data()
        else:
            labels, values = self.get_detail_data()

        pie = go.Pie(labels=labels, values=values)

        layout = go.Layout(title="Véhicules groupés par catégorie")
        fig = go.Figure(data=[pie], layout=layout)
        return plotly.offline.plot(fig, output_type='div')

    def get_aggregate_data(self):
        labels, values = self.layers.get_aggregate_category_chart_data(
            self.count_id, self.status, self.section_id)
        return labels, values

    def get_detail_data(self):
        labels, values = self.layers.get_detail_category_chart_data(
            self.count_id, self.status, self.section_id)
        return labels, values


class ChartTime(Chart):

    def __init__(
            self, layers, count_id, section_id,
            status, lane, direction_number):
        super().__init__(layers, count_id, section_id, status)
        if lane:
            self.lane_number = lane[0]
            self.lane_id = lane[1]
        self.direction_number = direction_number

    def get_div(self):
        is_aggregate = self.layers.is_data_aggregate(self.count_id)
        sensor_type = self.layers.get_sensor_type_of_count(self.count_id)
        sensor = sensor_type.attribute('name')

        xs = []
        ys = []
        days = []
        title = ''

        if is_aggregate and sensor == 'Boucle':
            xs, ys, days = self.get_aggregate_data_by_lane()
            title = 'Véhicules par heure, voie {}'.format(self.lane_number)
        elif is_aggregate and sensor == 'Tube':
            xs, ys, days = self.get_aggregate_data_by_direction()
            title = 'Véhicules par heure, direction {}'.format(
                self.direction_number)
        elif not is_aggregate and sensor == 'Boucle':
            xs, ys, days = self.get_detail_data_by_lane()
            title = 'Véhicules par heure, voie {}'.format(self.lane_number)
        else:
            xs, ys, days = self.get_detail_data_by_direction()
            title = 'Véhicules par heure, direction {}'.format(
                self.direction_number)

        data = []
        # In reverse order so if the first day is not complete, the
        # missing hours are added at the beginning of the chart
        for i in range(len(xs)-1, -1, -1):
            day = datetime.strptime(
                days[i], '%Y-%m-%d %H:%M:%S').strftime('%a %d.%m.%Y')

            mode = 'lines'
            if sum(y is not None for y in ys[i]) < 24:
                mode = 'lines+markers'

            data.append(
                go.Scatter(
                    x=xs[i],
                    y=ys[i],
                    name=day,
                    showlegend=True,
                    mode=mode
                )
            )

        layout = go.Layout(
            title=title,
            xaxis=dict(tickangle=-45),
            barmode='group'
        )

        fig = go.Figure(data=data, layout=layout)
        return plotly.offline.plot(fig, output_type='div')

    def get_aggregate_data_by_lane(self):
        xs, ys, days = \
            self.layers.get_aggregate_time_chart_data_by_lane(
                self.count_id, self.status, self.lane_id,
                self.section_id)
        return xs, ys, days

    def get_aggregate_data_by_direction(self):
        xs, ys, days = \
            self.layers.get_aggregate_time_chart_data_by_direction(
                self.count_id, self.status, self.direction_number,
                self.section_id)
        return xs, ys, days

    def get_detail_data_by_lane(self):
        xs, ys, days = \
            self.layers.get_detail_time_chart_data_by_lane(
                self.count_id, self.status, self.lane_id,
                self.section_id)
        return xs, ys, days

    def get_detail_data_by_direction(self):
        xs, ys, days = \
            self.layers.get_detail_time_chart_data_by_direction(
                self.count_id, self.status, self.direction_number,
                self.section_id)
        return xs, ys, days
