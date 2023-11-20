import os
from datetime import datetime
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
        only_sections_ids: Optional[list[str]] = None,
    ):
        self.basename = os.path.basename(file_path)
        super().__init__("Génération du rapport: {}".format(self.basename))

        self.count = count
        self.file_path = file_path
        self.template = template
        self.year = year
        self.section_id = section_id
        self.only_sections_ids = only_sections_ids

    def run(self):
        try:
            report.prepare_reports(
                self.file_path,
                self.count,
                self.year,
                self.template,
                self.section_id,
                self.only_sections_ids,
                callback_progress=self.setProgress,
            )
            return True
        except Exception as e:
            self.exception = e
            raise e
            # return False

    def finished(self, result):
        if result:
            QgsMessageLog.logMessage(
                "{} - Report generation {} ended".format(datetime.now(), self.basename),
                "Comptages",
                Qgis.Info,
            )

        else:
            QgsMessageLog.logMessage(
                "{} - Report generation {} ended with errors: {}".format(
                    datetime.now(), self.basename, self.exception
                ),
                "Comptages",
                Qgis.Info,
            )
