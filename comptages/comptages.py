import os
from datetime import datetime

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.PyQt.QtCore import QObject, Qt, QDateTime
from qgis.core import QgsMessageLog, Qgis, QgsApplication
from qgis.utils import qgsfunction, plugins

from comptages.core.settings import Settings, SettingsDialog
from comptages.core.layers import Layers
from comptages.core.filter_dialog import FilterDialog
from comptages.core.chart_dialog import ChartDock
from comptages.core.utils import push_info
from comptages.data.data_importer import DataImporter
from comptages.data.data_importer_vbv1 import DataImporterVbv1
from comptages.data.data_importer_int2 import DataImporterInt2
from comptages.config.config_creator import ConfigCreatorCmd
from comptages.plan.plan_creator import PlanCreator
from comptages.report.report_creator import ReportCreator
from comptages.ics.ics_importer import IcsImporter
from comptages.ui.resources import *


class Comptages(QObject):

    def __init__(self, iface):
        QgsMessageLog.logMessage('__init__', 'Comptages', Qgis.Info)
        QObject.__init__(self)

        self.iface = iface
        self.settings = Settings()
        self.settings_dialog = SettingsDialog()
        self.layers = Layers()
        self.chart_dock = ChartDock(self.iface, self.layers)
        self.iface.addDockWidget(Qt.BottomDockWidgetArea, self.chart_dock)
        self.filter_start_date = None
        self.filter_end_date = None
        self.filter_installation = None
        self.filter_sensor = None
        self.tm = QgsApplication.taskManager()

    def initGui(self):
        QgsMessageLog.logMessage('initGui', 'Comptages', Qgis.Info)

        self.connect_db_action = QAction(
            QIcon(':/plugins/Comptages/images/power.png'),
            'Connection DB',
            self.iface.mainWindow()
        )

        self.create_new_action = QAction(
            QIcon(':/plugins/Comptages/images/measure.png'),
            'Créer un nouveau comptage',
            None
        )

        self.select_edit_action = QAction(
            QIcon(':/plugins/Comptages/images/select_edit.png'),
            'Modifier comptage',
            None
        )

        self.import_files_action = QAction(
            QIcon(':/plugins/Comptages/images/import.png'),
            'Importation',
            None
        )

        self.validate_imported_files = QAction(
            QIcon(':/plugins/Comptages/images/validate.png'),
            'Validation',
            None
        )

        self.filter_action = QAction(
            QIcon(':/plugins/Comptages/images/filter.png'),
            'Filtrer',
            None
        )

        self.import_ics_action = QAction(
            QIcon(':/plugins/Comptages/images/calendar.png'),
            'Importer fichier ics',
            None
        )

        self.settings_action = QAction(
            QIcon(':/plugins/Comptages/images/settings.png'),
            'Réglages',
            None
        )

        self.connect_db_action.triggered.connect(
            self.do_connect_db_action)

        self.create_new_action.triggered.connect(
            self.do_create_new_action)

        self.select_edit_action.triggered.connect(
            self.do_select_edit_action)

        self.import_files_action.triggered.connect(
            self.do_import_files_action)

        self.validate_imported_files.triggered.connect(
            self.do_validate_imported_files_action)

        self.filter_action.triggered.connect(
            self.do_filter_action)

        self.import_ics_action.triggered.connect(
            self.do_import_ics_action)

        self.settings_action.triggered.connect(
            self.do_settings_action)

        self.create_new_action.setEnabled(False)
        self.select_edit_action.setEnabled(False)
        self.import_files_action.setEnabled(False)
        self.validate_imported_files.setEnabled(False)
        self.filter_action.setEnabled(False)
        self.import_ics_action.setEnabled(False)

        self.iface.addPluginToMenu('Comptages', self.connect_db_action)
        self.iface.addPluginToMenu('Comptages', self.create_new_action)
        self.iface.addPluginToMenu('Comptages', self.select_edit_action)
        self.iface.addPluginToMenu('Comptages', self.import_files_action)
        self.iface.addPluginToMenu('Comptages', self.validate_imported_files)
        self.iface.addPluginToMenu('Comptages', self.filter_action)
        self.iface.addPluginToMenu('Comptages', self.import_ics_action)
        self.iface.addPluginToMenu('Comptages', self.settings_action)

        self.toolbar = self.iface.addToolBar('Comptages')
        self.toolbar.setObjectName('Comptages')
        self.toolbar.setToolTip('Comptages toolbar')

        self.toolbar.addAction(self.connect_db_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.create_new_action)
        self.toolbar.addAction(self.select_edit_action)
        self.toolbar.addAction(self.import_files_action)
        self.toolbar.addAction(self.validate_imported_files)
        self.toolbar.addAction(self.filter_action)
        self.toolbar.addAction(self.import_ics_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.settings_action)

    def unload(self):
        self.iface.removePluginMenu('Comptages', self.connect_db_action)
        self.iface.removePluginMenu('Comptages', self.create_new_action)
        self.iface.removePluginMenu('Comptages', self.select_edit_action)
        self.iface.removePluginMenu('Comptages', self.filter_action)
        self.iface.removePluginMenu('Comptages', self.import_ics_action)
        self.iface.removePluginMenu('Comptages', self.settings_action)

        del self.connect_db_action
        del self.create_new_action
        del self.select_edit_action
        del self.filter_action
        del self.import_ics_action
        del self.settings_action

        del self.toolbar

    def do_connect_db_action(self):
        QgsMessageLog.logMessage(
            'do_connect_db_action', 'Comptages', Qgis.Info)
        self.layers.load_layers()
        self.enable_actions_if_needed()

    def do_create_new_action(self):
        QgsMessageLog.logMessage(
            'do_create_new_action', 'Comptages', Qgis.Info)
        self.layers.create_count()

    def do_select_edit_action(self):
        QgsMessageLog.logMessage(
            'do_select_edit_action', 'Comptages', Qgis.Info)
        self.layers.edit_count()

    def do_import_files_action(self):
        QgsMessageLog.logMessage(
            'do_import_files_action', 'Comptages', Qgis.Info)

        file_dialog = QFileDialog()
        title = 'Importer'
        path = self.settings.value('data_import_directory')
        files = QFileDialog.getOpenFileNames(
            file_dialog, title, path, "Data file (*.A?? *.aV? *.I?? *.V??)")[0]

        for file_path in files:
            self.import_file(file_path)

    def import_file(self, file_path, count_id=None):

        file_header = DataImporter.parse_file_header(file_path)
        if not count_id:
            count_id = self.layers.guess_count_id(
                file_header['SITE'],
                datetime.strptime(file_header['STARTREC'], "%H:%M %d/%m/%y"),
                datetime.strptime(file_header['STOPREC'], "%H:%M %d/%m/%y"))

        if not count_id:
            QgsMessageLog.logMessage(
                'Impossible de trouver le comptage associé {}'.format(
                    file_path),
                'Comptages', Qgis.Critical)
            return

        QgsMessageLog.logMessage(
            'Importation {}'.format(file_path), 'Comptages', Qgis.Info)

        file_format = file_header['FORMAT']

        if file_format == 'VBV-1':
            task = DataImporterVbv1(file_path, count_id)
        elif file_format == 'INT-2':
            task = DataImporterInt2(file_path, count_id)
        else:
            push_info('Format {} of {} not supported'.format(
                file_format, file_path))
            return

        self.tm.addTask(task)
        return task

    def do_validate_imported_files_action(self):
        QgsMessageLog.logMessage(
            'do_validate_imported_files_action', 'Comptages', Qgis.Info)
        self.chart_dock.show_next_quarantined_chart()

    def do_filter_action(self):
        QgsMessageLog.logMessage(
            'do_filter_action', 'Comptages', Qgis.Info)
        dlg = FilterDialog(self.iface)

        # Set last values in the filter
        if self.filter_start_date:
            dlg.start_date.setDateTime(self.filter_start_date)
        else:
            dlg.start_date.setDateTime(QDateTime())
        if self.filter_end_date:
            dlg.end_date.setDateTime(self.filter_end_date)
        else:
            dlg.end_date.setDateTime(QDateTime())
        if self.filter_installation:
            dlg.installation.setCurrentIndex(self.filter_installation)
        if self.filter_sensor:
            dlg.sensor.setCurrentIndex(self.filter_sensor)

        if dlg.exec_():
            self.filter_start_date = dlg.start_date.dateTime()
            self.filter_end_date = dlg.end_date.dateTime()
            self.filter_installation = dlg.installation.currentIndex()
            self.filter_sensor = dlg.sensor.currentIndex()

            self.layers.apply_filter(
                dlg.start_date.dateTime().toString('yyyy-MM-dd'),
                dlg.end_date.dateTime().toString('yyyy-MM-dd'),
                dlg.installation.currentIndex(),
                dlg.sensor.currentIndex())

    def do_import_ics_action(self):
        QgsMessageLog.logMessage(
            'do_import_ics_action', 'Comptages', Qgis.Info)
        IcsImporter(self.layers)

    def do_settings_action(self):
        QgsMessageLog.logMessage(
            'do_settings_action', 'Comptages', Qgis.Info)
        self.settings_dialog.exec_()

    def do_export_configuration_action(self, count_id):
        QgsMessageLog.logMessage(
            'do_export_configuration_action {}'.format(count_id),
            'Comptages', Qgis.Info)
        config_creator = ConfigCreatorCmd(self.layers, count_id)
        config_creator.set_section_commands()

        installation_name = self.layers.get_installation_name_of_count(
            count_id)

        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix('*.CMD')
        title = 'Exporter la configuration'
        path = os.path.join(
            self.settings.value('config_export_directory'),
            "{}.CMD".format(installation_name))
        file = QFileDialog.getSaveFileName(
            file_dialog, title, path, "Config file (*.CMD)")[0]

        if not file:
            return

        config_creator.write_file(file)
        push_info('Written config file {}'.format(file))

    def do_import_single_file_action(self, count_id):
        QgsMessageLog.logMessage(
            'do_import_single_file_action {}'.format(count_id),
            'Comptages', Qgis.Info)

        file_dialog = QFileDialog()
        title = 'Importation'
        path = self.settings.value('data_import_directory')
        file_path = QFileDialog.getOpenFileName(
            file_dialog, title, path, "Data file (*.A?? *.aV? *.I?? *.V??)")[0]

        if not file_path:
            return

        self.import_file(file_path, count_id)

    def do_generate_report_action(self, count_id):
        QgsMessageLog.logMessage(
            'do_generate_report_action {}'.format(count_id),
            'Comptages', Qgis.Info)

        report_creator = ReportCreator(self.layers)
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix('*.PDF')
        title = 'Exporter un rapport'
        path = os.path.join(
            self.settings.value('report_export_directory'),
            "{}.pdf".format("report"))
        file = QFileDialog.getSaveFileName(
            file_dialog, title, path, "Config file (*.PDF)")[0]

        if not file:
            return

        report_creator.export_pdf(count_id, file)

    def do_export_plan_action(self, count_id):
        QgsMessageLog.logMessage(
            'do_export_plan_action {}'.format(count_id),
            'Comptages', Qgis.Info)

        plan_creator = PlanCreator(self.layers)
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix('*.PDF')
        title = 'Exporter plan de pose'
        path = os.path.join(
            self.settings.value('config_export_directory'),
            "{}.pdf".format("plan_de_pose"))
        file = QFileDialog.getSaveFileName(
            file_dialog, title, path, "Config file (*.PDF)")[0]

        if not file:
            return

        plan_creator.export_pdf(count_id, file)

    def do_generate_chart_action(self, count_id):
        QgsMessageLog.logMessage(
            'do_generate_chart_action {}'.format(count_id),
            'Comptages', Qgis.Info)
        self.chart_dock.set_attributes(count_id)

        self.chart_dock.show()

    def enable_actions_if_needed(self):
        """Enable actions if the plugin is connected to the db
        otherwise disable them"""
        self.create_new_action.setEnabled(True)
        self.select_edit_action.setEnabled(True)
        self.import_files_action.setEnabled(True)
        self.validate_imported_files.setEnabled(True)
        self.import_ics_action.setEnabled(True)
        self.filter_action.setEnabled(True)

    def is_section_highlighted(self, section_id):
        return self.layers.is_section_highlighted(section_id)

    @qgsfunction(args="auto", group="Comptages")
    def is_highlighted(feature, parent):
        """Used by section layer to apply a style to the sections related to a
        count"""

        # Call the method of the current instance of the plugin
        return plugins['comptages'].is_section_highlighted(
            feature.attribute('id'))

    @qgsfunction(args="auto", group="Comptages")
    def check_dates(feature, parent):
        """Used by count layer to show if a count was during a special
        period"""

        return plugins['comptages'].layers.check_dates(
            feature.attribute('start_process_date'),
            feature.attribute('end_process_date')
        )
