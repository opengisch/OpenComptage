from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtWidgets import QDockWidget, QListWidgetItem
from comptages.core.utils import get_ui_class
from comptages.ui.resources import *

import plotly
import plotly.graph_objs as go

FORM_CLASS = get_ui_class('chart_dock.ui')


class ChartDock(QDockWidget, FORM_CLASS):
    def __init__(self, iface, parent=None):
        QDockWidget.__init__(self, parent)
        self.setupUi(self)

        self.chartList_icons = [
            QListWidgetItem(
                QIcon(':/plugins/Comptages/images/power.png'), ""),
            QListWidgetItem(
                QIcon(':/plugins/Comptages/images/measure.png'), ""),
            QListWidgetItem(
                QIcon(':/plugins/Comptages/images/filter.png'), ""),
        ]

        for i in self.chartList_icons:
            self.chartList.addItem(i)

        self.chartList.setCurrentRow(0)

    def plot_chart_1(self):

        # TODO aggiungere linea 
        import random
        
        x = ['00h-01h', '01h-02h', '02h-03h', '03h-04h', '04h-05h', '05h-06h',
             '06h-07h', '07h-08h', '08h-09h', '09h-10h', '10h-11h', '11h-12h',
             '12h-13h', '13h-14h', '14h-15h', '15h-16h', '16h-17h', '17h-18h',
             '18h-19h', '19h-20h', '20h-21h', '21h-22h', '22h-23h', '23h-24h', ]

        y = [[random.randint(0, 3000) for _ in range(24)],
             [random.randint(0, 3000) for _ in range(24)],
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
        for i in range(7):
            data.append(
                go.Bar(
                    x=x,
                    y=y[i],
                    name="Jour {}".format(i+1),
                    marker=dict(
                        color=colors[i]
                    )
                )
            )

        for i in range(7):
            data.append(
                go.Scatter(
                    x=x,
                    y=y[i],
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

    def plot_chart_3(self):
        
        bar = go.Bar(x=['0-10 km/h', '10-20 km/h', '20-30 km/h', '30-40 km/h', '40-50 km/h', '50-60 km/h', '60-70 km/h', '70-80 km/h', '80-90 km/h', '90-100 km/h'],
                      y=['20', '10', '34', '230', '650', '570', '230', '27', '12', '2'])

        layout = go.Layout(title='Véhicules groupés par vitesse')
        fig = go.Figure(data=[bar], layout=layout)
        div = plotly.offline.plot(fig, output_type='div')

        self.webView.setHtml(div)
