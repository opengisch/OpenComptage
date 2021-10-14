import os
from datetime import datetime

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog
from qgis.PyQt.QtCore import QObject, Qt, QDateTime
from qgis.core import (
    QgsMessageLog, Qgis, QgsApplication, QgsExpressionContextUtils,
    QgsProject)
from qgis.utils import qgsfunction, plugins


from comptages.core.settings import Settings, SettingsDialog
from comptages.core.layers import Layers
from comptages.core.filter_dialog import FilterDialog
from comptages.core.yearly_report_dialog import YearlyReportDialog
from comptages.core.utils import push_info
from comptages.importer.data_importer import DataImporter
from comptages.importer.data_importer_vbv1 import DataImporterVbv1
from comptages.importer.data_importer_int2 import DataImporterInt2
from comptages.importer.data_importer_mc import DataImporterMC
from comptages.chart.chart_dialog import ChartDock
from comptages.config.config_creator import ConfigCreatorCmd
from comptages.plan.plan_creator import PlanCreator
from comptages.report.report_creator import ReportCreator
from comptages.report.yearly_report_creator import YearlyReportCreator
from comptages.report.yearly_report_bike import YearlyReportBike
from comptages.ics.ics_importer import IcsImporter
from comptages.ui.resources import *


class Comptages(QObject):

    def __init__(self, iface):
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
        self.filter_tjm = None
        self.filter_axe = None
        self.tm = QgsApplication.taskManager()

    def initGui(self):
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

        self.yearly_report_action = QAction(
            QIcon(':/plugins/Comptages/images/filled_file.png'),
            'Rapport annuel',
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

        self.yearly_report_action.triggered.connect(
            self.do_yearly_report_action)

        self.import_ics_action.triggered.connect(
            self.do_import_ics_action)

        self.settings_action.triggered.connect(
            self.do_settings_action)

        self.create_new_action.setEnabled(False)
        self.select_edit_action.setEnabled(False)
        self.import_files_action.setEnabled(False)
        self.validate_imported_files.setEnabled(False)
        self.filter_action.setEnabled(False)
        self.yearly_report_action.setEnabled(False)
        self.import_ics_action.setEnabled(False)

        self.iface.addPluginToMenu('Comptages', self.connect_db_action)
        self.iface.addPluginToMenu('Comptages', self.create_new_action)
        self.iface.addPluginToMenu('Comptages', self.select_edit_action)
        self.iface.addPluginToMenu('Comptages', self.import_files_action)
        self.iface.addPluginToMenu('Comptages', self.validate_imported_files)
        self.iface.addPluginToMenu('Comptages', self.filter_action)
        self.iface.addPluginToMenu('Comptages', self.yearly_report_action)
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
        self.toolbar.addAction(self.yearly_report_action)
        self.toolbar.addAction(self.import_ics_action)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.settings_action)

    def unload(self):
        self.iface.removePluginMenu('Comptages', self.connect_db_action)
        self.iface.removePluginMenu('Comptages', self.create_new_action)
        self.iface.removePluginMenu('Comptages', self.select_edit_action)
        self.iface.removePluginMenu('Comptages', self.filter_action)
        self.iface.removePluginMenu('Comptages', self.yearly_report_action)
        self.iface.removePluginMenu('Comptages', self.import_ics_action)
        self.iface.removePluginMenu('Comptages', self.settings_action)

        del self.connect_db_action
        del self.create_new_action
        del self.select_edit_action
        del self.filter_action
        del self.yearly_report_action
        del self.import_ics_action
        del self.settings_action

        del self.toolbar

    def do_connect_db_action(self):
        self.layers.load_layers()
        self.enable_actions_if_needed()

    def do_create_new_action(self):
        if self.tm.countActiveTasks() > 0:
            push_info(("Veuillez patienter jusqu'à ce que l'importation "
                       "soit terminée."))
            return
        self.layers.create_count()

    def do_select_edit_action(self):
        if self.tm.countActiveTasks() > 0:
            push_info(("Veuillez patienter jusqu'à ce que l'importation "
                       "soit terminée."))
            return
        self.layers.edit_count()

    def do_import_files_action(self):
        if self.tm.countActiveTasks() > 0:
            push_info(("Veuillez patienter jusqu'à ce que l'importation "
                       "soit terminée."))
            return
        file_dialog = QFileDialog()
        title = 'Importer'
        path = self.settings.value('data_import_directory')
        files = QFileDialog.getOpenFileNames(
            file_dialog, title, path,
            "Data file (*.A?? *.aV? *.I?? *.V?? *.txt)")[0]

        for file_path in files:
            self.import_file(file_path)

    def import_file(self, file_path, count_id=None):

        # Manage binary files
        with open(file_path, 'rb') as fd:
            file_head = fd.read(24)

        if file_head == b'Golden River Traffic Ltd':  # is a binary file
            formatter = self.layers.get_formatter_name('GoldenRiver')
            file_path_formatted = "{}_for".format(file_path)
            os.system("{} {} {}".format(
                formatter, file_path, file_path_formatted))
            file_path = file_path_formatted

        file_header = DataImporter.parse_file_header(file_path)

        if not count_id:
            count_id = self.layers.guess_count_id(
                file_header['SITE'],
                datetime.strptime(file_header['STARTREC'], "%H:%M %d/%m/%y"),
                datetime.strptime(file_header['STOPREC'], "%H:%M %d/%m/%y"))

        if not count_id:
            QgsMessageLog.logMessage(
                """Impossible de trouver le comptage associé {}:
                section: {} start: {} end: {}""".format(
                    file_path,
                    file_header['SITE'],
                    datetime.strptime(file_header['STARTREC'], "%H:%M %d/%m/%y"),
                    datetime.strptime(file_header['STOPREC'], "%H:%M %d/%m/%y")
                ),
                'Comptages', Qgis.Critical)
            return

        QgsMessageLog.logMessage(
            'Importation {}'.format(os.path.basename(file_path)),
            'Comptages', Qgis.Info)

        file_format = file_header['FORMAT']

        if file_format == 'VBV-1':
            task = DataImporterVbv1(file_path, count_id)
        elif file_format == 'INT-2':
            task = DataImporterInt2(file_path, count_id)
        elif file_format == 'MC':
            task = DataImporterMC(file_path, count_id)
        else:
            push_info('Format {} of {} not supported'.format(
                file_format,
                os.path.basename(file_path)))
            return

        self.tm.allTasksFinished.connect(self.task_finished)
        self.tm.addTask(task)
        return task

    def task_finished(self):
        self.tm.allTasksFinished.disconnect(self.task_finished)
        push_info(('Toutes les tâches sont terminées. Consultez le journal '
                   'pour plus de détails.'))
        self.chart_dock.show_next_quarantined_chart()

    def do_validate_imported_files_action(self):
        if self.tm.countActiveTasks() > 0:
            push_info(("Veuillez patienter jusqu'à ce que l'importation "
                       "soit terminée."))
            return
        self.chart_dock.show_next_quarantined_chart()

    def do_filter_action(self):
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
        if self.filter_tjm:
            # dlg.tjm.setRange(self.filter_tjm[0], self.filter_tjm[1])
            dlg.tjm_min.setValue(self.filter_tjm[0])
            dlg.tjm_max.setValue(self.filter_tjm[1])
        else:
            # dlg.tjm.setRange(0, 30000)
            dlg.tjm_min.setValue(0)
            dlg.tjm_max.setValue(30000)
        if self.filter_axe:
            dlg.axe.setCurrentIndex(self.filter_axe)

        if dlg.exec_():
            self.filter_start_date = dlg.start_date.dateTime()
            self.filter_end_date = dlg.end_date.dateTime()
            self.filter_installation = dlg.installation.currentIndex()
            self.filter_sensor = dlg.sensor.currentIndex()
            # self.filter_tjm = [dlg.tjm.lowerValue(), dlg.tjm.upperValue()]
            self.filter_tjm = [dlg.tjm_min.value(), dlg.tjm_max.value()]
            self.filter_axe = dlg.axe.currentIndex()

            self.layers.apply_filter(
                dlg.start_date.dateTime().toString('yyyy-MM-dd'),
                dlg.end_date.dateTime().toString('yyyy-MM-dd'),
                dlg.installation.currentIndex(),
                dlg.sensor.currentIndex(),
                [self.filter_tjm[0], self.filter_tjm[1]],
                dlg.axe.currentData(),
            )

            if (not dlg.start_date.dateTime()) and (not dlg.end_date.dateTime()) and (dlg.installation.currentIndex() == 0) and \
               (dlg.sensor.currentIndex() == 0) and (dlg.tjm_min.value() == 0) and (dlg.tjm_max.value() == 30000) and \
               (dlg.axe.currentText() == 'Tous'):
                self.filter_action.setIcon(
                    QIcon(':/plugins/Comptages/images/filter.png'))
            else:
                self.filter_action.setIcon(
                    QIcon(':/plugins/Comptages/images/filter_active.png'))

    def do_yearly_report_action(self):

        if self.tm.countActiveTasks() > 0:
            push_info(("Veuillez patienter jusqu'à ce que l'importation "
                       "soit terminée."))
            return

        layer = self.layers.layers['section']

        selected_count = layer.selectedFeatureCount()
        if selected_count == 0:
            push_info("Veuillez sélectionner un tronçon")
            return
        elif selected_count > 1:
            push_info("Veuillez ne sélectionner qu'un tronçon")
            return
        else:
            selected_feature = next(layer.getSelectedFeatures())

        section_id = selected_feature.attribute('id')

        classes = self.layers.get_classes_of_section(section_id)
        dlg = YearlyReportDialog(self.iface)
        dlg.section.insert(section_id)
        dlg.classi.addItems(classes)

        if dlg.exec_():
            year = dlg.year.value()
            clazz = dlg.classi.currentText()

            file_dialog = QFileDialog()
            title = 'Exporter un rapport'
            path = self.settings.value('report_export_directory')
            file_path = QFileDialog.getExistingDirectory(
                file_dialog, title, path)
            print(file_path)

            if not file_path:
                return

            if clazz.startswith("SPCH-MD"):
                yrb = YearlyReportBike(file_path, year, section_id)
                yrb.run()
            else:
                yearly_report_creator = YearlyReportCreator(
                    file_path, self.layers, year, section_id, clazz)
                yearly_report_creator.run()


            push_info("Tronçon {} (année={}): Génération du rapport annuel terminée."
                      .format(section_id, year))

            # TODO: check if there are comptages for this section and year

    def do_import_ics_action(self):
        IcsImporter(self.layers)

    def do_settings_action(self):
        self.settings_dialog.exec_()

    def do_export_configuration_action(self, count_id):
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
        file_dialog = QFileDialog()
        title = 'Importation'
        path = self.settings.value('data_import_directory')
        file_path = QFileDialog.getOpenFileName(
            file_dialog, title, path,
            "Data file (*.A?? *.aV? *.I?? *.V?? *.txt)")[0]

        if not file_path:
            return

        self.import_file(file_path, count_id)

    def do_generate_report_action(self, count_id):

        if self.tm.countActiveTasks() > 0:
            push_info(("Veuillez patienter jusqu'à ce que l'importation "
                       "soit terminée."))
            return

        # Show message if there are no data to process
        contains_data = self.layers.count_contains_data(count_id)
        if not contains_data:
            push_info("Installation {}: Il n'y a pas de données à traiter pour "
                "le comptage {}".format(
                self.layers.get_installation_name_of_count(count_id),count_id))
            return

        file_dialog = QFileDialog()
        title = 'Exporter un rapport'
        path = self.settings.value('report_export_directory')
        file_path = QFileDialog.getExistingDirectory(
            file_dialog, title, path)
        print(file_path)

        if not file_path:
            return

        report_creator = ReportCreator(count_id, file_path, self.layers)
        report_creator.run()
        push_info("Installation {} (count={}): Génération du rapport terminée."
         .format(self.layers.get_installation_name_of_count(count_id),count_id))

    def do_export_plan_action(self, count_id):
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

        # Highlight the current sections and installation in the layout
        previous_highlightes_sections = self.layers.highlighted_sections
        self.layers.highlighted_sections = \
            self.layers.get_section_ids_of_count(count_id)
        QgsExpressionContextUtils.setProjectVariable(
            QgsProject.instance(), 'highlighted_installation',
            self.layers.get_installation_name_of_count(count_id))

        plan_creator.export_pdf(count_id, file)

        self.layers.highlighted_sections = previous_highlightes_sections
        QgsExpressionContextUtils.setProjectVariable(
            QgsProject.instance(), 'highlighted_installation',
            '')
        self.layers.layers['section'].triggerRepaint()

    def do_generate_chart_action(self, count_id):

        if self.tm.countActiveTasks() > 0:
            push_info(("Veuillez patienter jusqu'à ce que l'importation "
                       "soit terminée."))
            return
        self.chart_dock.set_attributes(count_id)

    def enable_actions_if_needed(self):
        """Enable actions if the plugin is connected to the db
        otherwise disable them"""
        self.create_new_action.setEnabled(True)
        self.select_edit_action.setEnabled(True)
        self.import_files_action.setEnabled(True)
        self.validate_imported_files.setEnabled(True)
        self.import_ics_action.setEnabled(True)
        self.filter_action.setEnabled(True)
        self.yearly_report_action.setEnabled(True)

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
