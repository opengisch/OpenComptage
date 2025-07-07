import os
import pytz
from datetime import date, datetime, timedelta
from functools import partial

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QFileDialog, QMessageBox
from qgis.PyQt.QtCore import QObject, Qt, QDateTime
from qgis.core import (
    QgsMessageLog,
    Qgis,
    QgsApplication,
    QgsExpressionContextUtils,
    QgsProject,
)
from qgis.utils import qgsfunction, plugins

from comptages.core.settings import Settings, SettingsDialog
from comptages.core.layers import Layers
from comptages.core.filter_dialog import FilterDialog
from comptages.core.yearly_report_dialog import YearlyReportDialog
from comptages.core.delete_dialog import DeleteDialog
from comptages.core.utils import push_info, push_error
from comptages.core.statistics import get_valid_days
from comptages.datamodel import models
from comptages.core import importer, importer_task, report, report_task
from comptages.chart.chart_dialog import ChartDock
from comptages.config.config_creator import ConfigCreatorCmd
from comptages.plan.plan_creator import PlanCreator
from comptages.report.yearly_report_bike import YearlyReportBike
from comptages.ics.ics_importer import IcsImporter
from comptages.ui.resources import *
from comptages.ui.select_reports import SelectSectionsToReport
from comptages.core import definitions

from django.core.management import call_command


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
        self.filter_sector = None
        self.tm = QgsApplication.taskManager()

    def initGui(self):
        self.connect_db_action = QAction(
            QIcon(":/plugins/Comptages/images/power.png"),
            "Connection DB",
            self.iface.mainWindow(),
        )

        self.create_new_action = QAction(
            QIcon(":/plugins/Comptages/images/measure.png"),
            "Créer un nouveau comptage",
            None,
        )

        self.select_edit_action = QAction(
            QIcon(":/plugins/Comptages/images/select_edit.png"),
            "Modifier comptage",
            None,
        )

        self.import_files_action = QAction(
            QIcon(":/plugins/Comptages/images/import.png"), "Importation", None
        )

        self.validate_imported_files = QAction(
            QIcon(":/plugins/Comptages/images/validate.png"), "Validation", None
        )

        self.filter_action = QAction(
            QIcon(":/plugins/Comptages/images/filter.png"), "Filtrer", None
        )

        self.yearly_report_action = QAction(
            QIcon(":/plugins/Comptages/images/filled_file.png"), "Rapport annuel", None
        )

        self.import_ics_action = QAction(
            QIcon(":/plugins/Comptages/images/calendar.png"),
            "Importer fichier ics",
            None,
        )

        self.settings_action = QAction(
            QIcon(":/plugins/Comptages/images/settings.png"), "Réglages", None
        )

        self.connect_db_action.triggered.connect(self.do_connect_db_action)

        self.create_new_action.triggered.connect(self.do_create_new_action)

        self.select_edit_action.triggered.connect(self.do_select_edit_action)

        self.import_files_action.triggered.connect(self.do_import_files_action)

        self.validate_imported_files.triggered.connect(
            self.do_validate_imported_files_action
        )

        self.filter_action.triggered.connect(self.do_filter_action)

        self.yearly_report_action.triggered.connect(self.do_yearly_report_action)

        self.import_ics_action.triggered.connect(self.do_import_ics_action)

        self.settings_action.triggered.connect(self.do_settings_action)

        self.create_new_action.setEnabled(False)
        self.select_edit_action.setEnabled(False)
        self.import_files_action.setEnabled(False)
        self.validate_imported_files.setEnabled(False)
        self.filter_action.setEnabled(False)
        self.yearly_report_action.setEnabled(False)
        self.import_ics_action.setEnabled(False)

        self.iface.addPluginToMenu("Comptages", self.connect_db_action)
        self.iface.addPluginToMenu("Comptages", self.create_new_action)
        self.iface.addPluginToMenu("Comptages", self.select_edit_action)
        self.iface.addPluginToMenu("Comptages", self.import_files_action)
        self.iface.addPluginToMenu("Comptages", self.validate_imported_files)
        self.iface.addPluginToMenu("Comptages", self.filter_action)
        self.iface.addPluginToMenu("Comptages", self.yearly_report_action)
        self.iface.addPluginToMenu("Comptages", self.import_ics_action)
        self.iface.addPluginToMenu("Comptages", self.settings_action)

        self.toolbar = self.iface.addToolBar("Comptages")
        self.toolbar.setObjectName("Comptages")
        self.toolbar.setToolTip("Comptages toolbar")

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
        self.iface.removePluginMenu("Comptages", self.connect_db_action)
        self.iface.removePluginMenu("Comptages", self.create_new_action)
        self.iface.removePluginMenu("Comptages", self.select_edit_action)
        self.iface.removePluginMenu("Comptages", self.filter_action)
        self.iface.removePluginMenu("Comptages", self.yearly_report_action)
        self.iface.removePluginMenu("Comptages", self.import_ics_action)
        self.iface.removePluginMenu("Comptages", self.settings_action)

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
            push_info(
                ("Veuillez patienter jusqu'à ce que l'importation " "soit terminée.")
            )
            return
        self.layers.create_count()

    def do_select_edit_action(self):
        if self.tm.countActiveTasks() > 0:
            push_info(
                ("Veuillez patienter jusqu'à ce que l'importation " "soit terminée.")
            )
            return
        self.layers.edit_count()

    def do_import_files_action(self):
        if self.tm.countActiveTasks() > 0:
            push_info(
                ("Veuillez patienter jusqu'à ce que l'importation " "soit terminée.")
            )
            return
        file_dialog = QFileDialog()
        title = "Importer"
        path = self.settings.value("data_import_directory")
        files = QFileDialog.getOpenFileNames(
            file_dialog, title, path, "Data file (*.A?? *.aV? *.I?? *.V?? *.txt)"
        )[0]

        self.tm.allTasksFinished.connect(partial(self.all_tasks_finished, "import"))

        tasks = []
        for file_path in files:
            tasks.append(self.import_file(file_path))

        for t in tasks:
            self.tm.addTask(t)

    def import_file(self, file_path, count_id=None):
        QgsMessageLog.logMessage(
            "{} - Prepare import file {} started".format(
                datetime.now(), os.path.basename(file_path)
            ),
            "Comptages",
            Qgis.Info,
        )

        # Manage binary files
        with open(file_path, "rb") as fd:
            file_head = fd.read(24)

        if file_head == b"Golden River Traffic Ltd":  # is a binary file
            formatter = self.layers.get_formatter_name("GoldenRiver")
            file_path_formatted = "{}_for".format(file_path)
            os.system("{} {} {}".format(formatter, file_path, file_path_formatted))
            file_path = file_path_formatted

        if count_id:
            count = models.Count.objects.get(id=count_id)
        else:
            count = importer.guess_count(file_path)

        if not count:
            QgsMessageLog.logMessage(
                "Impossible de trouver le comptage associé {}".format(
                    file_path,
                ),
                "Comptages",
                Qgis.Critical,
            )
            return

        QgsMessageLog.logMessage(
            "{} - Prepare import file {} ended".format(
                datetime.now(), os.path.basename(file_path)
            ),
            "Comptages",
            Qgis.Info,
        )

        task = importer_task.ImporterTask(file_path, count)
        return task

    def all_tasks_finished(self, task="import"):
        # Check if actually all tasks are finished because apparently it doesn't
        # work the same on all systems
        if not self.tm.countActiveTasks() == 0:
            QgsMessageLog.logMessage(
                "{} - all_tasks_finished signal raised, but active tasks still exist, ignoring it".format(
                    datetime.now()
                ),
                "Comptages",
                Qgis.Warning,
            )

            return

        self.tm.allTasksFinished.disconnect()
        push_info(
            (
                "Toutes les tâches sont terminées. Consultez le journal "
                "pour plus de détails."
            )
        )
        QgsMessageLog.logMessage(
            "{} - All tasks ended".format(datetime.now()), "Comptages", Qgis.Info
        )

        if task == "import":
            self.chart_dock.show_next_quarantined_chart()

    def do_validate_imported_files_action(self):
        if self.tm.countActiveTasks() > 0:
            push_info(
                ("Veuillez patienter jusqu'à ce que l'importation " "soit terminée.")
            )
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
            dlg.tjm.setRange(self.filter_tjm[0], self.filter_tjm[1])
        else:
            dlg.tjm.setRange(0, 30000)
        if self.filter_axe:
            dlg.axe.setCurrentIndex(self.filter_axe)

        if self.filter_sector:
            dlg.sector.setCurrentIndex(self.filter_sector)

        if dlg.exec_():
            self.filter_start_date = dlg.start_date.dateTime()
            self.filter_end_date = dlg.end_date.dateTime()
            self.filter_installation = dlg.installation.currentIndex()
            self.filter_sensor = dlg.sensor.currentIndex()
            self.filter_tjm = [dlg.tjm.lowerValue(), dlg.tjm.upperValue()]
            self.filter_axe = dlg.axe.currentIndex()
            self.filter_sector = dlg.sector.currentIndex()

            self.layers.apply_filter(
                dlg.start_date.dateTime().toString("yyyy-MM-dd"),
                dlg.end_date.dateTime().toString("yyyy-MM-dd"),
                dlg.installation.currentIndex(),
                dlg.sensor.currentIndex(),
                [self.filter_tjm[0], self.filter_tjm[1]],
                dlg.axe.currentData(),
                dlg.sector.currentData(),
            )

            if (
                (not dlg.start_date.dateTime())
                and (not dlg.end_date.dateTime())
                and (dlg.installation.currentIndex() == 0)
                and (dlg.sensor.currentIndex() == 0)
                and (dlg.tjm.lowerValue() == 0)
                and (dlg.tjm.upperValue() == 30000)
                and (dlg.axe.currentText() == "Tous")
                and (dlg.sector.currentText() == "Tous")
            ):
                self.filter_action.setIcon(
                    QIcon(":/plugins/Comptages/images/filter.png")
                )
            else:
                self.filter_action.setIcon(
                    QIcon(":/plugins/Comptages/images/filter_active.png")
                )

    def do_yearly_report_action(self):
        QgsMessageLog.logMessage(
            "{} - Generate task for yearly report action started".format(
                datetime.now()
            ),
            "Comptages",
            Qgis.Info,
        )

        if self.tm.countActiveTasks() > 0:
            push_info(
                ("Veuillez patienter jusqu'à ce que l'importation soit terminée.")
            )
            return

        layer = self.layers.layers["section"]

        selected_count = layer.selectedFeatureCount()
        if selected_count == 0:
            push_info("Veuillez sélectionner un tronçon")
            return
        elif selected_count > 1:
            push_info("Veuillez ne sélectionner qu'un tronçon")
            return
        else:
            selected_feature = next(layer.getSelectedFeatures())

        section_id = selected_feature.attribute("id")
        section = models.Section.objects.get(id=section_id)
        classes = self.layers.get_classes_of_section(section_id)
        years = self.layers.get_years_of_counts_on_section(section_id)

        dlg = YearlyReportDialog(self.iface)
        dlg.section.insert(section_id)
        dlg.classi.addItems(classes)
        if years is not None:
            years.sort()
            dlg.year.setValue(years[-1])

        if dlg.exec_():
            year = dlg.year.value()
            clazz = dlg.classi.currentText()

            file_dialog = QFileDialog()
            title = "Exporter un rapport"
            path = self.settings.value("report_export_directory")
            file_path = QFileDialog.getExistingDirectory(file_dialog, title, path)

            if not file_path:
                QgsMessageLog.logMessage(
                    "{} - Generate task for yearly report action cancelled: No file_path given".format(
                        datetime.now()
                    ),
                    "Comptages",
                    Qgis.Info,
                )
                return
            QgsMessageLog.logMessage(
                "{} - Generate task for yearly report action can really begin now for count {} with file_path: {}".format(
                    datetime.now(), selected_count, file_path
                ),
                "Comptages",
                Qgis.Info,
            )

            # Do not proceed unless the number of processed days exceeds 100 days
            valid_days = get_valid_days(year, section)
            if valid_days < 100:
                push_error(
                    f"This section ({section_id}) lacks valid days for this year ({year}). Found only {valid_days} out of 100."
                )
                return

            if clazz.startswith("SPCH-MD"):
                yrb = YearlyReportBike(file_path, year, section_id, clazz)
                yrb.run()
            else:
                self.tm.allTasksFinished.connect(
                    partial(self.all_tasks_finished, "report")
                )

                # TODO: consider the chosed class too
                self.tm.addTask(
                    report_task.ReportTask(
                        file_path=file_path,
                        template="yearly",
                        year=year,
                        section_id=section_id,
                    )
                )
            # TODO: check if there are comptages for this section and year

        QgsMessageLog.logMessage(
            "{} - Generate task for yearly report action ended".format(datetime.now()),
            "Comptages",
            Qgis.Info,
        )

    def do_import_ics_action(self):
        IcsImporter(self.layers)

    def do_settings_action(self):
        self.settings_dialog.exec_()

    def do_export_configuration_action(self, count_id):
        config_creator = ConfigCreatorCmd(self.layers, count_id)
        config_creator.set_section_commands()

        installation_name = self.layers.get_installation_name_of_count(count_id)

        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix("*.CMD")
        title = "Exporter la configuration"
        path = os.path.join(
            self.settings.value("config_export_directory"),
            "{}.CMD".format(installation_name),
        )
        file = QFileDialog.getSaveFileName(
            file_dialog, title, path, "Config file (*.CMD)"
        )[0]

        if not file:
            return

        config_creator.write_file(file)
        push_info("Written config file {}".format(file))

    def do_import_single_file_action(self, count_id):
        file_dialog = QFileDialog()
        title = "Importation"
        path = self.settings.value("data_import_directory")
        file_path = QFileDialog.getOpenFileName(
            file_dialog, title, path, "Data file (*.A?? *.aV? *.I?? *.V?? *.txt)"
        )[0]

        if not file_path:
            return

        self.tm.allTasksFinished.connect(partial(self.all_tasks_finished, "import"))

        self.tm.addTask(self.import_file(file_path, count_id))

    def do_generate_report_action(self, count_id):
        QgsMessageLog.logMessage(
            "{} - Generate report preparation started for count_id {}".format(
                datetime.now(), count_id
            ),
            "Comptages",
            Qgis.Info,
        )

        count = models.Count.objects.get(id=count_id)

        if self.tm.countActiveTasks() > 0:
            push_info(
                (
                    "Veuillez patienter jusqu'à ce que l'importation soit terminée,"
                    " puis relancer la génération du rapport."
                )
            )
            return

        # Show message if there are no data to process
        if not models.CountDetail.objects.filter(id_count=count).exists():
            push_info(
                "Installation {}: Il n'y a pas de données à traiter pour "
                "le comptage {}".format(count.id_installation.name, count.id)
            )
            QgsMessageLog.logMessage(
                "{} - Generate report preparation ended: No data for count {}".format(
                    datetime.now(), count.id
                ),
                "Comptages",
                Qgis.Info,
            )
            return

        file_dialog = QFileDialog()
        mondays = report._mondays_of_count(count)
        sections_ids = (
            models.Section.objects.filter(lane__id_installation__count=count)
            .distinct()
            .values_list("id", flat=True)
        )
        report_selection_dialog = SelectSectionsToReport(
            sections_ids=list(sections_ids), mondays=list(mondays)
        )

        if report_selection_dialog.exec_():
            selected_sections_dates: dict[str, list[date]] = (
                report_selection_dialog.get_inputs()
            )
            date_choosen = list()
            for selsec in selected_sections_dates:
                date_choosen.extend(selected_sections_dates[selsec])
            if len(date_choosen) == 0:
                QgsMessageLog.logMessage(
                    "{} - Generate report preparation ended: Nothing choosen to report on".format(
                        datetime.now()
                    ),
                    "Comptages",
                    Qgis.Info,
                )
                return

            title = "Exporter un rapport"
            path = self.settings.value("report_export_directory")
            file_path = QFileDialog.getExistingDirectory(file_dialog, title, path)

            if not file_path:
                QgsMessageLog.logMessage(
                    "{} - Generate report preparation ended: No file_path given".format(
                        datetime.now()
                    ),
                    "Comptages",
                    Qgis.Info,
                )
                return

            QgsMessageLog.logMessage(
                f"""{datetime.now()} - Generate report action can really begin now for count {count.id} with file_path: {file_path}.
                Selected sections and dates: {selected_sections_dates}""",
                "Comptages",
                Qgis.Info,
            )

            self.tm.allTasksFinished.connect(partial(self.all_tasks_finished, "report"))
            self.tm.addTask(
                report_task.ReportTask(
                    file_path=file_path,
                    count=count,
                    selected_sections_dates=selected_sections_dates,
                )
            )
        else:
            QgsMessageLog.logMessage(
                "{} - Generate report preparation ended: Cancel buton clicked...".format(
                    datetime.now()
                ),
                "Comptages",
                Qgis.Info,
            )
            return

        QgsMessageLog.logMessage(
            "{} - Generate report preparation ended for count_id {}".format(
                datetime.now(), count_id
            ),
            "Comptages",
            Qgis.Info,
        )

    def do_export_plan_action(self, count_id):
        count = models.Count.objects.get(id=count_id)
        plan_creator = PlanCreator()
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix("*.PDF")
        title = "Exporter plan de pose"
        path = os.path.join(
            self.settings.value("config_export_directory"),
            "{}.pdf".format("plan_de_pose"),
        )
        file = QFileDialog.getSaveFileName(
            file_dialog, title, path, "Config file (*.PDF)"
        )[0]

        if not file:
            return

        # Highlight the current sections and installation in the layout
        previous_highlightes_sections = self.layers.highlighted_sections
        self.layers.highlighted_sections = self.layers.get_section_ids_of_count(
            count_id
        )
        QgsExpressionContextUtils.setProjectVariable(
            QgsProject.instance(),
            "highlighted_installation",
            self.layers.get_installation_name_of_count(count_id),
        )

        plan_creator.export_pdf(count, file)

        self.layers.highlighted_sections = previous_highlightes_sections
        QgsExpressionContextUtils.setProjectVariable(
            QgsProject.instance(), "highlighted_installation", ""
        )
        self.layers.layers["section"].triggerRepaint()

    def do_generate_chart_action(self, count_id):
        QgsMessageLog.logMessage(
            "{} - Generate chart action started".format(datetime.now()),
            "Comptages",
            Qgis.Info,
        )

        if self.tm.countActiveTasks() > 0:
            push_info(
                ("Veuillez patienter jusqu'à ce que l'importation " "soit terminée.")
            )
            return
        count = models.Count.objects.get(id=count_id)
        self.chart_dock.set_attributes(count)

        QgsMessageLog.logMessage(
            "{} - Generate chart action ended".format(datetime.now()),
            "Comptages",
            Qgis.Info,
        )

    def do_delete_data_action(self, count_id):
        dlg = DeleteDialog(self.iface)
        tz = pytz.timezone("Europe/Zurich")

        if dlg.exec_():
            start = tz.localize(dlg.start_date.dateTime().toPyDateTime())
            end = tz.localize(dlg.end_date.dateTime().toPyDateTime())
            definitive = dlg.definitive.isChecked()
            quarantine = dlg.quarantine.isChecked()
            count = models.Count.objects.get(id=count_id)

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Effacement des données")
            # msg.setInformativeText(f"Effacement des données")
            msg.setDetailedText(
                "Les données suivantes seront supprimées:\n"
                f"comptage: {count_id}\n"
                f"de: {start.strftime('%d.%m.%Y')}\n"
                f"à: {end.strftime('%d.%m.%Y')} inclus\n"
                f"provisoires: {quarantine}\n"
                f"définitives: {definitive}"
            )
            msg.setWindowTitle("Effacement des données")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = msg.exec_()
            if retval == QMessageBox.Ok:
                qs = models.CountDetail.objects.filter(
                    id_count=count,
                    timestamp__range=(start, end + timedelta(days=1)),
                )

                if not definitive:
                    qs = qs.filter(status=definitions.IMPORT_STATUS_QUARANTINE)

                if not quarantine:
                    qs = qs.filter(status=definitions.IMPORT_STATUS_DEFINITIVE)

                qs.delete()
                call_command("tjmreset")
                QgsMessageLog.logMessage(
                    "Les TJMs ont été réinitialisés; rouvrir cette fenêtre pour afficher les données actualisées!",
                    "Comptages",
                    Qgis.Info,
                )

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
        return plugins["comptages"].is_section_highlighted(feature.attribute("id"))

    @qgsfunction(args="auto", group="Comptages")
    def check_dates(feature, parent):
        """Used by count layer to show if a count was during a special
        period"""

        return plugins["comptages"].layers.check_dates(
            feature.attribute("start_process_date"),
            feature.attribute("end_process_date"),
        )
