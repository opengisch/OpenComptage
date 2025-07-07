import os
from datetime import date, datetime
from typing import Optional

from qgis.core import QgsTask, Qgis, QgsMessageLog

from comptages.core import report


class ReportTask(QgsTask):
    def __init__(
        self,
        file_path,
        count=None,
        year=None,
        template="default",
        section_id=None,
        selected_sections_dates: Optional[dict[str, list[date]]] = None,
    ):
        self.basename = os.path.basename(file_path)
        super().__init__("Génération du rapport: {}".format(self.basename))

        self.count = count
        self.file_path = file_path
        self.template = template
        self.year = year
        self.section_id = section_id
        self.sections_dates = selected_sections_dates

    def run(self):
        try:
            report.prepare_reports(
                self.file_path,
                self.count,
                self.year,
                self.template,
                sections_ids=[self.section_id] if self.section_id else None,
                callback_progress=self.setProgress,
                sections_days=self.sections_dates,
            )
            return True
        except Exception as e:
            self.exception = e
            raise e
            # return False

    def finished(self, result):
        if result:
            QgsMessageLog.logMessage(
                "{} - Task report generation ended for {}".format(
                    datetime.now(), self.file_path
                ),
                "Comptages",
                Qgis.Info,
            )

        else:
            QgsMessageLog.logMessage(
                "{} - Task report generation creation for {} ended with errors: {}".format(
                    datetime.now(), self.file_path, self.exception
                ),
                "Comptages",
                Qgis.Warning,
            )
