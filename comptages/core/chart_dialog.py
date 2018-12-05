from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWidgets import QDockWidget, QListWidgetItem
from comptages.core.utils import get_ui_class
from comptages.ui.resources import *

import plotly
import plotly.graph_objs as go

FORM_CLASS = get_ui_class('chart_dock.ui')


class ChartDock(QDockWidget, FORM_CLASS):
    def __init__(self, iface, layers, count_id, parent=None):
        QDockWidget.__init__(self, parent)
        self.setupUi(self)
        self.layers = layers
        self.count_id = count_id

        self.chartList.addItem(QListWidgetItem('Par heure'))
        self.chartList.addItem(QListWidgetItem('Par catégorie'))
        self.chartList.addItem(QListWidgetItem('Par vitesse'))

        self.chartList.currentRowChanged.connect(self.chart_list_changed)
        self.chartList.setCurrentRow(0)

    def set_count_id(self, count_id):
        self.count_id = count_id
        self.chart_list_changed(0)

    def chart_list_changed(self, row):
        if row == 0:
            self.plot_chart_time()
        elif row == 1:
            self.plot_chart_category()
        elif row == 2:
            self.plot_chart_speed()

    def plot_chart_time(self):
        xs, ys = self.layers.get_aggregate_time_chart_data(self.count_id)
        data = []

        # In reverse order so if the first day is not complete, the
        # missing hours are added at the beginning of the chart
        for i in range(len(xs)-1, -1, -1):
            data.append(
                go.Scatter(
                    x=xs[i],
                    y=ys[i],
                    name="Jour {}".format(i+1),
                )
            )

        layout = go.Layout(
            title='Véhicules par heure',
            xaxis=dict(tickangle=-45),
            barmode='group'
        )

        fig = go.Figure(data=data, layout=layout)
        div = plotly.offline.plot(fig, output_type='div')

        self.webView.setHtml(div)

    def plot_chart_speed(self):
        x, y = self.layers.get_aggregate_speed_chart_data(self.count_id)

        bar = go.Bar(x=x, y=y)

        layout = go.Layout(title='Véhicules groupés par vitesse')
        fig = go.Figure(data=[bar], layout=layout)
        div = plotly.offline.plot(fig, output_type='div')

        self.webView.setHtml(div)

    def plot_chart_category(self):
        labels, values = self.layers.get_aggregate_category_chart_data(
            self.count_id)

        pie = go.Pie(labels=labels, values=values)

        layout = go.Layout(title="Véhicules groupés par catégorie")
        fig = go.Figure(data=[pie], layout=layout)
        div = plotly.offline.plot(fig, output_type='div')

        self.webView.setHtml(div)

    def plot_chart_1(self):

        # TODO aggiungere linea 
        import random

        x = [['02h-03h', '03h-04h', '04h-05h', '05h-06h',
             '06h-07h', '07h-08h', '08h-09h', '09h-10h', '10h-11h', '11h-12h',
             '12h-13h', '13h-14h', '14h-15h', '15h-16h', '16h-17h', '17h-18h',
              '18h-19h', '19h-20h', '20h-21h', '21h-22h', '22h-23h', '23h-24h'],
             ['00h-01h', '01h-02h', '02h-03h', '03h-04h', '04h-05h', '05h-06h',
             '06h-07h', '07h-08h', '08h-09h', '09h-10h', '10h-11h', '11h-12h',
             '12h-13h', '13h-14h', '14h-15h', '15h-16h', '16h-17h', '17h-18h',
             '18h-19h', '19h-20h', '20h-21h', '21h-22h', '22h-23h',]]

        y = [[random.randint(0, 3000) for _ in range(22)],
             [random.randint(0, 3000) for _ in range(23)],
             [random.randint(0, 3000) for _ in range(24)],
             [random.randint(0, 3000) for _ in range(24)],
             [random.randint(0, 3000) for _ in range(24)],
             [random.randint(0, 3000) for _ in range(24)],
             [random.randint(0, 3000) for _ in range(24)]]

        colors = ['rgb(255, 0, 0)',
                  'rgb(255, 128, 0)',
                  'rgb(255, 255, 0)',
                  'rgb(128, 255, 0)',
                  'rgb(0, 255, 255)',
                  'rgb(0, 128, 255)',
                  'rgb(0, 0, 255)']

        data = []
        for i in range(1, -1, -1):
            data.append(
                go.Scatter(
                    x=x[i],
                    y=y[i],
                    name="Jour {}".format(i+1),
                    marker=dict(
                        color=colors[i]
                    )
                )
            )

        layout = go.Layout(
            title='Véhicules par heure',
            xaxis=dict(tickangle=-45),
            barmode='group'
        )

        fig = go.Figure(data=data, layout=layout)
        div = plotly.offline.plot(fig, output_type='div')

        self.webView.setHtml(div)

    def plot_chart_2(self):

        labels = ['CAR (1)',
                  'MR (2)',
                  'PW (3)',
                  'PW+ANH (4)',
                  'LIE (5)',
                  'LIE+ANH (6)',
                  'LIE+AUFL (7)',
                  'LW (8)',
                  'LZ (9)',
                  'SZ (10)']
        values = [4522, 2500, 1053, 51, 345, 12, 22, 430, 76, 12]

        pie = go.Pie(labels=labels, values=values)

        layout = go.Layout(title="Véhicules groupés par catégorie")
        fig = go.Figure(data=[pie], layout=layout)
        div = plotly.offline.plot(fig, output_type='div')

        self.webView.setHtml(div)
