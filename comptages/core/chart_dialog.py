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

        # data = [go.Scatter(x=[1, 2, 3, 4, 5, 6, 7, 8], y=[4, 3, 2, 1, 2, 3, 4])]
        # layout = go.Layout(title="hello world")

        # TODO aggiungere linea 
        import random
        
        x = ['00h-01h', '01h-02h', '02h-03h', '03h-04h', '04h-05h', '05h-06h',
             '06h-07h', '07h-08h', '08h-09h', '09h-10h', '10h-11h', '11h-12h',
             '12h-13h', '13h-14h', '14h-15h', '15h-16h', '16h-17h', '17h-18h',
             '18h-19h', '19h-20h', '20h-21h', '21h-22h', '22h-23h', '23h-24h', ]

        data = []
        for i in range(7):
            data.append(
                go.Bar(
                    x=x,
                    y=[random.randint(0, 3000) for _ in range(24)],
                    name=f"Jour {i}",
                    marker=dict(
                        color='rgb(49, 130, 189)'
                    )
                )
            )

        layout = go.Layout(
            xaxis=dict(tickangle=-45),
            barmode='group'
        )

        fig = go.Figure(data=data, layout=layout)
        div = plotly.offline.plot(fig, output_type='div')

        self.webView.setHtml(div)

    def plot_chart_2(self):

        import random

        
