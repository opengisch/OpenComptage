from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.PyQt.QtCore import QObject, Qt
from qgis.core import QgsMessageLog, Qgis
from qgis.utils import qgsfunction, plugins

from comptages.core.settings import Settings, SettingsDialog
from comptages.core.layers import Layers
from comptages.core.filter_dialog import FilterDialog
from comptages.core.chart_dialog import ChartDock
from comptages.core.utils import push_info
from comptages.config.config_creator import ConfigCreatorCmd
from comptages.parser.data_parser import (
    DataParser, DataParserVbv1, DataParserInt2)
from comptages.ui.resources import *


class Comptages(QObject):

    def __init__(self, iface):
        QgsMessageLog.logMessage('__init__', 'Comptages', Qgis.Info)
        QObject.__init__(self)

        self.iface = iface
        self.settings = Settings()
        self.settings_dialog = SettingsDialog()
        self.layers = Layers()
        self.chart_dock = None

    def initGui(self):
        QgsMessageLog.logMessage('initGui', 'Comptages', Qgis.Info)

        self.connect_db_action = QAction(
            QIcon(':/plugins/Comptages/images/power.png'),
            'Connect DB',
            self.iface.mainWindow()
        )

        self.create_new_action = QAction(
            QIcon(':/plugins/Comptages/images/measure.png'),
            'Create new measure',
            None
        )

        self.select_edit_action = QAction(
            QIcon(':/plugins/Comptages/images/select_edit.png'),
            'Edit measure',
            None
        )

        self.filter_action = QAction(
            QIcon(':/plugins/Comptages/images/filter.png'),
            'Filter',
            None
        )

        self.settings_action = QAction(
            QIcon(':/plugins/Comptages/images/settings.png'),
            'Settings',
            None
        )

        self.connect_db_action.triggered.connect(
            self.do_connect_db_action)

        self.create_new_action.triggered.connect(
            self.do_create_new_action)

        self.select_edit_action.triggered.connect(
            self.do_select_edit_action)

        self.filter_action.triggered.connect(
            self.do_filter_action)

        self.settings_action.triggered.connect(
            self.do_settings_action)

        self.iface.addPluginToMenu('Comptages', self.connect_db_action)
        self.iface.addPluginToMenu('Comptages', self.create_new_action)
        self.iface.addPluginToMenu('Comptages', self.select_edit_action)
        self.iface.addPluginToMenu('Comptages', self.filter_action)
        self.iface.addPluginToMenu('Comptages', self.settings_action)

        self.toolbar = self.iface.addToolBar('Comptages')
        self.toolbar.setObjectName('Comptages')
        self.toolbar.setToolTip('Comptages toolbar')

        self.toolbar.addAction(self.connect_db_action)
        self.toolbar.addAction(self.create_new_action)
        self.toolbar.addAction(self.select_edit_action)
        self.toolbar.addAction(self.filter_action)
        self.toolbar.addAction(self.settings_action)

    def unload(self):
        self.iface.removePluginMenu('Comptages', self.connect_db_action)
        self.iface.removePluginMenu('Comptages', self.create_new_action)
        self.iface.removePluginMenu('Comptages', self.select_edit_action)
        self.iface.removePluginMenu('Comptages', self.filter_action)
        self.iface.removePluginMenu('Comptages', self.settings_action)

        del self.connect_db_action
        del self.create_new_action
        del self.select_edit_action
        del self.filter_action
        del self.settings_action

        del self.toolbar

    def do_connect_db_action(self):
        QgsMessageLog.logMessage(
            'do_connect_db_action', 'Comptages', Qgis.Info)
        self.layers.load_layers()

    def do_create_new_action(self):
        QgsMessageLog.logMessage(
            'do_create_new_action', 'Comptages', Qgis.Info)
        self.layers.create_count()

    def do_select_edit_action(self):
        QgsMessageLog.logMessage(
            'do_select_edit_action', 'Comptages', Qgis.Info)
        self.layers.edit_count()

    def do_filter_action(self):
        QgsMessageLog.logMessage(
            'do_filter_action', 'Comptages', Qgis.Info)
        dlg = FilterDialog(self.iface)
        if dlg.exec_():
            self.layers.apply_filter(
                dlg.start_date.dateTime().toString('yyyy-MM-dd'),
                dlg.end_date.dateTime().toString('yyyy-MM-dd'),
                dlg.installation.currentIndex(),
                dlg.sensor.currentIndex())

    def do_settings_action(self):
        QgsMessageLog.logMessage(
            'do_settings_action', 'Comptages', Qgis.Info)
        self.settings_dialog.exec_()

    def do_export_configuration_action(self, count_id):
        QgsMessageLog.logMessage(
            f'do_export_configuration_action {count_id}',
            'Comptages', Qgis.Info)
        config_creator = ConfigCreatorCmd(self.layers, count_id)
        config_creator.set_section_commands()

        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix('*.CMD')
        title = 'Export configuration file'
        path = '/home/mario/workspace/tmp/comptages_20181105/'
        file = QFileDialog.getSaveFileName(
            file_dialog, title, path, "Config file (*.CMD)")[0]
        config_creator.write_file(file)
        push_info(f'Written config file {file}')

    def do_import_data_action(self, count_id):
        QgsMessageLog.logMessage(
            f'do_import_data_action {count_id}',
            'Comptages', Qgis.Info)

        file_dialog = QFileDialog()
        title = 'Import data'
        path = '/home/mario/workspace/repos/OpenComptage/comptages/test/test_data/'
        file = QFileDialog.getOpenFileName(
            file_dialog, title, path, "Data file (*.A?? *.aV? *.I?? *.V??)")[0]

        format = DataParser.get_format(file)

        if format == 'VBV-1':
            data_parser = DataParserVbv1(self.layers, count_id, file)
            data_parser.parse_data()
        elif format == 'INT-2':
            data_parser = DataParserInt2(self.layers, count_id, file)
            data_parser.parse_data()
        else:
            push_info('Format not supported')
            return

    def do_generate_report_action(self, count_id):
        QgsMessageLog.logMessage(
            f'do_generate_report_action {count_id}',
            'Comptages', Qgis.Info)

    def do_export_plan_action(self, count_id):
        QgsMessageLog.logMessage(
            f'do_export_plan_action {count_id}',
            'Comptages', Qgis.Info)

    def do_generate_chart_action(self, count_id):
        QgsMessageLog.logMessage(
            f'do_generate_chart_action {count_id}',
            'Comptages', Qgis.Info)
        if not self.chart_dock:
            self.chart_dock = ChartDock(self.iface)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.chart_dock)

        self.chart_dock.show()
        self.chart_dock.plot_chart_1()

    def enable_actions_if_needed(self):
        """Enable actions if the plugin is connected to the db
        otherwise disable them"""
        pass

    def is_connected(self):
        """Return if the plugin is connected to the database"""
        pass

    def is_section_highlighted(self, section_id):
        return self.layers.is_section_highlighted(section_id)

    @qgsfunction(args="auto", group="Comptages")
    def is_highlighted(feature, parent):
        """Used by section layer to apply a style to the sections related to a
        count"""

        # Call the class method of the current instance of the plugin
        return plugins['comptages'].is_section_highlighted(
            feature.attribute('id'))
